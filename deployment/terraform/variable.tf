variable "project_id" {}
variable "region" {}
variable "service_name" {}
variable "image_url" {}
variable "gcp_credentials_file" {
  description = "Path to GCP credentials JSON file"
  type        = string
}