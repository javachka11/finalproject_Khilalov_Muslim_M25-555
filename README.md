# finalproject_Khilalov_Muslim_M25-555

# Проект "Платформа для отслеживания и симуляции торговли валютами"
### Домашнее задание №3. Платформа для отслеживания и симуляции торговли валютами.
#### Выполнил студент Хилалов Муслим, группа М25-555

#### Описание идеи

Программа эмулирует работу настоящей платформы для отслеживания и торговли фиатными и криптовалютами. Каждому новому пользователю при регистрации выдаётся 100 USD для возможности начального развития на платформе. Помимо Core Service, который отвечает за работу с пользователями, в программе также есть Parser Service, который отслеживает текущие курсы валют на фондовых рынках и даёт возможность синхронизировать с ними платформу.

#### Структура каталогов

<pre>
├── data/
│    ├── users.json          
│    ├── portfolios.json       
│    ├── rates.json
│    └── exchange_rates.json
├── valutatrade_hub/
│    ├── __init__.py
│    ├── logging_config.py         
│    ├── decorators.py            
│    ├── core/
│    │    ├── __init__.py
│    │    ├── currencies.py         
│    │    ├── exceptions.py         
│    │    ├── models.py           
│    │    ├── usecases.py          
│    │    └── utils.py             
│    ├── infra/
│    │    ├─ __init__.py
│    │     ── settings.py           
│    ├── parser_service/
│    │    ├── __init__.py
│    │    ├── config.py
│    │    ├── api_clients.py
│    │    ├── updater.py
│    │     ── storage.py
│    └── cli/
│         ├─ __init__.py
│         └─ interface.py     
│
├── main.py
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore               
</pre>

#### Сборка проекта

|Команда|Описание|
|:-|-:|
|`make` `install` \| `poetry` `install`|Установить пакет|
|`make` `project` \| `poetry` `run` `project`|Запустить проект|

#### Интерфейс для работы с платформой:

|Команда|Описание|
|:-|-:|
|`register` `--username` `<имя>` `--password` `<пароль>`|Зарегистрировать пользователя|
|`login` `--username` `<имя>` `--password` `<пароль>`|Залогиниться под конкретным пользователем|
|`show-portfolio`|Отобразить портфель пользователя (в долларах)|
|`show-portfolio` `--base` `<код_валюты>`|Отобразить портфель пользователя (в базовой валюте)|
|`buy` `--currency` `<код_валюты>` `--amount` `<количество_валюты>`|Купить валюту|
|`sell` `--currency` `<код_валюты>` `--amount` `<количество_валюты>`|Продать валюту|
|`get-rate` `--from` `<исходная_валюта>` `--to` `<целевая_валюта>`|Отобразить текущий курс валюты|
|`update-rates` `[crypto\|fiat]`|Обновить текущие курсы валют|
|`show-rates` `[--currency <код_валюты>]` `[--top <топ_курсов>]` `[--base <баз_валюта>]`|Отобразить курсы валют|
|`info`|Отобразить справку|
|`help` `<команда>`|Отобразить справку для команды|
|`quit`|Выйти из программы|


#### Пример работы с платформой:

<pre>&gt; register --username john --password qwerty
Пользователь &apos;john&apos; зарегистрирован (id=2). Войдите: login --username john --password ******
</pre>

<pre>&gt; login --username john --password qwerty
Добро пожаловать, john!</pre>

<pre>john&gt; get-rate --from EUR --to USD
Курс EUR→USD: 1.07860000 (обновлено: 2025-10-09 10:30:00)
Обратный курс USD→EUR: 0.92712776</pre>

<pre>john&gt; show-portfolio
Портфель пользователя &apos;john&apos; (база: USD):
- USD: 100.00000000  →  100.00000000 USD
---------------------------------
ИТОГО: 100.00000000 USD</pre>

<pre>john&gt; buy --currency EUR --amount 10
Покупка выполнена: 10.00000000 EUR по курсу 1.07860000 EUR -&gt; USD
Изменения в портфеле:
- EUR: было 0.00000000 → стало 10.00000000
Оценочная стоимость покупки: 10.78600000 USD
</pre>

<pre>john&gt; sell --currency EUR --amount 4.25
Продажа выполнена: 4.25000000 EUR по курсу 1.07860000 EUR -&gt; USD
Изменения в портфеле:
- EUR: было 10.00000000 → стало 5.75000000
Оценочная выручка: 4.58405000 USD
</pre>

<pre>john&gt; show-portfolio
Портфель пользователя &apos;john&apos; (база: USD):
- USD:  93.79805000  →   93.79805000 USD
- EUR:   5.75000000  →    6.20195000 USD
---------------------------------
ИТОГО: 100.00000000 USD
</pre>

<pre>john&gt; update-rates
INFO: Starting rates update...
INFO: Fetching from CoinGecko... OK (3 rates)
INFO: Fetching from ExchangeRate-API... OK (3 rates)
INFO: Writing 6 rates to data/rates.json...
Update successful. Total rates updated: 6. Last refresh: 2026-02-18T05:21:49.686155
</pre>

<pre>john&gt; show-rates
Rates from cache (updated at 2026-02-18T04:28:24.147427):
- BTC_USD: 67126.00000000
- ETH_USD: 1977.02000000
- SOL_USD: 84.33000000
- GBP_USD: 1.35556443
- EUR_USD: 1.18403560
- RUB_USD: 0.01298534
</pre>

<pre>john&gt; info
&lt;command&gt; register --username &lt;имя&gt; --password &lt;пароль&gt; - зарегистрировать пользователя
&lt;command&gt; login --username &lt;имя&gt; --password &lt;пароль&gt; - залогиниться под конкретным пользователем
&lt;command&gt; show-portfolio [--base &lt;код_валюты&gt;] - отобразить портфель пользователя (в базовой валюте)
&lt;command&gt; buy --currency &lt;код_валюты&gt; --amount &lt;количество_валюты&gt; - купить валюту
&lt;command&gt; sell --currency &lt;код_валюты&gt; --amount &lt;количество_валюты&gt; - продать валюту
&lt;command&gt; get-rate --from &lt;исх_валюта&gt; --to &lt;цел_валюта&gt; - получить текущий курс валюты
&lt;command&gt; update-rates [ctypto|fiat] - обновить курс валют
&lt;command&gt; show-rates [--currency &lt;код_валюты&gt;] [--top &lt;топ_курсов&gt;] [--base &lt;баз_валюта&gt;] - отобразить курсы валют
&lt;command&gt; info - отобразить справку
&lt;command&gt; help &lt;команда&gt; - отобразить справку для команды
&lt;command&gt; quit - выйти из программы
</pre>


#### Описание кэша/TTL

Платформа не даёт возможность проводить операции с конкретной валютой, если после последнего обновления её курса прошло как минимум RATES_TTL_SECONDS секунд (задаётся в config.json). Parser Service предоставляет пользователю возможность вручную обновить кэш валют с помощью команды `update-rates`. Помимо кэша, Parser Service заполняет исторические данные для дальнейшего возможного анализа.

#### Где хранить ExchangeRate-API ключ!!!

1) Введите в терминале команду `export EXCHANGERATE_API_KEY="<ВАШ API-КЛЮЧ>"`
2) Теперь ваш ключ записан в переменную окружения, можете проверить его с помощью команды терминала `echo $EXCHANGERATE_API_KEY`
3) Готово! Теперь можете запускать платформу с помощью команды `make project`.


#### Пример работы с платформой, Core Service (asciinema):

[![asciicast](https://asciinema.org/a/3UedtysJZ7u3IyUv.svg)](https://asciinema.org/a/3UedtysJZ7u3IyUv)

#### Пример работы с платформой, Parser Service (asciinema):

[![asciicast](https://asciinema.org/a/DerjVbK1JH4MqnF7.svg)](https://asciinema.org/a/DerjVbK1JH4MqnF7)

#### Пример работы с платформой, Обработка ошибок (asciinema):

[![asciicast](https://asciinema.org/a/AigQ1wKeYjc0Q26w.svg)](https://asciinema.org/a/AigQ1wKeYjc0Q26w)