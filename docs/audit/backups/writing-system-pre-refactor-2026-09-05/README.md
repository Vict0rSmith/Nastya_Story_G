# NON-CANONICAL BACKUP — Writing System pre-refactor snapshot

**Дата:** 2026-09-05  
**Назначение:** контрольная точка непосредственно перед рефакторингом writing/content-authoring architecture.  
**Snapshot ref:** `5acc909f1108da268c72e077db5039a9015c2142`  
**Предыдущий stress-test commit:** `c98134dd4d260f07052b6802644051e33b34b266`

> **NON-CANONICAL BACKUP. НЕ ИСПОЛЬЗОВАТЬ КАК ИСТОЧНИК ТЕКУЩЕГО КАНОНА.**
>
> Актуальные правила всегда читаются из обычных путей репозитория через `docs/MASTER_SPEC.md`. Этот каталог существует только для сравнения, аудита и восстановления состояния до рефакторинга.

## Почему snapshot хранится как immutable manifest

Git уже хранит полное точное содержимое каждого файла по commit/blob SHA. Чтобы не создавать рядом с каноном физические дубликаты, которые поиск AI/Codex может ошибочно принять за второй нормативный источник, backup фиксируется как **immutable manifest**: точный snapshot commit + blob SHA каждого файла.

Это дает полный побайтовый возврат к прежней версии без создания конкурирующей копии в рабочем дереве.

Для просмотра старой версии открыть файл на `Snapshot ref`. Для восстановления конкретного файла взять его содержимое из указанного commit/blob и вернуть в обычный канонический путь отдельной осознанной правкой.

## Snapshot files

| Обычный путь | Blob SHA до рефакторинга |
|---|---|
| `docs/content/ADULT_EROTIC_TONE_GUIDE.md` | `11e76f3be0fb03c17938ef46ae306109e9f15921` |
| `docs/content/DIALOGUE_WRITING_GUIDE.md` | `f7254352084f2d330f9a4c75abea759a971284a9` |
| `docs/systems/CHARACTERISTICS_SPEC.md` | `b03e4d6b8519bf57ca0cb4b298da0b80987d076d` |
| `docs/systems/SITUATIONAL_EVENTS_SPEC.md` | `eeac8000a8b33d3dda65f309cecafcf720c1310d` |
| `AGENTS.md` | `80feeba544c5e79013acafbc7d3ae61c94a8b9ff` |
| `docs/DEVELOPMENT_WORKFLOW.md` | `8869422b4d2cc8959c3ed23e1bf06cc25de6b6c7` |
| `docs/templates/TASK_TEMPLATE.md` | `0d791cb1f717dd902ceb36c06629d1e9376979d8` |
| `docs/templates/CONTEXT_MANIFEST_TEMPLATE.md` | `d0e8533df8dfd1cb631c3f2172dc613dc6298d8b` |
| `docs/tasks/README.md` | `7e9d0531d181cbab8807fb4e855a0641d75d7827` |
| `docs/content/README.md` | `9eab4c79f945a8c4f05c6bd00d9019aedeff0346` |
| `docs/MASTER_SPEC.md` | `80ea7c37827ac5a4382e61f1385c44019d25c032` |
| `README.md` | `2e3b2eba55e48b1a0119cc3665383c2bd9dbe48b` |
| `docs/REPOSITORY_MAP.md` | `8f0fb86287851c30c40651ed3b89e8fb6605a992` |
| `docs/systems/README.md` | `86b4665798bdcf9ee0016afdc5c3977eb44d5b92` |
| `docs/templates/README.md` | `b1e354f22fc2741d88047898802de33180e48b96` |
| `docs/PROCESS_INSTRUCTION_AUDIT.md` | `0f204a234a396c83e32a2761c64c8e9eb2104215` |

## Отдельно отсутствует до рефакторинга

`docs/content/WRITING_PIPELINE.md` — новый файл; в этом snapshot его нет.

## Контроль восстановления

При необходимости сравнения/rollback:

1. не читать этот backup как текущий канон;
2. открыть нужный обычный путь на commit `5acc909f1108da268c72e077db5039a9015c2142`;
3. при необходимости сверить blob SHA с таблицей;
4. сравнить со свежей версией обычного пути;
5. восстанавливать только явно выбранные правила/файлы, а не автоматически откатывать весь репозиторий.

Такой способ позволяет как посмотреть «как было раньше», так и полностью восстановить исходный файл, при этом не загрязняет актуальную базу знаний дублирующими нормативными документами.