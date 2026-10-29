default ui_phone_app = "home"
default ui_phone_selected = None
default ui_phone_month = (2026, 8)
default ui_phone_tab = "active"
default ui_phone_tooltip = None
default ui_phone_choices_open = False

init -35 python:
    NS_COLOR.update(phone_surface="#1D2330F2", phone_weekend="#D87468", phone_event="#4FA7A0", phone_today="#E4A63A")
    PHONE_APP_TITLES = {"home": "", "contacts": "Контакты", "contact": "Контакт", "quests": "Задания", "quest": "Задание", "calendar": "Календарь", "messages": "Сообщения", "chat": "Переписка", "university": "Институт", "bank": "Банк", "alarm": "Будильник", "settings": "Настройки"}
    PHONE_APPS = (("contacts", "Контакты", "coral"), ("quests", "Задания", "violet"), ("calendar", "Календарь", "teal"), ("messages", "Сообщения", "green"), ("bank", "Банк", "amber"), ("alarm", "Будильник", "coral"), ("gallery", "Галерея", "neutral_700"), ("map", "Карта", "neutral_700"), ("settings", "Настройки", "neutral_700"))

    def phone_home_apps(state=None):
        state = _state(state)
        apps = list(PHONE_APPS)
        if "phone_app:university" in state.story.flags:
            apps[7] = ("university", "Институт", "teal")
        return apps

style phone_text is ns_text:
    size 20
style phone_small is ns_muted:
    size 16
style phone_heading is ns_title:
    size 25
style phone_row is ns_button:
    xsize 420
    ysize None
    yminimum 54
    padding (16, 14)
    background Frame("ui/phone/glass.svg", 20, 20)
    hover_background Frame("ui/phone/glass_hover.svg", 20, 20)
    insensitive_background Frame("ui/phone/glass.svg", 20, 20)
style phone_row_text is phone_text:
    hover_color NS_COLOR["amber"]
    insensitive_color NS_COLOR["text_disabled"]
    xalign 0.5
    text_align 0.5
style phone_tab is ns_button:
    xsize 138
    ysize 48
    padding (2, 10)
    background Frame("ui/phone/glass.svg", 20, 20)
    hover_background Frame("ui/phone/glass_hover.svg", 20, 20)
    selected_background Frame("ui/phone/accent.svg", 20, 20)
    selected_hover_background Frame("ui/phone/accent.svg", 20, 20)
style phone_tab_text is ns_button_text:
    size 16
    bold True
    xalign 0.5
    text_align 0.5
    selected_color NS_COLOR["neutral_100"]

screen phone_icon(icon, action, label, size=44):
    button:
        id "phone_nav_" + label
        xysize (size, size)
        padding (8, 8)
        background None
        hover_background Solid(NS_COLOR["hud_hover"])
        action action
        tooltip label
        add "ui/phone/" + icon + ".svg" xysize (size-16, size-16)

screen phone_avatar(npc_id, size=52):
    $ portrait = NPCS.get(npc_id, {}).get("portrait")
    fixed:
        xysize (size, size)
        add Transform("ui/phone/tile.svg", matrixcolor=TintMatrix(NS_COLOR["violet"])) xysize (size, size)
        if portrait and renpy.loadable(portrait):
            add portrait xysize (size, size) fit "contain"
        else:
            add "ui/phone/contacts.svg" xysize (int(size*.7), int(size*.7)) align (0.5, 0.5)

screen phone_screen():
    modal True
    zorder 110
    on "show" action Function(phone_open)
    key "game_menu" action Hide("phone_screen")
    button:
        id "phone_overlay"
        background Solid(NS_COLOR["overlay"])
        hover_background Solid(NS_COLOR["overlay"])
        xsize config.screen_width
        ysize config.screen_height
        action Hide("phone_screen")
    fixed:
        align (0.5, 0.5)
        xysize (492, 960)
        add ("ui/phone/shell_night.svg" if game_state.phone_wallpaper == "night" else "ui/phone/shell.svg")
        button:
            xpos 16
            ypos 16
            xysize (460, 928)
            background None
            action NullAction()
        text game_state.clock.display_time xpos 44 ypos 29 style "phone_small"
        add "ui/phone/signal.svg" xpos 415 ypos 30 xysize (22, 22)
        fixed:
            xpos 32
            ypos 68
            xysize (428, 48)
            if ui_phone_app != "home":
                use phone_icon("back", Function(phone_back), "Назад")
            text PHONE_APP_TITLES.get(ui_phone_app, "Приложение") style "phone_heading" align (0.5, 0.5)
            fixed:
                xpos 384
                use phone_icon("close", Hide("phone_screen"), "Закрыть телефон")
        fixed:
            xpos 36
            ypos 126
            xysize (420, 744)
            if ui_phone_app == "home":
                use phone_home
            elif ui_phone_app == "contacts":
                use phone_contacts
            elif ui_phone_app == "contact":
                use phone_contact_card(ui_phone_selected)
            elif ui_phone_app == "quests":
                use phone_quests
            elif ui_phone_app == "quest":
                use phone_quest_card(ui_phone_selected)
            elif ui_phone_app == "calendar":
                use phone_calendar
            elif ui_phone_app == "messages":
                use phone_messages
            elif ui_phone_app == "chat":
                use phone_chat(ui_phone_selected)
            elif ui_phone_app == "university":
                use phone_university
            elif ui_phone_app == "bank":
                use phone_bank
            elif ui_phone_app == "alarm":
                use phone_alarm
            elif ui_phone_app == "settings":
                vbox:
                    spacing 20
                    text "Обои" style "phone_heading"
                    textbutton "Закат" action SetField(game_state, "phone_wallpaper", "sunset") style "phone_row"
                    textbutton "Ночь" action SetField(game_state, "phone_wallpaper", "night") style "phone_row"
            else:
                text "Приложение пока недоступно" style "phone_text" xsize 400
        hbox:
            xpos 136
            ypos 881
            spacing 44
            use phone_icon("home", Function(phone_open), "Главный экран")
            use phone_icon("messages", Function(phone_open, "messages"), "Сообщения")
            use phone_icon("settings", Function(phone_open, "settings"), "Настройки")

screen phone_home():
    vbox:
        spacing 10
        xalign 0.5
        text game_state.clock.date.strftime("%d.%m.%Y") style "phone_small" xalign 0.5
        text game_state.clock.display_time style "phone_heading" size 60 xalign 0.5
        null height 50
        grid 3 3:
            xspacing 16
            yspacing 28
            for app, title, color in phone_home_apps():
                vbox:
                    xsize 128
                    spacing 8
                    button:
                        id "phone_app_" + app
                        xalign 0.5
                        xysize (82, 82)
                        padding (16, 16)
                        background Transform("ui/phone/tile.svg", xysize=(82, 82), matrixcolor=TintMatrix(NS_COLOR[color]))
                        hover_background Transform("ui/phone/tile.svg", xysize=(82, 82), matrixcolor=TintMatrix(NS_COLOR[color]) * BrightnessMatrix(0.12))
                        action Function(phone_open, app)
                        add "ui/phone/" + app + ".svg" xysize (50, 50)
                    text title style "phone_small" xalign 0.5
                    if app in ("camera", "gallery", "map"):
                        text "Недоступно" style "phone_small" size 13 xalign 0.5

screen phone_university():
    vbox:
        spacing 18
        xfill True
        add "ui/phone/university.svg" xysize (82, 82) xalign 0.5
        text "Статус поступления" style "phone_small" xalign 0.5
        text "ЗАЧИСЛЕНА" style "phone_heading" color NS_COLOR["teal"] xalign 0.5
        frame:
            background Frame("ui/phone/glass.svg", 20, 20)
            padding (18, 18)
            xfill True
            vbox:
                spacing 10
                text "Начало занятий" style "phone_small"
                text "1 сентября 2026" style "phone_heading"
                text "Расписание и учебные разделы появятся после начала занятий." style "phone_text"

screen phone_alarm():
    vbox:
        spacing 18
        xfill True
        add "ui/phone/alarm.svg" xysize (82, 82) xalign 0.5
        text ("Будильник включен" if game_state.alarm.enabled else "Будильник выключен") style "phone_small" xalign 0.5
        frame:
            xfill True
            ysize 132
            padding (16, 16)
            background Frame("ui/phone/glass.svg", 20, 20)
            text alarm_display_time(game_state) style "phone_heading" size 54 align (0.5, 0.5)
        text "Часы" style "phone_small"
        hbox:
            spacing 12
            textbutton "−1 час" action [Function(adjust_alarm_time, -60), Function(renpy.restart_interaction)] style "phone_row" xsize 204
            textbutton "+1 час" action [Function(adjust_alarm_time, 60), Function(renpy.restart_interaction)] style "phone_row" xsize 204
        text "Минуты" style "phone_small"
        hbox:
            spacing 12
            textbutton "−1 мин" action [Function(adjust_alarm_time, -1), Function(renpy.restart_interaction)] style "phone_row" xsize 204
            textbutton "+1 мин" action [Function(adjust_alarm_time, 1), Function(renpy.restart_interaction)] style "phone_row" xsize 204
        textbutton ("Отключить" if game_state.alarm.enabled else "Включить"):
            action [Function(set_alarm_enabled, not game_state.alarm.enabled), Function(renpy.restart_interaction)]
            style "phone_row"
        if game_state.alarm.enabled:
            $ alarm_target = alarm_target_datetime(game_state)
            text "Сработает: [alarm_target.strftime('%d.%m.%Y %H:%M')]" style "phone_small" xalign 0.5

screen phone_contacts():
    viewport:
        mousewheel True
        draggable True
        ysize 734
        vbox:
            spacing 10
            for npc_id in phone_contacts():
                button:
                    style "phone_row"
                    action Function(phone_open, "contact", npc_id)
                    hbox:
                        spacing 14
                        use phone_avatar(npc_id)
                        vbox:
                            xsize 310
                            text NPCS[npc_id]["name"] style "phone_heading" substitute False
                            text NPCS[npc_id].get("description", "") style "phone_small" substitute False

screen phone_contact_card(npc_id):
    if npc_id in phone_contacts():
        viewport:
            ysize 734
            mousewheel True
            draggable True
            vbox:
                spacing 18
                use phone_avatar(npc_id, 132)
                text NPCS[npc_id]["name"] style "phone_heading" substitute False
                text NPCS[npc_id].get("description", "") style "phone_text" xsize 408 substitute False
                if npc_id in game_state.relationships:
                    for line in relationship_detail_lines(npc_id, game_state):
                        text line style "phone_small" xsize 408 substitute False
                for line in phone_known_fields(npc_id, "phone_stats") + phone_known_fields(npc_id, "phone_facts"):
                    text line style "phone_text" xsize 408 substitute False
                textbutton "Написать" action Function(phone_open, "chat", npc_id) style "phone_row"
                textbutton "Позвонить" action NullAction() sensitive phone_call_status(npc_id)[0] style "phone_row"
                text phone_call_status(npc_id)[1] style "phone_small"

screen phone_quests():
    vbox:
        spacing 18
        hbox:
            spacing 3
            for status, title in (("active", "Активные"), ("completed", "Выполненные"), ("failed", "Проваленные")):
                textbutton title action SetVariable("ui_phone_tab", status) selected ui_phone_tab == status style "phone_tab"
        viewport:
            ysize 668
            mousewheel True
            draggable True
            vbox:
                spacing 12
                for qid, quest in phone_quests(ui_phone_tab):
                    textbutton QUESTS[qid]["name"] action Function(phone_open, "quest", qid) style "phone_row"
                if not phone_quests(ui_phone_tab):
                    text "Здесь пока нет заданий" style "phone_small"

screen phone_quest_card(qid):
    if qid in game_state.quests and qid in QUESTS and not QUESTS[qid].get("hidden") and game_state.quests[qid].status != "locked":
        viewport:
            ysize 734
            mousewheel True
            draggable True
            vbox:
                spacing 16
                xsize 410
                frame:
                    background Frame("ui/phone/glass.svg", 20, 20)
                    padding (18, 18)
                    xsize 410
                    vbox:
                        spacing 12
                        text QUESTS[qid]["name"] style "phone_heading" xsize 374 substitute False
                        text QUESTS[qid].get("description", "") style "phone_small" xsize 374 substitute False
                $ visible_objectives = [o for o in QUESTS[qid]["objectives"] if not o.get("hidden")]
                $ completed_count = sum(game_state.quests[qid].objectives[o["id"]].completed for o in visible_objectives)
                text "Выполнено: %s из %s" % (completed_count, len(visible_objectives)) style "phone_small"
                frame:
                    background Frame("ui/phone/glass.svg", 20, 20)
                    padding (14, 14)
                    xsize 410
                    vbox:
                        spacing 10
                        for objective_index, objective in enumerate(visible_objectives):
                            $ done = game_state.quests[qid].objectives[objective["id"]].completed
                            if objective_index:
                                add Solid(NS_COLOR["hud_border"]) xsize 382 ysize 1
                            hbox:
                                spacing 12
                                add ("ui/phone/check_done.svg" if done else "ui/phone/check_empty.svg") xysize (26, 26)
                                text objective["text"] style "phone_text" color (NS_COLOR["text_secondary"] if done else NS_COLOR["neutral_100"]) xsize 344 substitute False
                for field in ("additional_conditions", "deadline"):
                    if QUESTS[qid].get(field):
                        text str(QUESTS[qid][field]) style "phone_small" substitute False

screen phone_calendar():
    $ year, month = ui_phone_month
    $ events = phone_calendar_events(year, month)
    vbox:
        spacing 14
        hbox:
            use phone_icon("back", Function(phone_calendar_shift, -1), "Предыдущий месяц")
            fixed:
                xysize (332, 44)
                text "%s %s" % (PHONE_MONTH_NAMES[month-1], year) style "phone_heading" align (0.5, 0.5)
            use phone_icon("next", Function(phone_calendar_shift, 1), "Следующий месяц")
        grid 7 1:
            for index, title in enumerate(("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")):
                fixed:
                    xysize (60, 24)
                    text title style "phone_small" xalign 0.5 color (NS_COLOR["phone_weekend"] if index >= 5 else NS_COLOR["text_secondary"])
        for week in calendar.Calendar().monthdayscalendar(year, month):
            hbox:
                for index, day in enumerate(week):
                    if day:
                        $ today = game_state.clock.date == datetime.date(year, month, day)
                        button:
                            xysize (60, 52)
                            padding (0, 0)
                            background Frame("ui/phone/today.svg" if today else "ui/phone/accent.svg" if day in events else "ui/phone/glass.svg", 12, 12)
                            hover_background Frame("ui/phone/glass_hover.svg", 12, 12)
                            hovered (SetVariable("ui_phone_tooltip", (day, events[day])) if day in events else NullAction())
                            action (SetVariable("ui_phone_tooltip", (day, events[day])) if day in events else NullAction())
                            text str(day) style "phone_text" align (0.5, 0.5) color (NS_COLOR["neutral_950"] if today else NS_COLOR["phone_weekend"] if index >= 5 and day not in events else NS_COLOR["neutral_100"])
                    else:
                        null width 60 height 52
        if ui_phone_tooltip and ui_phone_tooltip[1]:
            frame:
                style "ns_panel_compact"
                background Frame("ui/phone/glass.svg", 20, 20)
                xsize 420
                vbox:
                    text "%s %s" % (ui_phone_tooltip[0], PHONE_MONTH_NAMES[month-1]) style "phone_small"
                    if len(ui_phone_tooltip[1]) == 1:
                        text ui_phone_tooltip[1][0] style "phone_text" xsize 366 substitute False
                    else:
                        viewport:
                            ysize 120
                            mousewheel True
                            draggable True
                            scrollbars "vertical"
                            side_yfill False
                            vbox:
                                for title in ui_phone_tooltip[1]:
                                    text title style "phone_text" xsize 366 substitute False

screen phone_messages():
    viewport:
        ysize 734
        mousewheel True
        draggable True
        vbox:
            spacing 12
            for npc_id in phone_chats():
                $ history = phone_history(npc_id)
                button:
                    style "phone_row"
                    action Function(phone_open, "chat", npc_id)
                    hbox:
                        spacing 12
                        use phone_avatar(npc_id)
                        vbox:
                            xsize 312
                            text NPCS[npc_id]["name"] style "phone_heading" substitute False
                            text ((history[-1]["text"][:65] + ("…" if len(history[-1]["text"]) > 65 else "")) if history else "Нет сообщений") style "phone_small" substitute False
                            if any(not m.get("read", False) for m in history):
                                text "Новое сообщение" style "phone_small" color NS_COLOR["amber"]

screen phone_chat(npc_id):
    if npc_id in phone_contacts():
        fixed:
            xysize (420, 744)
            hbox:
                spacing 12
                use phone_avatar(npc_id, 44)
                text NPCS[npc_id]["name"] style "phone_heading" yalign 0.5 substitute False
            viewport:
                id "phone_chat_history"
                ypos 62
                ysize 594
                mousewheel True
                draggable True
                yinitial 1.0
                vbox:
                    spacing 14
                    xsize 420
                    for message in phone_history(npc_id):
                        frame:
                            xsize 346
                            xalign (1.0 if message.get("from") == "nastya" else 0.0)
                            padding (18, 16)
                            background Frame("ui/phone/accent.svg" if message.get("from") == "nastya" else "ui/phone/glass.svg", 20, 20)
                            text message["text"] style "phone_text" xsize 310 substitute False
            if ui_phone_choices_open:
                frame:
                    id "phone_message_menu"
                    ypos 374
                    xysize (420, 284)
                    padding (14, 14)
                    background Frame("ui/phone/menu.svg", 20, 20)
                    viewport:
                        ysize 256
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        vbox:
                            spacing 8
                            for option_id, option in PHONE_MESSAGE_OPTIONS.items():
                                if phone_context_matches(option, npc_id, game_state):
                                    $ allowed, reason, replies = phone_option_status(option_id, npc_id)
                                    textbutton option["text"] action Function(phone_choose_message, option_id, npc_id) sensitive allowed style "phone_row" xsize 366
                                    if reason:
                                        text reason style "phone_small" xsize 362
            textbutton ("Свернуть варианты" if ui_phone_choices_open else "Выбрать сообщение"):
                id "phone_message_toggle"
                ypos 680
                style "phone_row"
                action ToggleVariable("ui_phone_choices_open")
