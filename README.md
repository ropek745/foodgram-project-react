![Foodgram](https://github.com/ropek745/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Продуктовый помощник Foodgram

Проект доступен по ссылке http://51.250.97.227/

### Описание
Сервис, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Используемые технологии
 - Python
 - Django
 - Django Rest Framework
 - PosgreSQL
 - Docker
 
## Порядок запуска
 
### 1. Клонировать проект
```
git@github.com:ropek745/foodgram-project-react.git
```
### 2. Создать и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```
### 3. Создать БД, загрузить данные в БД, запустить локально
```
cd backend
python manage.py runserver
```
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
```
python manage.py csv_manager
python manage.py tags_manager
```
```
python manage.py runserver
```
### 4. Запустить frontend (запустить bash, перейти в директорию infra)
```
cd infra
docker-compose up --build
```

## Разработчик - [Роман Пекарев](https://github.com/ropek745) ##




