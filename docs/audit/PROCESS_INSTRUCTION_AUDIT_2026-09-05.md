# Process Instruction Audit — 2026-09-05

> Рабочий audit-report. Не является источником игрового канона. Проверка выполнена после рефакторинга writing/workflow-архитектуры по требованиям [`../PROCESS_INSTRUCTION_AUDIT.md`](../PROCESS_INSTRUCTION_AUDIT.md).

## 1. Причина проверки

Существенно изменены writing pipeline, handoff игрового текста, граница `Design/Discussion → In-game Authoring/Implementation`, роль In-game Progression Gate, TASK/Context Manifest для content authoring и модель исполнителей ChatGPT/Codex.

## 2. Проверенные актуальные источники

Проверены:

- Project Instructions текущего проекта ChatGPT;
- `AGENTS.md`;
- `README.md`;
- `docs/MASTER_SPEC.md`;
- `docs/DEVELOPMENT_WORKFLOW.md`;
- `docs/PROCESS_INSTRUCTION_AUDIT.md`;
- `docs/REPOSITORY_MAP.md`;
- `docs/content/README.md`;
- `docs/content/WRITING_PIPELINE.md`;
- `docs/content/ADULT_EROTIC_TONE_GUIDE.md`;
- `docs/content/DIALOGUE_WRITING_GUIDE.md`;
- `docs/tasks/README.md`;
- `docs/templates/TASK_TEMPLATE.md`;
- `docs/templates/CONTEXT_MANIFEST_TEMPLATE.md`;
- `docs/templates/README.md`;
- `docs/RENPY_MCP_WORKFLOW.md`;
- code-search по старым Codex-only формулировкам.

Исторические TASK и audit-файлы рассматриваются как история конкретной работы, а не как текущие нормативные владельцы процесса.

## 3. Результат

### PIA-001 — два полноценных исполнителя

**Статус: согласовано.**

ChatGPT и Codex — два полноценных исполнителя одного проекта. Оба могут разрабатывать код, документацию и игровой текст. Выбор определяется поручением владельца, доступными инструментами, масштабом/открытостью работы и фактически достижимым уровнем проверки, а не типом файла.

### PIA-002 — TASK не равен Codex

**Статус: согласовано.**

TASK может исполняться ChatGPT или Codex. Прямое поручение владельца — равноправный способ начать реализацию. Старые Codex-specific headings в исторических TASK не переписываются массово; при возврате такого TASK в активную работу он приводится к актуальному шаблону.

### PIA-003 — operational boundary writing

**Статус: согласовано.**

- `Design/Discussion` — In-game Progression Gate OFF;
- `In-game Authoring/Implementation` — Gate ON там, где применим;
- `Approved-text Transfer` — утвержденный текст переносится без самостоятельной художественной переработки.

Handoff определяется фактическим переходом к созданию/существенной редактуре игрового контента, а не наличием TASK.

### PIA-004 — Behavior Gate и Progression Gate разделены

**Статус: согласовано.**

Behavior Gate отвечает за сознательно допустимые решения/поведение Насти. In-game Progression Gate отвечает за художественную визуальную эскалацию фактической игры. Проектное обсуждение будущих и альтернативных вариантов Progression Gate не фильтрует.

### PIA-005 — единый Writing Pipeline

**Статус: согласовано.**

ChatGPT и Codex используют один `WRITING_PIPELINE.md` и одних владельцев подробных правил. Художественный стандарт не зависит от выбранного агента.

### PIA-006 — уровень технической проверки не привязан к агенту

**Статус: согласовано.**

`FULL_LOCAL` / `REMOTE_LIMITED` определяются фактически доступными средствами. Недоступность локального Ren'Py/MCP не делает Codex обязательным и сама по себе не запрещает ChatGPT реализовать изменение через GitHub.

### PIA-007 — локальные Codex-only формулировки вне process owners

**Статус: не являются распределением ролей; правятся по месту при затрагивании документа.**

Code-search может находить старые формулировки вроде «для Codex» в исторических TASK или отдельных предметных спецификациях. Они не переопределяют `AGENTS.md` и `DEVELOPMENT_WORKFLOW.md`. Массовая побочная правка несвязанных канонических спецификаций ради терминологии не выполняется; при следующем содержательном изменении такого документа формулировка приводится к executor-neutral виду.

Отдельно зафиксирован технический инцидент текущего аудита: при попытке точечно поправить `UI_VISUAL_SYSTEM_SPEC.md` через неполный текстовый fetch файл был непреднамеренно сокращен. Ошибка обнаружена сравнением с pre-refactor snapshot и полностью исправлена восстановлением исходного blob без переписывания истории. Это подтверждает правило: длинные канонические файлы нельзя заменять содержимым частичного/truncated fetch.

### PIA-008 — Project Instructions ChatGPT

**Статус: закрыто владельцем 2026-09-05.**

Владелец подтвердил, что ранее выявленный устаревший абзац Project Instructions заменен. Текущая внешняя инструкция теперь соответствует модели двух полноценных разработчиков: ChatGPT и Codex оба могут разрабатывать игровой код, документацию и игровой текст; Codex не становится обязательным только из-за `.rpy`, UI/runtime, многофайловости или самого факта программирования.

## 4. Change Impact

Проверено:

- `WRITING_PIPELINE.md` достижим через `MASTER_SPEC.md`, root README и `content/README.md`;
- TASK/templates направляют обоих исполнителей к одному pipeline;
- Repository Map содержит ответственность pipeline и dual-agent workflow;
- Ren'Py MCP workflow executor-neutral;
- старые Codex-specific headings в исторических TASK не являются текущими общими инструкциями;
- audit/backups остаются неканоническими рабочими/историческими материалами;
- pre-refactor compare после восстановления UI не показывает `UI_VISUAL_SYSTEM_SPEC.md` как измененный рефакторингом.

## 5. Итог

**Process Instruction Audit закрыт.** Известного конфликта между текущими Project Instructions, `AGENTS.md`, `DEVELOPMENT_WORKFLOW.md`, Writing Pipeline и TASK/templates по модели исполнителей и handoff игрового текста не осталось.
