init -5 python:
    def phone_test_contract_checks():
        state = create_new_game_state()
        assert phone_contacts(state) == ["masha", "nika"]
        state.relationships["anna"].social = "friend"
        assert "anna" not in phone_contacts(state)
        assert phone_chats(state) == ["nika"]
        assert phone_known_fields("anna", "phone_facts", state) == []
        state.schema_version = 6
        del state.phone_threads
        del state.phone_cooldowns
        history = copy.deepcopy(state.messages)
        ensure_current_schema(state)
        ensure_current_schema(state)
        assert state.schema_version == SCHEMA_VERSION and state.messages == history
        assert phone_calendar_events(2026, 5, state)[15] == ["День рождения: Настя"]
        assert phone_calendar_events(2027, 8, state)[1] == ["День рождения: Маша"]
        assert phone_calendar_events(2026, 11, state)[4] == ["День народного единства"]
        assert len(phone_calendar_events(2027, 1, state)) == 8
        assert calendar.monthrange(2028, 2) == (1, 29)
        assert calendar.monthrange(2026, 2)[1] == 28
        original_date = state.clock.date
        store.ui_phone_month = (2026, 12)
        phone_calendar_shift(1)
        assert store.ui_phone_month == (2027, 1)
        phone_calendar_shift(-1)
        assert store.ui_phone_month == (2026, 12) and state.clock.date == original_date
        backup = copy.deepcopy(CALENDAR_EVENTS)
        try:
            CALENDAR_EVENTS[:] = [dict(id="test_public", date="2026-08-29", title="Тест", public=True), dict(id="test_hidden", date="2026-08-29", title="Скрытый тест", known_flag="test_known"), dict(id="invalid", date="TBD", title="TBD", public=True)]
            assert phone_calendar_events(2026, 8, state)[29] == ["Тест"]
            state.story.flags.add("test_known")
            assert len(phone_calendar_events(2026, 8, state)[29]) == 2
        finally:
            CALENDAR_EVENTS[:] = backup
        qid = "quest_2026_08_29_first_normal_day"
        start_quest(qid, state)
        for status in ("active", "completed", "failed"):
            state.quests[qid].status = status
            assert [i[0] for i in phone_quests(status, state)] == [qid]
            assert not phone_quests("locked", state)
        return True

    def phone_test_message_checks():
        state = create_new_game_state()
        backup = copy.deepcopy(PHONE_MESSAGE_OPTIONS), store.PHONE_CASUAL_COOLDOWN_MINUTES
        try:
            store.PHONE_CASUAL_COOLDOWN_MINUTES = None
            assert not phone_send_option("how_are_you", "masha", state)
            store.PHONE_CASUAL_COOLDOWN_MINUTES = 15  # Test fixture, never production balance.
            PHONE_MESSAGE_OPTIONS["what_are_you_doing"]["responses"] = [
                dict(text="Тестовый ответ в комнате", locations=["loc_apartment_5_room"]),
                dict(text="Тестовый ответ на кухне", locations=["loc_apartment_5_kitchen"])]
            set_schedule_override("masha", "loc_apartment_5_kitchen", state=state)
            assert phone_send_option("what_are_you_doing", "masha", state)
            assert state.messages[-1]["text"] == "Тестовый ответ на кухне"
            assert not phone_send_option("what_are_you_doing", "masha", state)
            PHONE_MESSAGE_OPTIONS["test_story"] = dict(text="Тест сюжетной отправки", kind="story", once=True, set_flags=["test_flag"], contact="masha")
            assert phone_send_option("test_story", "masha", state)
            assert "test_flag" in state.story.flags
            assert not phone_send_option("test_story", "masha", state)
            state.clock.advance(15)
            assert phone_send_option("what_are_you_doing", "masha", state)
            state.clock.advance(15)
            set_schedule_override("masha", "loc_apartment_5_bathroom", state=state)
            assert not phone_send_option("what_are_you_doing", "masha", state)
            assert not phone_send_option("test_story", "anna", state)
        finally:
            PHONE_MESSAGE_OPTIONS.clear()
            PHONE_MESSAGE_OPTIONS.update(backup[0])
            store.PHONE_CASUAL_COOLDOWN_MINUTES = backup[1]
        return True

    def phone_test_visual_prepare(app):
        store.game_state = create_new_game_state()
        start_quest("quest_2026_08_29_first_normal_day")
        _prepare_visual_gameplay_context()
        # on-show initializes home; the test switches after the first interaction.

    def phone_test_visual_select(app):
        qid = "quest_2026_08_29_first_normal_day"
        if app in ("active", "completed", "failed", "quest"):
            game_state.quests[qid].status = "active" if app == "quest" else app
            store.ui_phone_tab = game_state.quests[qid].status
            if app == "quest":
                first = QUESTS[qid]["objectives"][0]["id"]
                game_state.quests[qid].objectives[first].completed = True
            phone_open("quest" if app == "quest" else "quests", qid)
        elif app == "contact": phone_open("contact", "masha")
        elif app in ("chat", "cooldown"):
            phone_open("chat", "nika")
            if app == "cooldown":
                game_state.phone_cooldowns["nika"] = phone_now() + 15
                store.ui_phone_choices_open = True
        elif app == "calendar_tooltip":
            phone_open("calendar")
            CALENDAR_EVENTS.extend([dict(id="test_calendar_%s" % i, date="2026-08-29", title="Тестовое событие с длинной русской подписью %s" % i, public=True) for i in range(5)])
            store.ui_phone_tooltip = (29, phone_calendar_events(2026, 8)[29])
        else: phone_open(app)

testsuite phone_suite:
    testcase contracts:
        assert eval phone_test_contract_checks()
    testcase messages:
        assert eval phone_test_message_checks()
    testcase visual:
        parameter app = ["home", "contacts", "contact", "active", "completed", "failed", "quest", "calendar", "calendar_tooltip", "messages", "chat", "cooldown"]
        $ phone_test_visual_prepare(app)
        run Show("phone_screen")
        pause 0.15
        run Function(phone_test_visual_select, app)
        pause 0.2
        assert screen "phone_screen"
        if eval (app == "home"):
            screenshot "phone_test_overlay.png"
        screenshot ("phone_test_" + app + ".png") crop (714, 60, 492, 960)
        $ phone_back()
        pause 0.1
        $ CALENDAR_EVENTS[:] = [e for e in CALENDAR_EVENTS if not e.get("id", "").startswith("test_calendar_")]
        run Hide("phone_screen")
        assert not screen "phone_screen"
    testcase navigation:
        $ phone_test_visual_prepare("home")
        run Show("phone_screen")
        pause 0.2
        click id "phone_app_contacts"
        assert eval (ui_phone_app == "contacts")
        click "Маша"
        assert eval (ui_phone_app == "contact" and ui_phone_selected == "masha")
        click "Написать"
        assert eval (ui_phone_app == "chat" and "masha" in game_state.phone_threads)
        assert eval (not ui_phone_choices_open)
        click id "phone_message_toggle"
        assert eval ui_phone_choices_open
        click id "phone_message_toggle"
        assert eval (not ui_phone_choices_open)
        click id "phone_nav_Назад"
        assert eval (ui_phone_app == "messages" and not ui_phone_choices_open)
        run Function(phone_open)
        click id "phone_app_settings"
        click "Ночь"
        assert eval (game_state.phone_wallpaper == "night")
        run Function(phone_open)
        screenshot "phone_test_night.png" crop (714, 60, 492, 960)
        click id "phone_nav_Закрыть телефон"
        assert not screen "phone_screen"
    testcase save_load:
        run Start("phone_test_save_fixture")
        pause 0.2
        $ renpy.session["phone_test_slot"] = "phone-test-" + str(__import__("uuid").uuid4())
        $ renpy.save(renpy.session["phone_test_slot"], include_screenshot=False)
        assert eval ("masha" in renpy.get_save_data(renpy.session["phone_test_slot"])["game_state"].phone_threads)
        $ game_state.phone_threads.clear()
        $ game_state.phone_cooldowns.clear()
        run Function(renpy.load, renpy.session["phone_test_slot"])
        pause 0.3
        assert eval ("masha" in renpy.store.game_state.phone_threads)
        assert eval (renpy.store.game_state.phone_cooldowns["masha"] > phone_now())
        assert eval (renpy.store.game_state.messages[0]["from"] == "nika" and not renpy.store.game_state.messages[0]["read"])
        $ renpy.unlink_save(renpy.session["phone_test_slot"])

# Real script checkpoint for save/load; never linked from gameplay.
label phone_test_save_fixture:
    $ game_state = create_new_game_state()
    $ game_state.phone_threads.add("masha")
    $ game_state.phone_cooldowns["masha"] = phone_now() + 15
    $ renpy.block_rollback()
    jump phone_test_save_fixture_wait

label phone_test_save_fixture_wait:
    $ renpy.pause(hard=True)
    jump phone_test_save_fixture_wait
