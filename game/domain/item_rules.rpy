# Contracts extending the existing inventory, wardrobe and event owners.
init -90 python:
    WARDROBE_ACCESS = {"loc_apartment_5_room": {"context": "home"}}
    # Balance is intentionally unset until approved in NUTRITION_SPEC.
    NUTRITION_THRESHOLDS = None

    def configure_nutrition_thresholds(thresholds):
        """Set approved nutrition thresholds without inventing a default balance."""
        if thresholds is None:
            store.NUTRITION_THRESHOLDS = None
            return None
        required = ("sated", "hungry", "very_hungry")
        if any(key not in thresholds for key in required):
            raise ValueError("Nutrition thresholds require sated, hungry and very_hungry")
        values = dict((key, int(thresholds[key])) for key in required)
        if values["sated"] < 0 or not (values["sated"] <= values["hungry"] < values["very_hungry"]):
            raise ValueError("Nutrition thresholds must be ordered and non-negative")
        store.NUTRITION_THRESHOLDS = values
        return values

    def item_owns(item_id, state=None):
        state = _state(state)
        return inventory_has(item_id, 1, state) or wardrobe_owns(item_id, state)

    def item_current_state(item_id, state=None):
        state = _state(state)
        if item_id in state.wardrobe.equipped.values(): return "worn"
        return state.inventory.item_states.get(item_id, "inventory")

    def body_item_active(item_id, state=None):
        return item_owns(item_id, state) and item_current_state(item_id, state) == "body"

    def conditions_match(conditions, state=None):
        state = _state(state)
        for key, value in conditions.items():
            if key == "required_flags":
                if not set(value).issubset(state.story.flags): return False
            elif key == "forbidden_flags":
                if set(value).intersection(state.story.flags): return False
            elif key == "body_items":
                if not all(body_item_active(item_id, state) == active for item_id, active in value.items()): return False
            elif key == "owns_items":
                if not all(item_owns(item_id, state) for item_id in value): return False
            elif key == "outfit_tags":
                if not set(value).issubset(wardrobe_get_outfit_tags(state)): return False
            elif key == "locations":
                if state.location_id not in value: return False
            elif key == "required_openness":
                if state.player.openness.rank < value: return False
            elif key == "minimum_arousal":
                if state.player.arousal < value: return False
            else:
                raise ValueError("Unknown condition: " + key)
        return True

    def item_purchase_reason(item_id, state=None):
        state = _state(state); item = ITEMS.get(item_id)
        if not item: return "Неизвестный предмет"
        if state.player.openness.rank < item["required_openness_purchase"]: return "Недостаточная раскрепощенность для покупки"
        if not conditions_match(item.get("purchase_conditions", {}), state): return "Покупка пока недоступна"
        return None

    def item_physically_available(item_id, state=None):
        state = _state(state)
        if not item_owns(item_id, state): return False
        position = item_current_state(item_id, state)
        return position in ("inventory", "worn") or position == state.location_id

    def item_use_reason(item_id, state=None):
        state = _state(state); item = ITEMS.get(item_id)
        if not item or not item_physically_available(item_id, state): return "Предмет физически недоступен"
        if not item.get("usable"): return "Предмет не используется напрямую"
        if state.player.openness.rank < item["required_openness_use"]: return "Недостаточная раскрепощенность для использования"
        if not conditions_match(item.get("use_conditions", {}), state): return "Условия использования не выполнены"
        if "energy_drink" in item.get("tags", ()):
            ready_at = getattr(state, "energy_drink_ready_at", None)
            if ready_at is not None and _game_datetime(state) < ready_at: return "Следующий энергетик можно выпить после %s" % ready_at.strftime("%d.%m %H:%M")
        return None

    def body_item_change_reason(item_id, active, state=None):
        state = _state(state); item = ITEMS.get(item_id)
        if not item or "persistent_body_item" not in item["use_modes"]: return "Предмет не поддерживает длительное состояние на теле"
        if not item_owns(item_id, state): return "Предмет не принадлежит Насте"
        if body_item_active(item_id, state) == bool(active): return None
        if active:
            reason = item_use_reason(item_id, state)
            if reason: return reason
            slot = item.get("body_slot")
            if slot and any(body_item_active(other_id, state) and ITEMS[other_id].get("body_slot") == slot for other_id in ITEMS):
                return "Это место уже занято другим предметом"
            blocked_slots = set(item.get("incompatible_clothing_slots", ()))
            if any(state.wardrobe.equipped.get(slot_id) for slot_id in blocked_slots): return "Предмет несовместим с надетой одеждой"
        return None

    def set_body_item(item_id, active, state=None):
        state = _state(state)
        reason = body_item_change_reason(item_id, active, state)
        if reason: return False, reason
        if body_item_active(item_id, state) == bool(active): return True, None
        if active:
            state.inventory.item_states[item_id] = "body"
        else:
            state.inventory.item_states.pop(item_id, None)
            if item_id == "remote_toy":
                runtime = remote_toy_runtime(state); runtime["active"] = False; runtime["active_minutes"] = 0; runtime["max_minutes"] = 0
        dispatch_game_event("body_item_changed", state, True, item_id=item_id, active=bool(active))
        return True, None

    def item_effects_reason(effects, state):
        for effect in effects:
            if effect[0] == "body_item":
                reason = body_item_change_reason(effect[1], effect[2], state)
                if reason: return reason
        return None

    def action_item_options(action_id, state=None):
        state = _state(state); action, reasons = check_action(action_id, state)
        if reasons or not action.item_capability: return []
        return [item_id for item_id, item in ITEMS.items()
                if action.item_capability in item.get("tags", ())
                and "action_tool" in item["use_modes"] and not item_use_reason(item_id, state)]

    def action_item_reason(action, item_id, state):
        if item_id is None:
            return None if action.allow_without_item else "Выберите подходящий предмет"
        if item_id not in action_item_options(action.id, state): return "Предмет не подходит или недоступен для этого действия"
        return None

    def wardrobe_access_rules(state=None):
        state = _state(state)
        # A script may explicitly grant a temporary context; movement revokes it.
        return state.wardrobe.access_context or WARDROBE_ACCESS.get(state.location_id, {})

    def wardrobe_access_allowed(state=None):
        state = _state(state); rules = wardrobe_access_rules(state)
        return bool(rules) and conditions_match(rules.get("conditions", {}), state)

    def wardrobe_context(state=None):
        state = _state(state)
        if state.wardrobe.active_workplace: return state.wardrobe.active_workplace
        return wardrobe_access_rules(state).get("context", "home")

    def wardrobe_work_locations(state=None):
        state = _state(state); workplace = state.wardrobe.active_workplace
        return {location_id for location_id, rules in WARDROBE_ACCESS.items() if rules.get("workplace") == workplace}

    def wardrobe_available_items(state=None):
        state = _state(state)
        if not wardrobe_access_allowed(state): return []
        personal = {item_id for item_id in state.wardrobe.owned if item_id in CLOTHES and item_physically_available(item_id, state)}
        external = {item_id for item_id, record in state.inventory.external_items.items()
                    if item_id in CLOTHES and record["location"] == state.location_id}
        return sorted(personal | external)

    def wardrobe_grant_scene_access(context, state=None, **rules):
        _state(state).wardrobe.access_context = dict(rules, context=context)

    def wardrobe_end_scene_access(state=None):
        _state(state).wardrobe.access_context = None

    def register_external_item(item_id, owner, location_id, state=None):
        state = _state(state)
        if item_id not in ITEMS or item_owns(item_id, state): raise ValueError("External item identity unavailable")
        state.inventory.external_items[item_id] = {"owner": owner, "location": location_id}

    def inventory_visible_items(category="all", state=None):
        state = _state(state)
        return [(item_id, quantity) for item_id, quantity in state.inventory.quantities.items()
                if quantity > 0 and ITEMS[item_id]["storage"] == "inventory"
                and (category == "all" or ITEMS[item_id]["category"] == category)]

    def nutrition_state(state=None):
        state = _state(state)
        if NUTRITION_THRESHOLDS is None: return None
        elapsed = getattr(state, "nutrition_elapsed_minutes", 0.0)
        if elapsed >= NUTRITION_THRESHOLDS["very_hungry"]: return "very_hungry"
        if elapsed >= NUTRITION_THRESHOLDS["hungry"]: return "hungry"
        return "sated" if elapsed < NUTRITION_THRESHOLDS["sated"] else "normal"

    def status_hud_entries(state=None):
        state = _state(state); result = []
        if state.player.energy <= 1:
            result.append(("tired", "Устала", "Энергия почти закончилась: %s/%s" % (state.player.energy, state.player.max_energy)))
        hunger = nutrition_state(state)
        if hunger in ("hungry", "very_hungry"):
            result.append(("hungry", "Голодна", "Часть физических действий требует больше энергии." if hunger == "hungry" else "Зарядка недоступна; физические действия ограничены питанием."))
        if 7 <= state.player.arousal <= 9:
            result.append(("arousal_yellow", "Сильно возбуждена", "Возбуждение: %s/10." % state.player.arousal))
        elif state.player.arousal == 10:
            result.append(("arousal_red", "Перевозбуждена", "Возбуждение достигло максимума: 10/10."))
        outfit_tags = set(wardrobe_get_outfit_tags(state))
        if "no_panties" in outfit_tags and ("skirt" in outfit_tags or state.wardrobe.equipped.get("dress")):
            result.append(("no_panties", "Без трусов", "Под юбкой или платьем нет трусиков."))
        if state.player.mood < 0:
            result.append(("mood", "Плохое настроение", "Текущее настроение отрицательное."))
        for item_id, item in ITEMS.items():
            if body_item_active(item_id, state): result.append((item_id, item["name"], "Предмет установлен. Остается на теле до извлечения."))
        return result
