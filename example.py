from cards.abilities.prelude import *
from cards.abilities import *
from cards.generate.ability import *
from cards.generate import generate_card
print(TriggeredAbility.dies)
print(TargetType.triggered_ability() | TargetType.unit() | TargetType.player())
print(DamageAbility(DamageAbility.variants()[0]))
card = generate_card()
print(ability(card))
