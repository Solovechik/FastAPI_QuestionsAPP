FROM 	python:3.11.3-slim
WORKDIR /code
COPY	./requirements.txt /code/requirements.txt
RUN	pip install pip --upgrade
RUN 	pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY	./questions_app /code/questions_app
CMD	["uvicorn", "questions_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
