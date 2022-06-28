"""Utility classes and functions."""

import logging
import os
from enum import Enum


class SimulationStatus(Enum):
    CREATED = 1
    INPROGRESS = 2
    COMPLETED = 3
    STOPPED = 4
    DOWNLOADED = 5
    ERROR = 6


# Global constant to define the path of the folder where all the simulations are saved
SIMULATIONS_FOLDER_PATH = "./simulation_files"


class SimulationConfig:
    def __init__(self, request_obj: dict):
        err_msg = f"Error creating simulation: {str(request_obj)}. "
        self.input_value: int = request_obj.get("inputValue", 1)
        if self.input_value < 5:
            err_msg += "Input Value is too small."
            logging.error(err_msg)
            raise ValueError(err_msg)


def create_input_files(foldername: str, simulationConfig: SimulationConfig):
    """
    Create the start configuration files for a MarketPlace simulation.

    Args:
        foldername: path to the custom folder for a simulation

        simulationConfig: specific configuration values for a run
    """
    if not os.path.isdir(foldername):
        os.mkdir(foldername)
    inputPath = os.path.join(foldername, "input")
    if not os.path.isdir(inputPath):
        os.mkdir(inputPath)

    templatesPath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates"
    )

    with open(os.path.join(templatesPath, "inputFile.template")) as templateFile:
        with open(
            os.path.join(foldername, "input", "inputFile.conf", "w")
        ) as inputFile:
            inputFile.write(
                f"{templateFile.read()}".format(
                    input_value=simulationConfig.input_value
                )
            )
