# Terraform configuration for AKS cluster

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "todo_rg" {
  name     = "todo-rg"
  location = var.location
}

# Log Analytics Workspace for monitoring
resource "azurerm_log_analytics_workspace" "todo_logs" {
  name                = "todo-logs"
  location            = azurerm_resource_group.todo_rg.location
  resource_group_name = azurerm_resource_group.todo_rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "todo_aks" {
  name                = "todo-aks"
  location            = azurerm_resource_group.todo_rg.location
  resource_group_name = azurerm_resource_group.todo_rg.name
  dns_prefix          = "todoaks"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  identity {
    type = "SystemAssigned"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.todo_logs.id
  }

  depends_on = [
    azurerm_resource_group.todo_rg
  ]
}

# Variables
variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "West US 2"
}

variable "node_count" {
  description = "Number of nodes in the node pool"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "VM size for the nodes"
  type        = string
  default     = "Standard_D2_v2"
}

# Outputs
output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.todo_aks.name
}

output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.todo_aks.id
}

output "aks_kube_config" {
  value     = azurerm_kubernetes_cluster.todo_aks.kube_config_raw
  sensitive = true
}

output "aks_host" {
  value     = azurerm_kubernetes_cluster.todo_aks.kube_config.0.host
  sensitive = true
}

output "aks_client_certificate" {
  value     = azurerm_kubernetes_cluster.todo_aks.kube_config.0.client_certificate
  sensitive = true
}

output "aks_client_key" {
  value     = azurerm_kubernetes_cluster.todo_aks.kube_config.0.client_key
  sensitive = true
}

output "aks_cluster_ca_certificate" {
  value     = azurerm_kubernetes_cluster.todo_aks.kube_config.0.cluster_ca_certificate
  sensitive = true
}