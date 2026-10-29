# Automated Ren'Py runtime/regression tests for the local self-hosted runner.
# These tests exercise real Ren'Py runtime initialization and selected game flows.

init -10 python:
    import os

    # Deterministic window for the test runner: with an isolated --savedir there is no
    # saved window size, so Ren'Py would fit the window to the monitor and screenshot
    # crops written for a 1920x1080 drawable would fall outside the surface.
    # The runner passes the window size in Windows logical units (1920x1080 / DPI scale).
    _ns_test_window = os.environ.get("NASTYA_RENPY_TEST_WINDOW_SIZE", "")
    if _ns_test_window:
        try:
            _ns_w, _ns_h = [int(_v) for _v in _ns_test_window.lower().split("x")]
            # Same effect as a window size saved by the player, but only inside the
            # runner's temporary --savedir (the real persistent is never used).
            renpy.game.preferences.fullscreen = False
            renpy.game.preferences.physical_size = (_ns_w, _ns_h)
        except Exception:
            pass

init -5 python:
    import os

    _test.timeout = 10.0
    _test.maximum_framerate = True
    _test.screenshot_directory = os.environ.get(
        "NASTYA_RENPY_SCREENSHOT_DIR",
        os.path.join(config.gamedir, "tests", "screenshots", "runtime"),
    )
    os.makedirs(_test.screenshot_directory, exist_ok=True)

    def _prepare_visual_gameplay_context():
        renpy.hide_screen("main_menu")
        renpy.hide_screen("choice")
        renpy.hide_screen("quick_menu")
        renpy.scene()
        renpy.show("ns_test_first_day_background", what=Solid("#766150"))


testsuite nastya_runtime:

    testcase new_game_state_smoke:
        description "New game state has canonical relationship states and core registries loaded."
        $ renpy.store.game_state = create_new_game_state()
        assert eval (renpy.store.game_state.location_id == "loc_apartment_5_room")
        assert eval ("action_unpack_luggage" in ACTIONS)
        assert eval ("loc_apartment_5_room" in LOCATIONS)
        assert eval (get_social_state("masha", renpy.store.game_state) == "friend")
        assert eval (get_intimacy_state("masha", renpy.store.game_state) == "none")
        assert eval (get_social_state("nika", renpy.store.game_state) == "neutral")
        assert eval (renpy.is_in_test())

    testcase apartment_exit_routes_follow_map:
        description "Hallway exposes the canonical exits and preserves the one-way fast route to the residential district."
        $ state = create_new_game_state()
        $ moved, reason = move_to("loc_apartment_5_hallway", state)
        assert eval (moved and state.location_id == "loc_apartment_5_hallway")
        assert eval ({"loc_entrance_1_floor_3", "loc_building_yard", "loc_residential_district_main"}.issubset(set(LOCATIONS[state.location_id]["transitions"])))
        $ moved, reason = move_to("loc_residential_district_main", state)
        assert eval (moved and state.location_id == "loc_residential_district_main")
        $ moved_back_directly, reason = move_to("loc_apartment_5_hallway", state)
        assert eval (not moved_back_directly)
        $ moved, reason = move_to("loc_building_yard", state)
        assert eval (moved and state.location_id == "loc_building_yard")
        $ moved, reason = move_to("loc_apartment_5_hallway", state)
        assert eval (moved and state.location_id == "loc_apartment_5_hallway")
        $ moved, reason = move_to("loc_entrance_1_floor_3", state)
        assert eval (moved and state.location_id == "loc_entrance_1_floor_3")
        $ moved, reason = move_to("loc_apartment_5_hallway", state)
        assert eval (moved and state.location_id == "loc_apartment_5_hallway")

    testcase masha_has_friendship_route_without_romance:
        description "Masha starts as Nastya's friend and has no romantic route."
        $ state = create_new_game_state()
        assert eval (state.relationships["masha"].social == "friend")
        assert eval (not NPCS["masha"].get("romantic_route_allowed", False))
        assert eval (not set_intimacy_state("masha", "romantic", "runtime-test", state))
        assert eval (state.relationships["masha"].intimacy == "none")

    testcase masha_friendship_sexual_route:
        description "Masha's friendship-sexual route: she starts as a friend, sexual intimacy can be set while staying friends, romance stays blocked."
        $ state = create_new_game_state()
        assert eval (state.relationships["masha"].social == "friend")
        assert eval (state.relationships["masha"].intimacy == "none")
        assert eval (NPCS["masha"].get("sexual_route_allowed", False))
        assert eval (sexual_interaction_allowed("masha"))
        $ became_sexual = set_intimacy_state("masha", "sexual", "runtime-test", state)
        assert eval (became_sexual)
        assert eval (state.relationships["masha"].intimacy == "sexual")
        assert eval (state.relationships["masha"].social == "friend")
        assert eval (state.story.event_history[-1].type == "relationship_intimacy_changed")
        assert eval (not set_intimacy_state("masha", "romantic", "runtime-test", state))
        assert eval (state.relationships["masha"].intimacy == "sexual")

    testcase relationship_events_are_independent:
        description "Social and intimacy changes are independent and emit distinct reasoned events."
        $ state = create_new_game_state()
        $ social_changed = set_social_state("nika", "friend", "runtime-test", state)
        $ intimacy_changed = set_intimacy_state("nika", "sexual", "runtime-test", state)
        assert eval (social_changed and intimacy_changed)
        assert eval (state.relationships["nika"].social == "friend")
        assert eval (state.relationships["nika"].intimacy == "sexual")
        assert eval (state.story.event_history[-2].type == "relationship_social_changed")
        assert eval (state.story.event_history[-2].data["reason"] == "runtime-test")
        assert eval (state.story.event_history[-1].type == "relationship_intimacy_changed")
        assert eval (state.story.event_history[-1].data["reason"] == "runtime-test")

    testcase npc_registry_has_no_kinship_mechanic:
        description "Relatives mechanic is removed: NPC definitions carry no kinship and the sexual route depends only on canon flags."
        assert eval (not any("kinship" in npc for npc in NPCS.values()))
        assert eval (sexual_interaction_allowed("masha") == bool(NPCS["masha"].get("sexual_route_allowed", False)))
        assert eval (sexual_interaction_allowed("nika") == bool(NPCS["nika"].get("sexual_route_allowed", False)))
        assert eval (not sexual_interaction_allowed("missing_npc"))
        assert eval (relationship_hud_label("masha", create_new_game_state()) == "Дружеские")

    testcase hud_renders:
        description "The gameplay HUD can be rendered in the real first-day gameplay background context and captured for visual review."
        $ renpy.store.game_state = create_new_game_state()
        $ _prepare_visual_gameplay_context()
        pause 1.0
        run Show("game_hud")
        pause 1.0
        assert screen "game_hud" timeout 5.0
        screenshot "01_hud_start_room.png"
        run Hide("game_hud")
        pause 1.0

    testcase profile_screen_renders:
        description "Nastya profile screen can be rendered in the real first-day gameplay background context and captured for visual review."
        $ renpy.store.game_state = create_new_game_state()
        $ _prepare_visual_gameplay_context()
        pause 1.0
        run Show("game_hud")
        pause 1.0
        assert screen "game_hud" timeout 5.0
        run Show("profile_screen")
        pause 1.0
        assert screen "profile_screen" timeout 5.0
        screenshot "02_profile_nastya.png"
        run Hide("profile_screen")
        pause 1.0
        run Hide("game_hud")
        pause 1.0

    testcase unpack_luggage_deferred_flow:
        description "Unpacking luggage starts as a deferred action and completion records the one-shot state."
        $ state = create_new_game_state()
        $ result = execute_action("action_unpack_luggage", state)
        assert eval (result.success and result.deferred)
        assert eval (state.story.pending_action == "action_unpack_luggage")
        assert eval (state.story.pending_scene == "scene_2026_08_29_unpack_luggage")
        $ completed = complete_deferred_action("action_unpack_luggage", state)
        assert eval (completed.success)
        assert eval (LUGGAGE_UNPACKED_FLAG in state.story.flags)
        assert eval (UNPACK_LUGGAGE_SCENE_FLAG in state.story.flags)
        assert eval (state.story.pending_action is None)

    testcase unpack_luggage_visual_states:
        description "Capture room HUD before and after real luggage completion flow."
        $ renpy.store.game_state = create_new_game_state()
        $ _prepare_visual_gameplay_context()
        pause 1.0
        run Show("game_hud")
        pause 1.0
        assert screen "game_hud" timeout 5.0
        screenshot "03_luggage_before.png"
        run Hide("game_hud")
        pause 1.0
        $ result = execute_action("action_unpack_luggage", renpy.store.game_state)
        assert eval (result.success and result.deferred)
        $ completed = complete_deferred_action("action_unpack_luggage", renpy.store.game_state)
        assert eval (completed.success)
        run Show("game_hud")
        pause 1.0
        assert screen "game_hud" timeout 5.0
        screenshot "04_luggage_after.png"
        run Hide("game_hud")
        pause 1.0

    testcase unpack_luggage_action_disappears_after_completion:
        description "Completed one-shot luggage action disappears while unavailable unfinished actions remain visible."
        $ state = create_new_game_state()
        $ state.clock.hour = 11
        assert eval (any(action.id == "action_unpack_luggage" for action in location_actions(state)))
        $ state.clock.hour = 8
        $ result = execute_action("action_unpack_luggage", state)
        assert eval (result.success and result.deferred)
        $ completed = complete_deferred_action("action_unpack_luggage", state)
        assert eval (completed.success)
        assert eval (not any(action.id == "action_unpack_luggage" for action in location_actions(state)))

# Every selected suite/testcase must exit, not just nastya_runtime.
# Ren'Py attaches all top-level suites to this root.
testsuite global:
    teardown:
        exit
