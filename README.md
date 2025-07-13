# Проект "Сириус путеводитель" для всероссийского ИТ-раунда

## Требования
- Python 3.12
- Docker
- Poetry

## Установка
1. Склонируйте репозиторий
```bash
git clone git@github.com:n9dn9/sirius-it.git
```

2. По примеру из **.env.example** создайте .env файл с переменными окружения

## Настройка
1. При необходимости измените конфигурацию .env 

## Запуск
1. Запустите проект
```bash
docker compose up --build
// при повторном запуске флаг build можно опустить
```
Сайт будет доступен на порту **80**

2. Чтобы выключить проект достаточно прожать Ctrl+C в терминале где был запущен Docker-compose

## Er-cхема
```mermaid
erDiagram
    places {
        INTEGER id PK
        STRING name
        STRING address
        STRING photo_url
        STRING category
        TEXT description
    }

    reviews {
        INTEGER id PK
        INTEGER place_id FK
        INTEGER rating
        TEXT comment
        STRING author
        DATETIME date
    }

    places ||--o{ reviews : ""
```
