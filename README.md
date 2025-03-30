# AT Simulation API

Микросервис подсистемы имитационного моделирования АТ-ТЕХНОЛОГИЯ

## Общая схема вычислений

TODO: Общая схема верна, но детали немного устарели и нужно ее обновить.

```mermaid
sequenceDiagram
    participant Translator as Model Translator
    participant Minio as MinIO Storage
    participant ComputeManager as Compute Manager
    participant OS as Operating System
    actor User as User
    participant Editor as Model Editor
    participant Postgres as Postgres DB

    rect rgb(102, 204, 255, .3)
        loop Create model
            User ->> Editor: CRUD Model Request
            activate Editor
            Editor ->> Postgres: CRUD DB Request
            activate Postgres
            Postgres -->> Editor: CRUD DB Response
            deactivate Postgres
            Editor -->> User: CRUD Model Response
            deactivate Editor
        end
    end

    User ->> Translator: Translate model
    activate Translator
    Translator ->> Postgres: Request model
    activate Postgres
    Postgres -->> Translator: Return model
    deactivate Postgres

    Translator ->> Minio: Save model
    activate Minio
    Minio -->> Translator: Return file ID
    deactivate Minio
    Translator -->> User: Return file ID
    deactivate Translator

    User ->> ComputeManager: Start model by file ID
    activate ComputeManager
    ComputeManager ->> Minio: Request model by file ID
    activate Minio
    Minio -->> ComputeManager: Return executable (.exe)
    deactivate Minio

    ComputeManager ->> OS: Start subprocess of executable
    activate OS
    OS -->> ComputeManager: Return stdin, stdout, stderr (PIPE)
    deactivate OS

    ComputeManager -->> User: Return process ID
    deactivate ComputeManager

    rect rgb(102, 204, 255, .3)
        loop Process ticks
            ComputeManager ->> User: Execute tick for process ID
            activate ComputeManager
            ComputeManager ->> OS: Execute next tick (process ID)
            activate OS
            OS ->> ComputeManager: Return tick results
            deactivate OS
            ComputeManager -->> User: Return current results
            deactivate ComputeManager
        end
    end

    User ->> ComputeManager: Terminate process (process ID)
    activate ComputeManager
    ComputeManager ->> OS: Terminate process
    activate OS
    OS -->> ComputeManager: Return final results
    deactivate OS

    ComputeManager ->> Postgres: Store final results
    activate Postgres
    Postgres -->> ComputeManager: Acknowledge (success/failure)
    deactivate Postgres
    ComputeManager ->> User: Return final results
    deactivate ComputeManager

```
## Локальный запуск

1. Установить и запустить сервис авторизации https://github.com/grigandal625/AT_USER по ридми, создать в нем пользователя
2. `git clone https://github.com/leerycorsair/at_simulation_api` и `cd at_simulation_api`

3. **Если делали это в AT_USER, пропускаем:** Установить Docker
4. **Если делали это в AT_USER, пропускаем:** Установить и запустить RabbtMQ (можно в докере, с открытием портов и с доступом RabbitMQ на localhost)
5. Установить python-пакет `poetry`
6. `poetry install`
7. `poetry update`
8. Скопировать файл [docker/local/.env.example](./docker/local/.env.example) в файл `docker/local/.env` (создать с тким же содержимым), и если надо, поменять настройки
9. `chmod +x ./alembic_upgrade_head.sh`
10. `./alembic_upgrade_head.sh`
11. **Если делали это в AT_USER, пропускаем:** Если нигде больше не запущен пакет `at_queue`, выполнить в отдельном терминале в этой же директории `poetry run python -m at_queue` (запустится только если запущен RabbitMQ, до конца раоты не выключать)
12. `make components`
13. `make run` - запустится бэкенд на адресе http://0.0.0.0:8081 или http://127.0.0.1:8081
14. запустить фронтенд на http://127.0.0.1:5000/ командой `docker run --name at-simulation-front -d -p 5000:5000 -e PORT=5000 -e API_PORT=8081 grigandal625/at-simulation-subsystem-front:latest`
15. Получить токен пользователя из сваггера AT_USER (пункт 1.)
16. 