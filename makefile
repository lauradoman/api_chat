.PHONY: help install test run down clean

help:
	@echo "Available commands:"
	@echo "  make install  -> Install all requirements"
	@echo "  make test     -> Run tests"
	@echo "  make run      -> Run the service in Docker"
	@echo "  make down     -> Stop Docker containers"
	@echo "  make clean    -> Remove Docker containers"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	python -m spacy download es_core_news_sm

test:
	pytest tests/ -v

run:
	docker build -t kavak_api .
	docker run -p 8000:8000 kavak_api

down:
	-docker ps -q | xargs -r docker stop

clean:
	-docker ps -a -q | xargs -r docker rm
	-docker images -q kavak_api | xargs -r docker rmi
