ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

test_env:
	echo "DEBUG=1" > .env
	echo "SECRET_KEY=foo" >> .env
	echo "DJANGO_ALLOWED_HOSTS=localhost" >> .env
	echo "PASSWORD_RESET_TIMEOUT=60" >> .env
	echo "POSTGRES_ENGINE=django.db.backends.postgresql" >> .env
	echo "POSTGRES_DB=postgres" >> .env
	echo "POSTGRES_USER=user" >> .env
	echo "POSTGRES_PASSWORD=hackme" >> .env
	echo "POSTGRES_HOST=localhost" >> .env
	echo "POSTGRES_PORT=5432" >> .env
	echo "POSTGRES_ENGINE=django" >> .env
	echo "DB_CONTAINER_NAME=network_postgres" >> .env

install:
	#pip install poetry
	poetry install
	poetry shell
	make test_env
	make db
	make migrate
	make superuser

db:
	docker-compose -f docker-compose.yml up -d

run:
	python src/manage.py runserver


create_migrations:
	python src/manage.py makemigrations

superuser:
	python src/manage.py createsuperuser --email test@test.ru --username super

migrate:
	python src/manage.py migrate

token:
	python src/manage.py drf_create_token super

schema:
	python src/manage.py generateschema --file openapi-schema.yml

open_db:
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)
