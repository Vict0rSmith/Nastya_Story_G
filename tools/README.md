# Tools

Служебные инструменты и контуры разработки проекта.

- `safe_sync_local.ps1`, `check_git_sync.ps1` — штатный локальный safe-sync контур (см. [`../docs/LOCAL_SYNC_SETUP.md`](../docs/LOCAL_SYNC_SETUP.md)).
- `run_local_renpy_verify.ps1` — запуск адресной локальной Ren'Py-проверки по правилам `docs/RENPY_MCP_WORKFLOW.md`. Работает и в Git-репозитории, и в обычной папке; saves/persistent во время проверки по умолчанию пишутся во временный каталог (`-SaveDir`), а не в реальный persistent игрока.
- `project_health_check.py` — дешевые детерминированные проверки структуры репозитория и жизненного цикла TASK.
- `sync_items.py` — компиляция канонических карточек предметов в регистрации Ren'Py.
- `sync_world_map.py` — компиляция карты мира и карточек доступа локаций в runtime-данные.

Этот раздел не является источником игрового канона.
