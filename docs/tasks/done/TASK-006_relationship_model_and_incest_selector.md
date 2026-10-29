---
id: TASK-006
status: done
title: Модель отношений, глобальный селектор «Отношения с родственниками» и закрытие регрессии чемоданов
created: 2026-09-04
completed: 2026-09-06
approved_by_owner: true
executor: ChatGPT
verification_level: FULL_LOCAL
merge_commit: 274f9c085a752659bfd98a7ae6a48fc3634cbc44
---

# TASK-006 — Модель отношений, глобальный селектор «Отношения с родственниками» и закрытие регрессии чемоданов

> **Историческая запись.** Документ описывает состояние на момент закрытия задачи, когда Маша была сестрой Насти. С 2026-10-28 по канону Маша — подруга, `kinship=None`, `sexual_route_allowed=False`; тест селектора использует временного тестового родственника. Текст ниже не исправлялся.

## Статус

**DONE. Принято владельцем 2026-09-06.**

## Результат

- Старая линейная модель отношений заменена независимыми kinship / social / intimacy.
- Social: `unmet`, `neutral`, `friend`, `enemy`; intimacy: `none`, `sexual`, `romantic`; relationship points не используются.
- Kinship хранится в metadata NPC; родственники определяются без hardcoded списка ID.
- Стартовые состояния и разрешенные routes Маши, Ники, Анны и Аслана перенесены в новую модель.
- Реализованы API `get_relationship_state`, `get_social_state`, `set_social_state`, `get_intimacy_state`, `set_intimacy_state`, `is_relative_to_nastya`, `sexual_interaction_allowed` и отдельные события social/intimacy с `reason`.
- Schema повышена до 5; реализована миграция старых relationship states.
- Реализован один global persistent selector `Отношения с родственниками`, default ON; OFF блокирует sexual route родственников, не стирая историю и не затрагивая несексуальный контент.
- HUD/profile переведены на новую модель; Маша отображается как `Сестра`, потенциальные routes не спойлерятся.
- Закрыта regression TASK-004: завершенный `action_unpack_luggage` полностью исчезает из HUD, но до выполнения при отсутствии Маши остается видимым и корректно отказывает без затрат.

## Проверка

Уровень: `FULL_LOCAL`.

GitHub Actions `Local Ren'Py verify` run #25 на self-hosted runner `ANOVI-HW`, Ren'Py 8.5.3, commit `3b042bd1646f6c1f2aec302a2db03799eb2ddeba`:

- Ren'Py lint — успешно;
- runtime suite — 8/8 testcase;
- assertions — 38/38;
- HUD/profile render — успешно;
- luggage deferred flow — успешно;
- `unpack_luggage_action_disappears_after_completion` — успешно;
- visual before/after — успешно.

После документационного перевода в review Project Health также завершился успешно. PR #18 слит в `main` merge commit `274f9c085a752659bfd98a7ae6a48fc3634cbc44`.

## Change Impact Check

Затронуты domain relationship state/API/save schema, NPC relationship metadata/routes, HUD/profile/phone relationship display, Settings selector, runtime regression tests, локальный verification workflow и UI-regression TASK-004. Канонический литературный текст сцен не менялся; параллельные системы не создавались.

## Приемка

Владелец после успешного локального прогона прямо поручил закончить TASK-006 и TASK-004. Известных блокеров TASK-006 не осталось.
