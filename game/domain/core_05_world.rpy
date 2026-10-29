# Ядро домена: присутствие NPC, расписания, доступ к локациям и перемещение.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import datetime

    def get_present_npcs(location_id=None, clock=None, state=None):
        state = _state(state); location_id = location_id or state.location_id; clock = clock or state.clock; result = []
        for npc_id, entries in SCHEDULES.items():
            override = state.schedule_overrides.get(npc_id)
            if override:
                if override.get("until") is None or state.clock.date <= override["until"]:
                    if override.get("location") == location_id: result.append(npc_id)
                    continue
                else: del state.schedule_overrides[npc_id]
            for entry in entries:
                if entry.get("date") and entry["date"] != clock.date.isoformat(): continue
                if entry.get("weekdays") and clock.weekday not in entry["weekdays"]: continue
                minute = clock.total_minutes
                if entry["start"] <= minute < entry["end"] and entry["location"] == location_id: result.append(npc_id); break
        return result

    def set_schedule_override(npc_id, location_id, until_date=None, reason=None, state=None):
        state = _state(state)
        if npc_id not in NPCS: raise ValueError("Unknown NPC")
        if location_id is not None and location_id not in LOCATIONS: raise ValueError("Unknown location")
        state.schedule_overrides[npc_id] = {"location": location_id, "until": until_date, "reason": reason}; dispatch_game_event("npc_schedule_overridden", state, True, npc_id=npc_id, location_id=location_id, reason=reason)
    def clear_schedule_override(npc_id, state=None): _state(state).schedule_overrides.pop(npc_id, None)
    def location_access_reason(location_id, state=None, arrival_minutes=0):
        state = _state(state)
        definition = LOCATIONS.get(location_id)
        if not definition or definition.get("kind") != "location": return "Это не место пребывания"
        if location_id == "loc_building_roof": return None
        access = definition.get("access_state", "tbd")
        condition = definition.get("access_condition", "TBD")
        if access == "open": return None
        if access == "conditional" and condition.startswith("requires_item:"):
            return None if inventory_has(condition.split(":", 1)[1], 1, state) else "Нужен ключ"
        if access == "conditional" and location_id == "loc_medical_institute_admissions":
            arrival = datetime.datetime.combine(state.clock.date, datetime.time(state.clock.hour, state.clock.minute)) + datetime.timedelta(minutes=arrival_minutes)
            if arrival.date() == datetime.date(2026, 8, 29) and 13 <= arrival.hour < 18: return None
            return "Прием 29 августа с 13:00 до 18:00"
        if access == "conditional" and location_id == "loc_apartment_6_hallway":
            arrival = datetime.datetime.combine(state.clock.date, datetime.time(state.clock.hour, state.clock.minute)) + datetime.timedelta(minutes=arrival_minutes)
            if arrival.date() == datetime.date(2026, 8, 29) and 19 <= arrival.hour < 22 and get_social_state("nika", state) == "neutral": return None
            return "Ника дома 29 августа с 19:00 до 22:00"
        return "Закрыто" if access == "locked" else "Доступ пока не определен"

    def transition_info(location_id, state=None, mode="walk"):
        state = _state(state)
        if mode == "walk":
            entries = LOCATIONS.get(state.location_id, {}).get("transitions", {})
            if location_id not in entries: return None, "Нет перехода"
            minutes = entries[location_id]
        elif mode == "bus":
            route = TRANSPORT_ROUTES.get(state.location_id, {}).get(location_id)
            if not route: return None, "Нет маршрута"
            minutes = route["duration_minutes"]
        else: return None, "Неизвестный транспорт"
        reason = location_access_reason(location_id, state, minutes or 0)
        if not reason and first_day_deadline_blocks(minutes or 0, state, location_id):
            reason = "Сначала нужно успеть подать документы в университет"
        return minutes, reason or ("Время пути не определено" if minutes is None else None)

    def move_to(location_id, state=None, mode="walk"):
        state = _state(state)
        minutes, reason = transition_info(location_id, state, mode)
        if reason: return False, reason
        if state.wardrobe.active_workplace and location_id not in wardrobe_work_locations(state):
            work_wardrobe_exit_and_restore(state)
        state.wardrobe.access_context = None
        state.location_id = location_id
        advance_time(minutes, "movement", state)
        dispatch_game_event("location_entered", state, True, location_id=location_id)
        return True, None
