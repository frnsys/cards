from cards.card import *
from enum import IntEnum, Enum


class Ability:
  def __init__(self, variant):
    self._variant = variant

  @property
  def variant(self):
    return self._variant


class DuplicateFlag(IntEnum):
  allow = 0
  flatten = 1
  reject = 2


class TargetType(int):
  @staticmethod
  def unit(): 
    return TargetType(1)

  @staticmethod
  def action(): 
    return TargetType(2) 

  @staticmethod
  def event(): 
    return TargetType(4)

  @staticmethod
  def property(): 
    return TargetType(8)

  @staticmethod
  def condition(): 
    return TargetType(16)

  @staticmethod
  def activated_ability(): 
    return TargetType(32)

  @staticmethod
  def triggered_ability(): 
    return TargetType(64)

  @staticmethod
  def permanent(): 
    return TargetType(26)

  @staticmethod
  def player(): 
    return TargetType(128)

  def __or__(self, x):
    return TargetType(int(self) | int(x))

  def __str__(self):
    return repr(self)

  def __repr__(self):
    types = []
    if self & TargetType.unit() != 0:
      types.append("Unit")
    if self & TargetType.action() != 0:
      types.append("Action")
    if self & TargetType.event() != 0:
      types.append("Event")
    if self & TargetType.property() != 0 : 
      types.append("Property")
    if self & TargetType.condition() != 0:
      types.append("Condition")
    if self & TargetType.activated_ability() != 0:
      types.append("Activated Ability")
    if self & TargetType.triggered_ability() != 0:
      types.append("Triggered Ability")
    if self & TargetType.player():
      types.append("Player")
    return ", or ".join(types)


class Zone(IntEnum):
  battlefield = 0
  graveyard = 1
  discard = 2
  stack = 3
  hand = 4
  anywhere = 5


class Trigger(tuple):
  @property
  def begin(self):
      return self[0] 
  
  @property
  def end(self):
      return self[1]


# Marker class for an ability type.
#
class AbilityType():
  pass

class StaticAbility(AbilityType):
  pass

class ActivatedAbility(AbilityType):
  pass

class TriggeredAbility(AbilityType, Enum):
  discarded = Trigger((Zone.hand, Zone.graveyard))
  dies = Trigger((Zone.battlefield, Zone.graveyard))
  cast = Trigger((Zone.hand, Zone.stack))    
  citp = Trigger((Zone.stack, Zone.battlefield))
  graveyard = Trigger((Zone.anywhere, Zone.graveyard))


# Template for an ability target. This is mostly a marker class.
# 
class AbilityTarget():
  def __init__(self, opponent, optional):
    self.can_target_opponent = opponent
    self.can_be_optional = optional

class SingleTarget(AbilityTarget):
  pass
  
class OwnerTarget(AbilityTarget):
  def __init__(self):
    AbilityTarget.__init__(self, False, False)

class GlobalTarget(AbilityTarget):
  pass

 
# Flags indicating if a card can be on a certain card type
#
class AbilityCardTarget(int):
  @staticmethod
  def unit():
    return AbilityCardTarget(1)

  @staticmethod
  def event():
    return AbilityCardTarget(2)

  @staticmethod
  def condition():
    return AbilityCardTarget(4)

  @staticmethod
  def property():
    return AbilityCardTarget(8)

  @staticmethod
  def action():
    return AbilityCardTarget(16)

  @staticmethod
  def spell():
    return AbilityCardTarget.action() | AbilityCardTarget.event()

  @staticmethod
  def permanent():
    return AbilityCardTarget.unit() | AbilityCardTarget.property() | AbilityCardTarget.condition()

  @staticmethod
  def all():
    return AbilityCardTarget.spell() | AbilityCardTarget.permanent()


# Properties of a variation of an ability.
#
class AbilityVariant():
  def __init__(self, ability_type, target_type, valid_targets, allowed_on, duplicate_flag):
    self.ability_type = ability_type
    self.target_type = target_type
    self.valid_targets = valid_targets
    self.duplicate_flag = duplicate_flag
    self.allowed_on = allowed_on