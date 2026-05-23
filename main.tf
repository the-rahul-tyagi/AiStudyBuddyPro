# ==========================================
# 1. CLOUD PROVIDER CONFIGURATION
# ==========================================
# This block tells Terraform that we are building our infrastructure on Amazon Web Services (AWS).
# We are specifying the 'us-east-1' region, which is a standard, cost-effective region.
provider "aws" {
  region = "us-east-1" 
}

# ==========================================
# 2. SECURITY GROUP (FIREWALL RULES)
# ==========================================
# A Security Group acts as a virtual firewall for your EC2 server. 
# We must explicitly define what inbound (ingress) and outbound (egress) traffic is allowed.
resource "aws_security_group" "aistudybuddy_sg" {
  name        = "aistudybuddy_security_group"
  description = "Allow web traffic, Streamlit, and SSH"

  # INGRESS RULE 1: SSH (Port 22)
  # Allows us to securely log into the server's command line later.
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # 0.0.0.0/0 means "allow from any IP address"
  }

  # INGRESS RULE 2: HTTP (Port 80)
  # Standard web traffic port. Useful if we later set up a domain name or reverse proxy.
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # INGRESS RULE 3: Streamlit (Port 8501)
  # The specific port our AI Study Buddy Pro Docker container runs on.
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # EGRESS RULE: All Outbound Traffic
  # Allows the server to access the internet (crucial for downloading Docker, pulling GitHub code, and calling the Gemini API).
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1 means all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ==========================================
# 3. EC2 INSTANCE (THE VIRTUAL SERVER)
# ==========================================
# This block provisions the actual hardware in the cloud.
resource "aws_instance" "app_server" {
  # AMI (Amazon Machine Image) dictates the Operating System. This specific ID is for Ubuntu 22.04 LTS in us-east-1.
  ami           = "ami-0c7217cdde317cfec" 
  
  # t2.micro is eligible for the AWS Free Tier (1 vCPU, 1GB RAM).
  instance_type = "t3.micro"
  # We attach the security group we created above to this server.
  vpc_security_group_ids = [aws_security_group.aistudybuddy_sg.id]

  # USER DATA: This is a bash script that runs automatically the very first time the server boots up.
  # We use this to install Docker and Docker Compose automatically so the server is ready for our app immediately.
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y docker.io docker-compose
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo usermod -aG docker ubuntu
              EOF

  # Tags help organize and identify resources in the AWS Console.
  tags = {
    Name = "AiStudyBuddyPro-Production"
  }
}

# ==========================================
# 4. OUTPUTS
# ==========================================
# Outputs print useful information to the terminal after Terraform finishes building.
# We want Terraform to tell us the exact public IP address of the new server so we can access our app.
output "server_public_ip" {
  value = aws_instance.app_server.public_ip
}