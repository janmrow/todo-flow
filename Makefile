.PHONY: run test lint docker-up docker-test init-db

run:
	FLASK_APP=app flask --app app run

init-db:
	FLASK_APP=app flask --app app init-db

test:
	pytest -q

lint:
	ruff check .

docker-up:
	docker compose up --build

docker-test:
	docker compose run --rm tests

docker-e2e:
	docker compose run --rm e2e

