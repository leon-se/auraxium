from ..datatypes import DataType


class Reward(DataType):
    """A reward.

    Rewards are granted to players for participating in alerts, gaining
    achievements or completing directives.

    """

    _collection = 'reward'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.count_max = None
        self.count_min = None
        self._reward_type_id = None
        # Set default values for attributes "param1" through "param5"
        s = ''
        for i in range(5):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

    # Define properties
    @property
    def reward_type(self):
        return RewardType.get(id_=self._reward_type_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.count_max = d.get('count_max')
        self.count_min = d.get('count_min')
        self._reward_type_id = d['reward_type_id']
        # Set attributes "param1" through "param5"
        s = ''
        for i in range(5):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)


class RewardType(DataType):
    """A type of reward.

    The type of reward a player will receive (experience or items, etc.). The
    "param" fields of the reward type document the function of the
    corresponding reward's.

    """

    _collection = 'reward_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.count_max = None
        self.count_min = None
        self.description = None
        # Set default values for attributes "param1" through "param5"
        s = ''
        for i in range(5):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.count_max = d.get('count_max')
        self.count_min = d.get('count_min')
        self.description = d['description']
        # Set attributes "param1" through "param5"
        s = ''
        for i in range(5):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
