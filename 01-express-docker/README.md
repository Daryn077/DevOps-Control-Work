# Вариант 1 — Express.js + Docker

## Что требуется
Минимальное приложение Express, которое по адресу `GET /` возвращает JSON:

```json
{"message":"Hello World"}
```

## Запуск
В папке проекта:

```bash
docker compose up -d --build
```

Открыть http://localhost:3000/ (или `curl http://localhost:3000/`).

## Команды для проверки

```bash
docker compose ps
docker compose logs -f web
docker compose down
```

## Основные файлы
- `app.js` — обработчик запроса и запуск сервера.
- `package.json` — зависимости Express и команда запуска.
- `Dockerfile` — инструкция сборки образа.
- `compose.yaml` — запуск и проброс порта.
- `.dockerignore` — файлы, исключённые из контекста сборки.

## Что изменять на контрольной
- Путь API — в `app.get('/', ...)`.
- JSON-ответ — в `res.json(...)`.
- Если нужен другой порт, одновременно меняй `PORT`, `EXPOSE` и `ports`.

> Первый запуск потребует интернет для скачивания образа Node и npm-зависимостей, если они ещё не закешированы.
