# Настройка безопасной локальной синхронизации и Ren'Py-проверки

## Что это дает

Локальный Windows-контур Nastya Story используется для двух задач:

1. безопасно подтягивать актуальный `main` в рабочую копию `T:\Nastya_Story_G`;
2. выполнять на реальном Ren'Py SDK локальные проверки, результаты которых доступны через GitHub Actions.

Текущая схема:

`GitHub main → self-hosted runner → safe fast-forward → Ren'Py lint → Ren'Py testcase/runtime suite → GitHub Actions logs/artifacts`

Синхронизация **не перезаписывает локальную работу**. При грязном рабочем дереве, локальных неопубликованных коммитах, неверной ветке, неожиданном `origin` или невозможности безопасного fast-forward workflow прекращает работу.

Рабочая копия проекта:

```text
T:\Nastya_Story_G
```

Ren'Py SDK:

```text
T:\Renpy_SDK
```

Поскольку `T:` — переносной диск, runner не запускается автоматически вместе с Windows.

## Что находится в репозитории

- `.github/workflows/local-safe-sync.yml` — безопасная синхронизация локальной рабочей копии;
- `.github/workflows/local-renpy-verify.yml` — локальный Ren'Py lint + automated runtime/testcase checks;
- `tools/safe_sync_local.ps1` — проверки состояния и `git pull --ff-only`;
- `tools/run_local_renpy_verify.ps1` — запуск Ren'Py SDK, lint и runtime testcase suite;
- `game/tests/runtime_regression_tests.rpy` — автоматические Ren'Py regression/runtime testcases.

## 1. Базовые требования Windows

Из обычного PowerShell текущего пользователя должны работать:

```powershell
git --version
git fetch origin
git status
```

Также используется GitHub CLI:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

Windows-пароль, PAT, registration token и другие credentials не передавать в чат и не сохранять в репозитории.

## 2. Self-hosted runner

Runner зарегистрирован для `Vict0rSmith/Nastya_Story_G` с labels:

- `self-hosted`;
- `Windows`;
- `nastya-story`.

Runner установлен в:

```text
C:\actions-runner
```

### Почему runtime runner запускается интерактивно

Ren'Py lint может выполняться из Windows-службы, но официальный Ren'Py testcase framework запускает полный движок и использует реальный renderer/GUI-контекст.

Windows-служба работает в session 0 и не является надежной средой для такого runtime-запуска. Поэтому штатный режим Nastya Story:

- Windows-служба GitHub runner остается `Manual / Stopped`;
- runner запускается вручную через `C:\actions-runner\run.cmd` **в интерактивной пользовательской Windows-сессии** (раздел 4);
- GitHub job и дочерний Ren'Py runtime наследуют нормальный desktop/GPU-контекст;
- перед отключением диска интерактивный runner останавливается вручную.

Пользователь должен оставаться вошедшим в Windows во время runtime/testcase-проверок.

## 3. Repository variables

Используются несекретные repository variables.

### `NASTYA_LOCAL_REPO`

```text
T:\Nastya_Story_G
```

### `RENPY_SDK_ROOT`

```text
T:\Renpy_SDK
```

### `LOCAL_SYNC_ENABLED`

```text
true
```

Пароли, PAT и иные credentials в repository variables не помещать.

## 4. Запуск и остановка runner

Отдельной панели управления нет: runner запускается и останавливается вручную.

### Запуск runner

1. Подключить переносной диск.
2. Убедиться, что существуют:

```text
T:\Nastya_Story_G
T:\Renpy_SDK
```

3. Убедиться, что Windows-служба runner остановлена (`Get-Service "actions.runner.*"` показывает `Stopped`).
4. Запустить runner интерактивно в текущей Windows-сессии:

```powershell
& "C:\actions-runner\run.cmd"
```

5. При необходимости вручную запустить workflow `Local safe sync` (`workflow_dispatch`).

Окно runner может быть свернуто. Не выходить из Windows-профиля, пока нужны runtime-проверки.

### Остановка runner

Перед отключением диска остановить интерактивный runner (`Ctrl+C` в окне `run.cmd`) и убедиться, что процессы `Runner.Listener` завершены, а Windows-служба runner не запущена.

## 5. Local safe sync

`tools/safe_sync_local.ps1` проверяет:

- доступность `git.exe`;
- корректность `RepoRoot`;
- ожидаемый `origin`;
- ветку `main`;
- чистоту рабочего дерева;
- состояние после `git fetch origin`;
- отсутствие локальных неопубликованных коммитов.

Разрешен только:

```text
git pull --ff-only origin main
```

Скрипт никогда автоматически не выполняет:

- `git reset --hard`;
- force checkout;
- `git rebase`;
- `git stash`;
- удаление локальных файлов;
- force push;
- переключение рабочей ветки.

Если fast-forward невозможен, требуется ручное решение владельца.

## 6. Local Ren'Py verify

`.github/workflows/local-renpy-verify.yml` запускается для изменений, затрагивающих `game/` и сам verification-контур, а также вручную через `workflow_dispatch`.

Последовательность:

1. проверить variables и локальный путь;
2. checkout служебных verification-скриптов;
3. безопасно fast-forward локальный `main`;
4. запустить настоящий Ren'Py lint через SDK;
5. если lint успешен — запустить suite `nastya_runtime` через официальный Ren'Py `test` command;
6. загрузить lint/test reports в GitHub Actions artifact.

Runtime test command использует полный Ren'Py engine. Для стабильности отключаются sound/joystick/fullscreen, но renderer остается реальным.

Runtime-запуск ограничен таймаутом. Если renderer/testcase завис, job завершается ошибкой вместо бесконечного зависания.

## 7. Automated regression tests

Основной suite:

```text
nastya_runtime
```

Файл:

```text
game/tests/runtime_regression_tests.rpy
```

Текущий стартовый набор проверяет:

- создание нового `GameState` и основные registry;
- возможность отрисовать `game_hud`;
- deferred-flow `action_unpack_luggage`;
- одноразовые flags после завершения разбора чемоданов;
- известный дефект `TASK-004`: завершенное действие `action_unpack_luggage` должно исчезнуть из `location_actions()`.

Последняя проверка временно помечена `xfail`, пока известный дефект `TASK-004` не исправлен. После исправления gameplay-кода `xfail` должен быть снят; неожиданное прохождение xfail служит сигналом, что тест пора сделать обычной обязательной регрессией.

Новые важные gameplay/UI-flow по мере реализации следует добавлять в этот suite или в отдельные тематические testsuite, а не проверять только вручную.

## 8. Что получает ChatGPT

После завершения workflow ChatGPT через GitHub может:

- увидеть статус каждого job/step;
- прочитать workflow logs;
- скачать artifact с lint/test reports;
- определить, какой testcase упал;
- исправить код через GitHub;
- повторить цикл до зеленого результата.

Это позволяет выполнять полноценный локальный проверочный цикл без обязательного использования Codex для каждой Ren'Py-правки.

## 9. Диагностика

Проверить старую службу:

```powershell
Get-Service "actions.runner.*"
```

В штатном интерактивном режиме она должна быть `Stopped`.

Проверить процессы:

```powershell
Get-Process Runner.Listener, cmd -ErrorAction SilentlyContinue
```

Runner logs:

```text
C:\actions-runner\_diag
```

GitHub CLI:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" run list --repo Vict0rSmith/Nastya_Story_G --limit 10
```

## 10. Безопасность

Self-hosted runner выполняет код на реальном компьютере. Поэтому:

- не давать недоверенным пользователям права менять workflows;
- не запускать на runner произвольные внешние PR;
- не хранить credentials в workflow-файлах;
- runner включать только когда подключен ожидаемый переносной диск;
- перед отключением диска всегда останавливать интерактивный runner;
- периодически обновлять GitHub Actions Runner и Ren'Py SDK осознанно, с повторной проверкой verification-контура.
