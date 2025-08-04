DEPLOYMENT = deployment/
TF_DIR = $(DEPLOYMENT)/terraform
DOCKER_DEV = docker-compose-dev.yml

IMAGE_DEV = playwright-dev-image
IMAGE_PROD = playwright-prod-image
GCP_IMAGE = $(REGION)-docker.pkg.dev/$(PROJECT_ID)/app-repo/$(IMAGE_PROD)


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

docker-build-prod:
	docker build -t $(GCP_IMAGE):latest -f $(DEPLOYMENT)/Dockerfile .
	docker push $(GCP_IMAGE):latest

terraform-init:
	cd $(TF_DIR) && terraform init

terraform-apply:
	cd $(TF_DIR) && terraform apply -auto-approve \
		-var="project_id=$(PROJECT_ID)" \
		-var="region=$(REGION)" \
		-var="image=$(GCP_IMAGE):latest"

terraform-destroy:
	cd $(TF_DIR) && terraform destroy -auto-approve \
		-var="project_id=$(PROJECT_ID)" \
		-var="region=$(REGION)" \
		-var="image=$(GCP_IMAGE):latest"