---
id: "anal_plug"
entity_type: "item"
status: "approved_partial"
name: "Анальная пробка"
category: "intimate"
storage: "inventory"
item_type: "body"
stackable: false
consumable: false
usable: true
required_openness_purchase: 3
required_openness_use: 3
price: TBD
tags: ["body"]
icon: null
use_modes: ["persistent_body_item"]
related_actions: []
related_effects: []
related_quests: []
related_events: []
description: "Анальная пробка."
use_conditions: {}
body_slot: "anal"
incompatible_clothing_slots: []
---

# Анальная пробка

## Что это

Анальная пробка.

## Категория и хранение

Вкладка «Интимное» единого inventory.

## Внешний вид

Детали внешнего вида — TBD.\n
## Покупка

Раскрепощенность для покупки: 3. Цена: TBD.

## Использование и условия доступности

Раскрепощенность для использования: 3. Владение и физическая доступность обязательны; условия самого действия/события проверяются независимо.

## Способы использования и состояния

persistent_body_item: inventory → вставить → body → действия/локации → вынуть → inventory. Установка из интерфейса и результата события использует один API. Владение сохраняется; HUD и общие conditions читают то же состояние.

## Графический ассет

TBD. Реалистичный предмет на прозрачном фоне, единый холст, согласованные свет и детализация, безопасные поля, читаемость при уменьшении. Схематическая пиктограмма не заменяет предмет.

## Связанный контент

[Механика items/гардероба](../../systems/RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md). [Каталог](README.md). Сцены, действия и цены этим каталогом не создаются.
