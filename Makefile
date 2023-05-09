ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

test_env:
	echo "DEBUG=1" > .env
	echo "SECRET_KEY=foo" >> .env
	echo "DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]" >> .env
	echo "POSTGRES_ENGINE=django" >> .env.db.backends.postgresql
	echo "POSTGRES_DB=postgres" >> .env
	echo "POSTGRES_USER=user" >> .env
	echo "POSTGRES_PASSWORD=hackme" >> .env
	echo "POSTGRES_HOST=localhost" >> .env
	echo "POSTGRES_PORT=5432" >> .env
	echo "DB_CONTAINER_NAME=network_postgres" >> .env

db:
	docker-compose -f docker-compose.yml up -d

run:
	cd src && python manage.py runserver

superuser:
	python src/manage.py createsuperuser --email test@test.ru --username super

migrate:
	cd src && python manage.py migrate

token:
	cd src && python manage.py drf_create_token nikita

schema:
	cd src && python manage.py generateschema --file openapi-schema.yml

open_db:
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)
