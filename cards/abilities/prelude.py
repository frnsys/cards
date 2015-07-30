from card import *
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
    self._opponent = opponent
    self._optional = optional

  @property
  def can_target_opponent(self): 
    return self._opponent

  @property
  def can_be_optional(self): 
    return self.optional 

class SingleTarget(AbilityTarget):
  pass
  
class OwnerTarget(AbilityTarget):
  def __init__(self):
    AbilityTarget.__init__(self, False, False)

class GlobalTarget(AbilityTarget):
  pass


# Properties of a variation of an ability.
#
class AbilityVariant():
  def __init__(self, ability_type, target_type, valid_targets, duplicate_flag):
    self._ability_type = ability_type
    self._target_type = target_type
    self._valid_targets = valid_targets
    self._duplicate_flag = duplicate_flag

  @property 
  def ability_type(self):
    return self._ability_type

  @property 
  def valid_targets(self):
    return self._valid_targets

  @property 
  def target_type(self):
    return self._target_type

  @property 
  def duplicate_flag(self):
    return self._duplicate_flag