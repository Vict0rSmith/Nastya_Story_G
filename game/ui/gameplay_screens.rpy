default ui_inventory_selected_item = None
default ui_inventory_category = "all"
default ui_wardrobe_selected_clothing = None
default ui_wardrobe_category = "all"

init -30 python:
    import re
    WEEKDAY_NAMES = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
    PERIOD_NAMES = {"morning": "Утро", "day": "День", "evening": "Вечер", "night": "Ночь", "late_night": "Поздняя ночь"}
    SOCIAL_STATE_NAMES = {"unmet": "Не знакомы", "neutral": "Нейтральные", "friend": "Дружеские", "enemy": "Враждебные"}
    INTIMACY_STATE_NAMES = {"none": "Нет", "sexual": "Сексуальные", "romantic": "Романтические"}
    RANK_NAMES = {
        "openness": ("Скромная", "Любопытная", "Смелая", "Раскрепощенная"),
        "fitness": ("Слабая", "Обычная", "Подтянутая", "Спортивная", "Отличная"),
        "intellect": ("Без подготовки", "Базовый уровень", "Хорошая подготовка", "Продвинутая", "Высокий уровень"),
    }
    HUD_LOCATION_ICONS = {
        "loc_apartment_5_hallway": "location_apartment_5_hallway",
        "loc_apartment_5_room": "location_apartment_5_room",
        "loc_apartment_5_kitchen": "location_apartment_5_kitchen",
        "loc_apartment_5_bathroom": "location_apartment_5_bathroom",
        "loc_apartment_5_balcony": "location_apartment_5_balcony",
    }
    HUD_ACTION_ICONS = {
        "action_look_in_mirror": "action_look_in_mirror",
        "action_exercise": "action_exercise",
        "action_clean_apartment": "action_clean_apartment",
        "action_unpack_luggage": "action_unpack_luggage",
        "action_rest_lie_down": "action_rest_lie_down",
        "action_watch_tv": "action_watch_tv",
        "action_sleep": "action_sleep",
        "action_prepare_meal": "action_prepare_meal",
        "action_eat_full_meal": "action_eat_full_meal",
        "action_morning_hygiene": "action_morning_hygiene",
        "action_take_shower": "action_take_shower",
        "action_take_bath": "action_take_bath",
        "action_toilet": "action_toilet",
        "action_shave_legs": "action_shave_legs",
        "action_shave_pubic": "action_shave_pubic",
        "action_admire_view": "action_admire_view",
        "action_remind_masha_school_documents": "action_remind_masha_school_documents",
        "action_talk_masha_admissions": "fallback",
        "action_wait": "fallback",
        "action_open_shop_menu": "top_inventory",
        "action_open_cafe_menu": "action_prepare_meal",
        "action_view_adult_magazine": "top_inventory",
        "action_watch_adult_movie": "action_watch_tv",
        "action_read_sex_illustrated_book": "top_inventory",
        "action_masturbate": "fallback",
    }
    HUD_NPC_ICONS = {"masha": "top_masha", "nika": "npc_nika"}

    def hud_button_image(icon_id, state, size):
        return Transform("ui/hud/buttons/{}-{}.png".format(icon_id, state), xysize=(size, size))

    def relationship_hud_label(npc_id, state=None):
        state = _state(state)
        social = get_social_state(npc_id, state)
        return SOCIAL_STATE_NAMES.get(social, social)

    def relationship_detail_lines(npc_id, state=None):
        state = _state(state)
        lines = []
        social = get_social_state(npc_id, state)
        lines.append("Социальные отношения: %s" % SOCIAL_STATE_NAMES.get(social, social))
        intimacy = get_intimacy_state(npc_id, state)
        if intimacy != "none":
            lines.append("Близость: %s" % INTIMACY_STATE_NAMES.get(intimacy, intimacy))
        return lines

    def location_actions(state=None):
        state = _state(state)
        result = []
        for action in ACTIONS.values():
            if action.required_npc or (action.locations and state.location_id not in action.locations):
                continue
            if "intimate" in action.tags and not conditions_match(action.conditions, state):
                continue
            if action.id == "action_unpack_luggage" and LUGGAGE_UNPACKED_FLAG in state.story.flags:
                continue
            result.append(action)
        return result

    def npc_actions(npc_id, state=None):
        state = _state(state)
        return [action for action in ACTIONS.values()
                if action.required_npc == npc_id
                and (not action.locations or state.location_id in action.locations)
                and (action.id != "action_remind_masha_school_documents" or masha_documents_reminder_available(state))
                and (action.id != "action_talk_masha_admissions" or admissions_conversation_available(state))]

    def run_action_ui(action_id, item_id=None, item_selected=False):
        if action_id == "action_open_shop_menu":
            renpy.show_screen("shop_screen", catalog_id="loc_shop", title="Купить продукты")
            renpy.restart_interaction()
            return
        if action_id == "action_open_cafe_menu":
            renpy.show_screen("shop_screen", catalog_id="loc_cafe", title="Заказать поесть")
            renpy.restart_interaction()
            return
        if ACTIONS[action_id].item_capability and not item_selected:
            renpy.show_screen("action_item_screen", action_id=action_id)
            renpy.restart_interaction()
            return
        result = execute_action(action_id, item_id=item_id)
        if not result.success:
            renpy.notify(result.reasons[0] if result.reasons else "Действие недоступно")
            if result.reasons and result.reasons[0] == "Сначала нужно успеть подать документы в университет": request_first_day_deadline_departure()
        run_pending_scene_ui()
        if result.success and not game_state.story.pending_action:
            renpy.notify("Действие выполнено")
        renpy.restart_interaction()

    def move_ui(location_id, mode="walk"):
        success, reason = move_to(location_id, mode=mode)
        if not success:
            renpy.notify(reason)
        if reason == "Сначала нужно успеть подать документы в университет": request_first_day_deadline_departure()
        run_pending_scene_ui()
        renpy.restart_interaction()

    def shop_offer_rows(catalog_id):
        rows = []
        for item_id, offer in SHOP_CATALOGS.get(catalog_id, {}).items():
            item = ITEMS[item_id]
            if not item.get("stackable", True) and inventory_has(item_id, 1, game_state):
                continue
            rows.append((item_id, offer))
        return rows

    def buy_shop_item_ui(catalog_id, item_id):
        success, reason = fulfill_shop_purchase(catalog_id, item_id)
        renpy.notify(("Заказ выполнен" if catalog_id == "loc_cafe" else "Покупка выполнена") if success else reason)
        renpy.restart_interaction()

    def shop_item_kind(item):
        tags = item.get("tags", ())
        if "food_kit" in tags: return "ПОЛНОЦЕННАЯ ЕДА · НУЖНО ГОТОВИТЬ"
        if "good_snack" in tags: return "ПЛОТНЫЙ ПЕРЕКУС"
        if "light_snack" in tags: return "ЛЕГКИЙ ПЕРЕКУС"
        if "energy_drink" in tags: return "ЭНЕРГЕТИК"
        if any(effect[0] == "nutrition_full" for effect in item.get("effects", ())): return "ПОЛНОЦЕННАЯ ЕДА"
        if any(effect[0] == "nutrition_cap" and effect[1] <= 120 for effect in item.get("effects", ())): return "ПЛОТНЫЙ ПЕРЕКУС"
        if any(effect[0] == "nutrition_cap" for effect in item.get("effects", ())): return "ЛЕГКИЙ ПЕРЕКУС"
        return "БЫТОВОЙ ТОВАР"

    def run_pending_scene_ui():
        while game_state.story.pending_scene:
            scene_label = game_state.story.pending_scene
            game_state.story.pending_scene = None
            renpy.call_in_new_context(scene_label)

    def location_context_name(location_id):
        node = WORLD_MAP[location_id]
        parent = WORLD_MAP.get(node.get("parent"), {})
        return "%s — %s" % (parent["name"], node["name"]) if parent else node["name"]

    def location_tile_name(location_id):
        name = LOCATIONS[location_id]["name"]
        apartment_match = re.match(r"loc_apartment_(\d+)(?:_hallway)?$", location_id)
        if apartment_match:
            apartment_number = int(apartment_match.group(1))
            name = {5: "Моя квартира", 6: "Квартира Ники", 7: "Квартира Анны"}.get(apartment_number, "Квартира №%s" % apartment_number)
        elif location_id.startswith("loc_entrance_") and "_floor_" in location_id:
            parts = location_id.split("_")
            name = "Подъезд %s\n%s этаж" % (parts[2], parts[4])
        elif location_id.startswith("loc_apartment_") and location_id.endswith("_hallway"):
            name = "Кв. %s\nПрихожая" % location_id.split("_")[2]
        elif location_id == "loc_cafe_hall":
            name = "Зал кафе"
        elif location_id == "loc_shop_hall":
            name = "Мини-маркет"
        elif "_boutique_repair_" in location_id:
            name += " №" + str(int(location_id.rsplit("_", 1)[1]))
        return name.upper()

    def apartment_door_hint(location_id):
        match = re.match(r"loc_apartment_(\d+)(?:_hallway)?$", location_id)
        if not match: return None
        number = int(match.group(1))
        return {5: "Квартира Насти и Маши", 6: "Квартира Ники", 7: "Квартира Анны"}.get(number, "Квартира №%s" % number)

    def hud_navigation_label(location_id, state=None):
        state = _state(state)
        if state.location_id == "loc_residential_district_main":
            if location_id == "loc_cafe_hall": return "Кафе"
            if location_id == "loc_masha_school_entrance": return "Колледж"
        if location_id.startswith("loc_apartment_5") and state.location_id.startswith("loc_entrance_1_floor_"):
            return "Моя квартира"
        if location_id.startswith("loc_entrance_") and "_floor_" in location_id:
            return "Выйти в подъезд"
        hint = apartment_door_hint(location_id)
        return hint or location_tile_name(location_id)

    def hud_room_label(location_id, state=None):
        state = _state(state)
        current = state.location_id
        if "_apartment_" in current:
            if location_id.endswith("_room"): return "Комната"
            if location_id.endswith("_kitchen"): return "Кухня"
            if location_id.endswith("_bathroom"): return "Ванная"
            if location_id.endswith("_hallway"): return "Прихожая"
            if location_id.startswith("loc_entrance_") and "_floor_" in location_id: return "Выйти в подъезд"
            if location_id == "loc_building_yard": return "Выйти на улицу"
            if location_id == "loc_residential_district_main": return "Выйти в район"
        return hud_navigation_label(location_id, state)

    def hud_navigation_hint(location_id, state=None):
        name = apartment_door_hint(location_id) or location_context_name(location_id)
        minutes, reason = transition_info(location_id, state)
        return name + (" · %s мин." % minutes if minutes is not None else "") + (" · " + reason if reason else "")

    HUD_ACTION_NAMES = {
        "action_look_in_mirror": "Зеркало", "action_exercise": "Зарядка",
        "action_clean_apartment": "Уборка", "action_unpack_luggage": "Чемоданы",
        "action_rest_lie_down": "Отдохнуть", "action_watch_tv": "Телевизор",
        "action_sleep": "Спать", "action_prepare_meal": "Готовить",
        "action_morning_hygiene": "Умыться", "action_take_shower": "Душ",
        "action_take_bath": "Ванна", "action_toilet": "Туалет",
        "action_shave_legs": "Побрить ноги", "action_shave_pubic": "Интимный уход",
        "action_admire_view": "Вид с балкона",
        "action_remind_masha_school_documents": "Документы Маши",
        "action_talk_masha_admissions": "Поступление",
        "action_wait": "Подождать час",
        "action_open_shop_menu": "Купить продукты",
        "action_open_cafe_menu": "Заказать поесть",
        "action_view_adult_magazine": "Порножурнал",
        "action_watch_adult_movie": "Порнофильм",
        "action_read_sex_illustrated_book": "Книга о сексе",
        "action_masturbate": "Мастурбировать",
    }

    def hud_action_name(action):
        return HUD_ACTION_NAMES.get(action.id, action.name)

    def food_kit_count(state=None):
        state = _state(state)
        return sum(state.inventory.quantities.get(item_id, 0) for item_id, item in ITEMS.items() if "food_kit" in item.get("tags", ()))

    def hud_action_hint(action, reasons, state=None):
        state = _state(state)
        detail = ""
        if action.id == "action_prepare_meal": detail = " · Комплектов: %s" % food_kit_count(state)
        elif action.id == "action_eat_full_meal": detail = " · Готовых порций: %s" % state.inventory.quantities.get("prepared_home_meal", 0)
        return action.name + " · %s мин." % action_duration_minutes(action, state=state) + detail + (" · " + reasons[0] if reasons else "")

    def hud_floor_level(location_id):
        if location_id == "loc_building_basement": return ("loc_entrance_1", 0)
        if location_id == "loc_building_roof": return ("loc_entrance_1", 6)
        parts = location_id.rsplit("_floor_", 1)
        if len(parts) == 2 and parts[1].isdigit(): return (parts[0], int(parts[1]))
        return None

    def hud_navigation_entries(state=None):
        state = _state(state)
        entries = []
        level = hud_floor_level(state.location_id)
        stairs = {"up": None, "down": None}
        targets = list(LOCATIONS[state.location_id].get("transitions", {}))
        def navigation_order(target):
            if hud_floor_level(state.location_id) and hud_floor_level(target): return (0, hud_floor_level(target)[1])
            if "_apartment_" in state.location_id:
                room_order = {"_room": 0, "_kitchen": 1, "_bathroom": 2, "_hallway": 3}
                for suffix, order in room_order.items():
                    if target.endswith(suffix): return (1, order)
            apartment = re.match(r"loc_apartment_(\d+)(?:_hallway)?$", target)
            if apartment: return (2, int(apartment.group(1)))
            return (3, LOCATIONS[target]["name"])
        for target in sorted(targets, key=navigation_order):
            target_level = hud_floor_level(target)
            if level and target_level and level[0] == target_level[0] and abs(level[1] - target_level[1]) == 1:
                stairs["up" if target_level[1] > level[1] else "down"] = target
            else:
                entries.append(("location", target))
        if any(stairs.values()): entries.insert(0, ("stairs", stairs))
        if TRANSPORT_ROUTES.get(state.location_id): entries.append(("bus", None))
        return entries

    def hud_row_metrics(count):
        width = min(124, (912 - 6 * max(0, count - 1)) // max(1, count))
        return width, min(104, width - 4)

    def use_item_ui(item_id):
        renpy.notify("Предмет использован" if inventory_use(item_id) else "Предмет нельзя использовать")
        renpy.restart_interaction()

    def toggle_remote_toy_ui(active):
        success, reason = set_remote_toy_active(active)
        renpy.notify(("Игрушка включена" if active else "Игрушка выключена") if success else reason)
        renpy.restart_interaction()

    def inventory_item_command(item_id):
        item = ITEMS[item_id]
        if "persistent_body_item" in item["use_modes"]:
            return "Вынуть" if body_item_active(item_id) else "Вставить"
        return "Выберите в действии" if item["use_modes"] else "Использовать"

    def inventory_direct_use_allowed(item_id):
        item = ITEMS[item_id]
        if body_item_active(item_id): return True
        return not item_use_reason(item_id) and (not item["use_modes"] or "persistent_body_item" in item["use_modes"])

    def equip_item_ui(item_id):
        success, reason = wardrobe_equip(item_id)
        if success: advance_time(10, "wardrobe_change")
        renpy.notify("Одежда надета" if success else reason)
        renpy.restart_interaction()

    def unequip_item_ui(slot):
        success = wardrobe_unequip(slot)
        if success: advance_time(10, "wardrobe_change")
        renpy.notify("Одежда снята" if success else "Одежду нельзя снять")
        renpy.restart_interaction()

    def unequip_all_ui():
        changed = False
        for slot in OUTFIT_SLOTS:
            if game_state.wardrobe.equipped.get(slot) and wardrobe_unequip(slot): changed = True
        if changed: advance_time(10, "wardrobe_change")
        renpy.notify("Одежда снята" if changed else "Нечего снимать")
        renpy.restart_interaction()

    def npc_current_location(npc_id, state=None):
        state = _state(state)
        for location_id in LOCATIONS:
            if npc_id in get_present_npcs(location_id=location_id, state=state):
                return location_id
        return None

screen hud_icon_button(icon_id, button_action, selected=False, enabled=True, size=104, hint=None, widget_id=None):
    fixed:
        xsize size
        ysize size
        xalign 0.5
        imagebutton:
            id widget_id
            idle hud_button_image(icon_id, "idle" if enabled else "disabled", size)
            hover hud_button_image(icon_id, "hover" if enabled else "disabled", size)
            selected_idle hud_button_image(icon_id, "selected", size)
            selected_hover hud_button_image(icon_id, "selected", size)
            insensitive hud_button_image(icon_id, "disabled", size)
            action (button_action if enabled else NullAction())
            selected selected
            sensitive True
            focus_mask True
            tooltip hint

screen hud_stair_button(stairs, size=104):
    vbox:
        spacing 0
        for direction in ("up", "down"):
            $ destination = stairs[direction]
            $ minutes, reason = transition_info(destination) if destination else (None, "Нет этажа")
            imagebutton:
                id ("stairs_" + direction)
                idle Transform("ui/hud/stairs-" + direction + "-idle.svg", xysize=(size, size // 2))
                hover Transform("ui/hud/stairs-" + direction + "-hover.svg", xysize=(size, size // 2))
                insensitive Transform("ui/hud/stairs-" + direction + "-disabled.svg", xysize=(size, size // 2))
                sensitive destination is not None
                action (Function(move_ui, destination) if destination and reason is None else NullAction())
                tooltip (hud_navigation_hint(destination) if destination else None)
                focus_mask True

screen hud_compact_caption(label, caption, width, current=False):
    fixed:
        xsize width
        ysize 54
        text label style "ns_hud_tile_label" size 13 xsize width xalign 0.5 text_align 0.5
    fixed:
        xsize width
        ysize 36
        text caption style "ns_hud_tile_caption" color (NS_COLOR["amber"] if current else NS_COLOR["text_secondary"]) size 12 xsize width xalign 0.5 text_align 0.5

screen game_hud():
    default selected_npc = None
    default selected_action = None
    zorder 10
    $ state = game_state
    $ location = LOCATIONS[state.location_id]
    $ present = get_present_npcs(state=state)

    frame:
        style "ns_hud_panel"
        xpos 24
        ypos 24
        xsize 240
        ysize 104
        vbox:
            spacing 5
            text "ДЕНЬГИ  [state.wallet.balance] ₽" style "ns_text" color NS_COLOR["amber"]
            text "ЭНЕРГИЯ  [state.player.energy] / [state.player.max_energy]" style "ns_text" color NS_COLOR["violet"]
            text "Ресурсы героини" style "ns_caption"

    hbox:
        xalign 0.5
        ypos 24
        spacing 8
        vbox:
            xsize 86
            use hud_icon_button("top_nastya", Show("profile_screen"), size=68)
            xalign 0.5
            text "НАСТЯ" style "ns_hud_tile_label" xalign 0.5
        vbox:
            xsize 86
            use hud_icon_button("top_masha", Show("masha_profile_screen"), size=68)
            xalign 0.5
            text "МАША" style "ns_hud_tile_label" xalign 0.5
        vbox:
            xsize 86
            use hud_icon_button("top_phone", [SetVariable("ui_phone_app", "home"), Show("phone_screen")], size=68)
            xalign 0.5
            text "ТЕЛЕФОН" style "ns_hud_tile_label" xalign 0.5
        vbox:
            xsize 86
            use hud_icon_button("top_inventory", [SetVariable("ui_inventory_selected_item", None), Show("inventory_screen")], size=68)
            xalign 0.5
            text "ВЕЩИ" style "ns_hud_tile_label" xalign 0.5
        vbox:
            xsize 86
            use hud_icon_button("top_wardrobe", [SetVariable("ui_wardrobe_selected_clothing", None), SetVariable("ui_wardrobe_category", "all"), Show("wardrobe_screen")], enabled=wardrobe_access_allowed(state), size=68)
            xalign 0.5
            text "ГАРДЕРОБ" style "ns_hud_tile_label" xalign 0.5
        vbox:
            xsize 86
            use hud_icon_button("top_menu", ShowMenu("preferences"), size=68)
            xalign 0.5
            text "МЕНЮ" style "ns_hud_tile_label" xalign 0.5

    frame:
        style "ns_hud_panel"
        xpos 1636
        ypos 24
        xsize 260
        ysize 104
        vbox:
            xfill True
            hbox:
                xfill True
                text "[state.clock.display_time]" style "ns_title" size 26
                text "[WEEKDAY_NAMES[state.clock.weekday]]" style "ns_muted" xalign 1.0
            hbox:
                xfill True
                text location["name"].upper() color NS_COLOR["amber"] size 14 xmaximum 174
                text PERIOD_NAMES[state.clock.period] style "ns_muted" xalign 1.0

    hbox:
        id "status_hud"
        xpos 276
        ypos 62
        spacing 8
        for status_id, status_name, status_description in status_hud_entries(state):
            imagebutton:
                idle Transform("ui/status/" + status_id + ".svg", xysize=(28, 28))
                hover Transform("ui/status/" + status_id + ".svg", xysize=(28, 28), alpha=0.8)
                action NullAction()
                tooltip (status_name + ". " + status_description)

    if present:
        vbox:
            xpos 1788
            ypos 155
            spacing 8
            text "ЗДЕСЬ" style "ns_hud_tile_caption" xalign 0.5
            for npc_id in present:
                vbox:
                    at ns_hud_active
                    use hud_icon_button(HUD_NPC_ICONS.get(npc_id, "fallback"), [SetScreenVariable("selected_npc", None if selected_npc == npc_id else npc_id), SetScreenVariable("selected_action", None)], selected=(selected_npc == npc_id), widget_id=("hud_npc_" + npc_id))
                    text NPCS[npc_id]["name"].upper() style "ns_hud_tile_label" xalign 0.5
                    text relationship_hud_label(npc_id, state) style "ns_hud_tile_caption" xalign 0.5

    if selected_npc and selected_npc in present:
        frame:
            style "ns_hud_panel"
            xpos 1450
            ypos 215
            xsize 330
            vbox:
                spacing 10
                text "ДЕЙСТВИЯ: [NPCS[selected_npc]['name'].upper()]" style "ns_hud_tile_caption"
                vbox:
                    spacing 6
                    for action in npc_actions(selected_npc, state):
                        $ checked, reasons = check_action(action.id, state)
                        button:
                            style "ns_button"
                            xfill True
                            padding (10, 7)
                            sensitive not reasons
                            action Function(run_action_ui, action.id)
                            tooltip hud_action_hint(action, reasons, state)
                            hbox:
                                spacing 10
                                yalign 0.5
                                add hud_button_image(HUD_ACTION_ICONS.get(action.id, "fallback"), "idle", 32)
                                text hud_action_name(action) style "ns_text" size 16 yalign 0.5 xmaximum 250

    if renpy.get_screen("say") is None:
        $ navigation = hud_navigation_entries(state)
        $ nav_width, nav_icon = hud_row_metrics(len(navigation))
        $ actions = location_actions(state)
        $ action_width, action_icon = hud_row_metrics(len(actions))
        hbox:
            id "world_navigation"
            xpos 24
            ypos 892
            spacing 6
            for kind, value in navigation:
                vbox:
                    xsize nav_width
                    spacing 2
                    if kind == "stairs":
                        hbox:
                            xalign 0.5
                            use hud_stair_button(value, nav_icon)
                    elif kind == "bus":
                        hbox:
                            xalign 0.5
                            use hud_icon_button("fallback", Show("transport_screen"), size=nav_icon, hint="Автобус · выбрать маршрут")
                        use hud_compact_caption("АВТОБУС", "", nav_width)
                    else:
                        $ blocked_reason = transition_info(value, state)[1]
                        hbox:
                            xalign 0.5
                            use hud_icon_button(HUD_LOCATION_ICONS.get(value, "fallback"), Function(move_ui, value), enabled=not blocked_reason, size=nav_icon, hint=hud_navigation_hint(value, state))
                        use hud_compact_caption(hud_room_label(value, state).upper(), "", nav_width)
        fixed:
            xpos 984
            ypos 892
            xsize 912
            ysize 198
            hbox:
                id "world_actions"
                xalign 1.0
                spacing 6
                for action in actions:
                    $ checked, reasons = check_action(action.id, state)
                    vbox:
                        xsize action_width
                        spacing 2
                        at (ns_hud_dimmed if selected_action and selected_action != action.id else ns_hud_active)
                        hbox:
                            xalign 0.5
                            if action.id == "action_open_shop_menu":
                                use hud_icon_button(HUD_ACTION_ICONS.get(action.id, "fallback"), [SetScreenVariable("selected_action", None), Show("shop_screen", catalog_id="loc_shop", title="Купить продукты")], enabled=not reasons, size=action_icon, hint=hud_action_hint(action, reasons, state))
                            elif action.id == "action_open_cafe_menu":
                                use hud_icon_button(HUD_ACTION_ICONS.get(action.id, "fallback"), [SetScreenVariable("selected_action", None), Show("shop_screen", catalog_id="loc_cafe", title="Заказать поесть")], enabled=not reasons, size=action_icon, hint=hud_action_hint(action, reasons, state))
                            else:
                                use hud_icon_button(HUD_ACTION_ICONS.get(action.id, "fallback"), [SetScreenVariable("selected_action", None), SetScreenVariable("selected_npc", None), Function(run_action_ui, action.id)], enabled=not reasons, size=action_icon, hint=hud_action_hint(action, reasons, state), widget_id=("hud_action_" + action.id))
                        use hud_compact_caption(hud_action_name(action).upper(), "", action_width)

    if GetTooltip():
        $ tooltip_x, tooltip_y = hud_tooltip_placement()
        frame:
            style "ns_hud_panel"
            xpos tooltip_x
            xanchor 0.5
            ypos tooltip_y
            xsize 440
            text GetTooltip() style "ns_caption" text_align 0.5

screen shop_screen(catalog_id="loc_shop", title="Купить продукты"):
    modal True
    zorder 100
    use modal_shell(title, Hide("shop_screen"), width=1520, height=900):
        frame:
            background Solid(NS_COLOR["box_dark"])
            padding (20, 20)
            vpgrid:
                cols 4
                xsize 1400
                ysize 760
                spacing 16
                mousewheel True
                draggable True
                scrollbars "vertical"
                for item_id, offer in shop_offer_rows(catalog_id):
                    $ item = ITEMS[item_id]
                    $ price = offer.get("price")
                    $ purchase_reason = item_purchase_reason(item_id, game_state)
                    $ can_afford = price is not None and game_state.wallet.balance >= int(price)
                    button:
                        style "ns_shop_item_button"
                        action Function(buy_shop_item_ui, catalog_id, item_id)
                        sensitive price is not None and not purchase_reason and can_afford
                        tooltip (purchase_reason or ("Недостаточно денег" if price is not None and not can_afford else item["name"]))
                        vbox:
                            spacing 8
                            xalign 0.5
                            if item.get("icon"):
                                add item["icon"] xysize (72, 72) xalign 0.5
                            else:
                                add "ui/hud/buttons/fallback-idle.png" xysize (72, 72) xalign 0.5
                            text item["name"] style "ns_text" bold True xalign 0.5 text_align 0.5
                            text shop_item_kind(item) style "ns_caption" color NS_COLOR["teal"] xalign 0.5 text_align 0.5
                            text ("%s ₽" % price if price is not None else "Цена не утверждена") style "ns_text" color NS_COLOR["amber"] xalign 0.5
                            text ("ЗАКАЗАТЬ" if offer.get("consume_immediately") else "КУПИТЬ") style "ns_caption" xalign 0.5
                for index in range(max(0, 12 - len(shop_offer_rows(catalog_id)))):
                    frame:
                        style "ns_empty_cell"
                        xsize 320
                        ysize 250

screen modal_shell(title, close_action, width=1660, height=940):
    button:
        background Solid(NS_COLOR["overlay"])
        hover_background Solid(NS_COLOR["overlay"])
        xsize config.screen_width
        ysize config.screen_height
        action close_action
    frame:
        style "ns_panel"
        xalign 0.5
        yalign 0.5
        xsize width
        ysize height
        fixed:
            button:
                background Solid("#00000001")
                hover_background Solid("#00000001")
                xsize width
                ysize height
                action NullAction()
            vbox:
                spacing 16
                hbox:
                    xfill True
                    text title style "ns_title"
                    null width 32
                    textbutton "Закрыть" action close_action style "ns_close_button" xalign 1.0
                transclude

screen character_preview(name, subtitle):
    frame:
        style "ns_surface_light"
        xsize 520
        yfill True
        vbox:
            spacing 16
            text subtitle.upper() style "ns_caption"
            text name.upper() style "ns_title" size 44
            frame:
                background Solid(NS_COLOR["neutral_900"] + "88")
                xfill True
                ysize 560
                text "ОБЛАСТЬ ПЕРСОНАЖА\nИзображение пока отсутствует" style "ns_muted" xalign 0.5 yalign 0.5 text_align 0.5

screen profile_screen():
    modal True
    zorder 100
    use modal_shell("Карточка Насти", Hide("profile_screen")):
        hbox:
            spacing 24
            use character_preview("Настя", "Главная героиня")
            vbox:
                spacing 16
                xfill True
                hbox:
                    spacing 16
                    frame:
                        style "ns_panel_compact"
                        xfill True
                        vbox:
                            text "ЭНЕРГИЯ" style "ns_caption" color NS_COLOR["violet"]
                            text "[game_state.player.energy] / [game_state.player.max_energy]" style "ns_title"
                    frame:
                        style "ns_panel_compact"
                        xfill True
                        vbox:
                            text "ДЕНЬГИ" style "ns_caption" color NS_COLOR["amber"]
                            text "[game_state.wallet.balance] ₽" style "ns_title"
                frame:
                    style "ns_panel_compact"
                    vbox:
                        text "Характеристики" style "ns_section_title"
                        null height 8
                        hbox:
                            spacing 44
                            vbox:
                                text "РАСКРЕПОЩЕННОСТЬ" style "ns_caption" color NS_COLOR["coral"]
                                text RANK_NAMES["openness"][game_state.player.openness.rank] style "ns_text"
                            vbox:
                                text "ФИЗИЧЕСКАЯ ФОРМА" style "ns_caption" color NS_COLOR["green"]
                                text RANK_NAMES["fitness"][game_state.player.fitness.rank] style "ns_text"
                            vbox:
                                text "ИНТЕЛЛЕКТ" style "ns_caption" color NS_COLOR["teal"]
                                text RANK_NAMES["intellect"][game_state.player.intellect.rank] style "ns_text"
                hbox:
                    spacing 16
                    frame:
                        style "ns_panel_compact"
                        xfill True
                        yfill True
                        vbox:
                            text "Состояние" style "ns_section_title"
                            text "Настроение: [('Подавленное' if game_state.player.mood < 0 else 'Приподнятое' if game_state.player.mood > 0 else 'Нормальное')]" style "ns_text"
                            text "Возбуждение: [arousal_label(game_state.player.arousal)]" style "ns_muted"
                            text "Местоположение: [LOCATIONS[game_state.location_id]['name']]" style "ns_muted"
                    frame:
                        style "ns_panel_compact"
                        xfill True
                        yfill True
                        vbox:
                            text "Навыки" style "ns_section_title"
                            if game_state.player.skills:
                                for skill_id, skill in game_state.player.skills.items():
                                    text "[skill_id]: уровень [skill.rank]" style "ns_text"
                            else:
                                text "Навыки пока не открыты" style "ns_muted"

screen masha_profile_screen():
    modal True
    zorder 100
    use modal_shell("Карточка Маши", Hide("masha_profile_screen")):
        hbox:
            spacing 24
            use character_preview("Маша", "Подруга Насти")
            vbox:
                spacing 16
                xfill True
                frame:
                    style "ns_panel_compact"
                    vbox:
                        text "Доступная информация" style "ns_section_title"
                        text NPCS["masha"]["description"] style "ns_text"
                        for line in relationship_detail_lines("masha", game_state):
                            text line style "ns_muted"
                        $ masha_location = npc_current_location("masha", game_state)
                        text "Сейчас: [(LOCATIONS[masha_location]['name'] if masha_location else 'местоположение неизвестно')]" style "ns_muted"
                frame:
                    style "ns_panel_compact"
                    xfill True
                    yfill True
                    text "Другие сведения пока недоступны игроку." style "ns_muted" xalign 0.5 yalign 0.5

screen action_item_screen(action_id):
    modal True
    zorder 110
    use modal_shell(ACTIONS[action_id].name, Hide("action_item_screen"), width=900, height=700):
        vbox:
            spacing 12
            if ACTIONS[action_id].allow_without_item:
                textbutton ("Руками" if action_id == "action_masturbate" else "Без предмета") action [Hide("action_item_screen"), Function(run_action_ui, action_id, None, True)] style "ns_button"
            for item_id in action_item_options(action_id):
                textbutton ITEMS[item_id]["name"] action [Hide("action_item_screen"), Function(run_action_ui, action_id, item_id, True)] style "ns_button"
            if not action_item_options(action_id) and not ACTIONS[action_id].allow_without_item:
                text "Нет доступных предметов для этого действия." style "ns_muted"

screen inventory_screen():
    modal True
    zorder 100
    $ visible_items = inventory_visible_items(ui_inventory_category)
    use modal_shell("Вещи Насти", Hide("inventory_screen")):
        frame:
            background Solid(NS_COLOR["box"])
            padding (24, 24)
            vbox:
                spacing 16
                hbox:
                    spacing 8
                    for category, title in (("all", "Все"), ("consumable", "Расходники"), ("quest", "Квестовые"), ("intimate", "Интимное")):
                        textbutton title action [SetVariable("ui_inventory_category", category), SetVariable("ui_inventory_selected_item", None)] selected ui_inventory_category == category style "ns_tab_button"
                hbox:
                    spacing 24
                    frame:
                        background Solid(NS_COLOR["box_dark"])
                        padding (16, 16)
                        vpgrid:
                            cols 5
                            xsize 866
                            ysize 676
                            mousewheel True
                            draggable True
                            scrollbars "vertical"
                            spacing 12
                            for item_id, quantity in visible_items:
                                button:
                                    style "ns_item_button"
                                    action SetVariable("ui_inventory_selected_item", item_id)
                                    selected ui_inventory_selected_item == item_id
                                    vbox:
                                        xalign 0.5
                                        yalign 0.5
                                        if ITEMS[item_id].get("icon"):
                                            add ITEMS[item_id]["icon"] xysize (80, 80) xalign 0.5
                                        text ITEMS[item_id]["name"] style "ns_text" xalign 0.5 text_align 0.5
                                        text ("Установлен" if body_item_active(item_id) else "Количество: %s" % quantity) style "ns_caption" xalign 0.5
                            for index in range(max(0, 20 - len(visible_items))):
                                frame:
                                    style "ns_empty_cell"
                    frame:
                        style "ns_panel"
                        xsize 460
                        ysize 708
                        if ui_inventory_selected_item in dict(visible_items):
                            $ selected_item = ITEMS[ui_inventory_selected_item]
                            vbox:
                                spacing 16
                                text "ВЫБРАННЫЙ ПРЕДМЕТ" style "ns_caption" color NS_COLOR["amber"]
                                text selected_item["name"] style "ns_title"
                                text selected_item["description"] style "ns_text"
                                if body_item_active(ui_inventory_selected_item):
                                    text "Установлен" style "ns_text" color NS_COLOR["teal"]
                                    if ui_inventory_selected_item == "remote_toy":
                                        $ remote_state = remote_toy_runtime()
                                        text ("Включен" if remote_state.get("active") else "Выключен") style "ns_text"
                                        text "Управление: [remote_state.get('controller', 'nastya')]" style "ns_caption"
                                elif item_use_reason(ui_inventory_selected_item):
                                    text item_use_reason(ui_inventory_selected_item) style "ns_muted"
                                textbutton inventory_item_command(ui_inventory_selected_item) action Function(use_item_ui, ui_inventory_selected_item) sensitive inventory_direct_use_allowed(ui_inventory_selected_item) style "ns_button"
                                if ui_inventory_selected_item == "remote_toy" and body_item_active("remote_toy") and remote_toy_runtime().get("controller", "nastya") == "nastya":
                                    textbutton ("Выключить" if remote_toy_is_active() else "Включить") action Function(toggle_remote_toy_ui, not remote_toy_is_active()) style "ns_button"
                        else:
                            text "Выберите предмет в коробке" style "ns_muted" xalign 0.5 yalign 0.5

screen wardrobe_screen():
    modal True
    zorder 100
    if not wardrobe_access_allowed():
        use modal_shell("Гардероб", Hide("wardrobe_screen")):
            text "Здесь нельзя переодеваться." style "ns_text"
    else:
        $ wardrobe_items = [item_id for item_id in wardrobe_available_items() if ui_wardrobe_category == "all" or CLOTHES[item_id].get("category") == ui_wardrobe_category]
        use modal_shell("Гардероб", Hide("wardrobe_screen")):
            frame:
                background Solid(NS_COLOR["wardrobe"])
                padding (24, 24)
                hbox:
                    spacing 24
                    frame:
                        background Solid(NS_COLOR["neutral_900"])
                        xsize 500
                        yfill True
                        padding (20, 20)
                        vbox:
                            text "ЗЕРКАЛО" style "ns_caption" xalign 0.5
                            frame:
                                background Solid(NS_COLOR["mirror"])
                                xfill True
                                ysize 590
                                text "ОБЛАСТЬ ПЕРСОНАЖА\nИзображение пока отсутствует" style "ns_muted" color NS_COLOR["neutral_900"] xalign 0.5 yalign 0.5 text_align 0.5
                            text "Текущий комплект" style "ns_section_title" xalign 0.5
                            text "[', '.join(wardrobe_get_outfit_tags())]" style "ns_caption" xalign 0.5 text_align 0.5
                    frame:
                        background Solid(NS_COLOR["box_dark"])
                        xfill True
                        yfill True
                        padding (20, 20)
                        vbox:
                            spacing 16
                            hbox:
                                spacing 8
                                textbutton "Все" action [SetVariable("ui_wardrobe_category", "all"), SetVariable("ui_wardrobe_selected_clothing", None)] selected ui_wardrobe_category == "all" style "ns_tab_button"
                                textbutton "Одежда" action [SetVariable("ui_wardrobe_category", "clothes"), SetVariable("ui_wardrobe_selected_clothing", None)] selected ui_wardrobe_category == "clothes" style "ns_tab_button"
                                textbutton "Белье" action [SetVariable("ui_wardrobe_category", "underwear"), SetVariable("ui_wardrobe_selected_clothing", None)] selected ui_wardrobe_category == "underwear" style "ns_tab_button"
                                textbutton "Обувь" action [SetVariable("ui_wardrobe_category", "shoes"), SetVariable("ui_wardrobe_selected_clothing", None)] selected ui_wardrobe_category == "shoes" style "ns_tab_button"
                            vpgrid:
                                cols 5
                                xsize 866
                                ysize 504
                                mousewheel True
                                scrollbars "vertical"
                                spacing 12
                                for item_id in wardrobe_items:
                                    $ item_slot = CLOTHES[item_id]["slot"]
                                    $ is_equipped = game_state.wardrobe.equipped.get(item_slot) == item_id
                                    $ can_equip, equip_reason = wardrobe_can_equip(item_id)
                                    button:
                                        style "ns_item_button"
                                        action SetVariable("ui_wardrobe_selected_clothing", item_id)
                                        selected ui_wardrobe_selected_clothing == item_id or is_equipped
                                        sensitive can_equip or is_equipped
                                        vbox:
                                            xalign 0.5
                                            yalign 0.5
                                            text ("НАДЕТО" if is_equipped else "ОДЕЖДА") style "ns_caption" color (NS_COLOR["teal"] if is_equipped else NS_COLOR["text_secondary"])
                                            text CLOTHES[item_id]["name"] style "ns_text" text_align 0.5 xalign 0.5
                                for index in range(max(0, 15 - len(wardrobe_items))):
                                    frame:
                                        style "ns_empty_cell"
                            hbox:
                                xalign 1.0
                                spacing 12
                                textbutton "Снять все" action Function(unequip_all_ui) style "ns_button"
                                textbutton "Снять выбранное" action Function(unequip_item_ui, CLOTHES[ui_wardrobe_selected_clothing]["slot"] if ui_wardrobe_selected_clothing else "") sensitive (ui_wardrobe_selected_clothing is not None and ui_wardrobe_selected_clothing in game_state.wardrobe.equipped.values()) style "ns_button"
                                textbutton "Надеть" action Function(equip_item_ui, ui_wardrobe_selected_clothing) sensitive (ui_wardrobe_selected_clothing is not None and wardrobe_can_equip(ui_wardrobe_selected_clothing)[0]) style "ns_button"

screen debug_screen():
    use modal_shell("Отладка", Hide("debug_screen")):
        vbox:
            spacing 12
            text "Schema: [game_state.schema_version] · Событий: [len(game_state.story.event_history)]" style "ns_muted"
            hbox:
                spacing 10
                textbutton "+30 минут" action [Function(advance_time, 30, "debug"), Function(renpy.restart_interaction)] style "ns_button"
                textbutton "+1 энергия" action [Function(change_energy, 1, None, "debug"), Function(renpy.restart_interaction)] style "ns_button"
                textbutton "+100 ₽" action [Function(add_money, 100, "debug"), Function(renpy.restart_interaction)] style "ns_button"
                textbutton "Флаг debug" action [Function(set_story_flag, "debug_flag"), Function(renpy.restart_interaction)] style "ns_button"
            textbutton "Запустить самопроверку" action Function(run_domain_self_tests, True) style "ns_button"


screen transport_screen():
    modal True
    zorder 50
    add Solid("#101018D9")
    frame:
        style "ns_hud_panel"
        align (0.5, 0.5)
        xsize 760
        padding (28, 24)
        vbox:
            spacing 18
            text "Автобус" style "ns_title"
            for target_id in TRANSPORT_ROUTES.get(game_state.location_id, {}):
                $ minutes, blocked_reason = transition_info(target_id, mode="bus")
                textbutton (LOCATIONS[target_id]["name"] + " — " + ("%s мин." % minutes if minutes is not None else "время не определено")):
                    style "ns_button"
                    action [Function(move_ui, target_id, "bus"), Hide("transport_screen")]
                    sensitive not blocked_reason
                if blocked_reason:
                    text blocked_reason style "ns_muted"
            textbutton "Отмена" action Hide("transport_screen") style "ns_button"
    key "game_menu" action Hide("transport_screen")

# HUD: устойчивые якоря подсказок и подсказки для недоступных действий NPC.

init -20 python:
    def _hud_tooltip_clamp(value, low, high):
        return min(max(value, low), high)

    def _hud_tooltip_matches(value, expected):
        return value is not None and expected is not None and str(value) == str(expected)

    def _hud_tooltip_focus_rect():
        try:
            return GetFocusRect("tooltip")
        except Exception:
            try:
                from renpy.display.focus import get_focus_rect
                return get_focus_rect("tooltip")
            except Exception:
                return None

    def hud_tooltip_placement():
        """Return stable HUD tooltip coordinates from the owning UI element.

        The important HUD families are resolved by their actual tooltip content and
        current HUD layout. This deliberately avoids using the mouse/focus rectangle
        for bottom controls, status icons and NPC rows, so entering a control from a
        different side cannot move the tooltip vertically or horizontally.
        """
        tooltip = GetTooltip()
        state = game_state

        # Status icons: fixed baseline below the status strip.
        for index, (status_id, status_name, status_description) in enumerate(status_hud_entries(state)):
            expected = status_name + ". " + status_description
            if _hud_tooltip_matches(tooltip, expected):
                center_x = 276 + index * 36 + 14
                return (_hud_tooltip_clamp(center_x, 220, config.screen_width - 220), 138)

        if renpy.get_screen("game_hud") is not None:
            # NPC actions/conversations: fixed column left of the panel, aligned to row.
            try:
                selected_npc = renpy.get_screen_variable("selected_npc", screen="game_hud")
            except Exception:
                selected_npc = None

            if selected_npc and selected_npc in get_present_npcs(state=state):
                for index, action in enumerate(npc_actions(selected_npc, state)):
                    checked, reasons = check_action(action.id, state)
                    expected = hud_action_hint(action, reasons, state)
                    if _hud_tooltip_matches(tooltip, expected):
                        row_y = 250 + index * 52
                        return (1210, _hud_tooltip_clamp(row_y, 180, 650))

            if renpy.get_screen("say") is None:
                # Bottom navigation: one fixed vertical level, x anchored to its cell.
                navigation = hud_navigation_entries(state)
                nav_width, nav_icon = hud_row_metrics(len(navigation))
                for index, (kind, value) in enumerate(navigation):
                    center_x = 24 + index * (nav_width + 6) + nav_width // 2
                    if kind == "bus":
                        if _hud_tooltip_matches(tooltip, "Автобус · выбрать маршрут"):
                            return (_hud_tooltip_clamp(center_x, 220, config.screen_width - 220), 790)
                    elif kind == "stairs":
                        for direction in ("up", "down"):
                            destination = value[direction]
                            expected = hud_navigation_hint(destination, state) if destination else None
                            if _hud_tooltip_matches(tooltip, expected):
                                return (_hud_tooltip_clamp(center_x, 220, config.screen_width - 220), 790)
                    else:
                        expected = hud_navigation_hint(value, state)
                        if _hud_tooltip_matches(tooltip, expected):
                            return (_hud_tooltip_clamp(center_x, 220, config.screen_width - 220), 790)

                # Bottom actions: same vertical level, x anchored to its right-aligned cell.
                actions = location_actions(state)
                action_width, action_icon = hud_row_metrics(len(actions))
                total_width = len(actions) * action_width + 6 * max(0, len(actions) - 1)
                start_x = 984 + 912 - total_width
                for index, action in enumerate(actions):
                    checked, reasons = check_action(action.id, state)
                    expected = hud_action_hint(action, reasons, state)
                    if _hud_tooltip_matches(tooltip, expected):
                        center_x = start_x + index * (action_width + 6) + action_width // 2
                        return (_hud_tooltip_clamp(center_x, 220, config.screen_width - 220), 790)

        # Fallback for unrelated tooltips. Targeted HUD families above never use this.
        rect = _hud_tooltip_focus_rect()
        if not rect:
            return (960, 740)
        try:
            x, y, width, height = rect
        except Exception:
            x, y, width, height = rect.x, rect.y, rect.w, rect.h
        center_x = x + width // 2
        return (
            _hud_tooltip_clamp(center_x, 220, config.screen_width - 220),
            max(120, y - 78),
        )

init -19 python:
    if "hud_disabled_npc_tooltips" not in config.overlay_screens:
        config.overlay_screens.append("hud_disabled_npc_tooltips")

style hud_tooltip_passthrough_button:
    background None
    hover_background None
    selected_background None
    selected_hover_background None
    insensitive_background None

# Insensitive Ren'Py buttons do not take focus, so unavailable NPC actions need
# a transparent focusable overlay that exposes only their reason tooltip.
screen hud_disabled_npc_tooltips():
    zorder 11

    if renpy.get_screen("game_hud") is not None:
        $ _hud_tt_selected_npc = renpy.get_screen_variable("selected_npc", screen="game_hud")
        $ _hud_tt_present = get_present_npcs(state=game_state)

        if _hud_tt_selected_npc and _hud_tt_selected_npc in _hud_tt_present:
            frame:
                background None
                xpos 1450
                ypos 215
                xsize 330
                padding (18, 14)

                vbox:
                    spacing 10
                    text "ДЕЙСТВИЯ: [NPCS[_hud_tt_selected_npc]['name'].upper()]" style "ns_hud_tile_caption" color "#00000000" outlines []

                    vbox:
                        spacing 6
                        for _hud_tt_action in npc_actions(_hud_tt_selected_npc, game_state):
                            $ _hud_tt_checked, _hud_tt_reasons = check_action(_hud_tt_action.id, game_state)

                            if _hud_tt_reasons:
                                button:
                                    style "hud_tooltip_passthrough_button"
                                    xfill True
                                    padding (10, 7)
                                    action NullAction()
                                    tooltip hud_action_hint(_hud_tt_action, _hud_tt_reasons, game_state)

                                    hbox:
                                        spacing 10
                                        yalign 0.5
                                        null width 32 height 32
                                        text hud_action_name(_hud_tt_action) style "ns_text" size 16 color "#00000000" yalign 0.5 xmaximum 250
                            else:
                                null height 46
