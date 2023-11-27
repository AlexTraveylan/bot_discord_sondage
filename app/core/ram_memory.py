"""This module contains the RAMemory class."""
from app.core.sondage import Sondage


class RAMemory:
    """Class to store data in RAM."""

    _sondages = {}

    @classmethod
    def get_sondages(cls) -> list[str]:
        """Get all sondages."""
        return cls._sondages

    @classmethod
    def get_sondage_by_name(cls, sondage_name: str) -> Sondage | None:
        """Get a sondage by its name."""
        return cls._sondages.get(sondage_name)

    @classmethod
    def add_sondage(cls, sondage: Sondage) -> None:
        """Add a sondage to the RAM."""
        cls._sondages[sondage.name] = sondage
