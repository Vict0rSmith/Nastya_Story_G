init -45 python:
    # Owner-approved dates and UI prompts; authored replies remain unapproved.
    PHONE_CASUAL_COOLDOWN_MINUTES = None
    # Annual holidays, not transferred days off; source: mintrud.gov.ru/labour/relationship/351.
    CALENDAR_EVENTS = [
        dict(id="ru:new_year:%s" % day, month=1, day=day, title="Новогодние каникулы", public=True)
        for day in (1, 2, 3, 4, 5, 6, 8)
    ] + [
        dict(id="ru:christmas", month=1, day=7, title="Рождество Христово", public=True),
        dict(id="ru:defender", month=2, day=23, title="День защитника Отечества", public=True),
        dict(id="ru:womens_day", month=3, day=8, title="Международный женский день", public=True),
        dict(id="ru:spring_labour", month=5, day=1, title="Праздник Весны и Труда", public=True),
        dict(id="ru:victory", month=5, day=9, title="День Победы", public=True),
        dict(id="ru:russia", month=6, day=12, title="День России", public=True),
        dict(id="ru:unity", month=11, day=4, title="День народного единства", public=True),
        # Calendar projections of the owner-approved character canon; known from the start.
        dict(id="birthday:nastya", month=5, day=15, title="День рождения: Настя", public=True),
        dict(id="birthday:masha", month=8, day=1, title="День рождения: Маша", public=True),
    ]
    PHONE_MESSAGE_OPTIONS = {
        "how_are_you": {"text": "Как дела?", "kind": "casual", "responses": []},
        "where_are_you": {"text": "Ты где?", "kind": "casual", "responses": []},
        "what_are_you_doing": {"text": "Что делаешь?", "kind": "casual", "responses": []},
    }
