## Проект Благотворительный фонд поддержки котиков QRKot
 Финальное задание 23 спринта

### QRKot реализован с использованием:
  - FastAPI
  - SQLite
  - AlchemySQL
  - Alembic

### Как развернуть проект:

Клонировать репозиторий и перейти в папку проекта:


Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
source venv/scripts/activate
```

Установить зависимости:
```bash
pip3 install -r requirements.txt
```

#### Запуск проекта:

Запустить проект:
```bash
uvicorn app.main:app --reload
```