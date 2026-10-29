# TASK-008 — Implementation Report

Статус: `done`.

Принято владельцем 2026-09-08 после проверки: «таск 8 проверил. ок».
Известные ограничения ниже сохранены; принятие TASK не утверждает значения `TBD`.

## Что сделано

- Создан канонический каталог `docs/world/items/` с ровно 20 товарными карточками секс-шопа и единым README.
- Создан `ITEM_TEMPLATE.md`; object и item разведены по ответственности.
- Добавлены генератор `tools/sync_items.py` и runtime registry `game/content/items.rpy`; ID уникальны, цены и неутвержденные графические параметры остаются `TBD`/`null`.
- Сохранен единый inventory с фильтрами `Все`, `Расходники`, `Квестовые`, `Интимное`; костюмы остаются в гардеробе, массажное масло — обычный расходник.
- Разделены purchase/use openness gates, capability-based выбор action tools и persistent body items.
- Добавлены `inventory.item_states`, `inventory.external_items`, API `body_item_active`/`set_body_item`, общие `conditions_match` для action/event/quest и миграция save schema 5→6.
- `remote_toy`, `anal_plug`, `tail_plug` сохраняют установку между действиями и локациями; `anal_beads`, `soft_handcuffs`, `vibrator` остаются action tools.
- Гардероб единый: разрешенные точки доступа, контексты, сюжетные unlocks, employer-owned clothing и восстановление гражданского комплекта без копирования item.
- Добавлен компактный status HUD: `Устала`, единый `Голодна`, `Перевозбуждена`, `Плохое настроение`, установленные persistent items.
- Синхронизированы системные спецификации, templates, MOC, карточка комнаты Насти и roadmap.

## Измененные файлы

Изменены runtime-файлы `game/domain/core.rpy`, `game/domain/item_rules.rpy`, `game/content/items.rpy`, `game/ui/gameplay_screens.rpy`, `game/ui/status/*.svg`, тесты `game/tests/task008_tests.rpy` и `game/tests/runtime_regression_tests.rpy`, генератор `tools/sync_items.py`, project health check, 20 item-карточек и README, шаблоны, MOC, системные спецификации, карточка комнаты и roadmap.

## Проверки

Уровень: `FULL_LOCAL`.

- `tools/project_health_check.py`: 0 ошибок, 0 предупреждений.
- `tools/sync_items.py --check`: PASS; ровно 20 карточек.
- `git diff --check`: PASS.
- Ren’Py MCP lint: returncode 0, findings 0; undefined screens: 0.
- `task008`: 10 тестов, 9 assertions — PASS; каталог, body-state, action/event/quest conditions, wardrobe contexts, status thresholds, migration, UI inventory/wardrobe и save roundtrip.
- `nastya_runtime`: 9 тестов, 46 assertions — PASS.
- Просмотрены screenshots inventory, wardrobe и status HUD.

## Отклонения и известные ограничения

- Автоматические временные пороги питания пока не утверждены; runtime не придумывает их. `hungry`/`very_hungry` сведены к одному HUD-status `Голодна`, внутренняя градация сохранена документально.
- Финальные item/clothing assets остаются `TBD`; UI использует существующую сетку и текстовый fallback.
- MCP `find_missing_assets` сообщает три прежних срабатывания на `scene expression Solid(...)` в `game/content/day_one.rpy`; lint и runtime проходят.
- Физический геймпад отдельно не проверялся.

## Change Impact Check

Основной источник item mechanics — `RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md`; карточки и шаблон ссылаются на него. HUD display rules находятся в `HUD_TEMPORARY_EFFECTS_SPEC.md`, характеристики не дублируют механику. Каталог достижим через `MASTER_SPEC → world/README.md → world/items/README.md`; object catalog явно ссылается на item distinction. Карта мира не менялась. Новые item IDs не создают object-дубликаты.

## Коммиты реализации

`3b8cec7` — финальный коммит реализации (исправлена прежняя ссылка на SHA до amend).

## Закрытие TASK

Изменены только статус, расположение карточки/отчета и сводные документы. Прежние runtime-проверки не повторяются для неизмененного кода. Выполняются project health, проверка ссылок/diff и публикация с подтверждением равенства локальной `main` и `origin/main`; итоговый SHA закрытия указывается в сообщении исполнителя после синхронизации.
