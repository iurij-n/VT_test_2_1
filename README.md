## Задание №2.1.

#### Стэк:
- Python
- Django
- Simple JWT
- REST API

Сервис с REST API. Авторизация по bearer токену (/info, /latency, /logout). 
Реализовать CORS. СУБД - Postgres. Токен генерируется по запросу /sigin, действителен 10 минут. Продлевать при любом запросе пользователя (кроме signin).

#### API:

```/signin [POST]``` - запрос bearer токена по id и паролю // данные принимает в json (поле id - адрес электронной почты или номер телефона в формате '+79998887766', пароль). Если пользователь с такими данными существует, возвращается пара токенов - access и refresh.

```/signup [POST]``` - регистрация нового пользователя: // данные принимает в json
Поля id и password, id - номер телефона или email. Определяется тип введенных данных, phone или mail. После регистрации тип id сохраняется в базе данных. При удачной регистрации возвращается пара токенов - access и refresh.

```/info [GET]``` - возвращает id пользователя и тип id (Доступ только по токену).

```/latency [GET]``` - возвращает задержку от сервиса до google.com (Доступ только по токену).

```/logout [GET]``` - заносит refresh-токен текущего пользователя в "черный список".

#### Инструкция по запуску

- Клонировать репозиторий
```
git clone https://github.com/iurij-n/VT_test_2_1.git
```
- Создать виртуальное окружение
```
python -m venv venv
```
- Активировать виртуальное окружение
для Windows
```
source venv/Scripts/actevate
```
для Linux
```
source venv/bin/actevate
```
- Установить зависимости
```
pip install -r requrements.txt
```

Из папки `token_task`
- Создать миграции
```
python migrate.py makemigrations
```
- Выполнить миграции
```
python migrate.py migrate
```
- Запустить сервер
```
python migrate.py runserver
```