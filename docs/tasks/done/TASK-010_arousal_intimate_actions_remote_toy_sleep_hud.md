---
id: TASK-010
status: done
title: Возбуждение, интимные действия, носимые игрушки, сон и HUD
created: 2026-09-09
approved_by_owner: true
executor: Codex
verification_level: FULL_LOCAL
dependencies: [TASK-008]
related_specs: [docs/systems/CHARACTERISTICS_SPEC.md, docs/systems/TIME_ACTIONS_QUESTS_EVENTS_SPEC.md, docs/systems/RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md, docs/systems/HUD_TEMPORARY_EFFECTS_SPEC.md]
related_entities: [adult_magazine, adult_movie, sex_illustrated_book, remote_toy, anal_plug, tail_plug, vibrator, bullet_vibrator, vacuum_stimulator, dildo, anal_beads]
implementation_commits: [18456f4]
implementation_report: docs/tasks/done/TASK-010_arousal_intimate_actions_remote_toy_sleep_hud.md
---

# TASK-010 — Возбуждение, интимные действия, носимые игрушки, сон и HUD

Принято владельцем 2026-09-14: «приемка TASK-010 завершена».

## Цель

Перевести единую временную характеристику `arousal` на шкалу 0…10 и реализовать согласованный контур ее изменения: естественный спад, источники с вероятностью/cooldown, мастурбацию, persistent body items, управляемый `remote_toy`, эротические сны и вычисляемые HUD-статусы.

## Утвержденные требования

- Диапазоны: 0 — «Спокойна»; 1–3 — «Слегка возбуждена»; 4–6 — «Возбуждена»; 7–9 — «Сильно возбуждена»; 10 — «Перевозбуждена».
- Спад: −1 за каждый накопленный полный час без компенсирующей стимуляции.
- Источники поддерживают +1/+2/+3, собственную вероятность и cooldown.
- Порножурнал: 20 минут, 40%, +1, cooldown 6 часов; порнофильм: 45 минут, 70%, +2, 12 часов; иллюстрированная книга: 30 минут, 50%, +1, 8 часов.
- Мастурбация доступна при `arousal >= 5`, openness rank >= 2, флаге `masturbation_unlocked`, наедине в комнате или ванной. Руками, дилдо и анальными бусами — 30 минут; вибратором, вибропулей и вакуумным стимулятором — 20 минут. `strapon` и `remote_toy` не являются способами обычной мастурбации. Результат — оргазм и `arousal = 0`.
- `remote_toy` занимает vaginal slot; `anal_plug`/`tail_plug` — anal slot. Разрешена одна vaginal + одна anal игрушка; две anal запрещены.
- Runtime `remote_toy`: одна физическая item-сущность, состояние installed/active/controller. Controller: `nastya`, `npc_id`, `quest:<quest_id>`.
- Активный `remote_toy` дает гарантированные +2 за полный час, подавляет естественный спад и собственную пассивную проверку. После достижения 10 непрерывная активность еще 30 минут запускает общий `auto_orgasm` event с `source=remote_toy` и контекстом. Прерывание сбрасывает отсчет. После события arousal=0; при controller=`nastya` игрушка выключается, иначе по умолчанию продолжает работать.
- В бодрствовании пассивные внутренние игрушки проверяются раз в 3 часа: одна — один бросок 30% на +1; vaginal remote + anal item — один общий бросок 50% на +1. Сюжетные события могут менять arousal независимо.
- С активной игрушкой заснуть нельзя. Во сне обычные пассивные проверки отключены; утром каждая установленная пассивная игрушка дает +1 (две дают +2).
- Эротический сон: шанс `min(60%, openness_rank*5% + bedtime_arousal*4%)`. Без сна действует обычный спад. При срабатывании итог сначала устанавливается в 3, затем применяются утренние бонусы игрушек (3+1=4, 3+1+1=5), максимум 10.
- HUD показывает максимум один значок возбуждения: ничего при 0–6, желтый статус при 7–9, красный при 10. Профиль использует вычисление названия по диапазону.
- «Без трусов» вычисляется только при пустом panties slot и надетой юбке или платье.
- Совместимость одежды/body items задается данными. `anal_plug` и `remote_toy` совместимы с трусиками; `tail_plug` несовместим двусторонне.
- Не создавать libido/desire, отдельный `no_panties_status`, combo-флаги или параллельную сексуальную систему.

## Критерии приемки

- Канон, save migration, runtime, actions, inventory/wardrobe, HUD/profile и тесты используют шкалу 0…10.
- Все временные накопители сохраняются и корректно обрабатывают неполные интервалы.
- Вероятность и cooldown источников тестируемы; повторный источник не фармится.
- Все утвержденные правила сна, remote auto-orgasm и совместимости покрыты regression-тестами.
- Ren'Py lint, адресный suite TASK-010, project health и runtime/визуальная проверка пройдены на доступном локальном контуре.

## Context Manifest

### READ REQUIRED

- `docs/systems/CHARACTERISTICS_SPEC.md`
- `docs/systems/TIME_ACTIONS_QUESTS_EVENTS_SPEC.md`
- `docs/systems/RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md`
- `docs/systems/HUD_TEMPORARY_EFFECTS_SPEC.md`
- `docs/world/actions/ACTIONS_29_AUGUST.md`
- карточки перечисленных `related_entities`

### CODE REQUIRED

- `game/domain/core.rpy`
- `game/content/definitions.rpy`
- `game/content/items.rpy`
- `game/ui/gameplay_screens.rpy`
- связанные regression suites в `game/tests/`

### READ IF NEEDED

- `game/content/day_one.rpy` — интеграция результата первого сна.
- `tools/sync_items.py` — генерация item registrations из канонических карточек.

### DO NOT SCAN

- весь `docs/` или `game/` рекурсивно;
- несвязанные персонажи, сцены и исторические TASK.

### CHECKS

- [ ] Item sync и `--check`.
- [ ] TASK-010 regression suite и затронутые first-day/TASK-008 suites.
- [ ] Project health check и diff check.
- [ ] Ren'Py lint/diagnostics.
- [ ] Runtime и визуальная проверка HUD/profile/inventory controls.
- [ ] Board/Roadmap impact check.

## Implementation report

### Что сделано

Реализованы все утвержденные требования TASK: шкала и migration 0…10, накопительный спад, probabilistic sources/cooldown, обычная мастурбация с выбором способа, persistent body timers, полный runtime/controller active remote-toy, auto-orgasm event, новый sleep contract, data-driven compatibility, HUD/profile и inventory controls.

### Измененные файлы

- Канон: четыре системные спецификации, action source и карточки участвующих items.
- Runtime/content: `game/domain/core.rpy`, `game/domain/item_rules.rpy`, `game/content/definitions.rpy`, сгенерированный `game/content/items.rpy`.
- UI/assets: `game/ui/gameplay_screens.rpy`, три status SVG.
- Проверки: новый `game/tests/task010_tests.rpy`, синхронизация first-day/TASK-008 regression и двух затронутых screenshot-baselines.

### Проверки и результат

- Уровень проверки: `FULL_LOCAL`.
- `tools/sync_items.py --check` — PASS.
- `task010_regression` — PASS.
- `first_day` — 4/4 PASS.
- Изолированный `task008::status_runtime` — PASS; новый HUD визуально просмотрен.
- Инвентарь remote-toy отрисован и визуально просмотрен: installed/active/controller и отдельная кнопка включения читаемы.
- Ren'Py lint — PASS.
- `tools/project_health_check.py` — 0 ошибок, 0 предупреждений.
- `git diff --check` — PASS.
- Общий suite: функциональные TASK-010, first-day и основные runtime-тесты проходят; общий результат не объявлен PASS из-за существующей нестабильности screenshot-baselines нескольких прежних suites. Изолированный inventory screenshot повторно отличается на 3072 пикселя при неизменном коде, поэтому не выдан за стабильный regression PASS.
- Приемка владельцем завершена 2026-09-14; карточка переведена в `done`, Git-синхронизация выполнена завершающим коммитом приемки.

### Отклонения от TASK

Нет продуктовых отклонений. Контекстные графические/сюжетные последствия auto-orgasm реализованы как расширяемый event payload и dispatcher hook; конкретные новые сцены/спрайты не создавались без отдельного утвержденного контента.

### Известные проблемы / осталось проверить

- Приемка владельцем завершена.
- Общий visual suite содержит нестабильные/устаревшие baselines прежних задач; это не скрыто и не включено в успех TASK-010.

### Коммиты реализации

- `18456f4`
