variable "project_id" {
  type = string
  default = "playwright-pytest-gcp-2508"
}

variable "region" {
  type    = string
  default = "asia-east1"
}

variable "terraform_repo" {
  type    = string
  default = "playwright-terraform-repo"
}

variable "service_name" {
  type    = string
  default = "playwright-terraform-service"
}

variable "port" {
  type    = number
  default = 9801
}

variable "image_name" {
  type    = string
  default = "playwright-terraform-image"
}

variable "image_tag" {
  type = string
  default = "latest"
}

variable "deploy_timestamp" {
  type    = string
  default = ""
}
