# Writing System Refactor — Change Impact Plan

**Дата:** 2026-09-05  
**Статус:** утвержденный порядок работ; основные источники еще не рефакторились.  
**Основание:** `WRITING_SYSTEM_AUDIT.md` + `WRITING_PIPELINE_APPROVAL.md`.

> Документ является рабочим планом изменения и не заменяет основные канонические/процессные источники.

## 1. Цель правки

Перенести утвержденную пятифазовую Writing Pipeline в основной контур проекта без создания нового мегагайда, устранить дубли художественных правил, отделить Behavior/Event/Player Visual/Progression/Reaction responsibilities и синхронизировать handoff к фактической реализации для ChatGPT и Codex.

## 2. Основные источники, которые требуется изменить

### 2.1. `docs/content/ADULT_EROTIC_TONE_GUIDE.md` — основной художественный владелец

**Изменить.**

Сохранить:
- жанровую роль эротики;
- participant meaning vs player optics;
- Player Visual Access;
- Visual/Erotic Selection;
- визуальную прогрессию;
- scripted override;
- принцип отсутствия дополнительной санитизации.

Уточнить:
- явно отделить `Design/Discussion Mode` от `In-game Authoring/Implementation`;
- In-game Progression Gate применяется только при handoff к созданию/существенной редакции фактического игрового контента;
- обсуждение, аудит, проектирование, варианты и тестовые примеры до handoff не фильтруются визуальной лестницей;
- progression не определяет объективную физику события, Behavior Gate или Reaction Model;
- scripted override модифицирует показ конкретного content/event, а не openness rank;
- заменить собственный длинный generation-order ссылкой/маршрутом через Writing Pipeline после появления pipeline-файла.

### 2.2. `docs/content/DIALOGUE_WRITING_GUIDE.md` — основной владелец общего writing/editing layer

**Изменить.**

Сохранить:
- natural conversational Russian;
- screen semantic blocks;
- physical/causal continuity;
- Semantic & Logic Pass;
- Character Voice boundary;
- Humanization Pass и диагностические тесты;
- защиту значимых физических фактов.

Уточнить/сократить:
- разделить `Scene Fact / Continuity Anchor` и эротический `Visual Selection`;
- закрепить locked anchor как `fact + required specificity`;
- эротический художественный выбор не дублировать, а ссылать на Erotic Guide;
- Humanization не определяет интенсивность и не уничтожает locked anchors;
- финальный огромный checklist заменить коротким invariant QA/ссылкой на Writing Pipeline;
- VERIFY диагностирует и возвращает на соответствующую фазу, а не самостоятельно переписывает все.

### 2.3. Новый короткий `docs/content/WRITING_PIPELINE.md`

**Создать.**

Назначение: исполняемый маршрутизатор существующих владельцев правил, а не третий мегагайд.

Содержимое:
- три режима `Design/Discussion`, `In-game Authoring/Implementation`, `Approved-text Transfer`;
- 5 фаз `LOAD & MODE → BUILD SCENE → SELECT CONTENT & REACTIONS → WRITE & EDIT → VERIFY`;
- sparse Scene Context Sheet;
- locked outputs/invariants;
- условные ветки;
- ссылки на владельцев подробных правил;
- правило возврата VERIFY на фазу-источник ошибки.

Не дублировать:
- индивидуальные голоса персонажей;
- таблицу openness ranks;
- полную визуальную лестницу;
- системную механику событий;
- полный Humanization checklist.

### 2.4. `docs/systems/CHARACTERISTICS_SPEC.md`

**Небольшое уточнение.**

Закрепить, что openness — Behavior Gate для осознанно допустимого поведения/выбора Насти и не является универсальным фильтром содержания сцены, физической видимости игроку или обсуждения проектных вариантов.

Не переносить сюда визуальную лестницу.

### 2.5. `docs/systems/SITUATIONAL_EVENTS_SPEC.md`

**Сократить и связать.**

Сохранить:
- source types;
- trigger modes;
- conditions;
- results;
- cooldown/RNG;
- Event Availability Gate;
- техническую возможность scripted/content override.

Удалить/сократить как дубли:
- нормативное описание индивидуальной неуклюжести Насти;
- нормативное описание беспечности Маши;
- повтор художественной эротической логики/визуальной лестницы.

Вместо этого дать ссылки на character canon и Erotic Guide/Writing Pipeline.

## 3. Процессные источники, которые требуется синхронизировать после художественного рефакторинга

### 3.1. `AGENTS.md`

**Изменить после content/system owners.**

- явно определить operational boundary: проектное обсуждение ≠ фактическая реализация игрового контента;
- для создания/существенной редакции игрового текста обязать применять Writing Pipeline;
- In-game Progression Gate включается при фактическом authoring/implementation независимо от TASK или прямого поручения;
- Approved-text Transfer не запускает самовольную художественную переработку;
- сохранить правило обязательного чтения Erotic Guide + Dialogue Guide + карточек участников для применимого текста.

### 3.2. `docs/DEVELOPMENT_WORKFLOW.md`

**Изменить после AGENTS/content.**

- описать handoff из design/discussion в actual content authoring;
- TASK и прямое поручение остаются равноправными способами handoff;
- при authoring передавать минимальный Content Authoring Context, не копируя художественные правила;
- технический перенос утвержденного текста отличать от substantial edit.

### 3.3. `docs/templates/TASK_TEMPLATE.md`

**Изменить.**

Добавить условный `Content Authoring Context` только для TASK, который создает/существенно редактирует игровой текст. Он должен передавать конкретные входы сцены, например:
- content mode;
- scene/source;
- participants;
- progression context, если применим;
- scripted override, если применим;
- mandatory facts/approved text reference.

Не копировать в TASK визуальную лестницу или character canon.

### 3.4. `docs/templates/CONTEXT_MANIFEST_TEMPLATE.md`

**Изменить.**

При content-authoring добавить `WRITING_PIPELINE.md` в обязательный стартовый набор и сохранить Erotic/Dialogue/character owners как прямые зависимости.

### 3.5. `docs/tasks/README.md`

**Небольшая синхронизация.**

Уточнить content-authoring handoff и ссылку на обновленный TASK template/pipeline. Не превращать tasks README в художественный источник.

## 4. Навигационные/MOC-файлы, которые требуется проверить и вероятно изменить

### `docs/content/README.md`

**Изменить:** добавить `WRITING_PIPELINE.md` как короткую точку входа в генерацию/редактуру и четко описать владельцев Erotic vs Dialogue vs Pipeline.

### `docs/MASTER_SPEC.md`

**Изменить навигационно:** при создании/существенной редактуре игрового текста направлять через Writing Pipeline и его владельцев, сохранив layered loading.

### `README.md`

**Проверить и вероятно минимально изменить:** раздел `Начало работы AI` и ownership, если после появления pipeline текущая навигация станет неполной.

### `docs/systems/README.md`

**Проверить:** текущий принцип `Erotic Guide — единственный художественный владелец прогрессии` уже правильный. Изменять только если ссылки/формулировки после рефакторинга станут неполными.

### `docs/templates/README.md`

**Проверить/минимально изменить**, если меняется назначение TASK/Context Manifest templates.

### `docs/REPOSITORY_MAP.md`

**Изменить:** добавить Writing Pipeline в матрицу ответственности/зависимостей и актуализировать Change Impact для общих writing rules и content-authoring workflow.

## 5. Process Instruction Audit

`docs/PROCESS_INSTRUCTION_AUDIT.md` сам по себе, вероятно, **не требует смысловой правки**: он уже правильно требует сверять Project Instructions, AGENTS, Workflow, MASTER_SPEC/tasks MOC после существенных процессных изменений.

После рефакторинга его необходимо **выполнить**, а не переписать без причины.

Project Instructions ChatGPT находятся вне GitHub. После репозиторных изменений отдельно сверить их с новым operational boundary. Если потребуется изменение, владельцу дать точный заменяемый фрагмент.

## 6. Что не менять в рамках этого рефакторинга без обнаруженной зависимости

- character canon cards — индивидуальные владельцы уже устроены правильно;
- `RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md` — openness используется корректно как Behavior Gate;
- готовые сцены/диалоги — не переписывать массово только из-за изменения writing architecture;
- `game/` — этот этап меняет систему инструкций/канона написания, а не реализацию игровых механик;
- Roadmap/Board — только если рефакторинг фактически меняет их отслеживаемый статус/приоритет.

## 7. Pre-refactor backup set

Перед первой правкой основных источников сохранить отдельный snapshot следующего **планируемого изменяемого контура**:

1. `docs/content/ADULT_EROTIC_TONE_GUIDE.md`;
2. `docs/content/DIALOGUE_WRITING_GUIDE.md`;
3. `docs/systems/CHARACTERISTICS_SPEC.md`;
4. `docs/systems/SITUATIONAL_EVENTS_SPEC.md`;
5. `AGENTS.md`;
6. `docs/DEVELOPMENT_WORKFLOW.md`;
7. `docs/templates/TASK_TEMPLATE.md`;
8. `docs/templates/CONTEXT_MANIFEST_TEMPLATE.md`;
9. `docs/tasks/README.md`;
10. `docs/content/README.md`;
11. `docs/MASTER_SPEC.md`;
12. `README.md`;
13. `docs/REPOSITORY_MAP.md`;
14. `docs/systems/README.md`;
15. `docs/templates/README.md`.

`docs/PROCESS_INSTRUCTION_AUDIT.md` включить в snapshot как контрольный процессный документ, даже если его текст по текущему плану не меняется.

Новый `WRITING_PIPELINE.md` в pre-refactor snapshot отсутствует, потому что до рефакторинга файла нет.

## 8. Backup policy

Snapshot хранить отдельно от канонических каталогов, например:

`docs/audit/backups/writing-system-pre-refactor-2026-09-05/`

В backup README обязательно указать:
- `NON-CANONICAL BACKUP`;
- исходный commit/ref;
- дату;
- перечень файлов и исходные blob SHA;
- что актуальный канон всегда читается из обычных путей репозитория;
- способ восстановления через исходный commit/blob даже если физическая копия backup-файла впоследствии удалена.

## 9. Последовательность выполнения

1. архитектура pipeline — утверждена;
2. Change Impact Plan — этот документ;
3. создать pre-refactor snapshot;
4. рефакторить content/system owners;
5. создать/подключить `WRITING_PIPELINE.md`;
6. синхронизировать AGENTS/workflow/TASK/Context Manifest;
7. синхронизировать MOC/Repository Map;
8. выполнить Process Instruction Audit;
9. проверить отсутствие конкурирующих источников/мертвых ссылок/старых TASK requirements;
10. провести контрольные ChatGPT/Codex tests.