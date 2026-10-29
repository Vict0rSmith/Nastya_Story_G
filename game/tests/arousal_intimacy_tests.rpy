init 100 python:
    def arousal_test_arousal_decay_tests():
        state = create_new_game_state(); state.player.arousal = 6
        advance_time(59, "test", state); assert state.player.arousal == 6
        advance_time(1, "test", state); assert state.player.arousal == 5
        change_arousal(20, state); assert state.player.arousal == 10
        change_arousal(-20, state); assert state.player.arousal == 0
        assert [arousal_label(value) for value in (0, 1, 4, 7, 10)] == ["Спокойна", "Слегка возбуждена", "Возбуждена", "Сильно возбуждена", "Перевозбуждена"]
        legacy = create_new_game_state(); legacy.schema_version = 8; legacy.player.arousal = 3; del legacy.inventory.body_runtime
        for attribute in ("arousal_decay_minutes", "passive_body_minutes", "arousal_source_ready_at"): delattr(legacy, attribute)
        ensure_current_schema(legacy); assert legacy.schema_version == SCHEMA_VERSION and legacy.player.arousal == 8 and legacy.inventory.body_runtime == {}
        return True

    def arousal_test_body_compatibility_tests():
        state = create_new_game_state(); state.player.openness.rank = 3
        for item_id in ("remote_toy", "anal_plug", "tail_plug"): inventory_add(item_id, state=state)
        assert set_body_item("remote_toy", True, state)[0]
        assert set_body_item("anal_plug", True, state)[0]
        assert not set_body_item("tail_plug", True, state)[0]
        assert set_body_item("anal_plug", False, state)[0]
        assert not set_body_item("tail_plug", True, state)[0]
        assert wardrobe_unequip("panties", state)
        assert set_body_item("tail_plug", True, state)[0]
        assert not wardrobe_can_equip("white_cotton_panties_1", state=state)[0]
        return True

    def arousal_test_remote_toy_tests():
        state = create_new_game_state(); state.player.openness.rank = 3; inventory_add("remote_toy", state=state); set_body_item("remote_toy", True, state)
        state.player.arousal = 8
        assert set_remote_toy_active(True, state)[0]
        advance_time(60, "test", state); assert state.player.arousal == 10
        advance_time(29, "test", state); assert remote_toy_is_active(state)
        advance_time(1, "test", state); assert state.player.arousal == 0 and not remote_toy_is_active(state)
        assert any(event.type == "auto_orgasm" and event.data["source"] == "remote_toy" for event in state.story.event_history)
        set_remote_toy_active(True, state); advance_time(15, "test", state); set_remote_toy_active(False, state); assert remote_toy_runtime(state)["max_minutes"] == 0
        set_remote_toy_controller("masha", state); set_remote_toy_active(True, state, scripted=True); state.player.arousal = 10
        advance_time(30, "test", state); assert remote_toy_is_active(state)
        return True

    def arousal_test_masturbation_tests():
        state = create_new_game_state(); state.location_id = "loc_apartment_5_bathroom"; state.player.openness.rank = 2; state.player.arousal = 5; state.story.flags.add("masturbation_unlocked")
        result = execute_action("action_masturbate", state=state); assert result.success and result.duration_minutes == 30 and state.player.arousal == 0
        state.player.arousal = 5; inventory_add("bullet_vibrator", state=state)
        result = execute_action("action_masturbate", state=state, item_id="bullet_vibrator"); assert result.success and result.duration_minutes == 20
        return True

    def arousal_test_source_cooldown_tests():
        state = create_new_game_state(); state.location_id = "loc_apartment_5_bathroom"; state.player.openness.rank = 1; inventory_add("adult_magazine", state=state)
        before = state.player.arousal; result = execute_action("action_view_adult_magazine", state=state)
        assert result.success and result.duration_minutes == 20 and state.player.arousal in (before, before + 1)
        assert not execute_action("action_view_adult_magazine", state=state).success
        return True

    def arousal_test_sleep_and_hud_tests():
        state = create_new_game_state(); state.location_id = "loc_apartment_5_room"; state.clock.hour = 23; state.player.energy = 4; state.player.openness.rank = 3; state.player.arousal = 8
        inventory_add("remote_toy", state=state); inventory_add("anal_plug", state=state); set_body_item("remote_toy", True, state); set_body_item("anal_plug", True, state)
        complete_sleep(state, dream_roll=0.0); assert state.player.arousal == 5
        state.wardrobe.equipped["panties"] = None; state.wardrobe.equipped["bottom"] = "casual_skirt"; state.player.arousal = 8
        ids = [entry[0] for entry in status_hud_entries(state)]; assert "arousal_yellow" in ids and "no_panties" in ids
        state.player.arousal = 10; ids = [entry[0] for entry in status_hud_entries(state)]; assert "arousal_red" in ids and "arousal_yellow" not in ids
        return True

    # Former TASK-010 acceptance scenario (sex shop) as a real regression check.
    # The acceptance catalog is registered only inside the test and removed afterwards.
    AROUSAL_TEST_SEX_SHOP_ITEMS = ("anal_beads", "anal_plug", "bullet_vibrator", "dildo", "remote_toy", "soft_handcuffs", "strapon", "tail_plug", "vacuum_stimulator", "vibrator")
    AROUSAL_TEST_TEST_SHOP_CATALOG = "loc_test_sex_shop"

    def arousal_test_sex_shop_state():
        state = create_new_game_state(); state.clock = GameClock(2026, 8, 30, 10, 30)
        state.location_id = "loc_central_shopping_center_floor_1_sex_shop"
        state.player.openness.rank = 3; state.player.arousal = 5; state.wallet.balance = 100000
        state.story.flags.update(("masturbation_unlocked", "university_documents_submitted"))
        return state

    def arousal_test_sex_shop_purchase_tests():
        assert "loc_central_shopping_center_floor_1_sex_shop" in LOCATIONS
        for item_id in AROUSAL_TEST_SEX_SHOP_ITEMS: assert item_id in ITEMS, item_id
        state = arousal_test_sex_shop_state()
        try:
            for item_id in AROUSAL_TEST_SEX_SHOP_ITEMS: register_shop_item(AROUSAL_TEST_TEST_SHOP_CATALOG, item_id, price=100)
            for item_id in AROUSAL_TEST_SEX_SHOP_ITEMS:
                balance = state.wallet.balance
                success, reason = fulfill_shop_purchase(AROUSAL_TEST_TEST_SHOP_CATALOG, item_id, state)
                assert success, (item_id, reason)
                assert inventory_has(item_id, state=state), item_id
                assert state.wallet.balance == balance - 100, item_id
        finally:
            SHOP_CATALOGS.pop(AROUSAL_TEST_TEST_SHOP_CATALOG, None)
        assert AROUSAL_TEST_TEST_SHOP_CATALOG not in SHOP_CATALOGS
        assert not fulfill_shop_purchase(AROUSAL_TEST_TEST_SHOP_CATALOG, "dildo", state)[0]
        assert set_body_item("anal_plug", True, state)[0]
        return True

    # Former "next day after university enrollment" checkpoint as a real regression check.
    def arousal_test_university_next_day_state():
        state = create_new_game_state(); state.clock = GameClock(2026, 8, 30, 8, 0)
        state.location_id = "loc_apartment_5_room"; state.wallet.balance = 30000
        state.story.flags.update(("university_documents_submitted", "phone_app:university"))
        return state

    def arousal_test_university_next_day_tests():
        state = arousal_test_university_next_day_state()
        assert state.clock.date == datetime.date(2026, 8, 30)
        assert "university" in [app[0] for app in phone_home_apps(state)]
        assert "university" not in [app[0] for app in phone_home_apps(create_new_game_state())]
        assert location_actions(state)
        return True

testsuite arousal_intimacy:
    testcase arousal_decay:
        assert eval (arousal_test_arousal_decay_tests())

    testcase body_compatibility:
        assert eval (arousal_test_body_compatibility_tests())

    testcase remote_toy:
        assert eval (arousal_test_remote_toy_tests())

    testcase masturbation:
        assert eval (arousal_test_masturbation_tests())

    testcase source_cooldown:
        assert eval (arousal_test_source_cooldown_tests())

    testcase sleep_and_hud:
        assert eval (arousal_test_sleep_and_hud_tests())

    testcase sex_shop_purchase:
        assert eval (arousal_test_sex_shop_purchase_tests())

    testcase sex_shop_hud:
        $ renpy.store.game_state = arousal_test_sex_shop_state()
        $ _prepare_visual_gameplay_context()
        pause 0.5
        run Show("game_hud")
        pause 0.5
        assert screen "game_hud" timeout 5.0
        screenshot "arousal_test_sex_shop_hud.png"
        run Hide("game_hud")
        pause 0.5

    testcase university_next_day:
        assert eval (arousal_test_university_next_day_tests())

    testcase university_next_day_phone:
        $ renpy.store.game_state = arousal_test_university_next_day_state()
        $ renpy.store.ui_phone_app = "home"
        $ _prepare_visual_gameplay_context()
        pause 0.5
        run Show("game_hud")
        pause 0.5
        assert screen "game_hud" timeout 5.0
        run Hide("game_hud")
        run Show("phone_screen")
        pause 0.5
        assert screen "phone_screen"
        click id "phone_app_university"
        pause 0.5
        assert eval (ui_phone_app == "university")
        screenshot "arousal_test_university_next_day_phone.png"
        run Hide("phone_screen")
        pause 0.5
