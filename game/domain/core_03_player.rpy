# Ядро домена: энергия, ранги, настроение, возбуждение, удаленная игрушка, навыки.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import random

    def change_energy(amount, state=None, reason=None):
        state = _state(state); old = state.player.energy
        state.player.energy = max(0, min(state.player.max_energy, old + int(amount)))
        dispatch_game_event("energy_changed", state, False, old=old, value=state.player.energy, reason=reason)
        return state.player.energy

    def _add_rank_progress(value, amount, thresholds, maximum, event_type, state, milestone=None):
        if milestone and milestone in value.milestones: return False
        if milestone: value.milestones.add(milestone)
        value.progress += max(0, int(amount)); changed = False
        while value.rank < maximum and value.progress >= thresholds[value.rank]:
            value.rank += 1; changed = True; dispatch_game_event(event_type, state, True, rank=value.rank)
        return changed

    def add_openness_progress(amount, milestone=None, state=None): return _add_rank_progress(_state(state).player.openness, amount, (3, 8, 15), 3, "openness_rank_changed", _state(state), milestone)
    def add_fitness_progress(amount, state=None): return _add_rank_progress(_state(state).player.fitness, amount, (3, 7, 12, 18), 4, "fitness_rank_changed", _state(state))
    def add_intellect_progress(amount, state=None): return _add_rank_progress(_state(state).player.intellect, amount, (3, 7, 12, 18), 4, "intellect_rank_changed", _state(state))
    def set_mood(value, state=None):
        state = _state(state); mapping = {"low": -1, "normal": 0, "good": 1}; state.player.mood = max(-1, min(1, mapping.get(value, value))); dispatch_game_event("mood_changed", state, False, value=state.player.mood)
    def change_arousal(amount, state=None):
        state = _state(state); old = state.player.arousal
        state.player.arousal = max(0, min(10, old + int(amount)))
        if state.player.arousal != old: dispatch_game_event("arousal_changed", state, False, old=old, value=state.player.arousal)
        return state.player.arousal

    def arousal_label(value):
        value = max(0, min(10, int(value)))
        if value == 0: return "Спокойна"
        if value <= 3: return "Слегка возбуждена"
        if value <= 6: return "Возбуждена"
        if value <= 9: return "Сильно возбуждена"
        return "Перевозбуждена"

    def remote_toy_runtime(state=None):
        state = _state(state)
        return state.inventory.body_runtime.setdefault("remote_toy", {"active": False, "controller": "nastya", "active_minutes": 0, "max_minutes": 0})

    def remote_toy_is_active(state=None):
        state = _state(state)
        return body_item_active("remote_toy", state) and bool(remote_toy_runtime(state).get("active"))

    def set_remote_toy_controller(controller, state=None):
        state = _state(state)
        if controller != "nastya" and not (controller in NPCS or (isinstance(controller, str) and controller.startswith("quest:"))):
            return False, "Неизвестный контроллер"
        remote_toy_runtime(state)["controller"] = controller
        dispatch_game_event("remote_toy_controller_changed", state, True, controller=controller)
        return True, None

    def set_remote_toy_active(active, state=None, scripted=False):
        state = _state(state); runtime = remote_toy_runtime(state)
        if not body_item_active("remote_toy", state): return False, "Игрушка не установлена"
        if not scripted and runtime.get("controller", "nastya") != "nastya": return False, "Управление игрушкой принадлежит не Насте"
        runtime["active"] = bool(active)
        if not active: runtime["active_minutes"] = 0; runtime["max_minutes"] = 0
        dispatch_game_event("remote_toy_activity_changed", state, True, active=bool(active), controller=runtime.get("controller"))
        return True, None

    def _installed_passive_body_items(state):
        result = []
        for item_id in ("remote_toy", "anal_plug", "tail_plug"):
            if body_item_active(item_id, state) and not (item_id == "remote_toy" and remote_toy_is_active(state)): result.append(item_id)
        return result

    def _trigger_remote_auto_orgasm(state):
        runtime = remote_toy_runtime(state); controller = runtime.get("controller", "nastya")
        context = {"source": "remote_toy", "location_id": state.location_id, "present_npcs": tuple(get_present_npcs(state=state)), "controller": controller, "quest_ids": tuple(sorted(state.quests.keys()))}
        state.player.arousal = 0; runtime["max_minutes"] = 0; runtime["active_minutes"] = 0
        if controller == "nastya": runtime["active"] = False
        dispatch_game_event("auto_orgasm", state, True, **context)

    def _process_arousal_time(minutes, state, reason=None, compensated=False, passive_checks=True):
        for unused in range(max(0, int(minutes))):
            if remote_toy_is_active(state):
                runtime = remote_toy_runtime(state); was_at_maximum = state.player.arousal >= 10; runtime["active_minutes"] += 1
                if runtime["active_minutes"] >= 60:
                    runtime["active_minutes"] -= 60; change_arousal(2, state)
                if state.player.arousal >= 10 and was_at_maximum:
                    runtime["max_minutes"] += 1
                    if runtime["max_minutes"] >= 30: _trigger_remote_auto_orgasm(state)
                elif state.player.arousal < 10: runtime["max_minutes"] = 0
            elif compensated:
                state.arousal_decay_minutes = 0
            elif state.player.arousal <= 0:
                state.arousal_decay_minutes = 0
            else:
                state.arousal_decay_minutes += 1
                if state.arousal_decay_minutes >= 60:
                    state.arousal_decay_minutes -= 60; change_arousal(-1, state)
            if passive_checks and _installed_passive_body_items(state):
                state.passive_body_minutes += 1
                if state.passive_body_minutes >= 180:
                    state.passive_body_minutes -= 180
                    passive = _installed_passive_body_items(state)
                    chance = 0.5 if "remote_toy" in passive and any(item in passive for item in ("anal_plug", "tail_plug")) else 0.3
                    if renpy.random.random() < chance: change_arousal(1, state)
            else:
                state.passive_body_minutes = 0
    def add_skill_progress(skill_id, amount, state=None):
        state = _state(state); skill = state.player.skills.setdefault(skill_id, SkillState()); skill.progress += max(0, int(amount)); thresholds = (3, 8)
        while skill.rank < 3 and skill.progress >= thresholds[skill.rank - 1]: skill.rank += 1; dispatch_game_event("skill_rank_changed", state, True, skill_id=skill_id, rank=skill.rank)
        return skill.rank
