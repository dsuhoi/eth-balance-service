# eth-balance-service
>Сервис для взаимодействия с кошельком криптовалюты Ethereum.
### Установка
В корневой директории создайте файл `.env` с конфигурациями сервиса
```sh
SECRET_KEY=<SECRET_KEY>
DB_DATABASE=<eth-balance>
DB_USERNAME=<postgres>
DB_PASSWORD=<postgres>
DB_HOST=<db>
DB_PORT=<5432>
CELERY_BROKER=<redis://redis:6379/0>
CELERY_RESULT_BACKEND=<redis://redis:6379/0>
WEB3_PROVIDER=<HTTP_URL>
```
и выполните команду
```sh
docker compose up -v --built
```
### Тестирование
```sh
docker compose run web pytest .
```

### Просмотр
Перейдите по адресу `0.0.0.0:8000/` или `0.0.0.0:8000/api/docs/` для работы с сервисом.
