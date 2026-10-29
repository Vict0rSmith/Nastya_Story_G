################################################################################
## Initialization
################################################################################

init offset = -1

init python:
    def ns_confirm_message(message):
        messages = {
            "Are you sure?": "Вы уверены?",
            "Are you sure you want to delete this save?": "Удалить это сохранение?",
            "Are you sure you want to overwrite your save?": "Перезаписать это сохранение?",
            "Loading will lose unsaved progress.\nAre you sure you want to do this?": "Несохраненный прогресс будет потерян.\nЗагрузить сохранение?",
            "Are you sure you want to quit?": "Выйти из игры?",
            "Are you sure you want to return to the main menu?\nThis will lose unsaved progress.": "Вернуться в главное меню?\nНесохраненный прогресс будет потерян.",
            "Are you sure you want to end the replay?": "Завершить повтор?",
            "Are you sure you want to begin skipping?": "Начать пропуск текста?",
            "Are you sure you want to skip to the next choice?": "Пропустить текст до следующего выбора?",
            "Are you sure you want to skip unseen dialogue to the next choice?": "Пропустить непрочитанный текст до следующего выбора?",
        }
        return messages.get(message, message)


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Solid(NS_COLOR["teal"])
    right_bar Solid(NS_COLOR["neutral_700"])

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    top_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    bottom_bar Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Solid(NS_COLOR["neutral_700"])
    thumb Solid(NS_COLOR["teal"], xsize=18, ysize=36)

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                style "namebox"
                text who id "who" style "say_label"

        text what id "what" style "say_dialogue" xpos (268 if who is not None and renpy.get_side_image("side") else 48) xsize (1604 if who is not None and renpy.get_side_image("side") else 1824)

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue
style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Solid(NS_COLOR["neutral_950"] + "EB")

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height
    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False


## Input screen ################################################################
screen input(prompt):
    style_prefix "input"

    window:
        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos
            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5
    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
screen quick_menu():
    zorder 100

    if quick_menu:
        frame:
            id "quick_menu_bar"
            style "ns_hud_panel"
            xalign 0.5
            yalign 1.0
            padding (10, 6)
            hbox:
                style_prefix "quick"
                spacing 4
                textbutton "Назад" action Rollback()
                textbutton "История" action ShowMenu('history')
                textbutton "Пропуск" action Skip() alternate Skip(fast=True, confirm=True)
                textbutton "Авто" action Preference("auto-forward", "toggle")
                textbutton "Сохранить" action ShowMenu('save')
                textbutton "Быстр. сохр." action QuickSave()
                textbutton "Быстр. загр." action QuickLoad()
                textbutton "Настройки" action ShowMenu('preferences')

init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
screen navigation():

    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing

        if main_menu:
            textbutton "Новая игра" action Start()
        else:
            textbutton "История" action ShowMenu("history")
            textbutton "Сохранить" action ShowMenu("save")

        textbutton "Загрузить" action ShowMenu("load")
        textbutton "Настройки" action ShowMenu("preferences")

        if _in_replay:
            textbutton "Завершить повтор" action EndReplay(confirm=True)
        elif not main_menu:
            textbutton "Главное меню" action MainMenu()

        textbutton "Об игре" action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton "Помощь" action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton "Выход" action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
screen main_menu():
    tag menu
    style_prefix "main_menu"

    add gui.main_menu_background

    use navigation

    if gui.show_name:
        vbox:
            text "[config.name!t]":
                style "main_menu_title"
            text "Версия [config.version] · временная сборка":
                style "main_menu_version"


style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_vbox:
    xalign 1.0
    xoffset -32
    yalign 1.0
    yoffset -28

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)
    xalign 1.0

style main_menu_title:
    properties gui.text_properties("title")
    xalign 1.0

style main_menu_version:
    properties gui.text_properties("version")
    xalign 1.0


## Game Menu screen ############################################################
screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame:
                style "game_menu_navigation_frame"
            frame:
                style "game_menu_content_frame"
                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        transclude
                else:
                    transclude

    use navigation

    textbutton "Вернуться":
        style "return_button"
        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar
style game_menu_vscrollbar is gui_vscrollbar
style game_menu_label is gui_label
style game_menu_label_text is gui_label_text
style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180
    background None

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 40
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
screen about():
    tag menu
    use game_menu("Об игре", scroll="viewport"):
        style_prefix "about"
        vbox:
            label "[config.name!t]"
            text "Версия [config.version!t]\n"
            if gui.about:
                text "[gui.about!t]\n"
            text "{a=https://www.renpy.org/}Создано на Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
screen save():
    tag menu
    use file_slots("Сохранить")

screen load():
    tag menu
    use file_slots("Загрузить")

screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern="Страница {}", auto="Автосохранения", quick="Быстрые сохранения")
    use game_menu(title):
        fixed:
            order_reverse True
            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        text FileTime(slot, format="{#file_time}%d.%m.%Y, %H:%M", empty="пустой слот"):
                            style "slot_time_text"
                        text FileSaveName(slot):
                            style "slot_name_text"
                        key "save_delete" action FileDelete(slot)
            vbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0
                hbox:
                    xalign 0.5
                    spacing gui.page_spacing
                    textbutton _("<") action FilePagePrevious()
                    if config.has_autosave:
                        textbutton "А" action FilePage("auto")
                    if config.has_quicksave:
                        textbutton "Б" action FilePage("quick")
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)
                    textbutton _(">") action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text
style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text
style page_label:
    xpadding 50
    ypadding 5
style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color
style page_button:
    properties gui.button_properties("page_button")
style page_button_text:
    properties gui.text_properties("page_button")
style slot_button:
    properties gui.button_properties("slot_button")
    background Solid(NS_COLOR["neutral_800"] + "B8")
    hover_background Solid(NS_COLOR["neutral_700"] + "E8")
    selected_background Solid(NS_COLOR["hud_selected"])
    insensitive_background Solid(NS_COLOR["neutral_900"] + "80")
    padding (10, 10)
style slot_button_text:
    properties gui.text_properties("slot_button")


## Preferences screen ##########################################################
screen preferences():
    tag menu
    use game_menu("Настройки", scroll="viewport"):
        vbox:
            hbox:
                box_wrap True
                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "radio"
                        label "Экран"
                        textbutton "В окне" action Preference("display", "window")
                        textbutton "На весь экран" action Preference("display", "fullscreen")
                vbox:
                    style_prefix "check"
                    label "Пропуск"
                    textbutton "Непрочитанный текст" action Preference("skip", "toggle")
                    textbutton "После выборов" action Preference("after choices", "toggle")
                    textbutton "Переходы" action InvertSelected(Preference("transitions", "toggle"))
                null height (4 * gui.pref_spacing)
            null height (4 * gui.pref_spacing)
            hbox:
                style_prefix "slider"
                box_wrap True
                vbox:
                    label "Скорость текста"
                    bar value Preference("text speed")
                    label "Скорость авточтения"
                    bar value Preference("auto-forward time")
                vbox:
                    if config.has_music:
                        label "Громкость музыки"
                        hbox:
                            bar value Preference("music volume")
                    if config.has_sound:
                        label "Громкость звуков"
                        hbox:
                            bar value Preference("sound volume")
                            if config.sample_sound:
                                textbutton "Проверить" action Play("sound", config.sample_sound)
                    if config.has_voice:
                        label "Громкость голоса"
                        hbox:
                            bar value Preference("voice volume")
                            if config.sample_voice:
                                textbutton "Проверить" action Play("voice", config.sample_voice)
                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing
                        textbutton "Выключить весь звук":
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

style radio_label is gui_label
style radio_label_text is gui_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style check_label is gui_label
style check_label_text is gui_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_label is gui_label
style slider_label_text is gui_label_text
style slider_vbox is vbox
style radio_button:
    properties gui.button_properties("radio_button")
style radio_button_text:
    properties gui.text_properties("radio_button")
style check_button:
    properties gui.button_properties("check_button")
style check_button_text:
    properties gui.text_properties("check_button")
style slider_slider:
    xsize 525
style slider_button:
    properties gui.button_properties("slider_button")
style slider_label_text:
    size gui.label_text_size
style slider_vbox:
    xsize 675


## History screen ##############################################################
screen history():
    tag menu
    predict False
    use game_menu("История", scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):
        style_prefix "history"
        for h in _history_list:
            window:
                has fixed:
                    yfit True
                if h.who:
                    label h.who:
                        style "history_name"
                        substitute False
                        if "color" in h.who_args:
                            text_color h.who_args["color"]
                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

style history_window is empty
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text
style history_text:
    ypos 5
    xpos 170
    xanchor 0.0
    xsize 740
    min_width 740
    textalign 0.0
    layout ("subtitle" if renpy.variant("small") else "tex")
style history_name:
    xpos 150
    xanchor 1.0
    ypos 0
    xsize 150
style history_name_text:
    min_width 150
    textalign 1.0


## Help screen #################################################################
screen help():
    tag menu
    default device = "keyboard"
    use game_menu("Помощь", scroll="viewport"):
        style_prefix "help"
        vbox:
            spacing 23
            hbox:
                textbutton "Клавиатура" action SetScreenVariable("device", "keyboard")
                textbutton "Мышь" action SetScreenVariable("device", "mouse")
                if GamepadExists():
                    textbutton "Геймпад" action SetScreenVariable("device", "gamepad")
            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

screen keyboard_help():
    hbox:
        label "Enter"
        text "Продолжает диалог и активирует элементы интерфейса."
    hbox:
        label "Пробел"
        text "Продолжает диалог, не выбирая варианты."
    hbox:
        label "Стрелки"
        text "Перемещают фокус по интерфейсу."
    hbox:
        label "Escape"
        text "Открывает игровое меню."
    hbox:
        label "Ctrl"
        text "Пропускает диалог, пока клавиша удерживается."
    hbox:
        label "Tab"
        text "Включает или выключает пропуск диалога."
    hbox:
        label "Page Up"
        text "Возвращает к предыдущему диалогу."
    hbox:
        label "Page Down"
        text "Переходит вперед по истории диалога."
    hbox:
        label "H"
        text "Скрывает интерфейс."
    hbox:
        label "S"
        text "Сохраняет снимок экрана."
    hbox:
        label "V"
        text "Включает или выключает озвучивание интерфейса."
    hbox:
        label "Shift+A"
        text "Открывает меню специальных возможностей."

screen mouse_help():
    hbox:
        label "Левая кнопка"
        text "Продолжает диалог и активирует элементы интерфейса."
    hbox:
        label "Средняя кнопка"
        text "Скрывает интерфейс."
    hbox:
        label "Правая кнопка"
        text "Открывает игровое меню."
    hbox:
        label "Колесо вверх"
        text "Возвращает к предыдущему диалогу."
    hbox:
        label "Колесо вниз"
        text "Переходит вперед по истории диалога."

screen gamepad_help():
    hbox:
        label "Правый триггер\nA / нижняя кнопка"
        text "Продолжает диалог и активирует элементы интерфейса."
    hbox:
        label "Левый триггер\nлевый бампер"
        text "Возвращает к предыдущему диалогу."
    hbox:
        label "Правый бампер"
        text "Переходит вперед по истории диалога."
    hbox:
        label "Крестовина, стики"
        text "Перемещают фокус по интерфейсу."
    hbox:
        label "Start, Guide"
        text "Открывает игровое меню."
    hbox:
        label "Y / верхняя кнопка"
        text "Скрывает интерфейс."


## Additional screens ##########################################################
screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    style_prefix "confirm"
    add Solid(NS_COLOR["overlay"])
    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 25
            label ns_confirm_message(message):
                xalign 0.5
            hbox:
                xalign 0.5
                spacing 100
                textbutton "Да" action yes_action
                textbutton "Нет" action no_action
    key "game_menu" action no_action

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text
style confirm_frame:
    background Solid(NS_COLOR["neutral_800"] + "F5")
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5
style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"
style confirm_button:
    properties gui.button_properties("confirm_button")
style confirm_button_text:
    properties gui.text_properties("confirm_button")

screen skip_indicator():
    zorder 100
    style_prefix "skip"
    frame:
        has hbox
        spacing 9
        text "Пропуск"
        text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

transform delayed_blink(delay, cycle):
    alpha .5
    pause delay
    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text
style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding
style skip_text:
    size gui.notify_text_size
style skip_triangle:
    font "DejaVuSans.ttf"

screen notify(message):
    zorder 100
    style_prefix "notify"
    frame at notify_appear:
        text "[message!tq]"
    timer 3.0 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text
style notify_frame:
    xalign 0.5
    ypos gui.notify_ypos
    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding
style notify_text:
    properties gui.text_properties("notify")

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"
        has vbox:
            spacing gui.nvl_spacing
        use nvl_dialogue(dialogue)
        for i in items:
            textbutton i.caption:
                id i.id
                action i.action

screen nvl_dialogue(dialogue):
    for d in dialogue:
        window:
            id d.window_id
        fixed:
            yfit gui.nvl_height is None
        if d.who is not None:
            text d.who:
                id d.who_id
        text d.what:
            id d.what_id

style nvl_window is default
style nvl_entry is default
style nvl_label is say_label
style nvl_dialogue is say_dialogue
style nvl_button is button
style nvl_button_text is button_text
style nvl_window:
    xfill True
    yfill True
    background "gui/nvl.png"
    padding gui.nvl_borders.padding
style nvl_entry:
    xfill True
    ysize gui.nvl_height
style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    xsize gui.nvl_name_width
    ypos gui.nvl_name_ypos
style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xsize gui.nvl_text_width
    ypos gui.nvl_text_ypos
style nvl_thought:
    xpos gui.nvl_thought_xpos
    xsize gui.nvl_thought_width
style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xalign gui.nvl_button_xalign


## Mobile Variants #############################################################
style pref_vbox:
    variant "medium"
    xsize 450

screen quick_menu():
    variant "touch"
    zorder 100
    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.5
            yalign 1.0
            textbutton "Назад" action Rollback()
            textbutton "Пропуск" action Skip() alternate Skip(fast=True, confirm=True)
            textbutton "Авто" action Preference("auto-forward", "toggle")
            textbutton "Меню" action ShowMenu()

style window:
    variant "small"
    background "gui/phone/textbox.png"
style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"
style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"
style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"
style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"
style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"
style game_menu_navigation_frame:
    variant "small"
    xsize 340
style game_menu_content_frame:
    variant "small"
    top_margin 0
style game_menu_viewport:
    variant "small"
    xsize 920
style return_button:
    variant "small"
    xpos 40
style slider_vbox:
    variant "small"
    xsize 675
