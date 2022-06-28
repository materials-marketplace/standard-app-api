import logging
import os
import shutil
import subprocess
import uuid

from ..simulation_controller.utils import (
    SIMULATIONS_FOLDER_PATH,
    SimulationConfig,
    SimulationStatus,
    create_input_files,
)


class Simulation:
    """Manage a single simulation."""

    def __init__(self, request_obj: dict):
        self.job_id: str = str(uuid.uuid4())
        self.simulationPath = os.path.join(SIMULATIONS_FOLDER_PATH, self.job_id)
        create_input_files(self.simulationPath, SimulationConfig(request_obj))
        self._status: SimulationStatus = SimulationStatus.CREATED
        self._process = None
        logging.info(
            f"Simulation '{self.job_id}' with " f"configuration {request_obj} created."
        )

    @property
    def status(self) -> SimulationStatus:
        """Getter for the status.

        If the simulation is running, the process is checked for completion.

        Returns:
            SimulationStatus: status of the simulation
        """
        if self._status == SimulationStatus.INPROGRESS:
            process_status = self.process.poll()
            if process_status is None:
                return SimulationStatus.INPROGRESS
            elif process_status == 0:
                logging.info(f"Simulation '{self.job_id}' is now completed.")
                self.status = SimulationStatus.COMPLETED
            else:
                logging.error(f"Error occurred in simulation '{self.job_id}'.")
                self.status = SimulationStatus.ERROR
        return self._status

    @status.setter
    def status(self, value: SimulationStatus):
        self._status = value

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, value):
        self._process = value

    def run(self):
        """
        Start running a simulation.

        A new process that calls SomeCommand is spawned, and the output
        is stored in a separate directory

        Raises:
            RuntimeError: when the simulation is already in progress
        """
        if self.status == SimulationStatus.INPROGRESS:
            msg = f"Simulation '{self.job_id}' already in progress."
            logging.error(msg)
            raise RuntimeError(msg)
        outputPath = os.path.join(self.simulationPath, "output")
        if not os.path.isdir(outputPath):
            os.mkdir(outputPath)
        os.chdir(self.simulationPath)

        self.process = subprocess.Popen(["sleep", "600"], stdout=subprocess.PIPE)
        self.status = SimulationStatus.INPROGRESS
        logging.info(f"Simulation '{self.job_id}' started successfully.")

    def stop(self):
        """Stop a running process.

        Raises:
            RuntimeError: if the simulation is not running
        """
        if self.process is None:
            msg = f"No process to stop. Is simulation '{self.job_id}' running?"
            logging.error(msg)
            raise RuntimeError(msg)

        self.process.terminate()
        self.status = SimulationStatus.STOPPED
        self.process = None
        logging.info(f"Simulation '{self.job_id}' stopped successfully.")

    def delete(self):
        """
        Delete all the simulation folders and files.

        Raises:
            RuntimeError: if deleting a running simulation
        """
        if self.status == SimulationStatus.INPROGRESS:
            msg = f"Simulation '{self.job_id}' is running. Stop it before deleting it."
            logging.error(msg)
            raise RuntimeError(msg)
        shutil.rmtree(self.simulationPath)
        logging.info(f"Simulation '{self.job_id}' and related files deleted.")
