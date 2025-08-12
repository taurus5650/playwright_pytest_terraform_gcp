DEPLOYMENT = deployment/

DOCKER_DEV := docker-compose-dev.yml
IMAGE_DEV := playwright-dev-image
DOCKER_FILE = Dockerfile

GCP_PROJECT_ID := playwright-pytest-gcp-2508
TF_DIR := $(DEPLOYMENT)/terraform
REPO := playwright-terraform-repo
SERVICE_NAME := playwright-terraform-service
ASIA_PKG := asia-east1-docker.pkg.dev
REGION := asia-east1

GIT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_NAME := playwright-terraform-image
IMAGE_TAG := $(GIT_SHA)
IMAGE_URI := $(ASIA_PKG)/$(GCP_PROJECT_ID)/$(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)


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

run-terraform-first-time-enable-tf:
	cd $(TF_DIR) && terraform init && terraform apply -auto-approve \
	-target=google_project_service.artifact_registry \
	-target=google_project_service.cloud_run \
	-target=google_project_service.compute \

run-terraform-init:
	cd $(TF_DIR) && terraform init

run-terraform-validate:
	cd $(TF_DIR) && terraform validate

run-terraform-fmt:
	cd $(TF_DIR) && terraform fmt -recursive

run-terraform-import-all: # Telling GCP that Terraform will handle these GCP resources ; Accept error and keep running github action
	cd $(TF_DIR) && terraform import \
		google_artifact_registry_repository.docker_repo $(REGION)/$(REPO) || true

	cd $(TF_DIR) && terraform import \
		google_cloud_run_service.playwright_terraform_service $(REGION)/$(SERVICE_NAME) || true

run-terraform-plan:
	cd $(TF_DIR) && terraform plan -out=tfplan\
		-var="image_name=$(IMAGE_NAME)" \
	  	-var="image_tag=$(IMAGE_TAG)"

run-terraform-apply:
	cd $(TF_DIR) && terraform apply -auto-approve \
		-var="image_name=$(IMAGE_NAME)" \
		-var="image_tag=$(IMAGE_TAG)" \
		-var="deploy_timestamp=$(shell date +%s)"

run-terraform-destroy:
	@echo "⚠️ Are you sure you want to destroy everything ? "
	@echo "⚠️ Press Ctrl+C to cancel."
	sleep 10
	cd $(TF_DIR) && terraform destroy -auto-approve

check-gcp-log:
	 gcloud logging read \
	  'resource.type="cloud_run_revision" \
	   AND resource.labels.service_name="$(SERVICE_NAME)" \
	   AND resource.labels.location="asia-east1"' \
	  --project=$(GCP_PROJECT_ID) \
	  --limit=1000 \
	  --format="value(textPayload)"


 run-docker-push-to-artifact-registry:
	gcloud auth configure-docker $(ASIA_PKG)
	docker build --platform=linux/amd64 -f $(DEPLOYMENT)$(DOCKER_FILE) -t $(IMAGE_URI) .
	docker push $(IMAGE_URI)

run-deploy-to-cloud-run:
	gcloud run deploy $(SERVICE_NAME) \
	  --image $(IMAGE_URI) \
	  --region $(REGION) \
	  --platform managed \
	  --project $(GCP_PROJECT_ID) \
	  --allow-unauthenticated \
	  --quiet
