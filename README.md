## Ansara_Notions
## Описание проекта
```
Данный проект - тестовое задание для компании Ansara
```

**_Ссылка на [проект](http://z-dachnik.ddns.net/api/ "Гиперссылка к проекту.")_**

**_Ссылка на [админ-зону](http://z-dachnik.ddns.net/admin/ "Гиперссылка к админке.")_**
admin - login 
admin - password



### Развернуть проект на удаленном сервере:
**Клонировать репозиторий:**
```
git clone https://github.com/Resurection1/Ansara_Notion.git
```

**_В общей директории файл .env.example переименовать в .env и заполнить своими данными:_**
```
POSTGRES_DB='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_NAME='postgres'
DB_HOST=db
DB_PORT=5432
DEBUG=False
SECRET_KEY= # django secret key
ALLOWED_HOSTS='localhost,127.0.0.1,domain,ip'
DATABASES=postgresql
DOMAIN = ''
```

**_Установить на сервере Docker, Docker Compose:_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```
**_Cоздать папку z-dachnik cкопировать на сервер файлы docker-compose.production.yml:_**
```
docker compose -f docker-compose.production.yml up 

docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic

docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/

docker compose -f docker-compose.production.yml exec backend python manage.py migrate

docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

## Документация
**Файл с документацией из schema.yaml можно посмотреть на [сайте](https://editor.swagger.io/)**



### Автор
[Podzorov Mihail] - https://github.com/Resurection1
