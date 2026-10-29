init -50 python:

    configure_nutrition_thresholds({"sated": 300, "hungry": 300, "very_hungry": 360})

    register_npc("masha", name="Маша", description="Подруга Насти из Лозовки", sexual_route_allowed=True, romantic_route_allowed=False)
    register_npc("nika", name="Ника", description="Соседка и хозяйка квартиры", sexual_route_allowed=True, romantic_route_allowed=True)
    register_npc("anna", name="Анна", description="Соседка", sexual_route_allowed=True, romantic_route_allowed=True)
    register_npc("aslan", name="Аслан", description="Владелец районного кафе", sexual_route_allowed=True, romantic_route_allowed=False)
    SCHEDULES["masha"] = [
        {"location": "loc_apartment_5_room", "start": 0, "end": 600, "weekdays": tuple(range(7))},
        {"location": "loc_masha_school", "start": 600, "end": 780, "weekdays": tuple(range(7))},
        {"location": "loc_apartment_5_room", "start": 780, "end": 1440, "weekdays": tuple(range(7))},
    ]
    SCHEDULES["nika"] = [
        {"location": "loc_apartment_6_hallway", "start": 1140, "end": 1320, "date": "2026-08-29"},
    ]
    SCHEDULES["anna"] = []
    SCHEDULES["aslan"] = []

    register_item("sandwich", name="Сэндвич с курицей", description="Готовый сэндвич. Хороший перекус: оставляет примерно три часа до голода.", type="consumable", stackable=True, consumable=True, usable=True, tags=["food", "good_snack"], effects=[("nutrition_cap", 120), ("energy", 1)])
    register_item("water", name="Вода", description="Бутылка воды.", type="consumable", stackable=True, consumable=True, usable=True, effects=[("energy", 1)])
    register_item("basement_key", name="Ключ от подвала", description="Постоянный ключ.", type="quest", stackable=False, consumable=False, usable=False)
    register_item("disposable_razor_pack_5", name="Одноразовые бритвы, 5 шт.", description="Упаковка одноразовых бритв для добровольного косметического ухода.", type="consumable", stackable=True, consumable=True, usable=False)
    register_item("food_kit_breakfast", name="Продуктовый комплект для завтрака", description="Комплект для приготовления полноценной еды дома.", type="consumable", stackable=True, consumable=True, usable=False, tags=["food", "food_kit"])
    register_item("food_kit_soup", name="Продуктовый комплект для супа", description="Комплект для приготовления полноценной еды дома.", type="consumable", stackable=True, consumable=True, usable=False, tags=["food", "food_kit"])
    register_item("food_kit_dinner", name="Продуктовый комплект для ужина", description="Комплект для приготовления полноценной еды дома.", type="consumable", stackable=True, consumable=True, usable=False, tags=["food", "food_kit"])
    register_item("prepared_home_meal", name="Готовая домашняя еда", description="Одна готовая порция полноценной еды.", type="consumable", stackable=True, consumable=True, usable=False, tags=["food", "prepared_meal"])
    register_item("yogurt_granola", name="Йогурт с гранолой", description="Готовый хороший перекус: оставляет примерно три часа до голода.", type="consumable", stackable=True, consumable=True, usable=True, tags=["food", "good_snack"], effects=[("nutrition_cap", 120)])
    register_item("banana", name="Банан", description="Готовый легкий перекус: оставляет примерно полтора часа до голода.", type="consumable", stackable=True, consumable=True, usable=True, tags=["food", "light_snack"], effects=[("nutrition_cap", 210)])
    register_item("chocolate_bar", name="Шоколадный батончик", description="Готовый легкий перекус: оставляет примерно полтора часа до голода.", type="consumable", stackable=True, consumable=True, usable=True, tags=["food", "light_snack"], effects=[("nutrition_cap", 210), ("energy", 1)])
    register_item("energy_drink", name="Энергетик", description="Немного восстанавливает энергию. Повторное употребление доступно через 12 часов.", type="consumable", stackable=True, consumable=True, usable=True, tags=["drink", "energy_drink"], effects=[("energy_boost", 2, 720)])

    register_item("cafe_chicken_pasta", name="Паста с курицей", description="Сытное горячее блюдо, полностью насыщает.", type="consumable", consumable=True, effects=[("nutrition_full",), ("energy", 1)])
    register_item("cafe_omelette_toast", name="Омлет с тостами", description="Сытное блюдо, полностью насыщает.", type="consumable", consumable=True, effects=[("nutrition_full",), ("energy", 1)])
    register_item("cafe_beef_soup", name="Суп с говядиной", description="Сытное горячее блюдо, полностью насыщает.", type="consumable", consumable=True, effects=[("nutrition_full",), ("energy", 1)])
    register_item("cafe_chicken_sandwich", name="Сэндвич с курицей", description="Хороший перекус: оставляет примерно три часа до голода.", type="consumable", consumable=True, effects=[("nutrition_cap", 120), ("energy", 1)])
    register_item("cafe_syrniki", name="Сырники", description="Хороший перекус: оставляет примерно три часа до голода.", type="consumable", consumable=True, effects=[("nutrition_cap", 120)])
    register_item("cafe_sausage_pastry", name="Сосиска в тесте", description="Хороший перекус: оставляет примерно три часа до голода.", type="consumable", consumable=True, effects=[("nutrition_cap", 120)])
    register_item("cafe_bun", name="Булочка", description="Легкий перекус: оставляет примерно полтора часа до голода.", type="consumable", consumable=True, effects=[("nutrition_cap", 210)])
    register_item("cafe_cake", name="Пирожное", description="Легкий перекус: оставляет примерно полтора часа до голода.", type="consumable", consumable=True, effects=[("nutrition_cap", 210)])
    register_item("cafe_raf", name="Раф", description="Сливочный кофейный напиток и легкий перекус.", type="consumable", consumable=True, effects=[("nutrition_cap", 210), ("energy", 1)])

    register_shop_item("loc_shop", "disposable_razor_pack_5", price=300, purchase_quantity=5)
    register_shop_item("loc_shop", "food_kit_breakfast", price=400)
    register_shop_item("loc_shop", "food_kit_soup", price=600)
    register_shop_item("loc_shop", "food_kit_dinner", price=700)
    register_shop_item("loc_shop", "sandwich", price=300)
    register_shop_item("loc_shop", "yogurt_granola", price=200)
    register_shop_item("loc_shop", "banana", price=100)
    register_shop_item("loc_shop", "chocolate_bar", price=200)
    register_shop_item("loc_shop", "energy_drink", price=200)

    register_shop_item("loc_cafe", "cafe_chicken_pasta", price=700, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_omelette_toast", price=600, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_beef_soup", price=600, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_chicken_sandwich", price=500, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_syrniki", price=500, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_sausage_pastry", price=300, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_bun", price=200, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_cake", price=400, consume_immediately=True)
    register_shop_item("loc_cafe", "cafe_raf", price=400, consume_immediately=True)

    register_clothing("white_cotton_bra_1", name="Белый хлопковый лифчик", slot="bra", category="underwear", required_openness_rank=0, context="home", tags=["underwear"])
    register_clothing("white_cotton_panties_1", name="Белые хлопковые трусики", slot="panties", category="underwear", required_openness_rank=0, context="home", tags=["underwear"])
    register_clothing("white_cotton_bra_2", name="Белый хлопковый лифчик", slot="bra", category="underwear", required_openness_rank=0, context="home", tags=["underwear"])
    register_clothing("white_cotton_panties_2", name="Белые хлопковые трусики", slot="panties", category="underwear", required_openness_rank=0, context="home", tags=["underwear"])
    register_clothing("casual_tshirt", name="Футболка", slot="top", category="clothes", required_openness_rank=0, context="home", tags=["top", "casual"])
    register_clothing("casual_skirt", name="Юбка", slot="bottom", category="clothes", required_openness_rank=0, context="home", tags=["bottom", "skirt", "casual"])
    register_clothing("sneakers", name="Кроссовки", slot="shoes", category="shoes", required_openness_rank=0, context="home", tags=["shoes", "casual"])

    register_action(ActionDefinition("action_look_in_mirror", "Посмотреться в зеркало", 5, locations=("loc_apartment_5_hallway",), tags=("home", "atmospheric")))
    register_action(ActionDefinition("action_exercise", "Сделать зарядку", 30, 2, physical=True, minimum_energy_cost=1, locations=("loc_apartment_5_room",), effects=[("fitness", 1)], tags=("physical", "home")))
    register_action(ActionDefinition("action_clean_apartment", "Убраться в квартире", 60, 2, physical=True, minimum_energy_cost=1, locations=("loc_apartment_5_room",), tags=("housework", "physical", "home")))
    register_action(ActionDefinition("action_unpack_luggage", "Разобрать чемоданы", 45, locations=("loc_apartment_5_room",), tags=("housework", "home")))
    register_action(ActionDefinition("action_rest_lie_down", "Поваляться и отдохнуть", 60, locations=("loc_apartment_5_room",), tags=("rest", "home")))
    register_action(ActionDefinition("action_watch_tv", "Посмотреть телевизор", 60, locations=("loc_apartment_5_room",), tags=("rest", "home")))
    register_action(ActionDefinition("action_sleep", "Лечь спать", locations=("loc_apartment_5_room",), tags=("sleep", "home")))
    register_action(ActionDefinition("action_prepare_meal", "Приготовить еду", 30, 0, locations=("loc_apartment_5_kitchen",), tags=("food", "home")))
    register_action(ActionDefinition("action_eat_full_meal", "Поесть", 20, 0, locations=("loc_apartment_5_kitchen",), effects=[("energy", 1)], tags=("food", "home")))
    register_action(ActionDefinition("action_morning_hygiene", "Умыться и почистить зубы", 10, 0, locations=("loc_apartment_5_bathroom",), tags=("hygiene", "home")))
    register_action(ActionDefinition("action_take_shower", "Принять душ", 25, 1, locations=("loc_apartment_5_bathroom",), tags=("hygiene", "home")))
    register_action(ActionDefinition("action_take_bath", "Принять ванну", 45, locations=("loc_apartment_5_bathroom",), tags=("hygiene", "home")))
    register_action(ActionDefinition("action_toilet", "Сходить в туалет", 5, locations=("loc_apartment_5_bathroom",), tags=("atmospheric", "home")))
    register_action(ActionDefinition("action_shave_legs", "Побрить ноги", 10, locations=("loc_apartment_5_bathroom",), tags=("cosmetic", "home")))
    register_action(ActionDefinition("action_shave_pubic", "Побрить интимную зону", 15, locations=("loc_apartment_5_bathroom",), tags=("cosmetic", "home")))
    register_action(ActionDefinition("action_admire_view", "Полюбоваться видом", 10, locations=("loc_apartment_5_balcony",), tags=("atmospheric", "home")))
    register_action(ActionDefinition("action_remind_masha_school_documents", "Напомнить Маше о документах", 15, 0, locations=("loc_apartment_5_room",), required_npc="masha", tags=("social", "quest")))
    register_action(ActionDefinition("action_wait", "Подождать час", 60, 0, tags=("wait",)))
    register_action(ActionDefinition("action_submit_university_documents", "Подать документы", 30, 0, locations=("loc_medical_institute_admissions",), tags=("university", "quest")))
    register_action(ActionDefinition("action_ask_shop_job", "Спросить о работе", 10, 0, locations=("loc_shop_hall",), tags=("work", "quest")))
    register_action(ActionDefinition("action_ask_cafe_job", "Спросить о работе", 10, 0, locations=("loc_cafe_hall",), tags=("work", "quest")))
    register_action(ActionDefinition("action_visit_nika", "Поговорить с Никой", 20, 0, locations=("loc_apartment_6_hallway",), required_npc="nika", tags=("social", "quest")))
    register_action(ActionDefinition("action_talk_masha_admissions", "Обсудить поступление", 15, 0, locations=("loc_apartment_5_room",), required_npc="masha", tags=("social", "story")))
    register_action(ActionDefinition("action_open_shop_menu", "Купить продукты", locations=("loc_shop_hall",), tags=("shop",)))
    register_action(ActionDefinition("action_open_cafe_menu", "Заказать поесть", locations=("loc_cafe_hall",), tags=("shop", "food")))
    register_action(ActionDefinition("action_view_adult_magazine", "Посмотреть порножурнал", 20, locations=("loc_apartment_5_room", "loc_apartment_5_bathroom"), conditions={"owns_items": ("adult_magazine",)}, required_openness=1, tags=("intimate", "adult_media")))
    register_action(ActionDefinition("action_watch_adult_movie", "Посмотреть порнофильм", 45, locations=("loc_apartment_5_room",), conditions={"owns_items": ("adult_movie",)}, required_openness=1, tags=("intimate", "adult_media")))
    register_action(ActionDefinition("action_read_sex_illustrated_book", "Почитать книгу о сексе", 30, locations=("loc_apartment_5_room", "loc_apartment_5_bathroom"), conditions={"owns_items": ("sex_illustrated_book",)}, required_openness=1, tags=("intimate", "adult_media")))
    register_action(ActionDefinition("action_masturbate", "Мастурбировать", 30, locations=("loc_apartment_5_room", "loc_apartment_5_bathroom"), conditions={"required_flags": ("masturbation_unlocked",)}, required_openness=2, item_capability="solo_masturbation_method", allow_without_item=True, tags=("intimate", "masturbation")))

    register_quest("quest_2026_08_29_first_normal_day", name="Первый нормальный день", description="Личный список дел Насти на 29 августа.", objectives=[
        {"id": "morning_hygiene", "text": "Умыться и почистить зубы", "event": "action_completed", "filters": {"action_id": "action_morning_hygiene"}, "required": False},
        {"id": "exercise", "text": "Сделать зарядку", "event": "action_completed", "filters": {"action_id": "action_exercise"}, "required": False},
        {"id": "clean_apartment", "text": "Убраться в квартире", "event": "action_completed", "filters": {"action_id": "action_clean_apartment"}, "required": False},
        {"id": "unpack_luggage", "text": "Разобрать чемоданы", "event": "action_completed", "filters": {"action_id": "action_unpack_luggage"}, "required": False},
        {"id": "shower_or_bath", "text": "Принять душ или ванну", "event": "action_completed", "filters": {"action_id": ("action_take_shower", "action_take_bath")}, "required": False},
        {"id": "remind_masha_school_documents", "text": "Поговорить с Машей о ее планах и документах", "event": "action_completed", "filters": {"action_id": "action_remind_masha_school_documents"}, "required": True},
        {"id": "breakfast", "text": "Позавтракать", "event": "action_completed", "filters": {"action_id": "action_eat_full_meal"}, "required": False},
        {"id": "submit_university_documents", "text": "Подать документы в университет", "event": "action_completed", "filters": {"action_id": "action_submit_university_documents"}, "required": True},
        {"id": "find_job_information", "text": "Узнать о возможной работе", "event": "action_completed", "filters": {"action_id": ("action_ask_shop_job", "action_ask_cafe_job")}, "required": False},
        {"id": "visit_nika", "text": "Зайти к Нике", "event": "action_completed", "filters": {"action_id": "action_visit_nika"}, "required": False},
    ])
