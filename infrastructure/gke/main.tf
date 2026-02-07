# Terraform configuration for GKE cluster

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# GKE Cluster
resource "google_container_cluster" "todo_gke" {
  name     = "todo-gke"
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  depends_on = [
    google_project_service.container,
    google_project_service.compute
  ]
}

# Default node pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-nodes"
  location   = var.zone
  cluster    = google_container_cluster.todo_gke.name
  node_count = var.node_count

  node_config {
    preemptible  = true
    machine_type = var.machine_type

    labels = {
      env = var.environment
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# Enable required services
resource "google_project_service" "container" {
  service = "container.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  project = var.project_id
}

# Variables
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-west1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-west1-a"
}

variable "node_count" {
  description = "Number of nodes in the node pool"
  type        = number
  default     = 2
}

variable "machine_type" {
  description = "Machine type for the nodes"
  type        = string
  default     = "e2-medium"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Outputs
output "cluster_name" {
  value = google_container_cluster.todo_gke.name
}

output "cluster_endpoint" {
  value     = google_container_cluster.todo_gke.endpoint
  sensitive = true
}

output "cluster_ca_certificate" {
  value     = google_container_cluster.todo_gke.master_auth.0.cluster_ca_certificate
  sensitive = true
}

output "cluster_location" {
  value = google_container_cluster.todo_gke.location
}

output "cluster_project" {
  value = google_container_cluster.todo_gke.project
}