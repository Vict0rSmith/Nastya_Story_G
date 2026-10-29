define config.name = _("Nastya Story")
define config.version = "0.1.0"
define gui.show_name = True
define gui.about = _("Nastya Story пересобирается с чистого листа по утвержденной архитектуре и дизайн-системе.")

define build.name = "nastya_story"
define build.version = config.version

define config.has_sound = True
define config.has_music = True
define config.has_voice = True

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

define config.window = "auto"
define config.window_show_transition = Dissolve(0.2)
define config.window_hide_transition = Dissolve(0.2)

# Sandbox state is forward-only during a running session.
# Returning to an earlier game state is allowed only through loading a save.
define config.rollback_enabled = False

define config.save_directory = "nastya-story-rebuild"
define config.window_icon = "gui/window_icon.png"

define config.developer = True
define config.console = True

init python:
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**.rpy", "archive")
    build.classify("**.rpyc", "archive")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.webp", "archive")
    build.classify("game/**.ogg", "archive")
    build.classify("game/**.opus", "archive")
    build.classify("game/**.mp3", "archive")
    build.classify("game/**.wav", "archive")
