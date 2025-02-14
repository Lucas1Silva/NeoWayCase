###########################
# Provider: Configura o provedor AWS
###########################
provider "aws" {
  # Define a região onde os recursos serão criados.
  region = var.aws_region
}

###########################
# Variable: Variáveis de entrada
###########################
variable "aws_region" {
  description = "Região da AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

###########################
# Locals: Variáveis locais para reutilização
###########################
locals {
  app_name = "neowaycase-app"
}

###########################
# Resource: Cria um repositório no ECR para armazenar imagens Docker
###########################
resource "aws_ecr_repository" "app_repo" {
  name = local.app_name
  # Esse recurso cria um repositório no Amazon ECR
}

###########################
# Resource: Cria uma VPC simples
###########################
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  # Este recurso define uma rede virtual onde outros recursos serão implantados.
}

###########################
# Resource: Cria uma sub-rede pública na VPC
###########################
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  # Esta sub-rede permite a comunicação externa dos recursos.
}

###########################
# Resource: Cria um Cluster ECS para orquestração dos containers
###########################
resource "aws_ecs_cluster" "cluster" {
  name = "${local.app_name}-cluster"
}

###########################
# Resource: Define uma Task do ECS (usando Fargate)
###########################
resource "aws_ecs_task_definition" "app_task" {
  family                   = "${local.app_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = local.app_name,
      image     = "${aws_ecr_repository.app_repo.repository_url}:latest",
      portMappings = [
        {
          containerPort = 8000,
          hostPort      = 8000
        }
      ]
    }
  ])
  # Essa definição instrui o ECS a executar o container com a imagem do ECR.
}

###########################
# Resource: Cria uma IAM Role para permitir que o ECS execute tasks
###########################
resource "aws_iam_role" "ecs_execution_role" {
  name = "ecsExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Principal = { Service = "ecs-tasks.amazonaws.com" },
      Effect    = "Allow",
      Sid       = ""
    }]
  })
  # Essa role permite que o ECS assuma as permissões necessárias para executar as tasks.
}

###########################
# Resource: Anexa a política padrão à IAM Role para execução de tasks ECS
###########################
resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

###########################
# Output: Exibe a URL do repositório ECR
###########################
output "ecr_repository_url" {
  description = "URL do repositório ECR para a aplicação"
  value       = aws_ecr_repository.app_repo.repository_url
}

###########################
# Comentários gerais:
# - Provider: define o provedor (AWS neste caso).
# - Variable: permite parametrizar valores (ex.: região AWS).
# - Locals: define variáveis locais para uso repetido.
# - Resource: cria recursos na AWS (ECR, VPC, Subnet, ECS, IAM Role).
# - Output: expõe informações relevantes após o apply (ex.: URL do repositório).
