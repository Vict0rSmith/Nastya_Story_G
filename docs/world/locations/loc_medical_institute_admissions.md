---
id: loc_medical_institute_admissions
entity_type: location
status: approved_partial
map_node_id: loc_medical_institute_admissions
access_state: conditional
access_condition: "2026-08-29 13:00-18:00 for first-day document submission"
objects: []
actions: []
npcs_possible: []
related_quests: [quest_2026_08_29_first_normal_day]
---
# Медицинский институт — кабинет приемной комиссии

> Топология и направления переходов задаются только [`../../graphs/map.drawio`](../../graphs/map.drawio).

## Назначение
Кабинет, где Настя завершает оформление поступления и передает документы.

## 29 августа
Приемная комиссия работает с 13:00 до 18:00. Подача документов — обязательная цель первого управляемого дня.

После успешной подачи устанавливается `university_documents_submitted` и разблокируется университетское приложение в телефоне.

## Визуальный паспорт
`TBD`.

## Условия доступа
29 августа доступ определяется рабочим окном 13:00–18:00 и защитой сюжетного дедлайна из [`../../systems/UNIVERSITY_SPEC.md`](../../systems/UNIVERSITY_SPEC.md). Дальнейшая политика доступа — `TBD`.

## Переходы
См. [`../../graphs/map.drawio`](../../graphs/map.drawio).
