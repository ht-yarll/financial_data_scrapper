provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "project" {
  project_id = var.project_id
}

resource "google_cloudbuildv2_connection" "github_conn" {
  name = "github-connection"
  location = var.region

  github_config {
    app_installation_id = var.github_app_installation_id
    authorizer_credential {
      oauth_token_secret_version = var.secret
    }
  }
}

resource "google_cloudbuildv2_repository" "default" {
  name              = var.github_repo
  remote_uri        = var.github_full_repo
  parent_connection = google_cloudbuildv2_connection.github_conn.id
  location          = var.region
}

module "project-services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  version                     = "17.0.0"
  disable_services_on_destroy = false

  project_id  = var.project_id
  enable_apis = true

  activate_apis = [
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
    "iam.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "servicemanagement.googleapis.com",
    "compute.googleapis.com",
    "bigquery.googleapis.com"
  ]
}

module "iam" {
  source = "./iam"
  project_id = var.project_id
}

module "cloud_build" {
  source = "./cloud_build"

  project_id = var.project_id
  region     = var.region
  service_account = "projects/${var.project_id}/serviceAccounts/${var.service_account}"
  
  repository_id = google_cloudbuildv2_repository.default.id
  selenium = var.selenium

  trigger_name = var.trigger_test
}