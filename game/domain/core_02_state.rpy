# Ядро домена: создание нового состояния, миграция схемы, диспетчер событий.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    def create_new_game_state():
        state = GameState()
        state.relationships["masha"] = RelationshipState("friend", "none")
        state.relationships["nika"] = RelationshipState("neutral", "none")
        state.relationships["anna"] = RelationshipState("unmet", "none")
        state.relationships["aslan"] = RelationshipState("unmet", "none")
        state.inventory.quantities.update({"sandwich": 1, "water": 2, "prepared_home_meal": 1})
        state.wardrobe.owned.update((
            "white_cotton_bra_1", "white_cotton_panties_1", "white_cotton_bra_2", "white_cotton_panties_2",
            "casual_tshirt", "casual_skirt", "sneakers",
        ))
        state.wardrobe.equipped.update({"panties": "white_cotton_panties_1", "top": "casual_tshirt"})
        state.messages.append({"from": "nika", "text": "Доброе утро! Напиши, когда освоитесь.", "read": False})
        state.story.flags.update(("phone_contact:masha", "phone_contact:nika"))
        return state

    def ensure_current_schema(state):
        if state.schema_version == 2:
            legacy_clothing = {"simple_bra", "simple_panties", "blue_dress", "jeans", "coral_top"}
            canonical_starting_clothing = {"white_cotton_bra_1", "white_cotton_panties_1", "white_cotton_bra_2", "white_cotton_panties_2", "casual_tshirt", "casual_skirt", "sneakers"}
            state.wardrobe.owned.difference_update(legacy_clothing)
            state.wardrobe.owned.update(canonical_starting_clothing)
            for slot, item_id in state.wardrobe.equipped.items():
                if item_id in legacy_clothing: state.wardrobe.equipped[slot] = None
            state.wardrobe.equipped.update({"bra": None, "panties": "white_cotton_panties_1", "top": "casual_tshirt", "bottom": None, "dress": None})
            state.schema_version = 3
        if state.schema_version == 3:
            state.grooming = GroomingState()
            if not hasattr(state.story, "pending_action"): state.story.pending_action = None
            state.schema_version = 4
        if state.schema_version == 4:
            legacy_relationships = getattr(state, "relationships", {})
            migrated = {}
            for npc_id, legacy in legacy_relationships.items():
                stage = getattr(legacy, "stage", "unmet")
                social = {"negative": "enemy", "neutral": "neutral", "friendly": "friend", "attraction": "friend", "partner": "friend"}.get(stage, "unmet")
                intimacy = "romantic" if stage == "partner" else ("sexual" if stage == "attraction" else "none")
                migrated[npc_id] = RelationshipState(social, intimacy)
            defaults = create_new_game_state().relationships
            for npc_id, relation in defaults.items():
                if npc_id not in migrated: migrated[npc_id] = relation
            state.relationships = migrated
            state.schema_version = 5
        if state.schema_version == 5:
            state.inventory.item_states = {}
            state.inventory.external_items = {}
            for location_id, item_ids in getattr(state.wardrobe, "work_storage", {}).items():
                for item_id in item_ids:
                    state.inventory.external_items[item_id] = {"owner": location_id, "location": location_id}
            if hasattr(state.wardrobe, "work_storage"): del state.wardrobe.work_storage
            state.wardrobe.access_context = None
            state.story.pending_action_item = None
            state.schema_version = 6
        if state.schema_version == 6:
            state.phone_threads = set()
            state.phone_cooldowns = {}
            state.story.flags.update(("phone_contact:masha", "phone_contact:nika"))
            state.schema_version = 7
        if state.schema_version == 7:
            state.nutrition_elapsed_minutes = 0.0
            state.energy_drink_ready_at = None
            state.schema_version = 8
        if state.schema_version == 8:
            legacy_arousal = max(0, min(3, int(getattr(state.player, "arousal", 0))))
            state.player.arousal = (0, 2, 5, 8)[legacy_arousal]
            state.arousal_decay_minutes = 0
            state.passive_body_minutes = 0
            state.arousal_source_ready_at = {}
            state.inventory.body_runtime = {}
            state.schema_version = 9
        if state.schema_version == 9:
            legacy_history = list(getattr(state.wallet, "history", []))
            state.wallet.transaction_sequence = 0
            state.wallet.loans = []
            state.wallet.transfer_recipients = set()
            state.wallet.history = []
            for row in legacy_history:
                if isinstance(row, MoneyTransaction):
                    state.wallet.history.append(row)
                    state.wallet.transaction_sequence = max(state.wallet.transaction_sequence, row.sequence)
                    continue
                try:
                    date, display_time, amount, reason = row
                except (TypeError, ValueError):
                    continue
                state.wallet.transaction_sequence += 1
                state.wallet.history.append(MoneyTransaction(
                    "money_%06d" % state.wallet.transaction_sequence,
                    state.wallet.transaction_sequence,
                    str(date), str(display_time), int(amount),
                    "income" if int(amount) > 0 else "expense",
                    "legacy", str(reason), source_event_id="legacy:%s" % state.wallet.transaction_sequence,
                ))
            state.schema_version = 10
        if state.schema_version == 10:
            state.alarm = AlarmState()
            state.schema_version = 11
        if state.schema_version == 11:
            state.awake_energy_minutes = 0
            state.schema_version = 12
        if state.schema_version != SCHEMA_VERSION:
            raise RuntimeError("Unsupported Nastya Story save schema: %s" % state.schema_version)
        return state

    def _state(state=None): return state if state is not None else store.game_state

    def dispatch_game_event(event_type, state=None, checkpoint=True, **data):
        state = _state(state)
        event = GameEvent(event_type, data, (state.clock.date.isoformat(), state.clock.display_time))
        state.story.event_history.append(event)
        _update_quests_from_event(state, event)
        if checkpoint: _dispatch_story_event(state, event)
        return event
