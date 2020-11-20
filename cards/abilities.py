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
        repr = '[{}]'.format(self.resources)
        if self.tap:
            repr += ', [T]'
        if self.life:
            repr += ', pay {} life'.format(self.life)
        if self.sacrifice:
            repr += ', sacrifice {} {}'.format('a' if self.sacrifice == 1 else self.sacrifice,
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

class BounceAbility(Ability):
    point_cost = 2
    valid_targets = [AbilityTarget.everyone,
                     AbilityTarget.target,
                     AbilityTarget.opponent]

    def __repr__(self):
        return '{cost}Return {prefix}{target}{poss} unit{plural} to {pron} owner\'s hand{plural}.'.format(
            cost=self.cost,
            effect=self.effect,
            prefix='target ' if self.target in [AbilityTarget.opponent] else '',
            target=self.target.name,
            pron='its' if self.target in [AbilityTarget.target, AbilityTarget.opponent] else 'their',
            poss='\'s' if self.target in [AbilityTarget.everyone, AbilityTarget.opponent] else '',
            plural='s' if self.target in [AbilityTarget.everyone] else '',
        )


class LifeAbility(Ability):
    point_cost = 2
    valid_targets = [AbilityTarget.everyone,
                     AbilityTarget.you]

    def __repr__(self):
        return '{cost}{target} {verb} {effect} life.'.format(
            cost=self.cost,
            verb='gain' if self.target == AbilityTarget.you else 'gains',
            effect=self.effect,
            target=self.target.name.capitalize()
        )

class DestroyAbility(Ability):
    point_cost = 2
    valid_targets = [AbilityTarget.everyone,
                     AbilityTarget.target,
                     AbilityTarget.opponent]

    def __repr__(self):
        return '{cost}Destroy {prefix}{target}{poss} unit{plural}.'.format(
            cost=self.cost,
            effect=self.effect,
            prefix='target ' if self.target in [AbilityTarget.opponent] else '',
            target=self.target.name,
            poss='\'s' if self.target in [AbilityTarget.everyone, AbilityTarget.opponent] else '',
            plural='s' if self.target in [AbilityTarget.everyone] else '',
        )

abilities = [
    DamageAbility,
    LifeAbility,
    BounceAbility,
    DestroyAbility
]
