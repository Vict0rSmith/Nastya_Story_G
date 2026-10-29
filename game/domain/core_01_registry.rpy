# Ядро домена: регистрация действий, предметов, одежды, локаций, NPC, квестов и товаров.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    def register_action(definition): ACTIONS[definition.id] = definition
    def register_item(item_id, **definition):
        if item_id in ITEMS: raise ValueError("Duplicate item: " + item_id)
        defaults = dict(entity_type="item", category=definition.get("type", "misc"), storage="inventory",
                        item_type=definition.get("type", "misc"), stackable=False, consumable=False,
                        usable=False, required_openness_purchase=0, required_openness_use=0,
                        price=None, tags=[], icon=None, use_modes=[], related_actions=[],
                        related_effects=[], related_quests=[], related_events=[])
        defaults.update(definition)
        ITEMS[item_id] = dict(defaults, id=item_id)
    def register_clothing(item_id, **definition):
        definition.setdefault("storage", "wardrobe")
        definition.setdefault("item_type", "clothing")
        definition.setdefault("required_openness_use", definition.get("required_openness_rank", 0))
        definition.setdefault("contexts", (definition.get("context", "home"),))
        register_item(item_id, **definition)
        CLOTHES[item_id] = ITEMS[item_id]
    def register_location(location_id, **definition): LOCATIONS[location_id] = dict(definition, id=location_id)
    def register_npc(npc_id, **definition): NPCS[npc_id] = dict(definition, id=npc_id)
    def register_quest(quest_id, **definition): QUESTS[quest_id] = dict(definition, id=quest_id)
    def register_shop_item(location_id, item_id, price=None, purchase_quantity=1, consume_immediately=False):
        SHOP_CATALOGS.setdefault(location_id, {})[item_id] = {"item_id": item_id, "price": price, "purchase_quantity": int(purchase_quantity), "consume_immediately": bool(consume_immediately)}
