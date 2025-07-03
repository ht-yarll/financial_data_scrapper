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

variable "app_name" {
  default = "financialdataextraction"
  type = string
}

variable "github_full_repo" {
  default = "https://github.com/ht-yarll/financial_data_scrapper"
  type = string
}