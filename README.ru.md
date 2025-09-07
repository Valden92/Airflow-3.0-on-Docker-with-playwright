## Airflow 3.0 в Docker с Playwright

Развёртывание Apache Airflow 3.0.x с CeleryExecutor в Docker (Postgres + Redis) и запуск Playwright-краулера из DAG.

[English](README.md) | [Русский](README.ru.md)

> ОС проекта: только UNIX (Linux/macOS/WSL2). Инструкции предназначены для UNIX-систем. Для Windows используйте WSL2.

### Возможности
- Airflow 3.0.6 (Python 3.12), CeleryExecutor
- Postgres + Redis, healthchecks, включён API server
- Playwright 1.55.0 (Chromium; браузеры ставятся при сборке образа)
- Пример краулера (`crawlers/playwright/my_crawler`) + пример DAG (`playwright_crawler`)
- Makefile для build/up/down/clean/sync
- `uv` для управления зависимостями
- `ruff` как линтер (см. `ruff.toml`)

### Требования (UNIX)
- Docker и Docker Compose (v2)
- Make (установите через пакетный менеджер, например Ubuntu: `sudo apt-get install make`)
- uv (рекомендуется локально для запуска инструментов разработчика):
  - `pipx install uv` (предпочтительно), или
  - `pip install uv`, или следуйте документации uv

### Быстрый старт
1) Создайте `.env` из шаблона (обязательно; без него проект НЕ запустится):
```bash
cp env_sample .env
# отредактируйте AIRFLOW_USER, AIRFLOW_PASSWORD, AIRFLOW_EMAIL, AIRFLOW_PORT
```
2) Сборка образов и подготовка директорий:
```bash
make build
```
3) Запуск стека:
```bash
make up
```
4) Откройте Airflow UI: `http://localhost:8080`  
   Войдите с данными из `.env` (по умолчанию admin/admin).
5) Запустите DAG:
   - Идентификатор DAG: `playwright_crawler`
   - Снимите паузу и нажмите “Trigger DAG”.

Остановка:
```bash
make down
```
Полная очистка (контейнеры, образы, тома, данные):
```bash
make clean
```

### Доступные цели Make
- `make build`: создаёт локальные каталоги данных и собирает Docker-образы (uv + Playwright).
- `make up`: поднимает стек в фоне; использует `.env` для учётки и порта.
- `make down`: останавливает контейнеры.
- `make clean`: удаляет контейнеры, образы, тома и каталог `data/`.
- `make sync`: устанавливает зависимости локально через uv (все группы) и браузер Playwright Chromium.
- `make lint`: запускает `ruff` для `crawlers`, `dags`, `operators`.

### Как это работает
- DAG `playwright_crawler` импортирует `crawlers.playwright.my_crawler.main` и вызывает `main()`.
- Краулер запускает headless Chromium (Playwright), итерируется по страницам (1..9), логирует прогресс и завершается.

### Разработка (локально)
Установка зависимостей и браузеров Playwright:
```bash
make sync
```
Запуск краулера напрямую:
```bash
uv run python crawlers/playwright/my_crawler/main.py
```
Линтинг:
```bash
make lint
```

### Конфигурация
- `.env` обязателен: задаёт учётные данные администратора и порт UI.
- Томами монтируются `dags/`, `crawlers/`, `operators/` и `data/*`.
- Образ собирается с зависимостями (`uv`) и браузерами Playwright.

### Проблемы и решения
- Ресурсы: требуется ≥4 ГБ RAM и ≥2 vCPU (иначе шаг инициализации предупредит).
- Браузеры Playwright: уже в образе; для локального запуска используйте `make sync`.
- Права в Linux: `AIRFLOW_UID` подставляется автоматически, чтобы избежать root-владения файлами.

### Лицензия
MIT


