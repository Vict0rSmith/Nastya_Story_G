testsuite dialogue_layout:
    testcase dialogue_replaces_controls:
        $ renpy.store.game_state = create_new_game_state()
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        pause 0.2
        assert eval (renpy.get_widget("game_hud", "world_navigation") is not None)
        run Show("say", who="Настя", what="Техническая проверка диалоговой панели.")
        pause 0.2
        assert eval (renpy.get_widget("game_hud", "world_navigation") is None)
        assert eval (renpy.get_widget("game_hud", "world_actions") is None)
        screenshot "dialogue_layout_character.png"
        run Hide("say")
        run Show("say", who=None, what="Техническая проверка авторского текста без пустого места под портрет.")
        pause 0.2
        screenshot "dialogue_layout_narration.png"
        run Hide("say")
        pause 0.2
        assert eval (renpy.get_widget("game_hud", "world_navigation") is not None)
        screenshot "dialogue_layout_free_roam.png"
        $ renpy.notify("Техническая проверка уведомления")
        pause 0.2
        screenshot "dialogue_layout_notify.png"
        run Hide("game_hud")
