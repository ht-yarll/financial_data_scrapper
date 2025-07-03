resource "google_cloudbuild_trigger" "test-trigger" {
  name     = "test-trigger"
  location = var.region # Região do Cloud Build
  description = "Trigger para executar testes automatizados"
  tags = ["tests"]

  service_account = var.service_account

  filename = "test-trigger.cloudbuild.yaml"

  # Dispara em push na branch main
  github {
    owner = var.github_owner
    name  = var.github_repo

    pull_request { 
        branch = "master" 
        }
  }
}