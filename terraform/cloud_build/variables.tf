variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "service_account" {
  type = string
}

variable "repository_id" {
  description = "ID do repositório Cloud Build Gen2"
  type        = string
}

variable "trigger_name" {
  type    = string
}
