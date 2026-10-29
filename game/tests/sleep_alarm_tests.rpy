init -5 python:
    def sleep_alarm_contract_tests():
        state = create_new_game_state()
        state.location_id = "loc_apartment_5_room"
        state.clock.date = datetime.date(2026, 8, 30)
        assert not execute_action("action_sleep", state).success
        assert check_action("action_sleep", state)[1][0] == "Спать пока не хочется"

        state.clock.hour, state.clock.minute = 23, 0
        state.player.energy = 2
        set_alarm_time_minutes(5 * 60 + 30, state)
        set_alarm_enabled(True, state)
        result = execute_action("action_sleep", state)
        assert result.success and result.duration_minutes == 390
        assert state.clock.date == datetime.date(2026, 8, 31) and state.clock.total_minutes == 5 * 60 + 30
        assert state.player.energy == 8 and not state.alarm.enabled

        state.clock.hour, state.clock.minute = 22, 0
        state.player.energy = 4
        set_alarm_time_minutes(8 * 60, state)
        set_alarm_enabled(True, state)
        result = execute_action("action_sleep", state)
        assert result.success and result.duration_minutes == 360
        assert state.clock.total_minutes == 4 * 60 and state.player.energy == 10
        assert not state.alarm.enabled
        return True

    def sleep_alarm_migration_and_time_tests():
        legacy = create_new_game_state()
        legacy.schema_version = 10
        del legacy.alarm
        del legacy.awake_energy_minutes
        ensure_current_schema(legacy)
        assert legacy.schema_version == SCHEMA_VERSION
        assert legacy.alarm.time_minutes is None and not legacy.alarm.enabled
        assert legacy.awake_energy_minutes == 0

        expected = {
            "action_look_in_mirror": 5,
            "action_unpack_luggage": 45,
            "action_rest_lie_down": 60,
            "action_watch_tv": 60,
            "action_take_bath": 45,
            "action_toilet": 5,
            "action_shave_legs": 10,
            "action_shave_pubic": 15,
            "action_admire_view": 10,
        }
        assert all(ACTIONS[action_id].duration_minutes == minutes for action_id, minutes in expected.items())

        state = create_new_game_state()
        state.location_id = "loc_shop_hall"
        before = state.clock.total_minutes
        assert fulfill_shop_purchase("loc_shop", "food_kit_breakfast", state)[0]
        assert state.clock.total_minutes == before + 15
        state.location_id = "loc_cafe_hall"
        before = state.clock.total_minutes
        assert fulfill_shop_purchase("loc_cafe", "cafe_chicken_pasta", state)[0]
        assert state.clock.total_minutes == before + 30
        inventory_add("water", state=state)
        before = state.clock.total_minutes
        assert inventory_use("water", state)
        assert state.clock.total_minutes == before + 5
        return True

    def awake_energy_time_tests():
        state = create_new_game_state()
        for unused in range(2):
            assert execute_action("action_wait", state).success
        assert state.player.energy == 10 and state.awake_energy_minutes == 120
        assert execute_action("action_wait", state).success
        assert state.player.energy == 9 and state.awake_energy_minutes == 0
        advance_time(360, "test", state)
        assert state.player.energy == 7 and state.awake_energy_minutes == 0
        state.player.energy = 4
        advance_time(90, "action_sleep", state)
        assert state.player.energy == 4 and state.awake_energy_minutes == 0
        return True

    def admissions_conversation_tests():
        state = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day", state)
        quest = state.quests["quest_2026_08_29_first_normal_day"]
        quest.objectives["remind_masha_school_documents"].completed = True
        quest.objectives["submit_university_documents"].completed = True
        state.clock.hour = 14
        assert admissions_conversation_available(state)
        assert "action_talk_masha_admissions" in [action.id for action in npc_actions("masha", state)]
        result = execute_action("action_talk_masha_admissions", state)
        assert result.success and result.deferred
        assert complete_deferred_action("action_talk_masha_admissions", state).duration_minutes == 15
        assert not admissions_conversation_available(state)
        assert "action_talk_masha_admissions" not in [action.id for action in npc_actions("masha", state)]

        state = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day", state)
        quest = state.quests["quest_2026_08_29_first_normal_day"]
        quest.objectives["remind_masha_school_documents"].completed = True
        quest.objectives["submit_university_documents"].completed = True
        state.clock.date = datetime.date(2026, 9, 1)
        assert not admissions_conversation_available(state)
        return True

testsuite sleep_alarm:
    testcase contract:
        assert eval sleep_alarm_contract_tests()

    testcase migration_and_durations:
        assert eval sleep_alarm_migration_and_time_tests()

    testcase awake_energy:
        assert eval awake_energy_time_tests()

    testcase admissions_conversation:
        assert eval admissions_conversation_tests()

    testcase alarm_visual:
        $ game_state = create_new_game_state()
        $ set_alarm_time_minutes(7 * 60 + 45, game_state)
        $ set_alarm_enabled(True, game_state)
        run Show("phone_screen")
        pause 0.2
        click id "phone_app_alarm"
        pause 0.3
        assert screen "phone_screen"
        assert eval (ui_phone_app == "alarm")
        screenshot "sleep_alarm_full.png"
        screenshot "sleep_alarm_phone.png" crop (714, 60, 492, 960)
        run Hide("phone_screen")
