init -5 python:
    def items_test_catalog_tests():
        expected = {"adult_magazine": (1,1), "adult_movie": (1,1), "sex_illustrated_book": (1,1),
            "lubricant": (1,1), "massage_oil": (1,1), "schoolgirl_costume": (1,1),
            "maid_costume": (1,1), "waitress_costume": (1,1), "nurse_costume": (1,1),
            "bullet_vibrator": (2,2), "vacuum_stimulator": (2,2), "soft_handcuffs": (2,2),
            "dildo": (3,3), "vibrator": (3,3), "anal_plug": (3,3), "tail_plug": (3,3),
            "anal_beads": (3,3), "strapon": (3,3), "remote_toy": (3,3), "condoms": (1,3)}
        assert len(expected) == 20
        state = create_new_game_state()
        for item_id, (purchase, use) in expected.items():
            item = ITEMS[item_id]
            assert item["price"] is None and item["icon"] is None
            assert (item["required_openness_purchase"], item["required_openness_use"]) == (purchase,use)
            assert bool(item_purchase_reason(item_id,state))
            inventory_add(item_id, state=state)
            assert item_owns(item_id,state)
            if item["storage"] == "wardrobe":
                assert CLOTHES[item_id] is item and item_id not in state.inventory.quantities
            else:
                assert item_use_reason(item_id,state)
        assert len(inventory_visible_items("intimate",state)) == 15
        assert "massage_oil" not in dict(inventory_visible_items("intimate",state))
        state.player.openness.rank=1
        assert item_purchase_reason("condoms",state) is None
        assert item_use_reason("condoms",state)

    def items_test_body_tests():
        state=create_new_game_state()
        inventory_add("remote_toy",state=state)
        assert not set_body_item("remote_toy",True,state)[0]
        state.player.openness.rank=3
        assert inventory_use("remote_toy",state)
        assert body_item_active("remote_toy",state)
        assert not inventory_remove("remote_toy",1,state)
        assert move_to("loc_apartment_5_hallway",state)[0]
        assert body_item_active("remote_toy",state) and inventory_has("remote_toy",1,state)
        state.player.openness.rank=0
        assert set_body_item("remote_toy",False,state)[0]
        assert inventory_has("remote_toy",1,state) and not body_item_active("remote_toy",state)
        for item_id in ("anal_beads","vibrator","soft_handcuffs"):
            inventory_add(item_id,state=state)
            assert not set_body_item(item_id,True,state)[0]
        state.player.openness.rank=3
        for item_id in ("anal_plug","tail_plug"): inventory_add(item_id,state=state)
        assert set_body_item("anal_plug",True,state)[0]
        assert not set_body_item("tail_plug",True,state)[0]
        assert set_body_item("anal_plug",False,state)[0]
        state.location_id="loc_apartment_5_room"
        assert wardrobe_unequip("panties",state)
        assert set_body_item("tail_plug",True,state)[0]

    def items_test_action_event_tests():
        state=create_new_game_state(); state.player.openness.rank=3
        for item_id in ("remote_toy","vibrator","lubricant"): inventory_add(item_id,state=state)
        action_id="items_test_test_action"; quest_id="items_test_test_quest"; event_id="items_test_test_event"
        register_action(ActionDefinition(action_id,"Техническая проверка",required_openness=3,item_capability="masturbation_tool",allow_without_item=False,conditions={"body_items":{"remote_toy":True}}))
        register_quest(quest_id,objectives=[{"id":"body_gate","event":"action_completed","conditions":{"body_items":{"remote_toy":True}}}])
        STORY_EVENTS[event_id]={"id":event_id,"trigger":"action_completed","once":True,"conditions":{"body_items":{"remote_toy":True}}}
        try:
            start_quest(quest_id,state)
            assert not execute_action(action_id,state,item_id="vibrator").success
            STORY_EVENTS["items_test_insert"]={"id":"items_test_insert","trigger":"items_test_insert","once":True,"effects":[("body_item","remote_toy",True)]}
            dispatch_game_event("items_test_insert",state)
            STORY_EVENTS.pop("items_test_insert")
            assert action_item_options(action_id,state)==["vibrator"]
            assert not execute_action(action_id,state,item_id="lubricant").success
            assert not execute_action(action_id,state).success
            assert execute_action(action_id,state,item_id="vibrator").success
            assert state.quests[quest_id].status=="completed" and event_id in state.story.flags
            assert inventory_has("vibrator",1,state) and not body_item_active("vibrator",state)
            state.player.openness.rank=1
            assert not execute_action(action_id,state,item_id="lubricant").success
        finally:
            ACTIONS.pop(action_id); QUESTS.pop(quest_id); STORY_EVENTS.pop(event_id)

    def items_test_wardrobe_tests():
        state=create_new_game_state(); state.player.openness.rank=3
        inventory_add("waitress_costume",state=state)
        assert wardrobe_equip("waitress_costume",state=state)[0]
        assert wardrobe_unequip("special",state)
        state.location_id="loc_building_yard"
        assert not wardrobe_equip("waitress_costume",state=state)[0]
        assert not wardrobe_unequip("top",state)
        original=dict(WARDROBE_ACCESS)
        try:
            WARDROBE_ACCESS["loc_cafe_backroom"]={"context":"cafe","workplace":"cafe","conditions":{"required_flags":["items_test_job"]}}
            state.location_id="loc_cafe_backroom"
            assert not work_wardrobe_enter("cafe",state)
            state.story.flags.add("items_test_job")
            snapshot=dict(state.wardrobe.equipped)
            assert work_wardrobe_enter("cafe",state)
            assert not wardrobe_equip("waitress_costume",state=state)[0]
            state.story.flags.add("cafe_waitress_costume_work_unlocked")
            assert wardrobe_equip("waitress_costume",state=state)[0]
            assert wardrobe_owns("waitress_costume",state)
            register_external_item("nurse_costume","cafe","loc_cafe_backroom",state)
            assert not item_owns("nurse_costume",state)
            assert "nurse_costume" in wardrobe_available_items(state)
            assert work_wardrobe_exit_and_restore(state)
            assert state.wardrobe.equipped==snapshot
            state.location_id="loc_apartment_5_room"
            assert "nurse_costume" not in wardrobe_available_items(state)
            for slot in OUTFIT_SLOTS: assert wardrobe_unequip(slot,state)
            assert all(value is None for value in state.wardrobe.equipped.values())
            employee=create_new_game_state(); employee.player.openness.rank=3
            employee.location_id="loc_cafe_backroom"
            employee.story.flags.update(("items_test_job","cafe_waitress_costume_work_unlocked"))
            register_external_item("waitress_costume","cafe","loc_cafe_backroom",employee)
            assert not wardrobe_can_equip("waitress_costume",state=employee)[0]
            before=dict(employee.wardrobe.equipped)
            assert work_wardrobe_enter("cafe",employee)
            assert wardrobe_equip("waitress_costume",state=employee)[0]
            assert not item_owns("waitress_costume",employee)
            assert move_to("loc_cafe_hall",employee)[0]
            assert employee.wardrobe.equipped==before and employee.wardrobe.active_workplace is None
        finally:
            WARDROBE_ACCESS.clear(); WARDROBE_ACCESS.update(original)

    def items_test_status_tests():
        state=create_new_game_state()
        assert status_hud_entries(state)==[]
        state.player.energy=1; state.player.mood=-1; state.player.arousal=10
        assert {entry[0] for entry in status_hud_entries(state)}=={"tired","mood","arousal_red"}
        state.player.energy=2; state.player.mood=0; state.player.arousal=2
        assert status_hud_entries(state)==[]
        # Fixture thresholds exercise both internal levels without approving production balance.
        original=store.NUTRITION_THRESHOLDS
        try:
            store.NUTRITION_THRESHOLDS={"sated":60,"hungry":120,"very_hungry":240}
            for elapsed in (120,240):
                state.nutrition_elapsed_minutes=elapsed
                assert [entry[0] for entry in status_hud_entries(state)]==["hungry"]
                assert status_hud_entries(state)[0][1]=="Голодна"
        finally: store.NUTRITION_THRESHOLDS=original

    def items_test_shop_tests():
        state = create_new_game_state()
        state.location_id = "loc_shop_hall"
        before_money = state.wallet.balance
        before_items = dict(state.inventory.quantities)
        assert len(SHOP_CATALOGS["loc_shop"]) == 9 and len(SHOP_CATALOGS["loc_cafe"]) == 9
        ok, reason = fulfill_shop_purchase("loc_shop", "disposable_razor_pack_5", state)
        assert ok and reason is None
        assert state.clock.total_minutes == 8 * 60 + 15
        assert state.wallet.balance == before_money - 300
        assert inventory_has("disposable_razor_pack_5", 5, state)
        state.wallet.balance = 0
        ok, reason = fulfill_shop_purchase("loc_shop", "food_kit_breakfast", state)
        assert not ok and reason == "Недостаточно денег"

    def items_test_nutrition_timestamp_tests():
        state = create_new_game_state()
        state.location_id = "loc_apartment_5_kitchen"
        state.clock.hour, state.clock.minute = 8, 0
        assert state.last_full_meal_at is None
        result = execute_action("action_eat_full_meal", state)
        assert result.success
        assert state.last_full_meal_at == datetime.datetime(2026, 8, 29, 8, 20)

    def items_test_nutrition_effect_tests():
        state = create_new_game_state()
        state.location_id = "loc_apartment_5_room"
        state.player.fitness.rank = 1
        state.nutrition_elapsed_minutes = 120
        original = store.NUTRITION_THRESHOLDS
        try:
            store.NUTRITION_THRESHOLDS = {"sated": 60, "hungry": 120, "very_hungry": 240}
            exercise = ACTIONS["action_exercise"]
            assert nutrition_state(state) == "hungry"
            assert calculate_action_energy_cost(exercise, state) == 3
            state.nutrition_elapsed_minutes = 240
            assert nutrition_state(state) == "very_hungry"
            assert not execute_action("action_exercise", state).success
            state.location_id = "loc_apartment_5_kitchen"
            assert execute_action("action_eat_full_meal", state).success
            assert nutrition_state(state) == "sated"
        finally:
            store.NUTRITION_THRESHOLDS = original

    def items_test_nutrition_config_tests():
        original = store.NUTRITION_THRESHOLDS
        try:
            assert configure_nutrition_thresholds({"sated": 60, "hungry": 120, "very_hungry": 240})["hungry"] == 120
            for invalid in ({"sated": 60, "hungry": 240, "very_hungry": 120}, {"sated": -1, "hungry": 60, "very_hungry": 120}):
                try:
                    configure_nutrition_thresholds(invalid)
                    assert False
                except ValueError:
                    pass
            assert configure_nutrition_thresholds(None) is None
        finally:
            store.NUTRITION_THRESHOLDS = original

    def items_test_approved_food_balance_tests():
        state = create_new_game_state()
        assert NUTRITION_THRESHOLDS == {"sated": 300, "hungry": 300, "very_hungry": 360}
        advance_time(300, "test", state)
        assert nutrition_state(state) == "hungry"
        advance_time(60, "test", state)
        assert nutrition_state(state) == "very_hungry"
        state.nutrition_elapsed_minutes = 0
        advance_time(300, "action_sleep", state)
        assert state.nutrition_elapsed_minutes == 60 and nutrition_state(state) == "sated"
        state.nutrition_elapsed_minutes = 360
        inventory_add("yogurt_granola", state=state)
        assert inventory_use("yogurt_granola", state)
        assert state.nutrition_elapsed_minutes == 120
        inventory_add("energy_drink", 2, state)
        state.player.energy = 5
        assert inventory_use("energy_drink", state)
        assert state.player.energy == 7 and item_use_reason("energy_drink", state)
        advance_time(720, "test", state)
        assert item_use_reason("energy_drink", state) is None
        state.wallet.balance = 10000
        state.nutrition_elapsed_minutes = 360
        ok, reason = fulfill_shop_purchase("loc_cafe", "cafe_chicken_pasta", state)
        assert ok and reason is None and state.nutrition_elapsed_minutes == 0
        assert not inventory_has("cafe_chicken_pasta", 1, state)
        inventory_add("food_kit_breakfast", state=state)
        state.location_id = "loc_apartment_5_kitchen"
        state.nutrition_elapsed_minutes = 360
        before_time = state.clock.total_minutes
        assert execute_action("action_prepare_meal", state).success
        assert state.clock.total_minutes == before_time + 30 and inventory_has("prepared_home_meal", 1, state)
        assert execute_action("action_eat_full_meal", state).success
        assert state.nutrition_elapsed_minutes == 0
        assert "Комплектов: 0" in hud_action_hint(ACTIONS["action_prepare_meal"], check_action("action_prepare_meal", state)[1], state)
        assert "Готовых порций: 1" in hud_action_hint(ACTIONS["action_eat_full_meal"], [], create_new_game_state())

    def items_test_migration_tests():
        state=create_new_game_state(); state.schema_version=5
        state.wardrobe.work_storage={"loc_cafe_backroom":["nurse_costume"]}
        before=dict(state.wardrobe.equipped); owned=set(state.wardrobe.owned)
        state.story.pending_action="action_unpack_luggage"
        ensure_current_schema(state)
        assert state.schema_version==SCHEMA_VERSION and not hasattr(state.wardrobe,"work_storage")
        assert state.wardrobe.owned==owned and state.wardrobe.equipped==before
        assert state.inventory.external_items["nurse_costume"]["location"]=="loc_cafe_backroom"
        assert state.story.pending_action=="action_unpack_luggage"
        ensure_current_schema(state)
        assert state.wardrobe.owned==owned

testsuite items_body_wardrobe:
    testcase catalog:
        $ items_test_catalog_tests()
    testcase body_states:
        $ items_test_body_tests()
    testcase action_event_quest:
        $ items_test_action_event_tests()
    testcase wardrobe_contexts:
        $ items_test_wardrobe_tests()
    testcase status_thresholds:
        $ items_test_status_tests()
    testcase shop_backend:
        $ items_test_shop_tests()
    testcase nutrition_timestamp:
        $ items_test_nutrition_timestamp_tests()
    testcase nutrition_effects:
        $ items_test_nutrition_effect_tests()
    testcase nutrition_config:
        $ items_test_nutrition_config_tests()
    testcase approved_food_balance:
        $ items_test_approved_food_balance_tests()
    testcase migration:
        $ items_test_migration_tests()
    testcase inventory_runtime:
        $ renpy.store.game_state=create_new_game_state()
        $ game_state.player.openness.rank=3
        $ inventory_add("remote_toy")
        $ inventory_add("vibrator")
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        run Show("inventory_screen")
        pause 0.2
        click "Интимное"
        click "Дистанционный носимый вибратор"
        click "Вставить"
        assert eval (body_item_active("remote_toy"))
        screenshot "items_test_inventory_body.png"
        click "Вынуть"
        assert eval (not body_item_active("remote_toy"))
        run Hide("inventory_screen")
        run Hide("game_hud")
    testcase wardrobe_runtime:
        $ renpy.store.game_state=create_new_game_state()
        $ game_state.player.openness.rank=3
        $ inventory_add("waitress_costume")
        $ _prepare_visual_gameplay_context()
        run Show("wardrobe_screen")
        pause 0.2
        click "Костюм официантки"
        click "Надеть"
        assert eval (game_state.wardrobe.equipped["special"]=="waitress_costume")
        screenshot "items_test_wardrobe.png"
        click "Снять выбранное"
        assert eval (game_state.wardrobe.equipped["special"] is None)
        run Hide("wardrobe_screen")
    testcase save_roundtrip:
        $ renpy.store.game_state=create_new_game_state()
        $ game_state.player.openness.rank=3
        $ inventory_add("remote_toy")
        $ set_body_item("remote_toy",True)
        $ items_test_slot="items-test-" + str(__import__("uuid").uuid4())
        $ renpy.save(items_test_slot, include_screenshot=False)
        $ set_body_item("remote_toy",False)
        $ restored=renpy.get_save_data(items_test_slot)["game_state"]
        $ ensure_current_schema(restored)
        assert eval (body_item_active("remote_toy",restored))
        assert eval (inventory_has("remote_toy",1,restored))
        $ moved, reason=move_to("loc_apartment_5_hallway",restored)
        assert eval (moved)
        assert eval (body_item_active("remote_toy",restored))
        $ renpy.unlink_save(items_test_slot)
    testcase status_runtime:
        $ renpy.store.game_state=create_new_game_state()
        $ game_state.player.openness.rank=3
        $ game_state.player.energy=1
        $ game_state.player.mood=-1
        $ game_state.player.arousal=10
        $ inventory_add("remote_toy")
        $ set_body_item("remote_toy",True)
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        pause 0.2
        assert eval (len(status_hud_entries())==4)
        screenshot "items_test_status.png"
        run Hide("game_hud")
    testcase shop_runtime:
        $ renpy.store.game_state=create_new_game_state()
        $ game_state.location_id="loc_shop_hall"
        $ _prepare_visual_gameplay_context()
        run Show("shop_screen")
        pause 0.2
        assert eval (renpy.get_screen("shop_screen") is not None)
        screenshot "items_test_shop.png"
        run Hide("shop_screen")
        run Show("shop_screen", catalog_id="loc_cafe", title="Меню кафе")
        pause 0.2
        screenshot "items_test_cafe.png"
        run Hide("shop_screen")
    testcase commerce_hud_one_click:
        $ renpy.store.game_state=create_new_game_state()
        $ game_state.location_id="loc_shop_hall"
        $ _prepare_visual_gameplay_context()
        run Show("game_hud")
        pause 0.2
        click pos (1834, 944)
        assert eval (renpy.get_screen("shop_screen") is not None)
        run Hide("shop_screen")
        run Hide("game_hud")
        $ game_state.location_id="loc_cafe_hall"
        run Show("game_hud")
        pause 0.2
        click pos (1834, 944)
        assert eval (renpy.get_screen("shop_screen") is not None)
        run Hide("shop_screen")
        run Hide("game_hud")
