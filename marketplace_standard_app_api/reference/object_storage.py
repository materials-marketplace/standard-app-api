import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Mapping, Tuple, Union

import sqlalchemy
from databases import Database
from databases.interfaces import Record
from fastapi import UploadFile
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, and_, select

from ..models.object_storage import (
    CollectionListItemModel,
    CollectionListResponse,
    CollectionName,
    DatasetListResponse,
    DatasetModel,
    DatasetName,
)
from .common import metadata

collections = sqlalchemy.Table(
    "collections",
    metadata,
    Column("name", String, primary_key=True),
)

collections_metadata = sqlalchemy.Table(
    "collections_metadata",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "collection_name",
        ForeignKey("collections.name", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("key", String),
    Column("value", String),
)

datasets = sqlalchemy.Table(
    "datasets",
    metadata,
    Column("name", String, primary_key=True),
    Column(
        "collection_name",
        ForeignKey("collections.name", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("content_type", String),
    Column("last_modified", DateTime),
)

datasets_metadata = sqlalchemy.Table(
    "datasets_metadata",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "collection_name",
        ForeignKey("collections.name", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "dataset_name", ForeignKey("datasets.name", ondelete="CASCADE"), nullable=False
    ),
    Column("key", String),
    Column("value", String),
)


class ConflictError(RuntimeError):
    pass


def metadata_from_headers(headers: Mapping):
    metadata_magic_keyword = "X-Object-Meta-"
    for key, value in headers.items():
        if key.lower().startswith(metadata_magic_keyword.lower()):
            yield key[len(metadata_magic_keyword) :], value


def metadata_to_headers(metadata: List[Record]):
    metadata_magic_keyword = "X-Object-Meta-"
    for key, value in metadata:
        yield metadata_magic_keyword + key, value


async def create_collection(
    database: Database, collection_name: CollectionName, headers: Mapping
):
    metadata = dict(metadata_from_headers(headers))
    async with database.transaction():
        insert_stmt = collections.insert().values(name=collection_name)
        await database.execute(insert_stmt)
        for key, value in metadata.items():
            insert_stmt = collections_metadata.insert().values(
                collection_name=collection_name, key=key, value=value
            )
            await database.execute(insert_stmt)


async def delete_collection(database: Database, collection_name: CollectionName):
    delete_stmt = collections.delete().where(collections.c.name == collection_name)
    try:
        await database.execute(delete_stmt)
    except sqlite3.IntegrityError:
        raise ConflictError("Collection is not empty.")


async def list_collections(
    database: Database, limit: int, offset: int
) -> CollectionListResponse:
    query = select(collections).offset(offset).limit(limit)
    result = await database.fetch_all(query)
    if len(result):
        return [
            CollectionListItemModel(name=row[0], count=0, bytes=0) for row in result
        ]
    else:
        return []


async def get_collection_metadata_headers(
    database: Database, collection_name: CollectionName
):
    query = select(collections).where(collections.c.name == collection_name)
    entry = await database.fetch_one(query)
    if entry:
        query = select(collections_metadata.c.key, collections_metadata.c.value).where(
            collections_metadata.c.collection_name == collection_name
        )
        rows = await database.fetch_all(query)
        headers = dict(metadata_to_headers(rows))
        return headers
    raise FileNotFoundError()


async def list_datasets(
    database: Database, collection_name: CollectionName, limit: int, offset: int
) -> Tuple[DatasetListResponse, dict]:
    headers = await get_collection_metadata_headers(database, collection_name)
    query = (
        select(datasets)
        .where(datasets.c.collection_name == collection_name)
        .offset(offset)
        .limit(limit)
    )
    rows = await database.fetch_all(query)
    if len(rows):
        return [
            DatasetModel(
                id=row._mapping["name"],
                content_type=row._mapping["content_type"],
                last_modified=str(row._mapping["last_modified"]),
            )
            for row in rows
        ], headers
    else:
        return [], headers


async def get_dataset_metadata_headers(
    database: Database, collection_name: CollectionName, dataset_name: DatasetName
) -> dict:
    query = select(datasets).where(
        and_(
            datasets.c.collection_name == collection_name,
            datasets.c.name == dataset_name,
        )
    )
    entry = await database.fetch_one(query)
    if entry:
        query = select(datasets_metadata.c.key, datasets_metadata.c.value).where(
            and_(
                datasets_metadata.c.collection_name == collection_name,
                datasets_metadata.c.dataset_name == dataset_name,
            )
        )
        rows = await database.fetch_all(query)
        headers = dict(metadata_to_headers(rows))
        headers["Content-Type"] = entry._mapping["content_type"]
        headers["Last-Modified"] = str(entry._mapping["last_modified"])
        return headers
    raise FileNotFoundError()


async def create_dataset(
    database: Database,
    data_dir: Path,
    collection_name: CollectionName,
    dataset_name: DatasetName,
    file: UploadFile,
    headers: dict,
):
    metadata = dict(metadata_from_headers(headers))

    async with database.transaction():
        # Create dataset entry in database
        insert_stmt = datasets.insert().values(
            name=dataset_name,
            collection_name=collection_name,
            content_type=file.content_type,
            last_modified=datetime.utcnow(),
        )
        await database.execute(insert_stmt)

        # Create dataset metadata in database
        for key, value in metadata.items():
            insert_stmt = datasets_metadata.insert().values(
                collection_name=collection_name,
                dataset_name=dataset_name,
                key=key,
                value=value,
            )
            await database.execute(insert_stmt)

        # Move file into data directory
        dst = data_dir / collection_name / dataset_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        contents = await file.read()  # TODO: optimize this
        if isinstance(contents, str):
            dst.write_text(contents)
        else:
            dst.write_bytes(contents)


async def get_dataset(
    database: Database,
    data_dir: Path,
    collection_name: CollectionName,
    dataset_name: DatasetName,
) -> Tuple[Union[str, bytes], dict]:
    # TODO: Support bytes
    src = data_dir / collection_name / dataset_name
    headers = await get_dataset_metadata_headers(
        database, collection_name, dataset_name
    )
    content = src.read_text()  # TODO: should be non-blocking
    return content, headers


async def delete_dataset(
    database: Database,
    data_dir: Path,
    collection_name: CollectionName,
    dataset_name: DatasetName,
):
    async with database.transaction():
        delete_stmt = datasets.delete().where(
            sqlalchemy.and_(
                datasets.c.collection_name == collection_name,
                datasets.c.name == dataset_name,
            )
        )
        path = data_dir / collection_name / dataset_name
        path.unlink()
        await database.execute(delete_stmt)
