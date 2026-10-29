# Ядро домена: течение времени и дедлайн первого дня.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import datetime

    def advance_time(minutes, reason=None, state=None, arousal_compensated=False, passive_checks=True):
        state = _state(state); minutes = int(minutes)
        if minutes < 0: raise ValueError("Time cannot move backwards")
        old_date, old_period = state.clock.date, state.clock.period; old_present = set(get_present_npcs(state=state))
        nutrition_minutes = float(minutes) / 5.0 if reason == "action_sleep" else float(minutes)
        state.nutrition_elapsed_minutes = max(0.0, getattr(state, "nutrition_elapsed_minutes", 0.0) + nutrition_minutes)
        _process_arousal_time(minutes, state, reason, arousal_compensated, passive_checks)
        state.clock.advance(minutes)
        if reason == "action_sleep":
            state.awake_energy_minutes = 0
        else:
            spent, state.awake_energy_minutes = divmod(getattr(state, "awake_energy_minutes", 0) + minutes, 180)
            if spent: change_energy(-spent, state, "awake_time")
        process_bank_time(state)
        dispatch_game_event("time_advanced", state, False, minutes=int(minutes), reason=reason)
        if state.clock.date != old_date: dispatch_game_event("day_started", state, True, date=state.clock.date.isoformat())
        if state.clock.period != old_period: dispatch_game_event("time_period_changed", state, True, period=state.clock.period)
        new_present = set(get_present_npcs(state=state))
        for npc_id in sorted(new_present - old_present): dispatch_game_event("npc_arrived", state, True, npc_id=npc_id, location_id=state.location_id)
        for npc_id in sorted(old_present - new_present): dispatch_game_event("npc_left", state, True, npc_id=npc_id, location_id=state.location_id)
        queue_first_day_deadline_scene(state)

    def is_first_day(state=None):
        return _state(state).clock.date == datetime.date(2026, 8, 29)

    def first_day_required_objectives_complete(state=None):
        state = _state(state)
        quest = state.quests.get("quest_2026_08_29_first_normal_day")
        return bool(quest and all(quest.objectives[key].completed for key in ("remind_masha_school_documents", "submit_university_documents")))

    def first_day_admissions_open_for_action(state=None):
        state = _state(state)
        return is_first_day(state) and state.location_id == "loc_medical_institute_admissions" and 13 * 60 <= state.clock.total_minutes and state.clock.total_minutes + 30 <= 18 * 60

    def first_day_minutes_to_admissions(state=None, start_location=None):
        state = _state(state); start = start_location or state.location_id; target = "loc_medical_institute_admissions"
        frontier = [(0, start)]; best = {start: 0}
        while frontier:
            frontier.sort(reverse=True); cost, location_id = frontier.pop()
            if cost != best.get(location_id): continue
            if location_id == target: return cost
            edges = list(LOCATIONS.get(location_id, {}).get("transitions", {}).items())
            edges += [(destination, route["duration_minutes"]) for destination, route in TRANSPORT_ROUTES.get(location_id, {}).items()]
            for destination, minutes in edges:
                if minutes is None: continue
                new_cost = cost + int(minutes)
                if new_cost < best.get(destination, 10 ** 9): best[destination] = new_cost; frontier.append((new_cost, destination))
        return None

    def first_day_deadline_blocks(extra_minutes=0, state=None, start_location=None):
        state = _state(state)
        if not is_first_day(state) or "university_documents_submitted" in state.story.flags: return False
        travel = first_day_minutes_to_admissions(state, start_location)
        if travel is None: return True
        return state.clock.total_minutes + int(extra_minutes) + travel + 30 > 18 * 60

    def queue_first_day_deadline_scene(state=None):
        state = _state(state)
        if not is_first_day(state) or "university_documents_submitted" in state.story.flags or "first_day_forced_departure_started" in state.story.flags: return False
        travel = first_day_minutes_to_admissions(state)
        if travel is None: return False
        margin = 18 * 60 - (state.clock.total_minutes + travel + 30)
        if margin <= 0:
            state.story.flags.add("first_day_forced_departure_started")
            state.story.pending_scene = "scene_2026_08_29_forced_university_departure"
            return True
        if margin <= 60 and "first_day_university_deadline_warned" not in state.story.flags and state.story.pending_scene is None:
            state.story.flags.add("first_day_university_deadline_warned")
            state.story.pending_scene = "scene_2026_08_29_university_warning"
            return True
        return False

    def request_first_day_deadline_departure(state=None):
        state = _state(state)
        if not is_first_day(state) or "university_documents_submitted" in state.story.flags: return False
        state.story.flags.add("first_day_forced_departure_started")
        state.story.pending_scene = "scene_2026_08_29_forced_university_departure"
        return True

    def force_first_day_university_departure(state=None):
        state = _state(state); travel = first_day_minutes_to_admissions(state)
        if travel is None: return False
        state.location_id = "loc_medical_institute_admissions"
        advance_time(travel, "forced_university_departure", state)
        dispatch_game_event("location_entered", state, True, location_id=state.location_id)
        return True
