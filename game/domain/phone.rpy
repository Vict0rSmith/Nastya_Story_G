init -20 python:
    import calendar

    PHONE_MONTH_NAMES = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")

    def phone_message_contact(message):
        return message.get("to") if message.get("from") == "nastya" else message.get("from")

    def phone_contacts(state=None):
        state = _state(state)
        existing = {phone_message_contact(m) for m in state.messages}
        return [npc_id for npc_id in NPCS if "phone_contact:" + npc_id in state.story.flags or npc_id in existing]

    def phone_known_fields(npc_id, field, state=None):
        state = _state(state)
        if npc_id not in phone_contacts(state): return []
        return [row["text"] for row in NPCS[npc_id].get(field, []) if row.get("known_flag") in state.story.flags]

    def phone_open(app="home", selected=None):
        store.ui_phone_choices_open = False
        store.ui_phone_app = app
        store.ui_phone_selected = selected
        store.ui_phone_tooltip = None
        if app == "calendar":
            store.ui_phone_month = (game_state.clock.date.year, game_state.clock.date.month)
        if app == "chat" and selected in phone_contacts():
            game_state.phone_threads.add(selected)
            for message in game_state.messages:
                if phone_message_contact(message) == selected: message["read"] = True

    def phone_back():
        parent = {"contact": "contacts", "quest": "quests", "chat": "messages"}
        phone_open(parent.get(store.ui_phone_app, "home"))

    def phone_chats(state=None):
        state = _state(state)
        ids = set(state.phone_threads) | {phone_message_contact(m) for m in state.messages}
        return [c for c in phone_contacts(state) if c in ids]

    def phone_history(contact_id, state=None):
        # Append order preserves undated legacy messages and equal-time sends.
        return [m for m in _state(state).messages if phone_message_contact(m) == contact_id]

    def phone_quests(status, state=None):
        state = _state(state)
        return [(qid, q) for qid, q in state.quests.items() if q.status == status and qid in QUESTS and not QUESTS[qid].get("hidden")]

    def phone_calendar_shift(delta):
        year, month = store.ui_phone_month
        index = year * 12 + month - 1 + delta
        year, month = divmod(index, 12)
        if 1 <= year <= 9999: store.ui_phone_month = (year, month + 1)
        store.ui_phone_tooltip = None

    def phone_calendar_events(year, month, state=None):
        state = _state(state)
        rows = list(CALENDAR_EVENTS)
        for qid, q in state.quests.items():
            if q.status != "locked" and qid in QUESTS and not QUESTS[qid].get("hidden"):
                rows.extend(QUESTS[qid].get("calendar_events", []))
        for npc_id in phone_contacts(state):
            birthday = NPCS[npc_id].get("birthday")
            if isinstance(birthday, dict):
                rows.append(dict(birthday, id="birthday:" + npc_id, title="День рождения: " + NPCS[npc_id]["name"], known_flag="birthday:" + npc_id))
        result, seen = {}, set()
        for row in rows:
            if not row.get("public") and row.get("known_flag") not in state.story.flags: continue
            try:
                date = datetime.date.fromisoformat(row["date"]) if row.get("date") else datetime.date(year, row["month"], row["day"])
            except (ValueError, TypeError, KeyError): continue
            if (date.year, date.month) != (year, month) or not row.get("title"): continue
            key = row.get("id", (date.isoformat(), row["title"]))
            if key in seen: continue
            seen.add(key)
            result.setdefault(date.day, []).append(row["title"])
        return result

    def phone_npc_location(npc_id, state=None):
        state = _state(state)
        override = state.schedule_overrides.get(npc_id)
        if override and (override.get("until") is None or state.clock.date <= override["until"]):
            return override.get("location")
        for entry in SCHEDULES.get(npc_id, []):
            if entry.get("weekdays") and state.clock.weekday not in entry["weekdays"]: continue
            if entry["start"] <= state.clock.total_minutes < entry["end"]: return entry["location"]
        return None

    def phone_now(state=None):
        clock = _state(state).clock
        return clock.date.toordinal() * 1440 + clock.total_minutes

    def phone_context_matches(row, npc_id, state):
        return (not row.get("contact") or row["contact"] == npc_id) and (not row.get("locations") or phone_npc_location(npc_id, state) in row["locations"]) and (not row.get("periods") or state.clock.period in row["periods"]) and ("available" not in row or bool(phone_npc_location(npc_id, state)) == row["available"]) and conditions_match(row.get("conditions", {}), state)

    def phone_option_status(option_id, npc_id, state=None):
        state = _state(state)
        option = PHONE_MESSAGE_OPTIONS.get(option_id)
        if npc_id not in phone_contacts(state) or not option: return False, "Контакт недоступен", []
        if not phone_context_matches(option, npc_id, state): return False, "Сейчас недоступно", []
        if option.get("once") and "phone_sent:" + npc_id + ":" + option_id in state.story.flags: return False, "Уже отправлено", []
        replies = [r for r in option.get("responses", []) if phone_context_matches(r, npc_id, state)]
        if option.get("kind") == "casual":
            remaining = state.phone_cooldowns.get(npc_id, 0) - phone_now(state)
            if remaining > 0: return False, "Можно написать через %s мин." % remaining, replies
            if not isinstance(PHONE_CASUAL_COOLDOWN_MINUTES, int) or isinstance(PHONE_CASUAL_COOLDOWN_MINUTES, bool) or PHONE_CASUAL_COOLDOWN_MINUTES <= 0: return False, "Бытовая переписка пока недоступна", replies
            if not replies: return False, "Сейчас нет доступного ответа", replies
        return True, "", replies

    def phone_send_option(option_id, npc_id, state=None):
        state = _state(state)
        allowed, reason, replies = phone_option_status(option_id, npc_id, state)
        if not allowed: return False
        option = PHONE_MESSAGE_OPTIONS[option_id]
        state.phone_threads.add(npc_id)
        # Record locks before event callbacks to prevent duplicate/reentrant sends.
        if option.get("once"): state.story.flags.add("phone_sent:" + npc_id + ":" + option_id)
        if option.get("kind") == "casual": state.phone_cooldowns[npc_id] = phone_now(state) + PHONE_CASUAL_COOLDOWN_MINUTES
        state.story.flags.update(option.get("set_flags", []))
        send_message(npc_id, option["text"], state)
        if option.get("social"): set_social_state(npc_id, option["social"], reason=option_id, state=state)
        if replies:
            reply = renpy.random.choice(replies)
            state.messages.append({"from": npc_id, "text": reply["text"], "read": state is game_state and store.ui_phone_app == "chat" and store.ui_phone_selected == npc_id, "timestamp": (state.clock.date.isoformat(), state.clock.display_time)})
        return True

    def phone_choose_message(option_id, npc_id):
        if phone_send_option(option_id, npc_id):
            store.ui_phone_choices_open = False

    def phone_call_status(npc_id):
        return False, "Звонки пока недоступны"
