# Ядро домена: действия, будильник, сон и применение эффектов.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import datetime
    import random

    def calculate_action_energy_cost(action, state):
        cost = action.base_energy_cost
        if action.physical: cost += (1, 0, -1, -2, -3)[state.player.fitness.rank]
        if action.physical and nutrition_state(state) in ("hungry", "very_hungry"): cost += 1
        return max(action.minimum_energy_cost, cost)
    AROUSAL_SOURCE_ACTIONS = {
        "action_view_adult_magazine": ("adult_magazine", 0.40, 1, 360),
        "action_watch_adult_movie": ("adult_movie", 0.70, 2, 720),
        "action_read_sex_illustrated_book": ("sex_illustrated_book", 0.50, 1, 480),
    }
    MASTURBATION_DURATIONS = {None: 30, "dildo": 30, "anal_beads": 30, "vibrator": 20, "bullet_vibrator": 20, "vacuum_stimulator": 20}

    def alarm_display_time(state=None):
        alarm = _state(state).alarm
        if alarm.time_minutes is None: return "--:--"
        hour, minute = divmod(int(alarm.time_minutes), 60)
        return "%02d:%02d" % (hour, minute)

    def set_alarm_time_minutes(value, state=None):
        state = _state(state)
        state.alarm.time_minutes = int(value) % 1440
        dispatch_game_event("alarm_time_changed", state, False, time_minutes=state.alarm.time_minutes)
        return state.alarm.time_minutes

    def adjust_alarm_time(minutes, state=None):
        state = _state(state)
        current = 8 * 60 if state.alarm.time_minutes is None else state.alarm.time_minutes
        return set_alarm_time_minutes(current + int(minutes), state)

    def set_alarm_enabled(enabled, state=None):
        state = _state(state)
        if enabled and state.alarm.time_minutes is None: state.alarm.time_minutes = 8 * 60
        state.alarm.enabled = bool(enabled)
        dispatch_game_event("alarm_enabled_changed", state, False, enabled=state.alarm.enabled, time_minutes=state.alarm.time_minutes)
        return state.alarm.enabled

    def alarm_target_datetime(state=None):
        state = _state(state); alarm = state.alarm
        if not alarm.enabled or alarm.time_minutes is None: return None
        current = _game_datetime(state)
        hour, minute = divmod(int(alarm.time_minutes), 60)
        target = datetime.datetime.combine(current.date(), datetime.time(hour, minute))
        if target <= current: target += datetime.timedelta(days=1)
        return target

    def sleep_duration_minutes(state=None):
        state = _state(state); current = _game_datetime(state)
        full_recovery = current + datetime.timedelta(minutes=max(0, state.player.max_energy - state.player.energy) * 60)
        alarm_target = alarm_target_datetime(state)
        wake_at = min(full_recovery, alarm_target) if alarm_target is not None else full_recovery
        return max(0, int((wake_at - current).total_seconds() // 60))

    def action_duration_minutes(action, item_id=None, state=None):
        if action.id == "action_masturbate": return MASTURBATION_DURATIONS.get(item_id, action.duration_minutes)
        if action.id == "action_sleep": return sleep_duration_minutes(state)
        return action.duration_minutes

    def admissions_conversation_available(state=None):
        state = _state(state)
        return (datetime.date(2026, 8, 29) <= state.clock.date < datetime.date(2026, 9, 1)
                and first_day_required_objectives_complete(state)
                and "masha_admissions_conversation_seen" not in state.story.flags)

    def masha_documents_reminder_available(state=None):
        state = _state(state)
        quest = state.quests.get("quest_2026_08_29_first_normal_day")
        objective = quest.objectives.get("remind_masha_school_documents") if quest else None
        return (is_first_day(state)
                and "masha_school_documents_reminded" not in state.story.flags
                and not (objective and objective.completed))

    def arousal_source_ready(action_id, state=None):
        state = _state(state); ready = state.arousal_source_ready_at.get(action_id)
        return ready is None or _game_datetime(state) >= ready

    def private_intimate_context(state=None):
        state = _state(state)
        return state.location_id in ("loc_apartment_5_room", "loc_apartment_5_bathroom") and not get_present_npcs(state=state)
    def check_action(action_id, state=None):
        state = _state(state); action = ACTIONS.get(action_id)
        if action is None: return None, ["Неизвестное действие"]
        reasons = []
        if state.player.openness.rank < action.required_openness: reasons.append("Недостаточная раскрепощенность для действия")
        if not conditions_match(action.conditions, state): reasons.append("Условия действия не выполнены")
        effect_reason = item_effects_reason(action.effects, state)
        if effect_reason: reasons.append(effect_reason)
        if action.locations and state.location_id not in action.locations: reasons.append("Действие недоступно в этой локации")
        if action.required_npc and action.required_npc not in get_present_npcs(state=state): reasons.append("Персонажа здесь нет")
        if action_id == "action_submit_university_documents":
            if "university_documents_submitted" in state.story.flags: reasons.append("Документы уже поданы")
            elif not first_day_admissions_open_for_action(state): reasons.append("Прием документов идет 29 августа с 13:00 до 18:00")
        if action_id in ("action_ask_shop_job", "action_ask_cafe_job") and action_id + "_completed" in state.story.flags: reasons.append("Об этой вакансии уже узнали")
        if action_id == "action_visit_nika" and "first_visit_nika_completed" in state.story.flags: reasons.append("К Нике сегодня уже заходили")
        if action_id == "action_sleep" and state.player.energy >= 5: reasons.append("Спать пока не хочется")
        if action_id == "action_sleep" and remote_toy_is_active(state): reasons.append("С включенной игрушкой заснуть нельзя")
        if action_id == "action_talk_masha_admissions" and not admissions_conversation_available(state): reasons.append("Эта тема сейчас недоступна")
        if action_id == "action_remind_masha_school_documents" and not masha_documents_reminder_available(state): reasons.append("Вы уже обсудили документы Маши")
        if action_id == "action_masturbate":
            if state.player.arousal < 5: reasons.append("Недостаточное возбуждение")
            if not private_intimate_context(state): reasons.append("Нужно остаться одной в комнате или ванной")
        if action_id in AROUSAL_SOURCE_ACTIONS:
            if not arousal_source_ready(action_id, state): reasons.append("Этот источник пока не вызывает новой реакции")
            if not private_intimate_context(state): reasons.append("Нужно остаться одной в комнате или ванной")
        if action_id == "action_prepare_meal" and not any(inventory_has(item_id, 1, state) for item_id, item in ITEMS.items() if "food_kit" in item.get("tags", ())): reasons.append("Нет продуктовых комплектов для приготовления")
        if action_id == "action_eat_full_meal" and not inventory_has("prepared_home_meal", 1, state): reasons.append("Нет готовой еды")
        if nutrition_state(state) == "very_hungry" and action_id == "action_exercise": reasons.append("При сильном голоде зарядка недоступна: сначала нужно поесть")
        if action_id != "action_submit_university_documents" and first_day_deadline_blocks(action_duration_minutes(action, state=state), state): reasons.append("Сначала нужно успеть подать документы в университет")
        if action_id == "action_unpack_luggage":
            if LUGGAGE_UNPACKED_FLAG in state.story.flags: reasons.append("Чемоданы уже разобраны")
            elif not npc_is_in_apartment("masha", state): reasons.append("Вещи лучше разобрать вместе с Машей. Нужно дождаться, когда она вернется домой.")
        if action_id in ("action_shave_legs", "action_shave_pubic") and not inventory_has(RAZOR_ITEM_ID, 1, state): reasons.append("Нужна одноразовая бритва")
        if action_id == "action_shave_pubic" and pubic_grooming_is_fresh(state): reasons.append("Обновлять интимный уход пока не требуется")
        cost = calculate_action_energy_cost(action, state)
        if state.player.energy < cost: reasons.append("Недостаточно энергии")
        return action, reasons
    def execute_action(action_id, state=None, item_id=None):
        state = _state(state); action, reasons = check_action(action_id, state)
        if reasons: return ActionResult(False, action_id, reasons=reasons)
        reason = action_item_reason(action, item_id, state)
        if reason: return ActionResult(False, action_id, reasons=[reason])
        deferred_scenes = {
            "action_unpack_luggage": "scene_2026_08_29_unpack_luggage",
            "action_remind_masha_school_documents": "scene_2026_08_29_masha_documents",
            "action_submit_university_documents": "scene_2026_08_29_university_documents",
            "action_ask_shop_job": "scene_2026_08_29_shop_job",
            "action_ask_cafe_job": "scene_2026_08_29_cafe_job",
            "action_visit_nika": "scene_2026_08_29_visit_nika",
            "action_talk_masha_admissions": "scene_2026_08_29_admissions_conversation",
        }
        if deferred_scenes.get(action_id):
            state.story.pending_action = action_id; state.story.pending_action_item = item_id; state.story.pending_scene = deferred_scenes[action_id]; return ActionResult(True, action_id, deferred=True)
        return _complete_action(action, state, item_id)
    def _complete_action(action, state, item_id=None):
        action_id = action.id
        if action_id == "action_sleep": return complete_sleep(state)
        if action_id == "action_submit_university_documents": state.story.flags.update(("university_documents_submitted", "phone_app:university"))
        if action_id == "action_prepare_meal":
            kit_id = next(item_id for item_id, item in ITEMS.items() if "food_kit" in item.get("tags", ()) and inventory_has(item_id, 1, state))
            inventory_remove(kit_id, 1, state)
            inventory_add("prepared_home_meal", 1, state)
        if action_id == "action_eat_full_meal":
            inventory_remove("prepared_home_meal", 1, state)
        arousal_effect = 0
        arousal_cooldown = None
        if action_id in AROUSAL_SOURCE_ACTIONS:
            source_item, chance, amount, cooldown = AROUSAL_SOURCE_ACTIONS[action_id]
            arousal_effect = amount if renpy.random.random() < chance else 0
            arousal_cooldown = cooldown
        duration = action_duration_minutes(action, item_id)
        cost = calculate_action_energy_cost(action, state); change_energy(-cost, state, action_id); advance_time(duration, action_id, state, arousal_compensated=bool(arousal_effect))
        for effect in action.effects: _apply_effect(state, effect)
        if arousal_effect: change_arousal(arousal_effect, state)
        if arousal_cooldown is not None: state.arousal_source_ready_at[action_id] = _game_datetime(state) + datetime.timedelta(minutes=arousal_cooldown)
        if action_id == "action_masturbate":
            state.player.arousal = 0
            dispatch_game_event("orgasm", state, True, source="masturbation", method=item_id or "hands")
        if action_id == "action_eat_full_meal":
            state.last_full_meal_at = _game_datetime(state)
            state.nutrition_elapsed_minutes = 0.0
        if action_id in ("action_shave_legs", "action_shave_pubic"):
            if not inventory_remove(RAZOR_ITEM_ID, 1, state): raise RuntimeError("Razor disappeared while completing grooming action")
        if action_id == "action_shave_pubic": maintain_pubic_grooming(state=state)
        if action_id == "action_unpack_luggage": state.story.flags.add(LUGGAGE_UNPACKED_FLAG); state.story.flags.add(UNPACK_LUGGAGE_SCENE_FLAG)
        if action_id in ("action_ask_shop_job", "action_ask_cafe_job"): state.story.flags.add(action_id + "_completed")
        if action_id == "action_visit_nika": state.story.flags.add("first_visit_nika_completed")
        if action_id == "action_remind_masha_school_documents": state.story.flags.add("masha_school_documents_reminded")
        if action_id == "action_talk_masha_admissions": state.story.flags.add("masha_admissions_conversation_seen")
        if item_id:
            if "adult_media" in ITEMS[item_id].get("tags", ()):
                counter_key = "media_reads_remaining:" + item_id
                remaining = int(state.story.counters.get(counter_key, 5)) - 1
                if remaining <= 0: inventory_remove(item_id, 1, state)
                else: state.story.counters[counter_key] = remaining
            elif ITEMS[item_id].get("consumable"): inventory_remove(item_id, 1, state)
            dispatch_game_event("inventory_item_used", state, False, item_id=item_id, action_id=action_id)
        dispatch_game_event("action_completed", state, True, action_id=action_id, item_id=item_id, tags=action.tags); return ActionResult(True, action_id, cost, duration)
    def complete_deferred_action(action_id, state=None):
        state = _state(state)
        if state.story.pending_action != action_id: return ActionResult(False, action_id, reasons=["Отложенное действие не ожидается"])
        item_id = state.story.pending_action_item
        reason = action_item_reason(ACTIONS[action_id], item_id, state)
        if reason: return ActionResult(False, action_id, reasons=[reason])
        state.story.pending_action = None; state.story.pending_action_item = None
        return _complete_action(ACTIONS[action_id], state, item_id)

    def complete_sleep(state=None, dream_roll=None):
        state = _state(state)
        if state.player.energy >= 5: return ActionResult(False, "action_sleep", reasons=["Спать пока не хочется"])
        if remote_toy_is_active(state): return ActionResult(False, "action_sleep", reasons=["С включенной игрушкой заснуть нельзя"])
        minutes = sleep_duration_minutes(state)
        bedtime_arousal = state.player.arousal
        dream_chance = min(0.60, state.player.openness.rank * 0.05 + bedtime_arousal * 0.04)
        dream_happened = (renpy.random.random() if dream_roll is None else float(dream_roll)) < dream_chance
        advance_time(minutes, "action_sleep", state, passive_checks=False)
        change_energy(minutes // 60, state, "action_sleep")
        state.alarm.enabled = False
        if dream_happened:
            state.player.arousal = 3
            dispatch_game_event("erotic_dream", state, True, bedtime_arousal=bedtime_arousal, chance=dream_chance)
        passive_bonus = len(_installed_passive_body_items(state))
        if passive_bonus: change_arousal(passive_bonus, state)
        dispatch_game_event("action_completed", state, True, action_id="action_sleep", item_id=None, tags=ACTIONS["action_sleep"].tags)
        return ActionResult(True, "action_sleep", 0, minutes)

    def _apply_effect(state, effect):
        kind = effect[0]
        if kind == "energy": change_energy(effect[1], state, "action_effect")
        elif kind == "mood": set_mood(effect[1], state)
        elif kind == "fitness": add_fitness_progress(effect[1], state)
        elif kind == "intellect": add_intellect_progress(effect[1], state)
        elif kind == "skill": add_skill_progress(effect[1], effect[2], state)
        elif kind == "flag": set_story_flag(effect[1], True, state)
        elif kind == "nutrition_full":
            state.last_full_meal_at = _game_datetime(state)
            state.nutrition_elapsed_minutes = 0.0
        elif kind == "nutrition_cap":
            state.nutrition_elapsed_minutes = min(getattr(state, "nutrition_elapsed_minutes", 0.0), float(effect[1]))
        elif kind == "energy_boost":
            change_energy(effect[1], state, "energy_drink")
            state.energy_drink_ready_at = _game_datetime(state) + datetime.timedelta(minutes=int(effect[2]))
        elif kind == "time": advance_time(effect[1], "item_use", state)
        elif kind == "body_item":
            success, reason = set_body_item(effect[1], effect[2], state)
            if not success: raise ValueError(reason)
        elif kind == "arousal": change_arousal(effect[1], state)
        elif kind == "remote_toy_active":
            success, reason = set_remote_toy_active(effect[1], state, scripted=True)
            if not success: raise ValueError(reason)
        elif kind == "remote_toy_controller":
            success, reason = set_remote_toy_controller(effect[1], state)
            if not success: raise ValueError(reason)
