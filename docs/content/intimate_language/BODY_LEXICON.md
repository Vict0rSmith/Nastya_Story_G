# Body Lexicon — современная телесная и интимная лексика

## 1. Правило отбора

Включаются современные слова и выражения, которые реально могут понадобиться повествованию, внутренней речи или диалогам Nastya Story. Редкие, устаревшие, региональные и словарно-экзотические формы не включаются без отдельного персонажного основания.

Теги регистров определены в [INTIMATE_LANGUAGE_SYSTEM.md](INTIMATE_LANGUAGE_SYSTEM.md).

Таблица описывает **семантические варианты**, а не рекомендует самое анатомически точное слово для диалога. В обычной речи действует разговорный default из `INTIMATE_LANGUAGE_SYSTEM.md`: техническая точность BODY target сначала устанавливается внутри системы, после чего выбирается естественная для ситуации формулировка. `NEUT` не следует читать как «обычное разговорное слово»: некоторые нейтральные формы остаются терминологически маркированными.

Особенно это относится к формам вроде `вульва`, `влагалище`, `наружные половые органы`, `вагинальный канал`: они нужны как точные анатомические обозначения, но **не являются дефолтом дружеской, бытовой или эротической речи**. В таком контексте персонаж с неуточненным профилем обычно использует простой разговорный вариант либо контекстное описание действия (`внутрь`, `между ног`, `по губкам`, `к клитору`) без обязательного называния структуры.

## 2. Общие обозначения интимной области

| Форма | Target | Регистр | Точность | Комментарий |
|---|---|---|---|---|
| гениталии | body.genitals_general | ANAT/NEUT | broad | общее |
| женские гениталии | body.genitals_general | ANAT/NEUT | broad | общее |
| половые органы | body.genitals_general | ANAT/NEUT | broad | общее |
| женские половые органы | body.genitals_general | ANAT/NEUT | broad | общее |
| наружные половые органы | body.vulva | ANAT | broad | наружная область |
| наружные гениталии | body.vulva | ANAT | broad | наружная область |
| интимная зона | body.genitals_general | NEUT/EUPH | broad | включает соседние области |
| интимное место | body.genitals_general | COLL/EUPH | broad | бытовое |
| интимные места | body.genitals_general | COLL/EUPH | broad | бытовое |
| там внизу | body.genitals_general | COLL/EUPH | contextual | уклончивое |
| внизу | body.genitals_general | COLL/EUPH | contextual | уклончивое |
| между ног | body.intimate_area | COLL/EUPH | broad | пространственное |

## 3. Грудь

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| грудь | body.breast | NEUT | основное нейтральное |
| груди | body.breast | NEUT | обе груди |
| женская грудь | body.breast | NEUT | уточняющее |
| молочная железа | body.breast | ANAT | точное медицинское |
| молочные железы | body.breast | ANAT | обе |
| бюст | body.breast | NEUT | внешний объем/форма |
| сиська | body.breast | COLL | одна грудь |
| сиськи | body.breast | COLL | распространенное разговорное |
| сися | body.breast | COLL/AFF/CHILD | мягкое |
| сиси | body.breast | COLL/AFF/CHILD | мягкое |
| титька | body.breast | COLL | грубее «сиська» |
| титьки | body.breast | COLL | разговорное |
| тити | body.breast | COLL/AFF | мягче |
| сисечка | body.breast | COLL/AFF | ласкательное |
| сисечки | body.breast | COLL/AFF | ласкательное |
| титечка | body.breast | COLL/AFF | ласкательное |
| титечки | body.breast | COLL/AFF | ласкательное |
| грудка | body.breast | COLL/AFF | мягкое |
| грудки | body.breast | COLL/AFF | мягкое |
| буфера | body.breast | JOKE/COLL | обычно про заметную грудь |
| бидоны | body.breast | JOKE/VULG | обычно про большую грудь |
| дыньки | body.breast | JOKE | размер/округлость |
| дыни | body.breast | JOKE/VULG | грубее |
| арбузы | body.breast | JOKE/VULG | очень большая грудь |
| шарики | body.breast | JOKE/AFF | округлая/небольшая |
| шары | body.breast | JOKE/VULG | объективационное |
| дойки | body.breast | VULG/DEROG | грубая объективация |
| вымя | body.breast | VULG/DEROG | оскорбительное/грубо-шутливое |

Полезные зоны: верх груди, нижняя часть груди, бок груди, основание груди, складка под грудью, подгрудная складка, между грудями, ложбинка между грудями.

## 4. Сосок и ареола

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| сосок | body.nipple | ANAT/NEUT | exact |
| соски | body.nipple | ANAT/NEUT | exact |
| сосочек | body.nipple | COLL/AFF | exact |
| сосочки | body.nipple | COLL/AFF | exact |
| кончик соска | body.nipple | NEUT | описательное |
| кончики сосков | body.nipple | NEUT | описательное |
| кнопочка | body.nipple | AFF/JOKE | figurative, только при ясном контексте |
| пуговка | body.nipple | AFF/JOKE | figurative |
| ареола | body.areola | ANAT/NEUT | exact |
| ареолы | body.areola | ANAT/NEUT | exact |
| ареола соска | body.areola | ANAT | exact |
| область вокруг соска | body.areola | NEUT | описательное |
| кружок вокруг соска | body.areola | COLL/NEUT | описательное |
| кружочки вокруг сосков | body.areola | COLL/AFF | мягкое |
| темный кружок | body.areola | COLL | contextual |

Состояния вроде «твердый сосок», «набухший сосок», «торчащий сосок» принадлежат STATES_SENSATIONS_REACTIONS, а не словарю сущностей.

## 5. Ягодицы и попа

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| ягодица | body.buttock | ANAT/NEUT | exact |
| ягодицы | body.buttock | ANAT/NEUT | exact |
| попа | body.buttock | COLL/NEUT | основное бытовое |
| попка | body.buttock | COLL/AFF | ласкательное |
| попочка | body.buttock | COLL/AFF | ласкательное |
| попец | body.buttock | COLL/AFF/JOKE | шутливое |
| зад | body.buttock | COLL | разговорное |
| задница | body.buttock | COLL | грубее «зад» |
| задок | body.buttock | COLL/JOKE | мягкое |
| булки | body.buttock | COLL/JOKE | две половинки |
| булочки | body.buttock | AFF/JOKE | мягкое |
| пятая точка | body.buttock | EUPH/JOKE | эвфемизм |
| орешек | body.buttock | JOKE/EROT | про форму |
| попка-орешек | body.buttock | JOKE/EROT | про форму |
| жопа | body.buttock | VULG | грубое |
| жопка | body.buttock | VULG/AFF | грубо-ласкательное |
| жопочка | body.buttock | VULG/AFF | грубо-ласкательное |
| срака | body.buttock | VULG | грубое |
| пердак | body.buttock | VULG/DEROG | грубое/уничижительное |

Связанные зоны: межъягодичная складка, складка между ягодицами, щель между ягодицами, между половинками попы, между булками, жопная щель, подъягодичная складка, складка под попой.

## 6. Анус и анальная область

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| анус | body.anus | ANAT/NEUT | exact |
| анальное отверстие | body.anus | ANAT | exact |
| задний проход | body.anus | ANAT/NEUT | exact |
| отверстие заднего прохода | body.anus | ANAT | exact |
| задняя дырочка | body.anus | COLL/AFF | contextual, понятное |
| дырочка сзади | body.anus | COLL/AFF | contextual |
| дырочка | body.anus | body.vaginal_opening | COLL/AFF | ambiguous |
| розочка | body.anus | EROT/AFF/JOKE | figurative |
| звездочка | body.anus | EROT/AFF/JOKE | figurative |
| очко | body.anus | SLANG/VULG | грубое |
| шоколадный глаз | body.anus | JOKE/VULG | шутливо-грубое |
| шоколадный глазик | body.anus | JOKE/VULG/AFF | шутливо-грубое |
| задняя дверь | body.anus | JOKE/EUPH | образное |
| жопная дырка | body.anus | VULG | грубое |
| дырка в жопе | body.anus | VULG | грубое |
| дырка | body.anus | body.vaginal_opening | VULG/DEROG | ambiguous |

«Анал» — не название ануса; это разговорное обозначение анальной практики/секса.

## 7. Вульва и наружные женские гениталии

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| вульва | body.vulva | ANAT | exact; терминологическое, не casual default |
| наружные половые органы | body.vulva | ANAT | broad |
| наружные гениталии | body.vulva | ANAT | broad |
| писька | body.vulva | COLL | broad |
| пися | body.vulva | COLL/CHILD | broad |
| пиписька | body.vulva | COLL/CHILD | broad |
| пипися | body.vulva | COLL/CHILD | broad |
| киска | body.vulva | COLL/EROT | broad/contextual |
| писечка | body.vulva | COLL/AFF | broad |
| кисочка | body.vulva | COLL/AFF/EROT | broad/contextual |
| пиписечка | body.vulva | CHILD/AFF | broad |
| писюшка | body.vulva | CHILD/AFF | broad |
| вареник | body.vulva | JOKE/SLANG | figurative |
| пельмень | body.vulva | JOKE/SLANG | figurative |
| мохнатка | body.vulva | body.pubic_hair | JOKE/VULG | contextual |
| щелка | body.vulvar_cleft | body.vulva | COLL/EROT/VULG | contextual |
| дырка | body.vulva | body.vaginal_opening | VULG/DEROG | неточное |
| манда | body.vulva | VULG/OBSC | грубое |
| мокрощелка | body.vulva | VULG/EROT/DEROG | резко сексуализированное |
| пизда | body.vulva | body.vagina | OBSC | broad/contextual |
| пизденка | body.vulva | OBSC/AFF | broad |
| пиздочка | body.vulva | OBSC/AFF | broad |
| пиздища | body.vulva | OBSC/VULG | усилительно-грубое |

## 8. Половые губы

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| половые губы | body.labia | ANAT/NEUT | exact |
| большие половые губы | body.labia_majora | ANAT | exact |
| малые половые губы | body.labia_minora | ANAT | exact |
| губы | body.labia | COLL/NEUT | contextual |
| внешние губы | body.labia_majora | COLL | понятное, не строго анатомическое |
| внутренние губы | body.labia_minora | COLL | понятное |
| губки | body.labia | COLL/AFF | ласкательное |
| губочки | body.labia | COLL/AFF | ласкательное |
| внешние губки | body.labia_majora | COLL/AFF | ласкательное |
| внутренние губки | body.labia_minora | COLL/AFF | ласкательное |
| складки | body.labia | NEUT/EROT | описательное |
| складочки | body.labia | AFF/EROT | описательное |
| лепестки | body.labia | EROT | figurative |
| лепесточки | body.labia | AFF/EROT | figurative |
| брыли | body.labia | VULG/DEROG | уничижительное |
| шторки | body.labia | JOKE/VULG/DEROG | насмешливое |

## 9. Клитор

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| клитор | body.clitoris | ANAT/NEUT | exact |
| головка клитора | body.clitoris_glans | ANAT | exact |
| капюшон клитора | body.clitoral_hood | ANAT | exact |
| клиторальный капюшон | body.clitoral_hood | ANAT | exact |
| клит | body.clitoris | COLL/SLANG | прямое |
| клиторчик | body.clitoris | COLL/AFF | ласкательное |
| кнопка | body.clitoris | JOKE/EROT | figurative |
| кнопочка | body.clitoris | AFF/EROT | figurative |
| бугорок | body.clitoris | NEUT/EROT | описательное |
| горошинка | body.clitoris | AFF/EROT | figurative |
| бусинка | body.clitoris | AFF/EROT | figurative |
| чувствительная точка | body.clitoris | EUPH/EROT | широкое |

## 10. Лобок и лобковые волосы

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| лобок | body.pubis | ANAT/NEUT | exact |
| лобковая область | body.pubis | ANAT | broad |
| область лобка | body.pubis | NEUT | broad |
| холмик над половыми органами | body.pubis | NEUT | описательное |
| холмик над киской | body.pubis | COLL/EROT | описательное |
| холмик над писькой | body.pubis | COLL | описательное |
| лобковые волосы | body.pubic_hair | ANAT/NEUT | exact |
| волосы на лобке | body.pubic_hair | NEUT | exact |
| волоски | body.pubic_hair | NEUT/AFF | мягкое |
| растительность | body.pubic_hair | NEUT/EUPH | broad |
| куст | body.pubic_hair | COLL/JOKE | figurative |
| кустик | body.pubic_hair | COLL/AFF | figurative |
| треугольник | body.pubic_hair | COLL | форма |
| полоска | body.pubic_hair | COLL | форма |
| дорожка | body.pubic_hair | COLL | форма |
| заросли | body.pubic_hair | JOKE/VULG | густые волосы |
| шерсть | body.pubic_hair | VULG/DEROG | грубое |

«Низ живота» может включать лобок, но не является его точным синонимом.

## 11. Половая щель

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| половая щель | body.vulvar_cleft | ANAT/NEUT | exact |
| щель вульвы | body.vulvar_cleft | ANAT | exact |
| щель | body.vulvar_cleft | COLL/EROT | contextual |
| щелка | body.vulvar_cleft | COLL/EROT/VULG | contextual |
| щелочка | body.vulvar_cleft | AFF/EROT | ласкательное |
| влажная щель | body.vulvar_cleft | NEUT/EROT | state + entity |
| мокрая щель | body.vulvar_cleft | COLL/EROT | state + entity |
| влажная щелка | body.vulvar_cleft | COLL/EROT | state + entity |
| мокрая щелка | body.vulvar_cleft | VULG/EROT | сильнее сексуализировано |

## 12. Вход во влагалище

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| вход во влагалище | body.vaginal_opening | ANAT/NEUT | exact |
| отверстие влагалища | body.vaginal_opening | ANAT | exact |
| вагинальное отверстие | body.vaginal_opening | ANAT | exact |
| вход | body.vaginal_opening | COLL/NEUT | contextual |
| вход внутрь | body.vaginal_opening | COLL | contextual |
| дырочка | body.vaginal_opening | COLL/AFF | ambiguous |
| отверстие | body.vaginal_opening | NEUT | contextual |
| вход в киску | body.vaginal_opening | COLL/EROT | анатомически неточно, понятно |
| вход в письку | body.vaginal_opening | COLL | неточно |
| вход в писечку | body.vaginal_opening | COLL/AFF | неточно |
| дырочка киски | body.vaginal_opening | COLL/EROT | неточно |
| дырочка письки | body.vaginal_opening | COLL | неточно |
| дырочка писечки | body.vaginal_opening | COLL/AFF | неточно |
| вход в пизду | body.vaginal_opening | OBSC | грубое |
| дырка в пизде | body.vaginal_opening | OBSC/VULG | грубое |

## 13. Влагалище

| Форма | Target | Регистр | Точность / оттенок |
|---|---|---|---|
| влагалище | body.vagina | ANAT | exact; терминологическое, не casual default |
| вагина | body.vagina | ANAT/NEUT | exact |
| вагинальный канал | body.vagina | ANAT | exact |
| стенки влагалища | body.vagina | ANAT | exact |
| внутри влагалища | body.vagina | ANAT/NEUT | exact |
| внутри | body.vagina | COLL | contextual |
| внутри нее | body.vagina | COLL/EUPH | contextual |
| внутри киски | body.vagina | COLL/EROT | разговорно, неточно |
| внутри письки | body.vagina | COLL | разговорно, неточно |
| внутри писечки | body.vagina | COLL/AFF | разговорно, неточно |
| внутри пизды | body.vagina | OBSC | разговорно, неточно |

В бытовом русском отдельного распространенного слова только для внутреннего влагалища почти нет; «киска», «писька», «пизда» часто смешивают наружную и внутреннюю анатомию.

## 14. Промежность, пах и внутренняя сторона бедер

| Форма | Target | Регистр | Точность |
|---|---|---|---|
| промежность | body.perineum | ANAT/NEUT | exact |
| область промежности | body.perineum | ANAT | broad |
| между вульвой и анусом | body.perineum | ANAT/NEUT | описательное |
| между влагалищем и анусом | body.perineum | NEUT | бытово понятное |
| между киской и попой | body.perineum | COLL | разговорное |
| между писькой и попой | body.perineum | COLL | разговорное |
| между писечкой и попкой | body.perineum | COLL/AFF | ласкательное |
| пах | body.groin | ANAT/NEUT | broad |
| паховая область | body.groin | ANAT | broad |
| паховая складка | body.groin | ANAT | exact |
| в паху | body.groin | COLL/NEUT | contextual |
| у самого паха | body.groin | COLL/EROT | contextual |
| внутренняя поверхность бедра | body.inner_thigh | ANAT/NEUT | exact |
| внутренняя сторона бедра | body.inner_thigh | NEUT | exact |
| внутренние стороны бедер | body.inner_thigh | NEUT | exact |
| внутренние бедра | body.inner_thigh | COLL | broad |
| между бедер | body.inner_thigh | COLL | пространственное |
| у основания бедра | body.inner_thigh | NEUT | описательное |

## 15. Уретра и внутренняя репродуктивная анатомия

Разговорных устойчивых синонимов здесь почти нет.

- body.urethra: уретра, мочеиспускательный канал;
- body.urethral_opening: отверстие уретры, наружное отверстие уретры, отверстие мочеиспускательного канала;
- body.hymen: девственная плева, гимен;
- body.cervix: шейка матки;
- body.uterus: матка, полость матки;
- body.ovary: яичник, яичники;
- body.fallopian_tube: маточная труба, маточные трубы.

Состояние гимена не используется как достоверное доказательство девственности или сексуального опыта.

## 16. Неоднозначные формы

Особой осторожности требуют:

- киска — broad/contextual: вульва, интимная область или разговорное влагалище;
- писька / писечка — broad: женские гениталии вообще;
- пизда — broad/contextual: наружные гениталии и/или влагалище;
- щель / щелка — обычно половая щель, иногда вся видимая область;
- дырочка — вход во влагалище или анус по контексту;
- дырка — то же, но грубее и часто объективационно;
- между ног — область, а не конкретный орган;
- бюст — внешний образ груди, не отдельная молочная железа;
- декольте — вырез одежды/открытая им область, а не самостоятельная часть тела;
- анал — практика, не анатомическая часть.

При сомнении выбирать более точный BODY target до выбора слова.
