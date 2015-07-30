from abilities.prelude import *

class DamageAbility(Ability):
  def __init__(self):
    Ability.__init__(self, DamageAbility.variants()[0])

  @staticmethod
  def variants():
    return [
      # Spell only variants
      AbilityVariant(
        StaticAbility(), 
        SingleTarget(True, True), 
        [TargetType.unit(), TargetType.player()], 
        DuplicateFlag.allow),

      AbilityVariant(
        StaticAbility(),
        GlobalTarget(True, False),
        [TargetType.unit(), TargetType.player()],
        DuplicateFlag.flatten),

      AbilityVariant(
        StaticAbility(),
        OwnerTarget(),
        [],
        DuplicateFlag.flatten),

      # Unit only variants
      AbilityVariant(
        TriggeredAbility.dies,
        SingleTarget(True, True),
        [TargetType.unit(), TargetType.player()],
        DuplicateFlag.allow),
    ]