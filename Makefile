build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs api

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

collectstaticfiles:
	docker compose -f local.yml run --rm api python manage.py collectstatic --no-input clear
	
superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inpsect src_local_postgres_data

authors-db:
	docker compose -f local.yml exec postgres psql --username=alphamale --dbname=authors-live

flake8:
	docker compose -f local.yml exec api flake8 .

black-check:
	docker compose -f local.yml exec api black --check --exclude=migrations .

black-check:
	docker compose -f local.yml exec api black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec api black --exclude=migrations --exclude=venv .

isort-check:
	docker compose -f local.yml exec api isort . --check-only --skip venve --skip migrations

isort-diff:
	docker compose -f local.yml exec api isort . --diff --skip venve --skip migrations

isort:
	docker compose -f local.yml exec api isort . --skip venve --skip migrations

backup:
	docker compose -f local.yml exec postgres backup	