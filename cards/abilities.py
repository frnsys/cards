from enum import Enum


class Ability():
    def __init__(self, effect, cost, target):
        self.effect = effect
        self.cost = cost
        self.target = target

class AbilityTarget(Enum):
    everyone = 0
    target = 1
    opponent = 2
    you = 3
    owner = 4

class AbilityCost():
    def __init__(self, resources, tap=False, life=0, sacrifice=0):
        self.tap = tap
        self.life = life
        self.resources = resources
        self.sacrifice = sacrifice

    def __repr__(self):
        repr = '{}'.format(self.resources)
        if self.tap:
            repr += ', T'
        if self.life:
            repr += ', pay {} life'.format(self.life)
        if self.sacrifice:
            repr += ', sacrifice {} {}'.format(self.sacrifice,
                                               'units' if self.sacrifice > 1
                                                       else 'unit')
        return repr + ': '

class DamageAbility(Ability):
    point_cost = 2
    valid_targets = [AbilityTarget.everyone,
                     AbilityTarget.target,
                     AbilityTarget.opponent]

    def __repr__(self):
        return '{cost}Deal {effect} damage to {target}.'.format(
            cost=self.cost,
            effect=self.effect,
            target=self.target.name
        )

class LifeAbility(Ability):
    point_cost = 2
    valid_targets = [AbilityTarget.everyone,
                     AbilityTarget.you]

    def __repr__(self):
        return '{cost}{target} gains {effect} life.'.format(
            cost=self.cost,
            effect=self.effect,
            target=self.target.name.capitalize()
        )


abilities = [
    DamageAbility,
    LifeAbility
]
