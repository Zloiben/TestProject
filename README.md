# Тестовое задание

**Настройка** происходит через файл **.env**

### Задача
Реализовать роуты для хранения по номеру телефону адреса в Redis

**Роуты**:
* /v1/contact-address/check_data - GET (Получение адреса)
* /v1/contact-address/write_data - POST, PUT (Создание и редактирование)


### Запуск приложения
```shell
docker-compose up --build --force-recreate
```