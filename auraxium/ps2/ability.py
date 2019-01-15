from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType


class Ability(CachableDataType):
    """A PS2 Ability.

    Abilities are persistent, player-bound objects responsible for persistent
    effects like AoE heal or the Heavy Assault's overshield. They are
    generally bound to a resource that is drained as the ability is used.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self._ability_type_id = None
        self.distance_max = None
        self.expires_after = None
        self.first_use_delay = None
        self.is_toggle = None
        self.next_use_delay = None
        self.radius_max = None
        self.resource_cast_cost = None
        self.resource_cost = None
        self._resource_type_id = None
        self.reuse_delay = None
        # Set default values for fields "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = None\n'.format(i + 1)
        exec(s)
        # Set default values for fields "string1" through "string4"
        s = ''
        for i in range(4):
            s += 'self.string{0} = None\n'.format(i + 1)
        exec(s)

        # Define properties
        @property
        def ability_type(self):
            try:
                return self._ability_type
            except AttributeError:
                self._ability_type = AbilityType.get(id=self._ability_type_id)
                return self._ability_type

        @property
        def resource_type(self):
            try:
                return self._resource_type
            except AttributeError:
                self._resource_type = ResourceType.get(
                    id=self._resource_type_id)
                return self._resource_type

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self._ability_type_id = data.get('ability_type_id')
        self.distance_max = data.get('distance_max')
        self.expires_after = data.get('expire_msec') / 1000
        self.first_use_delay = data.get('first_use_delay_msec') / 1000
        self.is_toggle = data.get('flag_toggle')
        self.next_use_delay = data.get('next_use_delay_msec') / 1000
        self.radius_max = data.get('radius_max')
        self.resource_cast_cost = data.get('resource_first_cost')
        self.resource_cost = data.get('resource_cost_per_msec') / 1000
        self._resource_type_id = data.get('resource_type_id')
        self.reuse_delay = data.get('reuse_delay_msec') / 1000
        # Set attributes "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = data.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
        # Set attributes "string1" through "string4
        s = ''
        for i in range(4):
            s += 'self.string{0} = data.get(\'string{0}\')\n'.format(i + 1)
        exec(s)


class AbilityType(EnumeratedDataType):
    """Represents a type of ability.

    Groups similarly functioning abilities together, the "param" and "string"
    fields of an ability type also explain the (unnamed) entries for the
    corresponding abilities.

    """

    _collection = 'ability_type'

    def __init__(self, id, data_override=None):
        self.id = id

        self.description = None
        # Set default values for fields "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = None\n'.format(i + 1)
        exec(s)
        # Set default values for fields "string1" through "string4"
        s = ''
        for i in range(4):
            s += 'self.string{0} = None\n'.format(i + 1)
        exec(s)

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.description = data.get('description')
        # Set attributes "param1" through "param14"
        s = ''
        for i in range(14):
            s += 'self.param{0} = data.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
        # Set attributes "string1" through "string4
        s = ''
        for i in range(4):
            s += 'self.string{0} = data.get(\'string{0}\')\n'.format(i + 1)
        exec(s)
