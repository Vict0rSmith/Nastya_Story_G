# Ядро домена: самопроверка реестров и default game_state.
# Все блоки core_*.rpy исполняются на init -100 в порядке имен файлов.

init -100 python:
    def run_domain_self_tests(notify=False):
        assert set(LOCATIONS) == {key for key, node in WORLD_MAP.items() if node["kind"] == "location"} | {"loc_masha_school"}
        assert "loc_apartment_5_hallway" not in LOCATIONS["loc_residential_district_main"]["transitions"]
        for source, node in LOCATIONS.items():
            assert all(target in LOCATIONS for target in node["transitions"])
        assert "route_bus_stop_residential" not in LOCATIONS
        for entries in SCHEDULES.values(): assert all(entry["location"] in LOCATIONS for entry in entries)
        for action in ACTIONS.values(): assert all(location_id in LOCATIONS for location_id in action.locations)
        if notify: renpy.notify("Самопроверка пройдена")
        return True

default game_state = create_new_game_state()
