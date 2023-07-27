# Yatube API

Yatube API - это REST API для социальной сети Yatube. Он позволяет пользователям создавать, редактировать и удалять посты, комментарии и подписки, а также просматривать информацию о пользователях.

# Установка

Для развертывания проекта на локальной машине выполните следующие шаги:

Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone https://github.com/DOLBYTNORMALNO/api_final_yatube.git
cd api_final_yatube
```
Создайте и активируйте виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```
Установите зависимости из файла requirements.txt:


```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполните миграции:


```
python3 manage.py migrate
```
Запустите проект:


```
python3 manage.py runserver
```
Теперь проект доступен по адресу http://localhost:8000/.

# Примеры запросов к API:

Получить список всех постов:


```
curl -H "Authorization: Token <your_token>" http://localhost:8000/api/v1/posts/
```
Создать новый пост:

```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <your_token>" -d '{"text":"New post"}' http://localhost:8000/api/v1/posts/
```
Получить список всех комментариев к посту с id=1:


```
curl -H "Authorization: Token <your_token>" http://localhost:8000/api/v1/posts/1/comments/
```
Подписаться на пользователя с username='user1':


```
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <your_token>" -d '{"following":"user1"}' http://localhost:8000/api/v1/follow/
```
Замените <your_token> на ваш персональный токен доступа. Если вы его не знаете, вы можете получить его, отправив POST-запрос на http://localhost:8000/api/v1/token/ с вашим именем пользователя и паролем в теле запроса.