from enum import Enum


class Card():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<{name} ({cost}) [{typ}]>'.format(name=self.name,
                                                  cost=self.cost,
                                                  typ=self.type)


class Unit(Card):
    def __repr__(self):
        return '<{name} ({cost}) [ATK:{atk}|DEF:{dfn}]>'.format(name=self.name,
                                                                cost=self.cost,
                                                                atk=self.attack,
                                                                dfn=self.defense)

class Action(Card):
    pass

class Property(Card):
    pass

class Condition(Card):
    pass

class Event(Card):
    pass

class CardType(Enum):
    unit = Unit
    action = Action
    property = Property
    condition = Condition
    event = Event

