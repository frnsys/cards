from abilities import *

if __name__ == "__main__":
  from abilities.prelude import *
  print(TriggeredAbility.dies)
  print(TargetType.triggered_ability() | TargetType.unit() | TargetType.player())
  print(DamageAbility())