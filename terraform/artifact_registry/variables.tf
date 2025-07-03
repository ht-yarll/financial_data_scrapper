variable "region" {
  type = string
}
variable "format" {
  type = string
  default = "DOCKER"
}
variable "description" {
  type = string
  default = "Docker repository for Cloud Build"
}
variable "repository_id" {
  type = string
  default = "gcr-repository"
}
