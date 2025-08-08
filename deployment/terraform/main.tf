provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = var.terraform_repo
  format        = "DOCKER"
}

resource "google_cloud_run_service" "playwright_terraform_service" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.image_url
        ports {
          container_port = var.port
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "noauth" {
  location = var.region
  service  = google_cloud_run_service.playwright_terraform_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
