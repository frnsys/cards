from cards.abilities.prelude import *

class DamageAbility(Ability):
  def __init__(self, variant):
    Ability.__init__(self, variant)

  @staticmethod
  def variants():
    return [
      AbilityVariant(
        StaticAbility(), 
        SingleTarget(True, True), 
        [TargetType.unit(), TargetType.player()], 
        AbilityCardTarget.spell(),
        DuplicateFlag.allow),

      AbilityVariant(
        StaticAbility(),
        GlobalTarget(True, False),
        [TargetType.unit(), TargetType.player()],
        AbilityCardTarget.spell(),
        DuplicateFlag.flatten),

      AbilityVariant(
        StaticAbility(),
        OwnerTarget(),
        [],
        AbilityCardTarget.spell(),
        DuplicateFlag.flatten),

      AbilityVariant(
        TriggeredAbility.dies,
        SingleTarget(True, True),
        [TargetType.unit(), TargetType.player()],
        AbilityCardTarget.unit(),
        DuplicateFlag.allow),
    ]