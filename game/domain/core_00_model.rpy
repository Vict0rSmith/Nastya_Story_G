# Ядро домена: константы схемы, реестры и классы состояния.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    import copy
    import datetime
    import random

    SCHEMA_VERSION = 12
    PERIODS = ((5, "morning"), (12, "day"), (18, "evening"), (23, "night"), (24, "late_night"))
    SOCIAL_STATES = ("unmet", "neutral", "friend", "enemy")
    INTIMACY_STATES = ("none", "sexual", "romantic")
    OUTFIT_SLOTS = ("bra", "panties", "top", "bottom", "dress", "outerwear", "shoes", "special")

    ACTIONS = {}
    ITEMS = {}
    CLOTHES = {}
    LOCATIONS = {}
    NPCS = {}
    SCHEDULES = {}
    QUESTS = {}
    STORY_EVENTS = {}
    SHOP_CATALOGS = {}

    RAZOR_ITEM_ID = "disposable_razor_pack_5"
    LUGGAGE_UNPACKED_FLAG = "obj_apartment_5_luggage_unpacked"
    UNPACK_LUGGAGE_SCENE_FLAG = "scene_2026_08_29_unpack_luggage_seen"

    class GameEvent(object):
        def __init__(self, event_type, data=None, timestamp=None):
            self.type = event_type
            self.data = dict(data or {})
            self.timestamp = timestamp

    class RankedValue(object):
        def __init__(self, rank=0, progress=0, milestones=None):
            self.rank = int(rank)
            self.progress = int(progress)
            self.milestones = set(milestones or [])

    class SkillState(object):
        def __init__(self, rank=1, progress=0):
            self.rank = int(rank)
            self.progress = int(progress)

    class PlayerState(object):
        def __init__(self):
            self.energy = 10
            self.max_energy = 10
            self.openness = RankedValue(0, 0)
            self.fitness = RankedValue(1, 0)
            self.intellect = RankedValue(1, 0)
            self.mood = 0
            self.arousal = 0
            self.skills = {}

    class GameClock(object):
        def __init__(self, year=2026, month=8, day=29, hour=8, minute=0):
            self.date = datetime.date(year, month, day)
            self.hour = int(hour)
            self.minute = int(minute)

        @property
        def weekday(self): return self.date.weekday()
        @property
        def is_weekend(self): return self.weekday >= 5
        @property
        def season(self):
            if self.date.month in (12, 1, 2): return "winter"
            if self.date.month in (3, 4, 5): return "spring"
            if self.date.month in (6, 7, 8): return "summer"
            return "autumn"
        @property
        def period(self):
            value = self.hour
            if value < 5: return "late_night"
            if value < 12: return "morning"
            if value < 18: return "day"
            if value < 23: return "evening"
            return "night"
        @property
        def total_minutes(self): return self.hour * 60 + self.minute
        @property
        def display_time(self): return "%02d:%02d" % (self.hour, self.minute)
        def advance(self, minutes):
            minutes = int(minutes)
            if minutes < 0: raise ValueError("Time cannot move backwards")
            total = self.total_minutes + minutes
            days, current = divmod(total, 1440)
            self.date += datetime.timedelta(days=days)
            self.hour, self.minute = divmod(current, 60)

    class InventoryState(object):
        def __init__(self):
            self.quantities = {}
            self.item_states = {}
            self.external_items = {}
            self.body_runtime = {}

    class GroomingState(object):
        def __init__(self):
            self.pubic_style = "natural"
            self.last_pubic_grooming_at = None
            self.pubic_grooming_due_at = None

    class WardrobeState(object):
        def __init__(self):
            self.owned = set()
            self.equipped = dict((slot, None) for slot in OUTFIT_SLOTS)
            self.access_context = None
            self.saved_civilian_outfit = None
            self.active_workplace = None

    class WalletState(object):
        def __init__(self, balance=0):
            self.balance = int(balance)
            self.history = []
            self.transaction_sequence = 0
            self.loans = []
            self.transfer_recipients = set()

    class AlarmState(object):
        def __init__(self):
            self.enabled = False
            self.time_minutes = None

    class RelationshipState(object):
        def __init__(self, social="unmet", intimacy="none"):
            if social not in SOCIAL_STATES: raise ValueError("Unknown social state")
            if intimacy not in INTIMACY_STATES: raise ValueError("Unknown intimacy state")
            self.social = social
            self.intimacy = intimacy

    class QuestObjectiveState(object):
        def __init__(self):
            self.progress = 0
            self.completed = False

    class QuestState(object):
        def __init__(self, definition):
            self.status = "active"
            self.objectives = dict((o["id"], QuestObjectiveState()) for o in definition["objectives"])

    class StoryState(object):
        def __init__(self):
            self.flags = set()
            self.stages = {}
            self.counters = {}
            self.event_history = []
            self.pending_scene = None
            self.pending_action = None
            self.pending_action_item = None
            self.event_last_date = {}

    class GameState(object):
        def __init__(self):
            self.schema_version = SCHEMA_VERSION
            self.player = PlayerState()
            self.clock = GameClock()
            self.location_id = "loc_apartment_5_room"
            self.relationships = {}
            self.inventory = InventoryState()
            self.grooming = GroomingState()
            self.wardrobe = WardrobeState()
            self.wallet = WalletState(10000)
            self.alarm = AlarmState()
            self.last_full_meal_at = None
            self.nutrition_elapsed_minutes = 0.0
            self.energy_drink_ready_at = None
            self.arousal_decay_minutes = 0
            self.passive_body_minutes = 0
            self.arousal_source_ready_at = {}
            self.awake_energy_minutes = 0
            self.quests = {}
            self.story = StoryState()
            self.messages = []
            self.phone_threads = set()
            self.phone_cooldowns = {}
            self.phone_wallpaper = "sunset"
            self.schedule_overrides = {}

    class ActionDefinition(object):
        def __init__(self, action_id, name, duration_minutes=0, base_energy_cost=0,
                     physical=False, minimum_energy_cost=0, locations=None,
                     required_npc=None, effects=None, tags=None, conditions=None,
                     required_openness=0, item_capability=None, allow_without_item=True):
            self.id = action_id
            self.name = name
            self.duration_minutes = int(duration_minutes)
            self.base_energy_cost = int(base_energy_cost)
            self.physical = bool(physical)
            self.minimum_energy_cost = int(minimum_energy_cost)
            self.locations = tuple(locations or ())
            self.required_npc = required_npc
            self.effects = list(effects or [])
            self.tags = tuple(tags or ())
            self.conditions = dict(conditions or {})
            self.required_openness = required_openness
            self.item_capability = item_capability
            self.allow_without_item = allow_without_item

    class ActionResult(object):
        def __init__(self, success, action_id, energy_cost=0, duration_minutes=0, reasons=None, deferred=False):
            self.success = bool(success)
            self.action_id = action_id
            self.energy_cost = int(energy_cost)
            self.duration_minutes = int(duration_minutes)
            self.reasons = list(reasons or [])
            self.deferred = bool(deferred)
