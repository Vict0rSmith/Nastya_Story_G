init -5 python:
    def ui_review_visual_prepare():
        store.game_state = create_new_game_state()
        store.game_state.location_id = "loc_apartment_5_room"
        start_quest("quest_2026_08_29_first_normal_day", store.game_state)
        _prepare_visual_gameplay_context()

    def ui_review_select_calendar_event():
        store.ui_phone_month = (2026, 8)
        store.ui_phone_tooltip = (1, phone_calendar_events(2026, 8)[1])
        renpy.restart_interaction()

testsuite ui_review:
    testcase one_click_wait_and_hud:
        $ ui_review_visual_prepare()
        $ game_state.player.energy = 1
        $ before = game_state.clock.total_minutes
        run Show("game_hud")
        pause 0.2
        click id "hud_action_action_wait"
        pause 3.5
        assert eval (game_state.clock.total_minutes == before + 60)
        assert screen "game_hud"
        screenshot "ui_review_hud_after_wait.png"
        run Hide("game_hud")

    testcase npc_compact_actions:
        $ ui_review_visual_prepare()
        run Show("game_hud")
        pause 0.2
        click id "hud_npc_masha"
        pause 0.2
        assert screen "game_hud"
        screenshot "ui_review_npc_actions.png"
        run Hide("game_hud")

    testcase phone_quest_and_calendar:
        $ ui_review_visual_prepare()
        run Show("phone_screen")
        pause 0.2
        run Function(phone_open, "quest", "quest_2026_08_29_first_normal_day")
        pause 0.2
        screenshot "ui_review_phone_quest.png" crop (714, 60, 492, 960)
        run Function(phone_open, "calendar")
        run Function(ui_review_select_calendar_event)
        pause 0.2
        assert eval (ui_phone_tooltip and ui_phone_tooltip[0] == 1 and ui_phone_tooltip[1])
        screenshot "ui_review_phone_calendar_selected.png" crop (714, 60, 492, 960)
        run Hide("phone_screen")

    testcase system_menus:
        run Show("save")
        pause 0.15
        screenshot "ui_review_save.png"
        run Show("load")
        pause 0.15
        screenshot "ui_review_load.png"
        run Show("preferences")
        pause 0.15
        screenshot "ui_review_preferences.png"
        run Show("history")
        pause 0.15
        screenshot "ui_review_history.png"
        run Show("about")
        pause 0.15
        screenshot "ui_review_about.png"
        run Show("help")
        pause 0.15
        screenshot "ui_review_help.png"
        run Hide("help")

    testcase quit_confirm_and_quick_menu:
        run Show("confirm", message="Are you sure you want to quit?", yes_action=Hide("confirm"), no_action=Hide("confirm"))
        pause 0.2
        assert screen "confirm"
        screenshot "ui_review_confirm.png"
        run Hide("confirm")
        $ ui_review_visual_prepare()
        $ store.quick_menu = True
        run Show("game_hud")
        $ renpy.show_screen("quick_menu", _layer="overlay")
        pause 0.2
        assert eval quick_menu
        assert eval (renpy.get_screen("quick_menu", layer="overlay") is not None)
        assert eval (renpy.get_widget("quick_menu", "quick_menu_bar", layer="overlay") is not None)
        screenshot "ui_review_quick_menu.png"
        $ renpy.hide_screen("quick_menu", layer="overlay")
        run Hide("game_hud")
