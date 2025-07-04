resource "google_cloudbuild_trigger" "gen2_trigger" {
  project  = var.project_id
  location = var.region
  name     = var.trigger_name

  service_account = var.service_account

  filename = "test-trigger.cloudbuild.yaml"

  substitutions = {
    _SELENIUM_URL = var.selenium
    }

  repository_event_config {
    repository = var.repository_id

    pull_request {
      branch = "^master$"
    }
  }
}