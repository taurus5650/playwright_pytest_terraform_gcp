provider "google" {
  project = var.project_id
  region = var.region
}

resource "google-artifact-registry-repository" "repo" {
  location      = var.region
  repository_id = "app-repo"
  format        = "DOCKER"
}

resource "google-cloud-run-service" "service" {
  name      = "playwriht-service"
  location  = var.region

  template {
    spec {
      container {
        image = var.image
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true

}

resource "google-cloud-run-service-iam-member" "noauth" {
  location  = google-cloud-run-service.service.location
  service   = google-cloud-run-service.service.name
  role      = "roles/run.invoker"
  member    = "allUsers"
}