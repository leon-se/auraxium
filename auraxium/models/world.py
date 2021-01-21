"""Data classes for :mod:`auraxium.ps2.world`."""

from typing import Optional

from .._base import Ps2Data
from ..types import LocaleData

__all__ = [
    'WorldData'
]

# pylint: disable=too-few-public-methods


class WorldData(Ps2Data):
    """Data class for :class:`auraxium.ps2.World`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    world_id: int
    state: str
    name: LocaleData
    description: Optional[LocaleData] = None
