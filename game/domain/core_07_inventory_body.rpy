# Ядро домена: инвентарь, покупки в магазинах, уход за телом.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import datetime

    def inventory_add(item_id, quantity=1, state=None):
        state = _state(state); definition = ITEMS[item_id]; quantity = int(quantity)
        if quantity <= 0: raise ValueError("Quantity must be positive")
        if item_id in state.inventory.external_items: raise ValueError("Item belongs to another owner")
        if definition["storage"] == "wardrobe":
            state.wardrobe.owned.add(item_id)
            dispatch_game_event("inventory_item_added", state, True, item_id=item_id, quantity=1)
            return
        if not definition.get("stackable", True): quantity = 1
        state.inventory.quantities[item_id] = state.inventory.quantities.get(item_id, 0) + quantity
        if not definition.get("stackable", True): state.inventory.quantities[item_id] = 1
        dispatch_game_event("inventory_item_added", state, True, item_id=item_id, quantity=quantity)
    def inventory_has(item_id, quantity=1, state=None): return _state(state).inventory.quantities.get(item_id, 0) >= quantity
    def inventory_remove(item_id, quantity=1, state=None):
        state = _state(state)
        if quantity <= 0: raise ValueError("Quantity must be positive")
        if body_item_active(item_id, state): return False
        if not inventory_has(item_id, quantity, state): return False
        left = state.inventory.quantities[item_id] - quantity
        if left: state.inventory.quantities[item_id] = left
        else:
            del state.inventory.quantities[item_id]
            state.inventory.item_states.pop(item_id, None)
        dispatch_game_event("inventory_item_removed", state, True, item_id=item_id, quantity=quantity); return True
    def inventory_use(item_id, state=None):
        state = _state(state); definition = ITEMS[item_id]
        if "persistent_body_item" in definition["use_modes"]:
            success, reason = set_body_item(item_id, not body_item_active(item_id, state), state)
            if success: advance_time(5, "body_item_change", state)
            return success
        if item_use_reason(item_id, state): return False
        if definition["use_modes"]: return False
        advance_time(5, "inventory_item_use", state)
        for effect in definition.get("effects", []): _apply_effect(state, effect)
        if "adult_media" in definition.get("tags", ()):
            counter_key = "media_reads_remaining:" + item_id
            remaining = int(state.story.counters.get(counter_key, 5)) - 1
            if remaining <= 0:
                inventory_remove(item_id, 1, state)
            else:
                state.story.counters[counter_key] = remaining
        elif definition.get("consumable", False): inventory_remove(item_id, 1, state)
        dispatch_game_event("inventory_item_used", state, True, item_id=item_id); return True
    def fulfill_shop_purchase(location_id, item_id, state=None):
        state = _state(state)
        offer = SHOP_CATALOGS.get(location_id, {}).get(item_id)
        if offer is None: return False, "Товар отсутствует в ассортименте"
        if offer.get("price") is None: return False, "Цена товара еще не утверждена"
        price = int(offer["price"])
        if price < 0: return False, "Цена товара указана некорректно"
        reason = item_purchase_reason(item_id, state)
        if reason: return False, reason
        if state.wallet.balance < price: return False, "Недостаточно денег"
        if not spend_money(price, "Покупка: " + ITEMS[item_id]["name"], state): return False, "Недостаточно денег"
        if offer.get("consume_immediately"):
            duration = 30 if any(effect[0] == "nutrition_full" for effect in ITEMS[item_id].get("effects", ())) else 15
            advance_time(duration, "cafe_order", state)
            for effect in ITEMS[item_id].get("effects", []): _apply_effect(state, effect)
            dispatch_game_event("shop_item_consumed", state, True, item_id=item_id, location_id=location_id)
        else:
            inventory_add(item_id, offer["purchase_quantity"], state)
            advance_time(15, "shop_purchase", state)
        return True, None

    def npc_is_in_apartment(npc_id, state=None):
        state = _state(state); apartment_locations = {"loc_apartment_5_hallway", "loc_apartment_5_room", "loc_apartment_5_kitchen", "loc_apartment_5_bathroom", "loc_apartment_5_balcony"}
        return any(npc_id in get_present_npcs(location_id=location_id, state=state) for location_id in apartment_locations)
    def _game_datetime(state): return datetime.datetime.combine(state.clock.date, datetime.time(state.clock.hour, state.clock.minute))
    def pubic_grooming_is_fresh(state=None):
        state = _state(state); grooming = state.grooming
        return grooming.pubic_style != "natural" and grooming.pubic_grooming_due_at is not None and _game_datetime(state) < grooming.pubic_grooming_due_at
    def pubic_grooming_needs_maintenance(state=None):
        state = _state(state); grooming = state.grooming
        return grooming.pubic_style != "natural" and grooming.pubic_grooming_due_at is not None and _game_datetime(state) >= grooming.pubic_grooming_due_at
    def set_pubic_grooming_style(style, state=None):
        if style not in ("natural", "smooth", "styled"): raise ValueError("Unsupported pubic grooming style category: %s" % style)
        state = _state(state); state.grooming.pubic_style = style
        if style == "natural": state.grooming.last_pubic_grooming_at = None; state.grooming.pubic_grooming_due_at = None
    def maintain_pubic_grooming(style=None, state=None):
        state = _state(state); grooming = state.grooming; selected_style = style or grooming.pubic_style
        if selected_style == "natural": selected_style = "smooth"
        if selected_style not in ("smooth", "styled"): raise ValueError("Unsupported maintained grooming style: %s" % selected_style)
        now = _game_datetime(state); grooming.pubic_style = selected_style; grooming.last_pubic_grooming_at = now; grooming.pubic_grooming_due_at = now + datetime.timedelta(days=7); return selected_style
