import dataclasses
import logging
from typing import ClassVar, Optional, Tuple

from ..base import Cached, Ps2Data
from ..cache import TLRUCache
from ..client import Client
from ..census import Query
from ..proxy import InstanceProxy
from ..types import CensusData

from .item import Item

log = logging.getLogger('auraxium')


@dataclasses.dataclass(frozen=True)
class WeaponData(Ps2Data):
    # Required
    weapon_id: int
    weapon_group_id: int
    turn_modifier: float
    move_modifier: float
    sprint_recovery_ms: int
    equip_ms: int
    unequip_ms: int
    to_iron_sights_ms: int
    from_iron_sights_ms: int
    # Optional
    heat_capacity: Optional[int] = None
    heat_bleed_off_rate: Optional[float] = None
    heat_overheat_penalty_ms: Optional[int] = None
    melee_detect_width: Optional[float] = None
    melee_detect_height: Optional[float] = None

    @classmethod
    def from_census(cls, data: CensusData) -> 'WeaponData':
        heat_capacity = data.get('heat_capacity')
        if heat_capacity is not None:
            heat_capacity = int(heat_capacity)
        heat_bleed_off_rate = data.get('heat_bleed_off_rate')
        if heat_bleed_off_rate is not None:
            heat_bleed_off_rate = int(heat_bleed_off_rate)
        heat_overheat_penalty_ms = data.get('heat_overheat_penalty_ms')
        if heat_overheat_penalty_ms is not None:
            heat_overheat_penalty_ms = int(heat_overheat_penalty_ms)
        melee_detect_width = data.get('melee_detect_width')
        if melee_detect_width is not None:
            melee_detect_width = float(melee_detect_width)
        melee_detect_height = data.get('melee_detect_height')
        if melee_detect_height is not None:
            melee_detect_height = float(melee_detect_height)
        return cls(
            # Required
            int(data['weapon_id']),
            int(data['weapon_group_id']),
            float(data['turn_modifier']),
            float(data['move_modifier']),
            int(data['sprint_recovery_ms']),
            int(data['equip_ms']),
            int(data['unequip_ms']),
            int(data['to_iron_sights_ms']),
            int(data['from_iron_sights_ms']),
            # Optional
            int(data['heat_capacity']),
            float(data['heat_bleed_off_rate']),  # float or int?
            int(data['heat_overheat_penalty_ms']),
            melee_detect_width,
            melee_detect_height)


class Weapon(Cached, cache_size=128, cache_ttu=3600.0):

    _cache: ClassVar[TLRUCache[int, 'Weapon']]
    data: WeaponData
    collection = 'weapon'
    id_field = 'weapon_id'

    @property
    def equip_times(self) -> Optional[Tuple[float, float]]:
        """Return the equip and unequip times in seconds."""
        equip_time: Optional[int] = self.data.equip_ms
        unequip_time: Optional[int] = self.data.unequip_ms
        if equip_time is None or unequip_time is None:
            return None
        return equip_time / 1000.0, unequip_time / 1000.0

    @property
    def ads_times(self) -> Optional[Tuple[float, float]]:
        """Return the ADS enter and exit times in seconds."""
        enter_ads: Optional[float] = self.data.to_iron_sights_ms
        exit_ads: Optional[float] = self.data.from_iron_sights_ms
        if enter_ads is None or exit_ads is None:
            return None
        return enter_ads / 1000.0, exit_ads / 1000.0

    @property
    def melee_hitbox(self) -> Optional[Tuple[float, float]]:
        """Return the ADS enter and exit times in seconds."""
        width: Optional[float] = self.data.melee_detect_width
        height: Optional[float] = self.data.melee_detect_height
        if width is None or height is None:
            return None
        return width / 1000.0, height / 1000.0

    @property
    def spring_recovery(self) -> Optional[float]:
        """Return the sprint recovery time in seconds."""
        value: Optional[float]
        if (value := self.data.sprint_recovery_ms) is not None:
            value /= 1000.0
        return value

    def _build_dataclass(self, data: CensusData) -> WeaponData:
        return WeaponData.from_census(data)

    @classmethod
    async def get_by_name(cls, name: str, *, locale: str = 'en',
                          client: Client) -> Optional['Weapon']:
        """Retrieve a weapon by name.

        This is a helper method provided as weapons themselves do not
        have a name. This looks up an item by name, then returns the
        weapon associated with this item.

        Returns:
            The weapon associated with the given item, or None

        """
        item = await Item.get_by_name(name, locale=locale, client=client)
        if item is None:
            return None
        return await item.weapon().resolve()

    def item(self) -> InstanceProxy[Item]:
        query = Query('item_to_weapon', service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join('item')
        join.parent_field = 'item_id'
        return InstanceProxy(Item, query, client=self._client)
