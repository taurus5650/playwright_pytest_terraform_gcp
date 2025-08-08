output "url" {
  value = google_cloud_run_service.playwright_terraform_service.status[0].url
}