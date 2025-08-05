DEPLOYMENT = deployment/

DOCKER_DEV = docker-compose-dev.yml
IMAGE_DEV = playwright-dev-image


TF_DIR = $(DEPLOYMENT)/terraform

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



docker-push:
	gcloud auth configure-docker asia-east1-docker.pkg.dev
	docker build -f $(DEPLOYMENT)Dockerfile -t asia-east1-docker.pkg.dev/playwright-pytest-gcp-2508/playwright-repo/playwright-image:latest .
	docker push asia-east1-docker.pkg.dev/playwright-pytest-gcp-2508/playwright-repo/playwright-image:latest



terraform-init:
	cd $(TF_DIR) && terraform init

terraform-apply:
	cd $(TF_DIR) && terraform apply -auto-approve
