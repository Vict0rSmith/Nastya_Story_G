init -5 python:
    def run_navigation_tests():
        # Exercise every compiled edge through the real movement API.
        for source, node in LOCATIONS.items():
            for target, duration in node["transitions"].items():
                state = create_new_game_state()
                state.story.flags.add("university_documents_submitted")
                state.location_id = source
                before = state.clock.total_minutes
                expected = LOCATIONS[target]["access_state"] == "open" or target == "loc_building_roof"
                moved, reason = move_to(target, state)
                assert moved == expected, (source, target, reason)
                assert state.location_id == (target if moved else source)
                assert state.clock.total_minutes == before + (duration if moved else 0)
        state = create_new_game_state()
        state.story.flags.add("university_documents_submitted")
        assert move_to("loc_apartment_5_hallway", state)[0]
        assert LOCATIONS["loc_apartment_5_room"]["transitions"]["loc_apartment_5_hallway"] == 1
        assert move_to("loc_residential_district_main", state)[0]
        before = state.clock.total_minutes
        assert move_to("loc_medical_institute_area", state, "bus")[0]
        assert state.clock.total_minutes == before + 20
        assert not move_to("route_bus_stop_residential", state)[0]
        assert move_to("loc_residential_district_main", state, "bus")[0]
        assert move_to("loc_central_street", state, "bus")[0]
        state.location_id = "loc_entrance_1_floor_1"
        assert not move_to("loc_building_basement", state)[0]
        state.inventory.quantities["basement_key"] = 1
        assert move_to("loc_building_basement", state)[0]
        assert move_to("loc_entrance_1_floor_1", state)[0]
        state.location_id = "loc_medical_institute_building_floor_1"
        state.clock.hour, state.clock.minute = 12, 58
        assert not move_to("loc_medical_institute_admissions", state)[0]
        state.clock.minute = 59
        assert move_to("loc_medical_institute_admissions", state)[0]
        assert move_to("loc_medical_institute_building_floor_1", state)[0]
        state.clock.hour, state.clock.minute = 17, 59
        assert not move_to("loc_medical_institute_admissions", state)[0]
        assert run_domain_self_tests()

    def run_hud_grouping_tests():
        for source, node in LOCATIONS.items():
            state = create_new_game_state()
            state.location_id = source
            entries = hud_navigation_entries(state)
            represented = []
            for kind, value in entries:
                if kind == "location": represented.append(value)
                elif kind == "stairs": represented.extend(target for target in value.values() if target)
            assert set(represented) == set(node["transitions"]), source
            assert len(represented) == len(set(represented)), source
            assert sum(kind == "stairs" for kind, value in entries) <= 1
            width, icon = hud_row_metrics(len(entries))
            assert width * len(entries) + 6 * (len(entries) - 1) <= 912
            assert icon == 104, (source, len(entries))

testsuite navigation:
    testcase begin_day_enters_free_roam:
        $ renpy.store.game_state = create_new_game_state()
        run Jump("begin_first_day")
        pause 0.2
        click
        pause 0.2
        click
        pause 0.2
        click
        pause 0.2
        click
        pause 0.2
        click
        pause 0.2
        click
        pause 0.2
        click
        pause 0.2
        assert screen "game_hud"
        assert not screen "say"
        assert eval (game_state.location_id == "loc_apartment_5_room")

    testcase all_routes:
        $ run_navigation_tests()

    testcase bus_interface:
        $ renpy.store.game_state = create_new_game_state()
        $ game_state.location_id = "loc_residential_district_main"
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        run Show("transport_screen")
        pause 0.3
        assert screen "transport_screen"
        click "РАЙОН МЕДИЦИНСКОГО ИНСТИТУТА — 20 мин."
        assert eval (game_state.location_id == "loc_medical_institute_area")
        assert eval (game_state.clock.total_minutes == 500)
        run Hide("transport_screen")
        run Hide("game_hud")

    testcase hud_click_moves:
        $ renpy.store.game_state = create_new_game_state()
        $ game_state.location_id = "loc_residential_district_main"
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        pause 0.2
        $ moved, reason = move_to("loc_building_yard", game_state)
        assert eval (game_state.location_id == "loc_building_yard")
        assert eval (game_state.clock.total_minutes == 485)
        run Hide("game_hud")

    testcase floor_button_grouping:
        $ run_hud_grouping_tests()

    testcase entrance_navigation_order_and_labels:
        $ state = create_new_game_state()
        $ state.location_id = "loc_entrance_1_floor_3"
        $ entries = hud_navigation_entries(state)
        assert eval ([kind for kind, value in entries] == ["stairs", "location", "location"])
        assert eval ([value for kind, value in entries if kind == "location"] == ["loc_apartment_5_hallway", "loc_apartment_6_hallway"])
        assert eval (hud_navigation_label("loc_apartment_5_hallway", state) == "Моя квартира")
        assert eval (hud_navigation_hint("loc_apartment_5_hallway", state).startswith("Квартира Насти и Маши · "))
        assert eval (hud_navigation_label("loc_apartment_6_hallway", state) == "Квартира Ники")
        $ state.location_id = "loc_entrance_1_floor_4"
        $ entries = hud_navigation_entries(state)
        assert eval ([value for kind, value in entries if kind == "location"] == ["loc_apartment_7_hallway", "loc_apartment_8"])
        assert eval (location_tile_name("loc_apartment_7_hallway") == "КВАРТИРА АННЫ")
        assert eval (location_tile_name("loc_apartment_8") == "КВАРТИРА №8")

    testcase residential_short_labels:
        $ state = create_new_game_state()
        $ state.location_id = "loc_residential_district_main"
        assert eval (hud_navigation_label("loc_cafe_hall", state) == "Кафе")
        assert eval (hud_navigation_label("loc_masha_school_entrance", state) == "Колледж")

    testcase apartment_labels_and_order:
        $ state = create_new_game_state()
        $ state.location_id = "loc_apartment_5_hallway"
        $ entries = hud_navigation_entries(state)
        assert eval ([value for kind, value in entries if kind == "location"][:3] == ["loc_apartment_5_room", "loc_apartment_5_kitchen", "loc_apartment_5_bathroom"])
        assert eval (hud_room_label("loc_apartment_5_room", state) == "Комната")
        assert eval (hud_room_label("loc_apartment_5_kitchen", state) == "Кухня")
        assert eval (hud_room_label("loc_apartment_5_bathroom", state) == "Ванная")
        assert eval (hud_room_label("loc_apartment_5_hallway", state) == "Прихожая")
        assert eval (hud_room_label("loc_entrance_1_floor_3", state) == "Выйти в подъезд")
        assert eval (hud_room_label("loc_building_yard", state) == "Выйти на улицу")

    testcase floor_button_clicks:
        $ renpy.store.game_state = create_new_game_state()
        $ game_state.location_id = "loc_entrance_1_floor_3"
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        pause 0.2
        # Both halves share a circle; the transparent top-left corner is not clickable.
        click pos (166, 882)
        assert eval (game_state.location_id == "loc_entrance_1_floor_3")
        click pos (86, 906)
        assert eval (game_state.location_id == "loc_entrance_1_floor_4")
        assert eval (game_state.clock.total_minutes == 481)
        click pos (86, 958)
        assert eval (game_state.location_id == "loc_entrance_1_floor_3")
        assert eval (game_state.clock.total_minutes == 482)
        run Hide("game_hud")

    testcase floor_button_disabled_half:
        $ renpy.store.game_state = create_new_game_state()
        $ game_state.location_id = "loc_entrance_1_floor_1"
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        pause 0.2
        click pos (86, 958)
        assert eval (game_state.location_id == "loc_entrance_1_floor_1")
        assert eval (game_state.clock.total_minutes == 480)
        click pos (86, 906)
        assert eval (game_state.location_id == "loc_entrance_1_floor_2")
        run Hide("game_hud")
