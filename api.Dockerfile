FROM 	python:3.11.3-slim
WORKDIR /code
COPY	./requirements.txt /code/requirements.txt
RUN	pip install pip --upgrade
RUN 	pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY	./questions_app /code/questions_app
CMD	["sh", "-c", "uvicorn questions_app.main:app --host $API_HOST --port $API_PORT"]
