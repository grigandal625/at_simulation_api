
include docker/local/.env
run:
	bash -c "poetry run python at_simulation_api"

clear:
	find . -type d -name '__pycache__' -exec rm -rf {} +

components:
	docker compose -f ./docker/local/docker-compose.yml down --remove-orphans
	docker compose -f ./docker/local/docker-compose.yml up --build -d