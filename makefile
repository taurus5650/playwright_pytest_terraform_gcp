DEPLOYMENT = deployment/

DOCKER_DEV = docker-compose-dev.yml
IMAGE_DEV = playwright-dev-image


TF_DIR = $(DEPLOYMENT)/terraform


run-dev-docker:
	docker compose -f $(DEPLOYMENT)$(DOCKER_DEV) down
	docker rmi -f playwright-dev-image || true
	docker image prune -f
	docker compose -f $(DEPLOYMENT)$(DOCKER_DEV) up --build
	docker ps
	# pytest --env=test -s -v

install-poetry:
	pip install poetry

install-playwright-chromium:
	poetry install --no-root
	poetry run playwright install chromium

gcloud-auth-docker-to-artifact-registry:
	gcloud auth configure-docker asia-east1-docker.pkg.dev

docker-push:
	gcloud auth configure-docker asia-east1-docker.pkg.dev
	docker build -f $(DEPLOYMENT)Dockerfile -t asia-east1-docker.pkg.dev/playwright-pytest-gcp-2508/playwright-repo/playwright-image:latest .
	docker push asia-east1-docker.pkg.dev/playwright-pytest-gcp-2508/playwright-repo/playwright-image:latest

terraform-init:
	cd $(TF_DIR) && terraform init

terraform-import-existing:
	cd $(TF_DIR) && terraform import google_artifact_registry_repository.docker_repo asia-east1/playwright-repo || true
	cd $(TF_DIR) && terraform import google_cloud_run_service.service asia-east1/automation-ui-service || true

terraform-plan:
	cd $(TF_DIR) && terraform plan -out=tfplan

terraform-apply:
	cd $(TF_DIR) && terraform apply -auto-approve
