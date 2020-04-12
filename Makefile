build:
	docker-compose build

up:
	docker-compose up -d

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest

logs:
	docker-compose logs --tail=25 api redis_pubsub

down:
	docker-compose down --remove-orphans

bash: up
	docker-compose run --rm bash

shell: up
	docker-compose run --rm ./manage.py shell

all: down build up test
