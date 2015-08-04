import random
from cards.card import *
from cards.abilities import *
from cards.abilities.prelude import *


ABILITIES = [
  DamageAbility
]


def ability(card):
  abl = random.choice(ABILITIES)

  if isinstance(card, Unit):
    fltr = AbilityCardTarget.unit()
  elif isinstance(card, Event):
    fltr = AbilityCardTarget.event()
  elif isinstance(card, Action):
    fltr = AbilityCardTarget.action()
  elif isinstance(card, Condition):
    fltr = AbilityCardTarget.condition()
  elif isinstance(card, Property):
    fltr = AbilityCardTarget.property()
  else:
    raise NotImplementedError("ability generation not implemented for card type")

  variations = filter(lambda v: v.validtargets & fltr, abl.variants())
