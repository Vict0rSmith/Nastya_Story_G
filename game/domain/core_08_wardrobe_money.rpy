# Ядро домена: гардероб и деньги.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import copy

    def wardrobe_owns(item_id, state=None): return item_id in _state(state).wardrobe.owned
    def wardrobe_can_equip(item_id, context=None, state=None):
        state = _state(state); item = CLOTHES.get(item_id)
        if not wardrobe_access_allowed(state): return False, "Здесь нельзя переодеваться"
        if not item or item_id not in wardrobe_available_items(state): return False, "Вещь недоступна"
        external = state.inventory.external_items.get(item_id)
        if external and state.wardrobe.active_workplace != external["owner"]: return False, "Нужен разрешенный рабочий контекст"
        if state.player.openness.rank < item.get("required_openness_use", 0): return False, "Недостаточная раскрепощенность"
        active_context = wardrobe_context(state)
        if context is not None and context != active_context: return False, "Контекст недоступен"
        unlock = item.get("context_unlocks", {}).get(active_context)
        if active_context not in item.get("contexts", ()) and "any" not in item.get("contexts", ()):
            if not unlock or unlock not in state.story.flags: return False, "Одежда не разрешена в этом контексте"
        if not conditions_match(item.get("use_conditions", {}), state): return False, "Сюжетные условия не выполнены"
        clothing_slot = item.get("slot")
        for body_id in ITEMS:
            if body_item_active(body_id, state) and clothing_slot in ITEMS[body_id].get("incompatible_clothing_slots", ()):
                return False, "Одежда несовместима с установленным предметом"
        return True, None
    def wardrobe_equip(item_id, context=None, state=None):
        state = _state(state); allowed, reason = wardrobe_can_equip(item_id, context, state)
        if not allowed: return False, reason
        item = CLOTHES[item_id]; slot = item["slot"]
        if slot == "dress": state.wardrobe.equipped["top"] = state.wardrobe.equipped["bottom"] = None
        elif slot in ("top", "bottom"): state.wardrobe.equipped["dress"] = None
        state.wardrobe.equipped[slot] = item_id; dispatch_game_event("outfit_changed", state, True, item_id=item_id, slot=slot); return True, None
    def wardrobe_unequip(slot, state=None):
        state = _state(state)
        if slot not in OUTFIT_SLOTS or not wardrobe_access_allowed(state): return False
        access = wardrobe_access_rules(state)
        if slot in access.get("forbidden_empty_slots", ()): return False
        if state.player.openness.rank < access.get("required_openness_undress", 0): return False
        state.wardrobe.equipped[slot] = None
        dispatch_game_event("outfit_changed", state, True, slot=slot)
        return True
    def wardrobe_get_outfit_tags(state=None):
        state = _state(state); tags = set()
        for item_id in state.wardrobe.equipped.values():
            if item_id: tags.update(CLOTHES.get(item_id, {}).get("tags", []))
        if not state.wardrobe.equipped["bra"]: tags.add("no_bra")
        if not state.wardrobe.equipped["panties"]: tags.add("no_panties")
        return sorted(tags)
    def work_wardrobe_enter(workplace_id, state=None):
        state = _state(state); wardrobe = state.wardrobe
        if wardrobe.active_workplace: return False
        rules = wardrobe_access_rules(state)
        if not rules or rules.get("workplace") != workplace_id: return False
        if not conditions_match(rules.get("conditions", {}), state): return False
        wardrobe.saved_civilian_outfit = copy.deepcopy(wardrobe.equipped); wardrobe.active_workplace = workplace_id; return True
    def work_wardrobe_exit_and_restore(state=None):
        state = _state(state); wardrobe = state.wardrobe
        if wardrobe.saved_civilian_outfit is None: return False
        wardrobe.equipped = wardrobe.saved_civilian_outfit; wardrobe.saved_civilian_outfit = None; wardrobe.active_workplace = None; dispatch_game_event("work_outfit_restored", state, True); return True
    def add_money(amount, reason, state=None):
        state = _state(state); amount = int(amount)
        if amount < 0: raise ValueError("Use spend_money for expenses")
        result = post_transaction(amount, "income", reason, category_id="income", state=state)
        return result.balance
    def spend_money(amount, reason, state=None):
        state = _state(state); amount = int(amount)
        if amount < 0: raise ValueError("Amount must be positive")
        return post_transaction(-amount, "expense", reason, category_id="expense", state=state).success
