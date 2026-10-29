# Локации — карта раздела

Канонические карточки конкретных игровых пространств и связанных пространственных сущностей. Для новой карточки использовать [`../../templates/LOCATION_TEMPLATE.md`](../../templates/LOCATION_TEMPLATE.md).

## Источник топологии

**Единственный канонический источник состава карты, вложенности пространств, существования переходов и направления стрелок — [`../../graphs/map.drawio`](../../graphs/map.drawio).**

Карточки ниже хранят назначение, визуальные факты, действия, NPC, состояния и доступность. Поля `access_state` / `access_condition` не меняют топологию карты: закрытая или еще не разработанная локация все равно может существовать на `map.drawio`.

## Спальный район

- [`loc_residential_district_main.md`](loc_residential_district_main.md) — основной экран района.

### Дом на ул. Лесная, дом 1

- [`apartment_building.md`](apartment_building.md) — жилой дом.
- [`building_yard.md`](building_yard.md) — двор дома.
- [`loc_playground.md`](loc_playground.md) — детская площадка.
- [`entrance_1.md`](entrance_1.md) — первый подъезд как группа пространств.
  - [`entrance_1_floor_1.md`](entrance_1_floor_1.md) — первый этаж;
  - [`entrance_1_floor_2.md`](entrance_1_floor_2.md) — второй этаж;
  - [`entrance_1_floor_3.md`](entrance_1_floor_3.md) — третий этаж;
  - [`entrance_1_floor_4.md`](entrance_1_floor_4.md) — четвертый этаж;
  - [`entrance_1_floor_5.md`](entrance_1_floor_5.md) — пятый этаж;
  - [`building_roof.md`](building_roof.md) — крыша;
  - [`building_basement.md`](building_basement.md) — подвал.
- [`entrance_2.md`](entrance_2.md) — второй подъезд как группа пространств.
  - [`entrance_2_floor_1.md`](entrance_2_floor_1.md) — первый этаж второго подъезда.

### Квартиры первого подъезда

Минимальные карточки существуют для всех квартир, уже показанных на карте:

- [`apartment_1.md`](apartment_1.md) — квартира №1;
- [`apartment_2.md`](apartment_2.md) — квартира №2;
- [`apartment_3.md`](apartment_3.md) — квартира №3;
- [`apartment_4.md`](apartment_4.md) — квартира №4;
- [`apartment_5.md`](apartment_5.md) — квартира Насти и Маши;
- [`apartment_6.md`](apartment_6.md) — квартира Ники;
- [`apartment_7.md`](apartment_7.md) — квартира Анны;
- [`apartment_8.md`](apartment_8.md) — квартира №8;
- [`apartment_9.md`](apartment_9.md) — квартира №9;
- [`apartment_10.md`](apartment_10.md) — квартира №10.

### Квартира №5 — Настя и Маша

- [`apartment_5_hallway.md`](apartment_5_hallway.md) — прихожая;
- [`apartment_5_room.md`](apartment_5_room.md) — общая жилая комната;
- [`apartment_5_kitchen.md`](apartment_5_kitchen.md) — кухня;
- [`apartment_5_bathroom.md`](apartment_5_bathroom.md) — совмещенная ванная/туалет;
- [`apartment_5_balcony.md`](apartment_5_balcony.md) — балкон.

### Квартира №6 — Ника

- [`apartment_6_hallway.md`](apartment_6_hallway.md) — прихожая;
- [`apartment_6_living_room.md`](apartment_6_living_room.md) — гостиная;
- [`apartment_6_kitchen.md`](apartment_6_kitchen.md) — кухня;
- [`apartment_6_bathroom.md`](apartment_6_bathroom.md) — совмещенная ванная/туалет;
- [`apartment_6_photo_studio.md`](apartment_6_photo_studio.md) — фотостудия;
- [`apartment_6_bedroom.md`](apartment_6_bedroom.md) — спальня;
- [`apartment_6_balcony.md`](apartment_6_balcony.md) — балкон.

### Квартира №7 — Анна

- [`apartment_7_hallway.md`](apartment_7_hallway.md) — прихожая;
- [`apartment_7_room.md`](apartment_7_room.md) — общая комната;
- [`apartment_7_kitchen.md`](apartment_7_kitchen.md) — кухня;
- [`apartment_7_bathroom.md`](apartment_7_bathroom.md) — совмещенная ванная/туалет;
- [`apartment_7_balcony.md`](apartment_7_balcony.md) — балкон.

### Мини-маркет

- [`loc_shop.md`](loc_shop.md) — мини-маркет как группа пространств;
- [`loc_shop_hall.md`](loc_shop_hall.md) — торговый зал;
- [`loc_shop_storage.md`](loc_shop_storage.md) — подсобка/склад;
- [`loc_shop_manager_office.md`](loc_shop_manager_office.md) — кабинет управляющего.

### Кафе

- [`loc_cafe.md`](loc_cafe.md) — кафе как группа пространств;
- [`loc_cafe_hall.md`](loc_cafe_hall.md) — зал;
- [`loc_cafe_aslan_office.md`](loc_cafe_aslan_office.md) — кабинет Аслана;
- [`loc_cafe_backroom.md`](loc_cafe_backroom.md) — подсобка/гардероб;
- [`loc_cafe_toilet.md`](loc_cafe_toilet.md) — туалет;
- [`loc_cafe_kitchen.md`](loc_cafe_kitchen.md) — кухня.

### Районный колледж (ID `loc_masha_school*`)

- [`loc_masha_school.md`](loc_masha_school.md) — колледж как группа пространств;
- [`loc_masha_school_entrance.md`](loc_masha_school_entrance.md) — вход;
- [`loc_masha_school_floor_1.md`](loc_masha_school_floor_1.md) — первый этаж;
- [`loc_masha_school_sports_ground.md`](loc_masha_school_sports_ground.md) — спортивная площадка.

### Транспорт

- [`loc_bus_stop_residential.md`](loc_bus_stop_residential.md) — системная автобусная точка маршрутизации. Исторический `loc_...` ID карточки сохранен ради стабильности ссылок, но сущность не является `location_id` пребывания игрока.

## Район медицинского института

Гиперкластер описан в [`../hyperclusters/hc_university.md`](../hyperclusters/hc_university.md); его стабильный системный ID — `hc_university`, а игровое название — «Район медицинского института».

- [`loc_medical_institute_area.md`](loc_medical_institute_area.md) — основной экран района;
- [`loc_medical_institute_sports_ground.md`](loc_medical_institute_sports_ground.md) — спортивная площадка;
- [`loc_medical_institute_building_floor_1.md`](loc_medical_institute_building_floor_1.md) — первый этаж учебного корпуса;
- [`loc_medical_institute_dormitory.md`](loc_medical_institute_dormitory.md) — студенческое общежитие;
- [`loc_medical_institute_admissions.md`](loc_medical_institute_admissions.md) — кабинет приемной комиссии.

## Правило минимальных карточек

Если пространство уже существует на `map.drawio`, для него создается хотя бы минимальная карточка. Неутвержденные свойства не додумываются: используются `status: draft`, подходящий `access_state` и `TBD` в неизвестных полях. Видимые подписи вроде «(закрыто)» на карте не используются как система доступности.

Полная change-impact карта: [`../../REPOSITORY_MAP.md`](../../REPOSITORY_MAP.md).

## Центральный район

- [`loc_central_park.md`](loc_central_park.md) — Парк.
- [`loc_central_street.md`](loc_central_street.md) — Центральная улица.
- [`loc_central_bank.md`](loc_central_bank.md) — Банк.
- [`loc_central_forest.md`](loc_central_forest.md) — Лес.
- [`loc_central_lake.md`](loc_central_lake.md) — Озеро.
- [`loc_central_health_beauty_center.md`](loc_central_health_beauty_center.md) — Центр здоровья и красоты.
- [`loc_central_health_beauty_center_reception.md`](loc_central_health_beauty_center_reception.md) — Ресэпшен.
- [`loc_central_health_beauty_center_massage_room.md`](loc_central_health_beauty_center_massage_room.md) — Массажный кабинет.
- [`loc_central_health_beauty_center_solarium.md`](loc_central_health_beauty_center_solarium.md) — Кабинет салярия.
- [`loc_central_health_beauty_center_hair_salon.md`](loc_central_health_beauty_center_hair_salon.md) — Парикмахерская.
- [`loc_central_health_beauty_center_sauna.md`](loc_central_health_beauty_center_sauna.md) — Сауна.
- [`loc_central_health_beauty_center_gym.md`](loc_central_health_beauty_center_gym.md) — Спортивный зал.
- [`loc_central_health_beauty_center_changing_room_shower.md`](loc_central_health_beauty_center_changing_room_shower.md) — Раздевалка с душевой.
- [`loc_central_shopping_center.md`](loc_central_shopping_center.md) — Торговый центр.
- [`loc_central_shopping_center_floor_2.md`](loc_central_shopping_center_floor_2.md) — 2 этаж.
- [`loc_central_shopping_center_floor_2_boutique_repair_03.md`](loc_central_shopping_center_floor_2_boutique_repair_03.md) — Бутик на ремонте.
- [`loc_central_shopping_center_floor_2_boutique_repair_06.md`](loc_central_shopping_center_floor_2_boutique_repair_06.md) — Бутик на ремонте.
- [`loc_central_shopping_center_floor_1_sex_shop.md`](loc_central_shopping_center_floor_1_sex_shop.md) — Секс-шоп.
- [`loc_central_shopping_center_floor_1.md`](loc_central_shopping_center_floor_1.md) — 1 этаж.
- [`loc_central_shopping_center_floor_1_grocery.md`](loc_central_shopping_center_floor_1_grocery.md) — Продукты.
- [`loc_central_shopping_center_floor_1_appliances.md`](loc_central_shopping_center_floor_1_appliances.md) — Бытовая техника.
- [`loc_central_shopping_center_floor_1_clothing_store.md`](loc_central_shopping_center_floor_1_clothing_store.md) — Одежда.
- [`loc_central_shopping_center_floor_1_fitting_room.md`](loc_central_shopping_center_floor_1_fitting_room.md) — Примерочная.
- [`loc_central_shopping_center_floor_1_boutique_repair_01.md`](loc_central_shopping_center_floor_1_boutique_repair_01.md) — Бутик на ремонте.
- [`loc_central_shopping_center_floor_2_boutique_repair_05.md`](loc_central_shopping_center_floor_2_boutique_repair_05.md) — Бутик на ремонте.
- [`loc_central_shopping_center_floor_2_boutique_repair_04.md`](loc_central_shopping_center_floor_2_boutique_repair_04.md) — Бутик на ремонте.
- [`loc_central_shopping_center_floor_2_boutique_repair_02.md`](loc_central_shopping_center_floor_2_boutique_repair_02.md) — Бутик на ремонте.
- [`loc_central_shopping_center_floor_2_boutique_repair_01.md`](loc_central_shopping_center_floor_2_boutique_repair_01.md) — Бутик на ремонте.
