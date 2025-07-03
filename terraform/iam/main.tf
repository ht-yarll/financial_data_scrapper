resource "google_service_account" "cloudbuild_sa" {
  account_id   = "cloudbuild-sa"
  display_name = "cloudbuild-sa"
  description  = "Cloud build service account"
}

resource "google_service_account" "airflow_sa" {
  account_id   = "airflow-sa"
  display_name = "airflow-sa"
  description  = "Cloud build service account"
}

resource "google_project_iam_member" "cloudbuild_roles" {
  for_each = toset(var.cloudbuild_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloudbuild_sa.email}"
}

resource "google_project_iam_member" "airflow_roles" {
  for_each = toset(var.airflow_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.airflow_sa.email}"
}