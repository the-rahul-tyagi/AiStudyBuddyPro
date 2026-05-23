# ==========================================
# TERRAFORM CONFIGURATION & PROVIDERS
# ==========================================
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Set the AWS Region to Mumbai for lower latency in India
provider "aws" {
  region = "ap-south-1"
}

# ==========================================
# DATA SOURCES
# ==========================================
# Dynamically fetches the latest Ubuntu 22.04 LTS AMI in the selected region.
# This prevents the script from breaking if AWS changes hardcoded AMI IDs.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS Account ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ==========================================
# SECURITY GROUPS (FIREWALL RULES)
# ==========================================
resource "aws_security_group" "aistudybuddy_sg" {
  name        = "aistudybuddy_security_group"
  description = "Firewall rules for AI Study Buddy Pro"

  # Inbound: Allow SSH for terminal access
  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Note: In a strict corporate environment, this would be locked to a specific VPN IP
  }

  # Inbound: Allow standard HTTP web traffic
  ingress {
    description = "HTTP Traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound: Allow Streamlit application traffic
  ingress {
    description = "Streamlit App Port"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound: Allow Jenkins Dashboard
  ingress {
    description = "Jenkins Dashboard"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: Allow the server to download updates and pull from GitHub/Docker
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1 means all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ==========================================
# EC2 INSTANCE (VIRTUAL SERVER)
# ==========================================
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro" # Free-tier eligible in newer AWS accounts

  # Attach the firewall rules created above
  vpc_security_group_ids = [aws_security_group.aistudybuddy_sg.id]

  # Bootstrap script: Runs once automatically when the server boots for the first time
  user_data = <<-EOF
              #!/bin/bash
              # Update package lists
              sudo apt-get update -y
              
              # Install Docker and Docker Compose
              sudo apt-get install -y docker.io docker-compose
              
              # Start and enable Docker service to run on boot
              sudo systemctl start docker
              sudo systemctl enable docker
              
              # Grant the default 'ubuntu' user permission to run docker commands without sudo
              sudo usermod -aG docker ubuntu
              EOF

  # Tag the server so it is easily identifiable in the AWS Console
  tags = {
    Name        = "AiStudyBuddyPro-Production"
    Environment = "Production"
  }
}

# ==========================================
# OUTPUTS
# ==========================================
# Prints the public IP to the terminal after a successful 'terraform apply'
output "server_public_ip" {
  description = "The public IP address to access the Streamlit application."
  value       = aws_instance.app_server.public_ip
}