# Intimate Language System — единая семантическая модель

## 1. Назначение

Система связывает физическую сцену и ее языковую реализацию. Она не является генератором сексуального поведения и не определяет допустимость события сама по себе.

Основная цепочка:

BODY → STATE → CHANGE → SENSATION → ACTION → CONTEXT → PRACTICE → RESPONSE → OUTCOME → LANGUAGE → CHARACTER_PROFILE

Каждый следующий слой может уточнять предыдущий, но не переписывать его.

## 2. Слои

### BODY

Физическая сущность или зона: breast, nipple, areola, buttock, anus, vulva, labia, clitoris, vagina, pubis, groin, inner_thigh и т. д.

### STATE

Объективное состояние в конкретный момент: wet, dry, hard, soft, swollen, tense, relaxed, reddened, irritated, sensitive, stretched.

### CHANGE

Изменение состояния: harden, soften, swell, moisten, dry, relax, tighten, stretch, redden, return_to_normal.

### SENSATION

Субъективное ощущение персонажа: pleasure, pain, pressure, warmth, cold, wetness, tickling, itch, burning, tingling, pulsation, overstimulation.

### ACTION

Наблюдаемое физическое действие: touch, stroke, rub, press, squeeze, pinch, pull, scratch, bite, kiss, lick, suck, spread, insert, remove, restrain, watch, show и т. д.

### CONTEXT

Не действие, а параметры смысла:

- ACTOR — кто делает;
- TARGET_PERSON — с чьим телом;
- BODY_TARGET — конкретная часть тела;
- CONTACT_OBJECT — пальцы, ладонь, губы, предмет и т. п.;
- INTENSITY — сила воздействия;
- INTENT — зачем действие совершается;
- CONSENT — статус согласия;
- RISK — риск повреждения;
- PRIVACY — приватность и вероятность быть замеченной;
- AWARENESS — знает ли участник о наблюдении/демонстрации.

### PRACTICE

Контекст нескольких действий: masturbation, clitoral_stimulation, bondage, pain_play, voyeurism, exhibition, fetish_play, toy_play, orgasm_control и т. д.

Практика не подменяет конкретные ACTION. Фраза «она мастурбировала» сообщает меньше физической информации, чем установленная последовательность действий.

### RESPONSE

Непроизвольная или непосредственная реакция: sharp_inhale, tremble, tense, relax, pull_away, lean_in, moan, gasp, laugh, genital_pulsation и т. д.

### OUTCOME

Результат эпизода: arousal_increase, pleasure, discomfort, pain, orgasm, no_orgasm, overstimulation, relaxation, marks, irritation, desire_to_continue, desire_to_stop.

### LANGUAGE

Конкретные русские слова и выражения с регистром и оттенком.

### CHARACTER_PROFILE

Выбор из LANGUAGE для конкретного персонажа. Основной источник этого выбора — canon-карточка персонажа.

## 3. Стабильные ID

Формат ID:

- body.genitals_general
- body.intimate_area
- body.breast
- body.nipple
- body.areola
- body.buttock
- body.anus
- body.vulva
- body.labia
- body.labia_majora
- body.labia_minora
- body.vulvar_cleft
- body.clitoris
- body.clitoris_glans
- body.clitoral_hood
- body.vaginal_opening
- body.vagina
- body.pubis
- body.pubic_hair
- body.groin
- body.inner_thigh
- body.perineum
- body.urethra
- body.urethral_opening
- body.hymen
- body.cervix
- body.uterus
- body.ovary
- body.fallopian_tube

- state.wet
- state.hard
- state.swollen
- change.moisten
- change.harden

- sensation.pleasure
- sensation.pain
- sensation.itch
- sensation.pulsation

- action.touch
- action.stroke
- action.rub
- action.squeeze
- action.pinch
- action.spread
- action.insert
- action.restrain
- action.watch
- action.show

- practice.masturbation
- practice.bondage
- practice.pain_play
- practice.exhibition
- practice.voyeurism

ID описывает смысл, а не конкретное русское слово.

## 4. Регистры языка

Одна форма может иметь несколько тегов.

| Код | Значение |
|---|---|
| ANAT | анатомическое / медицинское |
| NEUT | нейтральное общеупотребительное |
| COLL | разговорное |
| AFF | уменьшительное / ласкательное |
| CHILD | детско-бытовое |
| JOKE | шутливое / игровое |
| EUPH | эвфемистическое / уклончивое |
| EROT | явно эротически окрашенное |
| SLANG | жаргонное |
| VULG | грубое / вульгарное |
| OBSC | обсценное / матерное |
| DEROG | уничижительное / объективационное |

### Разговорный default surface language

Для реплик, внутренней речи и обычного неформального общения **дефолт Nastya Story — естественный современный разговорный русский**, а не анатомически или терминологически наиболее точная форма.

- Точный BODY/STATE/ACTION ID нужен для внутренней семантики и не обязан совпадать с произнесенным словом.
- `ANAT` и технически точные формы не становятся предпочтительными только потому, что они точнее описывают BODY target. Их выбирать при медицинском, научном, формальном, системном контексте, при реальной необходимости снять неоднозначность либо если такой регистр закреплен за персонажем.
- `NEUT` означает отсутствие грубой/эротической окраски, но **не гарантирует бытовую разговорность**. Форма может быть нейтральной и при этом заметно терминологической.
- Если индивидуальная интимная лексика персонажа `TBD`, он наследует общий разговорный default проекта. `TBD` не разрешает придумывать ему устойчивое любимое слово, но и не переводит его автоматически в `ANAT`/technical register.
- В репликах и внутренней речи допустимо вообще не называть анатомическую структуру, если смысл остается ясным: `внутрь`, `между ног`, `там`, `рядом с клитором`, `по губкам` и другие контекстные реализации могут точнее соответствовать естественной речи, чем термин из таблицы.
- **Это разрешение не распространяется на авторскую речь.** Если часть тела находится в фокусе действия, повествование ее называет; пространственные замены `впереди`, `сзади`, `там внизу` и подобные вместо названия запрещены. Каким словом называть — [`CHARACTER_LANGUAGE_PROFILE.md`](CHARACTER_LANGUAGE_PROFILE.md) §5.
- В потребительском, дружеском и эротическом объяснении предмета или действия обычно предпочтительнее язык **ощущений и понятных действий** (`прижать`, `провести`, `вставить внутрь`, `становится чувствительно`, `ощущается давление/наполненность`) вместо медицинской классификации тела.

Семантическая точность проверяется **до** surface wording: разговорная форма может быть шире точного BODY target, если контекст не меняет физический факт и не создает ложной конкретности.

## 5. Точность термина

- exact — конкретная анатомическая структура;
- broad — область или несколько структур;
- contextual — смысл зависит от контекста;
- figurative — образное название, не анатомический термин.

Например, «вульва» — exact/broad в зависимости от задачи, «писька» — broad, «киска» — broad/contextual, «дырочка» — contextual.

## 6. Шкала грубости

| Уровень | Значение |
|---:|---|
| 0 | медицинское / полностью нейтральное |
| 1 | обычное бытовое |
| 2 | разговорное |
| 3 | фамильярное / заметно сексуализированное |
| 4 | грубое / вульгарное |
| 5 | матерное или резко уничижительное |

Ласкательность хранится отдельно. «Жопочка» может одновременно иметь высокую ласкательность и грубость 4.

## 7. Интенсивность действия

| Уровень | Значение |
|---:|---|
| 0 | почти нет воздействия |
| 1 | очень легкое |
| 2 | легкое |
| 3 | заметное |
| 4 | сильное |
| 5 | грубое / потенциально болезненное |

Уровень 5 не означает автоматически сексуальность, насилие или травму.

## 8. INTENT

Базовые значения:

HYGIENE, MEDICAL, CHECKING, DRESSING, ACCIDENTAL, COMFORT, PLAYFUL, AFFECTION, CURIOSITY, SEXUAL, MASTURBATION, PARTNER_STIMULATION, DOMINATION, SUBMISSION, PAIN_PLAY, HUMILIATION_PLAY, PERFORMANCE, PHOTOGRAPHY, OBSERVATION.

Одинаковое движение может иметь совершенно разный смысл при разных INTENT.

## 9. CONSENT

- SELF — действие с собственным телом;
- CONSENSUAL — согласованное;
- NEGOTIATED — заранее проговоренное;
- SPONTANEOUS_CONSENSUAL — согласие возникло в ситуации;
- UNCLEAR — сценой не установлено;
- WITHDRAWN — согласие отозвано;
- NONCONSENSUAL — согласия нет.

Для restraint, pain play, domination, humiliation, exhibition, voyeurism и recording это поле особенно важно.

Семантическая классификация NONCONSENSUAL не делает событие сексуальной игрой и не смягчает его смысл.

## 10. RISK и повреждение

RISK:

NONE, LOW, MODERATE, HIGH, INJURY.

PAIN и INJURY не тождественны. Боль — ощущение; повреждение — объективное состояние.

Практики с реальным риском травмы могут присутствовать в справочнике как распознаваемые категории, но справочник не превращается в инструкцию по их выполнению.

## 11. Participant meaning и Player Visual Access

Объективно видимая часть тела не означает, что участник считает ситуацию эротической.

Аналогично:

- нагота ≠ exhibition;
- взгляд ≠ voyeurism;
- влажность ≠ доказательство сексуального намерения;
- боль ≠ BDSM;
- связывание ≠ автоматически насилие;
- стоны ≠ автоматически оргазм;
- необычное действие ≠ постоянный фетиш персонажа.

Эти значения устанавливаются CONTEXT и сценой.

## 12. Порядок применения при написании

1. Установить физическую сцену по Writing Pipeline.
2. Определить применимые BODY / STATE / CHANGE / ACTION.
3. Отдельно определить SENSATION только для того персонажа, который ее реально испытывает.
4. Определить CONTEXT: intent, consent, intensity, risk, awareness/privacy.
5. Если требуется — классифицировать PRACTICE.
6. Выбрать объективные RESPONSE и OUTCOME, не превращая их в обязательный шаблон.
7. Только после этого выбрать LANGUAGE.
8. Для реплики/внутренней речи применить canon-карточку говорящего; для авторской речи — [`CHARACTER_LANGUAGE_PROFILE.md`](CHARACTER_LANGUAGE_PROFILE.md) §5.
9. Проверить, что синоним не изменил физический факт или степень конкретности.

## 13. Что система не канонизирует

Наличие записи в справочнике не означает:

- что Настя или другой персонаж знает термин;
- что персонаж использует термин в речи;
- что практика ему нравится;
- что он готов на действие;
- что действие доступно по progression;
- что существует соответствующая механика;
- что событие уже произошло в каноне.

Для этого нужны соответствующие владельцы фактов: character canon, systems, scene, quest, runtime.
