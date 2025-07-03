resource "google_artifact_registry_repository" "creating_repository" {
  provider = google-beta
  location = var.region
  repository_id = var.repository_id
  description = var.description
  format = var.format
}