# Игровые системы — карта раздела

Канонические технические спецификации общих механик. Для конкретной задачи читать только нужную спецификацию и ее явные зависимости.

- [`CHARACTERISTICS_SPEC.md`](CHARACTERISTICS_SPEC.md) — характеристики, энергия, раскрепощенность, возбуждение и развитие персонажа.
- [`RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md`](RELATIONSHIPS_INVENTORY_WARDROBE_SPEC.md) — отношения, инвентарь и гардероб.
- [`TIME_ACTIONS_QUESTS_EVENTS_SPEC.md`](TIME_ACTIONS_QUESTS_EVENTS_SPEC.md) — время, действия, расписания, квесты и события.
- [`ROLLBACK_POLICY_SPEC.md`](ROLLBACK_POLICY_SPEC.md) — глобальный запрет интерактивного отката игрового состояния и разграничение rollback с обычной UI-навигацией.
- [`SLEEP_ALARM_SPEC.md`](SLEEP_ALARM_SPEC.md) — доступность и длительность сна, почасовое восстановление энергии и одноразовый будильник телефона.
- [`UI_VISUAL_SYSTEM_SPEC.md`](UI_VISUAL_SYSTEM_SPEC.md) — HUD, телефон, инвентарь и визуальный интерфейс.
- [`NPC_INTERACTION_CONVERSATION_SPEC.md`](NPC_INTERACTION_CONVERSATION_SPEC.md) — взаимодействие с присутствующими NPC, действие «Поговорить», контекстные темы после событий и короткий бытовой разговор при отсутствии специальных тем.
- [`NUTRITION_SPEC.md`](NUTRITION_SPEC.md) — питание, голод и сытость.
- [`ACTION_EFFECT_COOLDOWNS_SPEC.md`](ACTION_EFFECT_COOLDOWNS_SPEC.md) — кулдауны восстановительных эффектов.
- [`TRANSPORT_SPEC.md`](TRANSPORT_SPEC.md) — транспорт и перемещение между гиперкластерами.
- [`UNIVERSITY_SPEC.md`](UNIVERSITY_SPEC.md) — университет, прогресс и стипендия.
- [`HUD_TEMPORARY_EFFECTS_SPEC.md`](HUD_TEMPORARY_EFFECTS_SPEC.md) — временные эффекты HUD.
- [`SITUATIONAL_EVENTS_SPEC.md`](SITUATIONAL_EVENTS_SPEC.md) — ситуативные события персонажей и ненавязчивый пикантный/эротический слой.
- [`PERSONAL_GROOMING_SPEC.md`](PERSONAL_GROOMING_SPEC.md) — добровольный косметический уход, одноразовые бритвы и недельное поддержание выбранного состояния интимной зоны.
- [`ECONOMY_BANKING_SPEC.md`](ECONOMY_BANKING_SPEC.md) — единый кошелек, история операций, банковское приложение, переводы, займы и кредиты.

Художественный смысл постепенной эротической прогрессии, который механически поддерживают раскрепощенность, возбуждение, одежда и ситуативные события, задается только [`../content/ADULT_EROTIC_TONE_GUIDE.md`](../content/ADULT_EROTIC_TONE_GUIDE.md), а не дублируется в каждой системной спецификации.

Верхнеуровневая карта: [`../MASTER_SPEC.md`](../MASTER_SPEC.md). Правила зависимостей и change-impact: [`../REPOSITORY_MAP.md`](../REPOSITORY_MAP.md).
