DEPLOYMENT = deployment/

DOCKER_DEV := docker-compose-dev.yml
IMAGE_DEV := playwright-dev-image
DOCKER_FILE = Dockerfile

GCP_PROJECT_ID := playwright-pytest-gcp-2508
TF_DIR := $(DEPLOYMENT)/terraform
TF_REPO := playwright-terraform-repo
ASIA_PKG := asia-east1-docker.pkg.dev

IMAGE_NAME := playwright-terraform-image
GIT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_TAG := $(GIT_SHA)
IMAGE_URI := $(ASIA_PKG)/$(GCP_PROJECT_ID)/$(TF_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)
TF_SERVICE_NAME := playwright-terraform-service

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

run-terraform-init:
	cd $(TF_DIR) && terraform init

run-terraform-validate:
	cd $(TF_DIR) && terraform validate

run-terraform-fmt:
	cd $(TF_DIR) && terraform fmt -recursive

run-docker-push-to-artifact-registry:
	gcloud auth configure-docker $(ASIA_PKG)
	docker build --platform=linux/amd64 -f $(DEPLOYMENT)$(DOCKER_FILE) -t $(IMAGE_URI) .
	docker push $(IMAGE_URI)

run-terraform-import-all: # Telling GCP that Terraform will handle these GCP resources ; Accept error and keep running github action
	cd $(TF_DIR) && terraform import \
		google_artifact_registry_repository.docker_repo asia-east1/$(TF_REPO) || true

	cd $(TF_DIR) && terraform import \
		google_cloud_run_service.playwright_terraform_service asia-east1/$(TF_SERVICE_NAME) || true

run-terraform-plan:
	cd $(TF_DIR) && terraform plan -out=tfplan

run-terraform-apply:
	cd $(TF_DIR) && terraform apply -auto-approve

run-terraform-destroy:
	@echo "⚠️ Are you sure you want to destroy everything ? "
	@echo "⚠️ Press Ctrl+C to cancel."
	sleep 10
	cd $(TF_DIR) && terraform destroy -auto-approve
