---
id: TASK-002
status: done
title: Синхронизировать квартиру №5 с каноном и удалить legacy-код старой планировки
created: 2026-08-24
completed: 2026-09-06
approved_by_owner: true
verification_level: REMOTE_LIMITED
implementation_commits:
  - 5aaef88f946b838d96d71ff75a888d205007c888
  - 19777cb545c93a5ba154eafa2e83579e9549ea25
  - b200311f0c1487a2140301b3b2a63342edadd021
related_specs:
  - docs/graphs/map.drawio
  - docs/graphs/README.md
  - docs/world/locations/README.md
  - docs/world/locations/apartment_5.md
  - docs/world/actions/ACTIONS_29_AUGUST.md
---

# TASK-002 — Синхронизировать квартиру №5 с каноном и удалить legacy-код старой планировки

## Статус

**DONE. Принято владельцем 2026-09-06 после финальной синхронизации runtime-переходов с каноническим `docs/graphs/map.drawio`.**

## Результат

- Runtime квартиры №5 переведен на пять стабильных ID: прихожая, общая комната, кухня, совмещенная ванная/туалет и балкон.
- Отдельные legacy-помещения квартиры №5 `bedroom` и `living_room` удалены; параллельная старая модель не поддерживается.
- Стартовая управляемая домашняя локация — `loc_apartment_5_room`.
- Актуальные action ID, HUD-привязки, расписание Маши и квестовые ссылки переведены на новую модель.
- Прототипные `school_morning`, `wash_face`, `morning_exercise`, `eat_breakfast` и обслуживающий legacy-код удалены из runtime.
- После консолидации карты 2026-09-06 внутренние runtime transitions в `game/content/definitions.rpy` и assertions в `game/domain/core.rpy` дополнительно приведены к текущему `map.drawio`.

## Важное правило топологии

Этот TASK **не является источником списка переходов**. Единственный канонический источник существования пространств, вложенности и направления маршрутов — [`../../graphs/map.drawio`](../../graphs/map.drawio).

Исторические редакции TASK-002 содержали более старую схему переходов. После консолидации карты эти буквальные списки считаются устаревшей историей реализации и не используются как требования.

## Проверка

Первоначальная реализация TASK-002 ранее проходила Ren'Py 8.5.3 lint/runtime-проверку, зафиксированную в implementation report.

Финальная корректировка 2026-09-06 выполнена на уровне `REMOTE_LIMITED`:

- напрямую сверены внутренние стрелки квартиры №5 в `map.drawio` с `game/content/definitions.rpy`;
- синхронизированы domain self-tests;
- проверены commit diff двух runtime-правок;
- выполнен статический поиск legacy-ID; рабочих совпадений старых ID квартиры №5 в `game/` не обнаружено;
- внешние переходы района не подменялись фиктивными runtime-локациями: их реализация остается отдельным P0-направлением «Спальный район и переходы первого дня».

Новый локальный Ren'Py lint/runtime после финальной синхронизации карты в этом проходе не запускался; GitHub CI-status для финального commit отсутствовал. Владелец принял завершение задачи с этим уровнем проверки.

## Коммиты

- `5aaef88f946b838d96d71ff75a888d205007c888` — базовая миграция и legacy cleanup;
- `19777cb545c93a5ba154eafa2e83579e9549ea25` — синхронизация runtime transitions с актуальной картой;
- `b200311f0c1487a2140301b3b2a63342edadd021` — синхронизация domain self-tests.

Подробный итог: [`TASK-002_IMPLEMENTATION_REPORT.md`](TASK-002_IMPLEMENTATION_REPORT.md).
