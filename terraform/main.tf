provider "google" {
  project = var.project_id
  region  = var.region
}

module "cloud_build" {
  source = "./cloud_build"
  
  project_id = var.project_id
  region     = var.region

  github_owner = var.github_owner
  github_repo  = var.github_repo

  app_name = var.app_name
}