DEPLOYMENT = deployment/
DOCKER_DEV = docker-compose-dev.yml
IMAGE_DEV = playwright-dev-image


install-playwright-chromium:
	poetry install
	poetry run playwright install chromium

run-dev-docker:
	docker compose -f $(DEPLOYMENT)$(DOCKER_DEV) down
	docker rmi -f playwright-dev-image || true
	docker image prune -f
	docker compose -f $(DEPLOYMENT)$(DOCKER_DEV) up --build
	docker ps
	# pytest --env=test -s -v