# finalproject_Khilalov_Muslim_M25-555

# Проект "Платформа для отслеживания и симуляции торговли валютами"
### Домашнее задание №3. Платформа для отслеживания и симуляции торговли валютами.
#### Выполнил студент Хилалов Муслим, группа М25-555

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

<pre>john&gt; info
&lt;command&gt; register --username &lt;имя&gt; --password &lt;пароль&gt; - зарегистрировать пользователя
&lt;command&gt; login --username &lt;имя&gt; --password &lt;пароль&gt; - залогиниться под конкретным пользователем
&lt;command&gt; show-portfolio - отобразить портфель пользователя (в долларах)
&lt;command&gt; show-portfolio --base &lt;код_валюты&gt; - отобразить портфель пользователя (в базовой валюте)
&lt;command&gt; buy --currency &lt;код_валюты&gt; --amount &lt;количество_валюты&gt; - купить валюту
&lt;command&gt; sell --currency &lt;код_валюты&gt; --amount &lt;количество_валюты&gt; - продать валюту
&lt;command&gt; get-rate --from &lt;исх_валюта&gt; --to &lt;цел_валюта&gt; - получить текущий курс валюты
&lt;command&gt; info - отобразить справку
&lt;command&gt; help &lt;команда&gt; - отобразить справку для команды
&lt;command&gt; quit - выйти из программы</pre>



#### Пример работы с платформой (asciinema):

[![asciicast](https://asciinema.org/a/3UedtysJZ7u3IyUv.svg)](https://asciinema.org/a/3UedtysJZ7u3IyUv)
