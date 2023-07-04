# Проект "Продуктовый помощник"

Онлайн сервис, в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Используемые технологии:<br/>
- Django
- Django Rest Framework
- Python 3.7
- PostgreSQL
- Docker
- Docker-compose
- Gunicorn
- Nginx
- React
- CI/CD

## Структура проекта:<br/>
- frontend — файлы необходимые для сборки фронтенда приложения
- infra — конфигурационный файл nginx и docker-compose.yml
- backend — файлы для сборки бекенд приложения
- data подготовлены теги и список ингредиентов с единицами измерения
- docs — файлы спецификации API, по которым работает проект


## Локальный запуск проекта в контейнерах:

- Склонировать репозиторий к себе на компьютер и перейти в корневую папку
```
git clone git@github.com:Maltassarus/foodgram-project-react.git
```
```
cd foodgram-project-react
```
- Создать файл .env с переменными окружения, необходимыми для работы

> DB_ENGINE=django.db.backends.postgresql<br/>
> DB_NAME=postgres<br/>
> POSTGRES_USER=postgres<br/>
> POSTGRES_PASSWORD=postgres<br/>
> DB_HOST=db<br/>
> DB_PORT=5432<br/>
> SECRET_KEY=postgres<br/>

- Перейти в папку /infra и запустить сборку контейнеров (запущены контейнеры db, web, nginx)
```
sudo docker-compose up -d
```
- Внутри контейнера backend создать миграции, выполнить миграции, создать суперпользователя, собрать статику и загрузить ингредиенты и теги
```
sudo docker-compose exec web python manage.py makemigrations
```
```
sudo docker-compose exec web python manage.py migrate
```
```
sudo docker-compose exec web python manage.py createsuperuser
```
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
```
sudo docker-compose exec web python manage.py importcsv
```

## Доступ к ресурсу
http://foodgrammaltassarus.ddns.net
актуально на 06.07.2023.