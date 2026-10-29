init -5 python:
    def first_day_core_checks():
        state = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day", state)

        reminder = execute_action("action_remind_masha_school_documents", state)
        assert reminder.success and reminder.deferred
        assert complete_deferred_action("action_remind_masha_school_documents", state).success
        assert objective_complete("quest_2026_08_29_first_normal_day", "remind_masha_school_documents", state)
        assert "action_remind_masha_school_documents" not in [action.id for action in npc_actions("masha", state)]
        assert not execute_action("action_remind_masha_school_documents", state).success

        state.location_id = "loc_medical_institute_admissions"
        state.clock.hour, state.clock.minute = 13, 0
        documents = execute_action("action_submit_university_documents", state)
        assert documents.success and documents.deferred
        assert complete_deferred_action("action_submit_university_documents", state).success
        assert state.clock.total_minutes == 13 * 60 + 30
        assert "university_documents_submitted" in state.story.flags
        assert "phone_app:university" in state.story.flags
        assert state.quests["quest_2026_08_29_first_normal_day"].status == "completed"

        state.location_id = "loc_shop_hall"
        shop = execute_action("action_ask_shop_job", state)
        assert shop.success and shop.deferred
        assert complete_deferred_action("action_ask_shop_job", state).success
        assert objective_complete("quest_2026_08_29_first_normal_day", "find_job_information", state)
        assert not execute_action("action_ask_shop_job", state).success

        state.clock.hour, state.clock.minute = 19, 0
        state.location_id = "loc_entrance_1_floor_3"
        assert location_access_reason("loc_apartment_6_hallway", state, 1) is None
        assert move_to("loc_apartment_6_hallway", state)[0]
        assert "nika" in get_present_npcs(state=state)
        visit = execute_action("action_visit_nika", state)
        assert visit.success and visit.deferred
        assert complete_deferred_action("action_visit_nika", state).success
        assert objective_complete("quest_2026_08_29_first_normal_day", "visit_nika", state)

        state.location_id = "loc_apartment_5_room"
        conversation = execute_action("action_talk_masha_admissions", state)
        assert conversation.success and conversation.deferred
        assert complete_deferred_action("action_talk_masha_admissions", state).success
        assert "masha_admissions_conversation_seen" in state.story.flags
        assert "action_talk_masha_admissions" not in [action.id for action in npc_actions("masha", state)]
        state.clock.hour, state.clock.minute = 22, 30
        state.player.energy = 1; state.player.arousal = 0
        slept = execute_action("action_sleep", state)
        assert slept.success and slept.duration_minutes == 540
        assert state.clock.date == datetime.date(2026, 8, 30) and state.clock.total_minutes == 7 * 60 + 30
        assert state.player.energy == state.player.max_energy and state.player.arousal == 0
        return True

    def first_day_deadline_checks():
        state = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day", state)
        state.location_id = "loc_medical_institute_admissions"
        state.clock.hour, state.clock.minute = 17, 30
        assert first_day_admissions_open_for_action(state)
        state.clock.minute = 31
        assert not first_day_admissions_open_for_action(state)

        state.location_id = "loc_apartment_5_room"
        state.clock.hour, state.clock.minute = 16, 30
        travel = first_day_minutes_to_admissions(state)
        assert travel is not None and travel > 0
        state.clock.hour, state.clock.minute = divmod(18 * 60 - travel - 30, 60)
        assert not first_day_deadline_blocks(0, state)
        assert first_day_deadline_blocks(1, state)
        assert queue_first_day_deadline_scene(state)
        assert state.story.pending_scene == "scene_2026_08_29_forced_university_departure"
        assert force_first_day_university_departure(state)
        assert state.location_id == "loc_medical_institute_admissions"
        assert state.clock.total_minutes + 30 == 18 * 60

        blocked = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day", blocked)
        blocked.location_id = "loc_apartment_5_room"
        assert not execute_action("action_sleep", blocked).success
        return True

    def first_day_end_to_end_checks():
        state = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day", state)
        assert execute_action("action_remind_masha_school_documents", state).deferred
        assert complete_deferred_action("action_remind_masha_school_documents", state).success
        for unused in range(5): assert execute_action("action_wait", state).success
        assert move_to("loc_apartment_5_hallway", state)[0]
        assert move_to("loc_residential_district_main", state)[0]
        assert move_to("loc_medical_institute_area", state, "bus")[0]
        assert move_to("loc_medical_institute_building_floor_1", state)[0]
        assert move_to("loc_medical_institute_admissions", state)[0]
        assert execute_action("action_submit_university_documents", state).deferred
        assert complete_deferred_action("action_submit_university_documents", state).success
        assert move_to("loc_medical_institute_building_floor_1", state)[0]
        assert move_to("loc_medical_institute_area", state)[0]
        assert move_to("loc_residential_district_main", state, "bus")[0]
        assert move_to("loc_shop_hall", state)[0]
        assert execute_action("action_ask_shop_job", state).deferred
        assert complete_deferred_action("action_ask_shop_job", state).success
        assert move_to("loc_residential_district_main", state)[0]
        for unused in range(4): assert execute_action("action_wait", state).success
        assert 19 * 60 <= state.clock.total_minutes < 22 * 60
        assert move_to("loc_building_yard", state)[0]
        assert move_to("loc_apartment_5_hallway", state)[0]
        assert move_to("loc_entrance_1_floor_3", state)[0]
        assert move_to("loc_apartment_6_hallway", state)[0]
        assert execute_action("action_visit_nika", state).deferred
        assert complete_deferred_action("action_visit_nika", state).success
        assert move_to("loc_entrance_1_floor_3", state)[0]
        assert move_to("loc_apartment_5_hallway", state)[0]
        assert move_to("loc_apartment_5_room", state)[0]
        assert execute_action("action_talk_masha_admissions", state).deferred
        assert complete_deferred_action("action_talk_masha_admissions", state).success
        state.player.energy = 4
        assert execute_action("action_sleep", state).success
        assert state.clock.date == datetime.date(2026, 8, 30)
        assert first_day_required_objectives_complete(state)
        assert objective_complete("quest_2026_08_29_first_normal_day", "find_job_information", state)
        assert objective_complete("quest_2026_08_29_first_normal_day", "visit_nika", state)
        return True

testsuite first_day:
    testcase core_flow:
        assert eval first_day_core_checks()

    testcase deadline:
        assert eval first_day_deadline_checks()

    testcase end_to_end:
        assert eval first_day_end_to_end_checks()

    testcase university_phone:
        $ renpy.store.game_state = create_new_game_state()
        $ game_state.story.flags.update(("university_documents_submitted", "phone_app:university"))
        $ _prepare_visual_gameplay_context()
        run Show("phone_screen")
        pause 0.5
        assert screen "phone_screen"
        click id "phone_app_university"
        pause 0.5
        assert eval (ui_phone_app == "university")
        screenshot "first_day_university_phone.png"
        run Hide("phone_screen")
