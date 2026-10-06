terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.38"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment_v1" "ai_assisted_devops" {
  metadata {
    name = "ai-assisted-devops"
    labels = {
      app = "ai-assisted-devops"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "ai-assisted-devops"
      }
    }

    template {
      metadata {
        labels = {
          app = "ai-assisted-devops"
        }
      }

      spec {
        automount_service_account_token = false
        enable_service_links            = false

        container {
          name              = "ai-assisted-devops"
          image             = "ai-assisted-devops-platform:3"
          image_pull_policy = "IfNotPresent"

          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "ai_assisted_devops" {
  metadata {
    name = "ai-assisted-devops-service"
  }

  spec {
    type = "NodePort"


    selector = {
      app = "ai-assisted-devops"
    }

    port {
      port        = 5000
      target_port = 5000
    }
  }
}
