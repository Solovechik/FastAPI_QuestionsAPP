# FastAPI_QuestionsAPP


Переменные для запуска можно изменить в файле .env.

Сборка образа:
  - docker-compose build --no-cache;
  - docker-compose up.

Для подключения к БД: 
  - psql -h 127.0.0.1 -p 5433 -d bewise -U bewiseusr.

Получение вопросов:

curl -X 'POST' \
  'http://127.0.0.1:8000/questions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "questions_num": 2
}'
