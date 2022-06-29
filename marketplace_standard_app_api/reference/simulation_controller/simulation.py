import logging
import os
import shutil
import subprocess
import uuid

from ..simulation_controller.utils import (
    SIMULATIONS_FOLDER_PATH,
    SimulationConfig,
    SimulationState,
    create_input_files,
)


class Simulation:
    """Manage a single simulation."""

    def __init__(self, request_obj: dict):
        self.job_id: str = str(uuid.uuid4())
        self.path = SIMULATIONS_FOLDER_PATH / self.job_id
        self.config = SimulationConfig(**request_obj)
        create_input_files(self.path, self.config)
        self._state: SimulationState = SimulationState.CREATED
        self._process = None
        logging.info(
            f"Simulation '{self.job_id}' with " f"configuration {request_obj} created."
        )

    @property
    def state(self) -> SimulationState:
        """Getter for the status.

        If the simulation is running, the process is checked for completion.

        Returns:
            SimulationStatus: status of the simulation
        """
        if self._state == SimulationState.RUNNING:
            process_status = self.process.poll()
            if process_status is None:
                return SimulationState.RUNNING
            elif process_status == 0:
                logging.info(f"Simulation '{self.job_id}' is now completed.")
                self.state = SimulationState.COMPLETED
            else:
                logging.error(f"Error occurred in simulation '{self.job_id}'.")
                self.state = SimulationState.FAILED
        return self._state

    @state.setter
    def state(self, value: SimulationState):
        self._state = value

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
        if self.state == SimulationState.RUNNING:
            msg = f"Simulation '{self.job_id}' already in progress."
            logging.error(msg)
            raise RuntimeError(msg)
        output_path = self.path / "output"
        output_path.mkdir(parents=True, exist_ok=True)

        os.chdir(self.path)
        self.process = subprocess.Popen(["sleep", "3"], stdout=subprocess.PIPE)
        self.state = SimulationState.RUNNING
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
        self.state = SimulationState.STOPPED
        self.process = None
        logging.info(f"Simulation '{self.job_id}' stopped successfully.")

    def delete(self):
        """
        Delete all the simulation folders and files.

        Raises:
            RuntimeError: if deleting a running simulation
        """
        if self.state == SimulationState.RUNNING:
            msg = f"Simulation '{self.job_id}' is running. Stop it before deleting it."
            logging.error(msg)
            raise RuntimeError(msg)
        shutil.rmtree(self.path)
        logging.info(f"Simulation '{self.job_id}' and related files deleted.")
