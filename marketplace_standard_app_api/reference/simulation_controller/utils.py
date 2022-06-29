"""Utility classes and functions."""

from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path


class SimulationState(Enum):
    CREATED = 1
    RUNNING = 2
    COMPLETED = 3
    STOPPED = 4
    FAILED = 6


# Global constant to define the path of the folder where all the simulations are saved
SIMULATIONS_FOLDER_PATH = Path.cwd() / "simulation_files"


@dataclass
class SimulationConfig:

    input_value: int

    def __post_init__(self):
        if self.input_value < 5:
            raise ValueError("Input value is too small.")


def create_input_files(foldername: Path, simulationConfig: SimulationConfig):
    """
    Create the start configuration files for a MarketPlace simulation.

    Args:
        foldername: path to the custom folder for a simulation

        simulationConfig: specific configuration values for a run
    """
    templatesPath = Path(__file__).parent / "templates"
    templateFile = templatesPath / "inputFile.template"

    inputPath = foldername / "input"
    inputPath.mkdir(parents=True, exist_ok=True)

    inputFile = inputPath / "inputFile.conf"
    inputFile.write_text(templateFile.read_text().format(**asdict(simulationConfig)))
