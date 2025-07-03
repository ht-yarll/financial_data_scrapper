variable "project_id" {
  default = "estud-460321"
  type = string
}
variable "region" {
  default = "southamerica-west1"
  type = string
}

variable "service_account" {
  default = "learning-and-grinding@estud-460321.iam.gserviceaccount.com"
  type = string
}

# Cloud Build variables
variable "github_owner" {
  default = "ht-yarll"
  type = string
}
variable "github_repo" {
  default = "financial_data_scrapper"
  type = string
}

variable "remote_uri" {
  default = "projects/estud-460321/locations/southamerica-east1/connections/financial-data-scrapper/repositories/ht-yarll-financial_data_scrapper"
  type = string
}

variable "app_name" {
  default = "financialdataextraction"
  type = string
}

variable "github_full_repo" {
  default = "https://github.com/ht-yarll/financial_data_scrapper.git"
  type = string
}

variable "github_app_installation_id" {
  default = 68211684
  type = number
}

variable "secret" {
  default = "projects/212994923775/secrets/financial-data-scrapper-github-oauthtoken-b70c0a/versions/1"
  type = string
}

variable "trigger_test" {
  default = "test-trigger"
  type    = string
}