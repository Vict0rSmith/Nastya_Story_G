---
id: "item_example"
entity_type: "item"
status: "draft"
name: "Название предмета"
category: "misc"
storage: "inventory"
item_type: "misc"
stackable: false
consumable: false
usable: true
required_openness_purchase: null
required_openness_use: null
price: TBD
tags: []
icon: null
use_modes: []
related_actions: []
related_effects: []
related_quests: []
related_events: []
---

# Название предмета

## Что это

Переносимая или принадлежащая персонажу физическая вещь. Для устойчивого объекта пространства используется [OBJECT_TEMPLATE](OBJECT_TEMPLATE.md); видимость товара в магазине не требует второго object.

## Категория

## Хранение

`storage` — обычное хранение, не текущее runtime-состояние экземпляра.

## Внешний вид

## Игровое описание

## Покупка

## Использование

## Способы использования

`action_tool` — использование внутри действия; `persistent_body_item` — длительное состояние до снятия. Режимы определяет конкретная карточка.

## Условия доступности

Для одежды: `storage: "wardrobe"`, обычный технический `slot`, `contexts`, `context_unlocks`; дополнительные условия — `use_conditions`. Для persistent item при утвержденной физической необходимости — `body_slot`. Неутвержденные значения остаются TBD/null.

## Состояния

Владение, физическая доступность, текущий state и контекстные разрешения разделены. Пустые слоты не требуют фиктивных nude/topless items.

## Графический ассет

Реалистичный предмет, прозрачный фон, единый холст, свет, детализация, безопасные поля и читаемость при уменьшении. До производства ассета `icon: null`.

## Связанный контент

[Каталог](../world/items/README.md). [Владелец механики](../systems/RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md).

Неприменимые разделы можно опустить. Для компилируемых карточек используются плоские YAML-поля с JSON-совместимыми значениями; `price: TBD` допустимо. Каталог синхронизируется через `tools/sync_items.py`.
