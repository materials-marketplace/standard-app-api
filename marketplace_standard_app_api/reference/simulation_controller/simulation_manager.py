import logging

from ..simulation_controller.simulation import Simulation
from ..simulation_controller.utils import SimulationState


class SimulationManager:
    def __init__(self):
        self.simulations: dict = {}

    def _get_simulation(self, job_id: str) -> Simulation:
        """
        Get the simulation corresponding to the job_id.

        Args:
            job_id: unique id of he simulation

        Raises:
            KeyError: if there is no simulation matching the id

        Returns:
            Simulation instance
        """
        try:
            simulation = self.simulations[job_id]
            return simulation
        except KeyError as ke:
            message = f"Simulation with id '{job_id}' not found"
            logging.error(message)
            raise KeyError(message) from ke

    def _add_simulation(self, simulation: Simulation) -> str:
        """Append a simulation to the internal datastructure.

        Args:
            simulation: Object to add

        Returns:
            str: ID of the added object
        """
        job_id: str = simulation.job_id
        self.simulations[job_id] = simulation
        return job_id

    def _delete_simulation(self, job_id: str):
        """Remove a simulation from the internal datastructure.

        Args:
            job_id: id of the simulation to remove
        """
        del self.simulations[job_id]

    def create_simulation(self, request_obj: dict) -> str:
        """Create a new simulation given the arguments.

        Args:
           requestObj: dictionary containing input configuration

        Returns:
            str: unique job id
        """
        return self._add_simulation(Simulation(request_obj))

    def run_simulation(self, job_id: str):
        """Execute a simulation.

        Args:
            job_id: unique simulation id
        """
        self._get_simulation(job_id).run()

    def stop_simulation(self, job_id: str):
        """Force terminate a simulation.

        Args:
            job_id: unique id of the simulation
        """
        self._get_simulation(job_id).stop()

    def delete_simulation(self, job_id: str):
        """Delete all the simulation information.

        Args:
            job_id: unique id of simulation
        """
        self._get_simulation(job_id).delete()
        self._delete_simulation(job_id)

    def get_simulation_state(self, job_id: str) -> SimulationState:
        """Return the state of a particular simulation.

        Args:
            job_id: id of the simulation

        Returns:
            SimulationState: state of the simulation
        """
        return self._get_simulation(job_id).state

    def get_simulation_list(self) -> list[str]:
        """Returns unique ids of all the simulations.

        Returns:
            list: list of simulation ids
        """
        return list(self.simulations.keys())
