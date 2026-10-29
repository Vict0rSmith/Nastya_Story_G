# Ядро домена: отношения, сюжетные флаги, квесты, сюжетные события, сообщения.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import random

    def get_relationship_state(npc_id, state=None): return _state(state).relationships[npc_id]
    def get_social_state(npc_id, state=None): return get_relationship_state(npc_id, state).social
    def set_social_state(npc_id, social, reason=None, state=None):
        if social not in SOCIAL_STATES: raise ValueError("Unknown social state")
        state = _state(state); relation = state.relationships[npc_id]
        if relation.social == social: return False
        relation.social = social; dispatch_game_event("relationship_social_changed", state, True, npc_id=npc_id, social=social, reason=reason); return True
    def get_intimacy_state(npc_id, state=None): return get_relationship_state(npc_id, state).intimacy
    def set_intimacy_state(npc_id, intimacy, reason=None, state=None):
        if intimacy not in INTIMACY_STATES: raise ValueError("Unknown intimacy state")
        state = _state(state); relation = state.relationships[npc_id]
        if intimacy == "sexual" and not sexual_interaction_allowed(npc_id): return False
        if intimacy == "romantic" and not NPCS.get(npc_id, {}).get("romantic_route_allowed", False): return False
        if relation.intimacy == intimacy: return False
        relation.intimacy = intimacy; dispatch_game_event("relationship_intimacy_changed", state, True, npc_id=npc_id, intimacy=intimacy, reason=reason); return True
    def sexual_interaction_allowed(npc_id):
        return bool(NPCS.get(npc_id, {}).get("sexual_route_allowed", False))

    def set_story_flag(flag, value=True, state=None):
        state = _state(state)
        if value: state.story.flags.add(flag)
        else: state.story.flags.discard(flag)
        dispatch_game_event("story_flag_changed", state, False, flag=flag, value=bool(value))
    def start_quest(quest_id, state=None):
        state = _state(state)
        if quest_id in state.quests: return False
        state.quests[quest_id] = QuestState(QUESTS[quest_id]); dispatch_game_event("quest_started", state, False, quest_id=quest_id); return True
    def _update_quests_from_event(state, event):
        for quest_id, quest_state in list(state.quests.items()):
            if quest_state.status not in ("active", "completed"): continue
            definition = QUESTS[quest_id]
            for objective in definition["objectives"]:
                progress = quest_state.objectives[objective["id"]]
                if progress.completed or objective["event"] != event.type: continue
                if not conditions_match(objective.get("conditions", {}), state): continue
                matches = True
                for key, expected in objective.get("filters", {}).items():
                    actual = event.data.get(key)
                    if isinstance(expected, (tuple, list, set)):
                        if actual not in expected: matches = False
                    elif actual != expected: matches = False
                if not matches: continue
                progress.progress = min(objective.get("target", 1), progress.progress + 1); progress.completed = progress.progress >= objective.get("target", 1)
            required_ids = [o["id"] for o in definition["objectives"] if o.get("required", True)]
            if quest_state.status == "active" and all(quest_state.objectives[objective_id].completed for objective_id in required_ids):
                quest_state.status = "completed"; state.story.flags.add("quest_%s_completed" % quest_id); completion = GameEvent("quest_completed", {"quest_id": quest_id}, (state.clock.date.isoformat(), state.clock.display_time)); state.story.event_history.append(completion); _dispatch_story_event(state, completion)
    def _dispatch_story_event(state, trigger_event):
        candidates = []
        for definition in STORY_EVENTS.values():
            if definition["trigger"] != trigger_event.type: continue
            if not conditions_match(definition.get("conditions", {}), state): continue
            if item_effects_reason(definition.get("effects", ()), state): continue
            event_id = definition["id"]
            if definition.get("once") and event_id in state.story.flags: continue
            count = state.story.counters.get("event:%s" % event_id, 0)
            if definition.get("repeat_limit") is not None and count >= definition["repeat_limit"]: continue
            last_date = state.story.event_last_date.get(event_id)
            if last_date and definition.get("cooldown_days", 0) > 0 and (state.clock.date - last_date).days < definition["cooldown_days"]: continue
            required = set(definition.get("required_flags", [])); forbidden = set(definition.get("forbidden_flags", []))
            if not required.issubset(state.story.flags) or forbidden.intersection(state.story.flags): continue
            candidates.append(definition)
        if not candidates: return None
        chosen = sorted(candidates, key=lambda value: value.get("priority", 0), reverse=True)[0]
        if random.random() > chosen.get("chance", 1.0): return None
        event_id = chosen["id"]
        if chosen.get("once"): state.story.flags.add(event_id)
        counter_key = "event:%s" % event_id; state.story.counters[counter_key] = state.story.counters.get(counter_key, 0) + 1; state.story.event_last_date[event_id] = state.clock.date
        for effect in chosen.get("effects", ()): _apply_effect(state, effect)
        if chosen.get("scene"): state.story.pending_scene = chosen["scene"]
        return chosen
    def send_message(contact_id, text, state=None):
        state = _state(state)
        state.messages.append({"from": "nastya", "to": contact_id, "text": text, "read": True, "timestamp": (state.clock.date.isoformat(), state.clock.display_time)})
        dispatch_game_event("message_sent", state, True, contact_id=contact_id)
    def objective_complete(quest_id, objective_id, state=None): return _state(state).quests[quest_id].objectives[objective_id].completed
