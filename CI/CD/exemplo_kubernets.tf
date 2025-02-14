###########################
# Provider: Configura o provedor Kubernetes
###########################
provider "kubernetes" {
  # Indica o caminho para o arquivo kubeconfig que conecta ao cluster
  config_path = var.kube_config_path
}

###########################
# Variable: Variáveis de entrada
###########################
variable "kube_config_path" {
  description = "Caminho para o arquivo kubeconfig para acessar o cluster Kubernetes"
  type        = string
  default     = "~/.kube/config"
}

variable "app_image" {
  description = "Imagem Docker da aplicação a ser implantada no cluster Kubernetes"
  type        = string
  default     = "neowaycase-app:latest"
}

###########################
# Locals: Variáveis locais para reutilização
###########################
locals {
  app_name  = "neowaycase-app"
  namespace = "default"
}

###########################
# Resource: Cria um Deployment no Kubernetes para a aplicação
###########################
resource "kubernetes_deployment" "app_deployment" {
  metadata {
    name      = local.app_name
    namespace = local.namespace
    labels = {
      app = local.app_name
    }
  }

  spec {
    replicas = 2  # Número de réplicas para alta disponibilidade

    selector {
      match_labels = {
        app = local.app_name
      }
    }

    template {
      metadata {
        labels = {
          app = local.app_name
        }
      }

      spec {
        container {
          name  = local.app_name
          image = var.app_image

          ports {
            container_port = 8000
          }
        }
      }
    }
  }
  # Esse recurso gerencia os pods que executam a aplicação.
}

###########################
# Resource: Cria um Service para expor o Deployment
###########################
resource "kubernetes_service" "app_service" {
  metadata {
    name      = "${local.app_name}-service"
    namespace = local.namespace
  }

  spec {
    selector = {
      app = local.app_name
    }

    port {
      port        = 8000
      target_port = 8000
    }

    type = "LoadBalancer"  # Permite acesso externo via um IP público
  }
  # Esse recurso cria um endpoint para acessar a aplicação.
}

###########################
# Output: Exibe o endereço IP do Service
###########################
output "service_ip" {
  description = "Endereço IP do Service do Kubernetes para a aplicação"
  # O acesso pode variar conforme o provedor; esse é um exemplo.
  #value       = kubernetes_service.app_service.status[0].load_balancer[0].ingress[0].ip
}

###########################
# Comentários gerais:
# - Provider: define o provedor (Kubernetes).
# - Variable: permite parametrizar valores (ex.: caminho do kubeconfig, imagem da app).
# - Locals: define variáveis locais para uso repetido (ex.: nome da app, namespace).
# - Resource: cria recursos no Kubernetes (Deployment, Service).
# - Output: expõe informações relevantes após o apply (ex.: IP do Service).
