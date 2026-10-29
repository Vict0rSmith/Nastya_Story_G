---
id: loc_apartment_5_bathroom
entity_type: location
status: draft
map_node_id: loc_apartment_5_bathroom
access_state: open
access_condition: always
objects: []
actions:
  - action_take_shower
  - action_take_bath
  - action_morning_hygiene
  - action_toilet
  - action_shave_legs
  - action_shave_pubic
npcs_possible:
  - npc_nastya
  - npc_masha
related_quests:
  - quest_2026_08_29_first_normal_day
---

# Квартира №5 — совмещенная ванная и туалет

> Существующие переходы и их направление задаются только [`../../graphs/map.drawio`](../../graphs/map.drawio).

## Действия первого этапа
- принять душ;
- принять ванну;
- умыться и почистить зубы (единое действие утренней гигиены);
- сходить в туалет;
- побрить ноги;
- побрить лобок.

Душ/ванна продвигают время и могут давать восстановительный эффект с общим кулдауном. Повторное мытье во время кулдауна допустимо, но не должно повторно выдавать восстановительный бонус. Точные параметры являются системными данными, а не свойством описания помещения.

## Условия доступа
Доступна с начала управляемой игры.

## Переходы
См. [`../../graphs/map.drawio`](../../graphs/map.drawio).

## Визуальный паспорт
Не утвержден.
