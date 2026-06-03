# 🎓 AI Study Buddy

<div align="center">

### AI-Powered Personalized Learning Platform with Complete DevOps Automation

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Application-red?style=for-the-badge\&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge\&logo=docker)
![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-red?style=for-the-badge\&logo=jenkins)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?style=for-the-badge\&logo=terraform)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue?style=for-the-badge\&logo=kubernetes)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange?style=for-the-badge\&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-yellow?style=for-the-badge\&logo=grafana)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?style=for-the-badge\&logo=amazonaws)

</div>

---

# 📖 Project Overview

AI Study Buddy is a cloud-native educational platform designed to provide personalized learning assistance while demonstrating a complete end-to-end DevOps implementation. The project combines Artificial Intelligence, Cloud Computing, Infrastructure as Code (IaC), Containerization, CI/CD Automation, Kubernetes Orchestration, and Monitoring into a single production-oriented solution.

The application is developed using Python and Streamlit and deployed on AWS EC2 using Docker containers. The deployment lifecycle is automated through Jenkins CI/CD pipelines, infrastructure provisioning is handled using Terraform, and monitoring is achieved through Prometheus, Grafana, and Node Exporter.

This project serves as both:

* An AI-powered educational platform
* A practical implementation of modern DevOps practices

---

# 🎯 Project Objectives

The primary objectives of this project are:

### Educational Objectives

* Provide personalized study assistance
* Create an interactive learning environment
* Enhance student learning experience
* Demonstrate AI-assisted education concepts

### Technical Objectives

* Implement Infrastructure as Code (IaC)
* Automate deployment through CI/CD
* Containerize the application using Docker
* Deploy cloud infrastructure on AWS
* Demonstrate Kubernetes configuration and orchestration
* Implement real-time monitoring and observability
* Follow modern DevOps best practices

---

# 🚀 Key Features

## Application Features

### 📚 Personalized Learning Support

Provides intelligent educational assistance tailored to learning needs.

### 🎨 Interactive User Interface

Built using Streamlit for a modern and user-friendly experience.

### ⚡ Fast and Lightweight Deployment

Containerized architecture ensures efficient deployment and portability.

### ☁ Cloud Hosted

Application deployed on AWS EC2 for accessibility and scalability.

---

## DevOps Features

### 🔄 CI/CD Automation

Automated build and deployment using Jenkins.

### 🐳 Docker Containerization

Application packaged into portable Docker containers.

### ☸ Kubernetes Configuration

Deployment manifests prepared for container orchestration.

### 🏗 Infrastructure as Code

AWS infrastructure provisioned using Terraform.

### 📊 Real-Time Monitoring

Prometheus and Node Exporter collect metrics.

### 📈 Dashboard Visualization

Grafana dashboards provide infrastructure insights.

---

# 🏗 System Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
Jenkins CI/CD Pipeline
    │
    ▼
Docker Build Process
    │
    ▼
Docker Containers
    │
    ▼
AWS EC2 (t3.small)
    │
 ┌──┼─────────────────────────────┐
 │  │                             │
 ▼  ▼                             ▼
Application                 Prometheus
(Streamlit)                     │
                                 ▼
                          Node Exporter
                                 │
                                 ▼
                              Grafana
```

---

# 🛠 Technology Stack

| Category                   | Technology     |
| -------------------------- | -------------- |
| Programming Language       | Python         |
| Frontend Framework         | Streamlit      |
| Version Control            | Git            |
| Repository Hosting         | GitHub         |
| Containerization           | Docker         |
| Multi-Container Management | Docker Compose |
| CI/CD                      | Jenkins        |
| Infrastructure as Code     | Terraform      |
| Container Orchestration    | Kubernetes     |
| Cloud Platform             | AWS EC2        |
| Monitoring                 | Prometheus     |
| Visualization              | Grafana        |
| Metrics Collection         | Node Exporter  |

---

# ☁ Cloud Infrastructure

The project is deployed on Amazon Web Services (AWS).

### Deployment Environment

| Component        | Details          |
| ---------------- | ---------------- |
| Cloud Provider   | AWS              |
| Compute Service  | EC2              |
| Instance Type    | t3.small         |
| Operating System | Ubuntu 24.04 LTS |
| Region           | ap-south-1       |
| Access Method    | SSH              |

---

# 📂 Repository Structure

```text
AI_STUDY_BUDDY_PRO
│
├── .streamlit/                  # Streamlit configuration
├── .venv/                       # Python virtual environment
│
├── app/                         # Application source code
│
├── jenkins/                     # Jenkins pipeline files
│
├── kubernetes/                  # Kubernetes manifests
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── namespace.yaml
│   ├── secret.yaml
│   └── service.yaml
│
├── monitoring/
│   ├── grafana/
│   └── prometheus/
│
├── terraform/                   # Infrastructure as Code files
│
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── Project_Presentation.pptx
├── Project_Report.pdf
│
└── README.md
```

---

# 🔄 Complete DevOps Workflow

```text
Code Development
       │
       ▼
Git Commit
       │
       ▼
GitHub Push
       │
       ▼
Jenkins Pipeline
       │
       ▼
Docker Build
       │
       ▼
Container Deployment
       │
       ▼
AWS EC2 Hosting
       │
       ▼
Prometheus Monitoring
       │
       ▼
Grafana Visualization
```
---

# ⚙️ Installation & Setup Guide

This section explains how to set up and run AI Study Buddy in a local environment and deploy it using Docker.

---

# 📋 Prerequisites

Before running the project, ensure the following software is installed on your system.

## Required Software

| Software       | Version |
| -------------- | ------- |
| Python         | 3.10+   |
| Git            | Latest  |
| Docker         | Latest  |
| Docker Compose | Latest  |
| Terraform      | Latest  |
| AWS CLI        | Latest  |
| Kubectl        | Latest  |
| Jenkins        | LTS     |
| Prometheus     | Latest  |
| Grafana        | Latest  |

---

# 💻 Local Development Setup

## Step 1: Clone the Repository

Clone the GitHub repository to your local machine.

```bash
git clone https://github.com/the-rahul-tyagi/AiStudyBuddyPro.git

cd AiStudyBuddyPro
```

---

## Step 2: Create Virtual Environment

A Python virtual environment is used to isolate project dependencies.

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

After activation, the terminal prompt should display:

```text
(.venv)
```

---

## Step 3: Install Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create and configure the `.env` file.

Location:

```text
AI_STUDY_BUDDY_PRO/.env
```

Example:

```env
OPENAI_API_KEY=your_api_key_here
APP_ENV=development
```

### Why Environment Variables?

Environment variables help:

* Secure sensitive information
* Separate configuration from code
* Support multiple deployment environments

---

## Step 5: Run the Application

Start the Streamlit application.

```bash
streamlit run app/app.py
```

Application URL:

```text
http://localhost:8501
```

---

# 🐳 Docker Deployment

---

# Why Docker?

Docker was used to package the application into a portable container.

Benefits include:

* Consistent execution environment
* Easy deployment
* Simplified dependency management
* Platform independence

---

# Docker Architecture

```text
Application Source Code
          │
          ▼
       Dockerfile
          │
          ▼
      Docker Image
          │
          ▼
    Docker Container
          │
          ▼
      AWS EC2 Server
```

---

# Dockerfile Overview

The Dockerfile defines how the application image is created.

### Main Responsibilities

* Select Python base image
* Install dependencies
* Copy application files
* Configure Streamlit
* Start application

---

# Build Docker Image

Create the Docker image.

```bash
docker build -t ai-study-buddy-pro .
```

Verify image creation.

```bash
docker images
```

Expected image:

```text
ai-study-buddy-pro
```

---

# Run Docker Container

Start the application container.

```bash
docker run -d \
--name ai-study-buddy-container \
-p 8501:8501 \
--env-file .env \
ai-study-buddy-pro
```

---

# Verify Container Status

```bash
docker ps
```

Expected container:

```text
ai-study-buddy-container
```

---

# View Container Logs

```bash
docker logs ai-study-buddy-container
```

---

# Restart Container

```bash
docker restart ai-study-buddy-container
```

---

# Stop Container

```bash
docker stop ai-study-buddy-container
```

---

# Remove Container

```bash
docker rm ai-study-buddy-container
```

---

# 🐳 Docker Compose Setup

The project uses Docker Compose to manage multiple services simultaneously.

---

# Services Managed

| Service     | Container Name           |
| ----------- | ------------------------ |
| Application | ai-study-buddy-container |
| Jenkins     | jenkins-container        |
| Prometheus  | prometheus-container     |
| Grafana     | grafana-container        |

---

# Start All Services

```bash
docker compose up -d
```

---

# Stop All Services

```bash
docker compose down
```

---

# Check Running Services

```bash
docker compose ps
```

---

# View Logs

```bash
docker compose logs
```

---

# ☁️ AWS Deployment

---

# Deployment Environment

The application is deployed on an Amazon EC2 instance.

| Parameter        | Value               |
| ---------------- | ------------------- |
| Cloud Provider   | AWS                 |
| Service          | EC2                 |
| Instance Type    | t3.small            |
| Operating System | Ubuntu 24.04 LTS    |
| Region           | ap-south-1 (Mumbai) |

---

# Why t3.small?

The t3.small instance was selected because it provides:

* 2 vCPUs
* 2 GB RAM
* Better performance than t2.micro
* Ability to run multiple containers simultaneously
* Cost-effective for academic projects

---

# Connect to EC2

Use SSH to access the server.

```bash
ssh -i ai-study-buddy-key.pem ubuntu@<PUBLIC_IP>
```

Example:

```bash
ssh -i ai-study-buddy-key.pem ubuntu@3.x.x.x
```

---

# Clone Repository on EC2

```bash
git clone https://github.com/the-rahul-tyagi/AiStudyBuddyPro.git

cd AiStudyBuddyPro
```

---

# Deploy Services

```bash
docker compose up -d
```

---

# Verify Running Containers

```bash
docker ps
```

Expected containers:

```text
ai-study-buddy-container
jenkins-container
prometheus-container
grafana-container
```

---

# 🔒 Security Group Configuration

The following inbound rules were configured on AWS.

| Port | Protocol | Purpose                    |
| ---- | -------- | -------------------------- |
| 22   | TCP      | SSH Access                 |
| 8081 | TCP      | Jenkins Dashboard          |
| 8501 | TCP      | AI Study Buddy Application |
| 9090 | TCP      | Prometheus                 |
| 3000 | TCP      | Grafana                    |
| 9100 | TCP      | Node Exporter              |

---

# 🌐 Service Endpoints

Replace `<EC2_PUBLIC_IP>` with your server IP address.

## AI Study Buddy Application

```text
http://<EC2_PUBLIC_IP>:8501
```

---

## Jenkins

```text
http://<EC2_PUBLIC_IP>:8081
```

---

## Prometheus

```text
http://<EC2_PUBLIC_IP>:9090
```

---

## Grafana

```text
http://<EC2_PUBLIC_IP>:3000
```

---

# 📸 Screenshots to Include

Add screenshots of:

### Application

* Home Page
* Main Dashboard

### Docker

* `docker ps` Output
* Docker Images

### AWS

* EC2 Instance Details
* Security Group Rules

### Deployment

* Running Containers
* Successful Application Access

---

# 🔄 CI/CD Pipeline with Jenkins

One of the primary goals of this project was to automate the software delivery process using Continuous Integration and Continuous Deployment (CI/CD).

Jenkins was integrated to automatically build and deploy the application whenever changes are pushed to the GitHub repository.

This eliminates manual deployment steps and ensures consistency across deployments.

---

# Why Jenkins?

Traditional Deployment Process:

```text
Developer
    │
    ▼
Manual Build
    │
    ▼
Manual Deployment
    │
    ▼
Manual Verification
```

Problems:

* Time consuming
* Human errors
* Inconsistent deployments
* Difficult maintenance

---

Automated Deployment Process:

```text
Developer
    │
    ▼
Git Push
    │
    ▼
GitHub Repository
    │
    ▼
Jenkins Pipeline
    │
    ▼
Build & Deploy
    │
    ▼
Application Updated
```

Benefits:

* Automated deployment
* Faster delivery
* Reduced human intervention
* Consistent releases
* Improved productivity

---

# Jenkins Architecture

```text
GitHub Repository
        │
        ▼
     Jenkins
        │
 ┌──────┼────────┐
 │      │        │
 ▼      ▼        ▼
Build  Deploy  Verify
        │
        ▼
 Docker Container
        │
        ▼
 AWS EC2 Server
```

---

# Jenkins Deployment

Jenkins was deployed as a Docker container on the AWS EC2 instance.

### Container Details

| Property       | Value               |
| -------------- | ------------------- |
| Container Name | jenkins-container   |
| Image          | jenkins/jenkins:lts |
| Port Mapping   | 8081:8080           |
| Purpose        | CI/CD Automation    |

---

# Jenkins Dashboard Access

```text
http://<EC2_PUBLIC_IP>:8081
```

Example:

```text
http://3.x.x.x:8081
```

---

# Jenkins Pipeline Workflow

The pipeline automates the complete deployment process.

### Stage 1 – Source Code Checkout

Retrieves the latest code from GitHub.

Purpose:

* Fetch latest commit
* Ensure latest version deployment

---

### Stage 2 – Verify Environment

Checks required tools and dependencies.

Example:

```bash
docker --version
```

Purpose:

* Verify Docker availability
* Validate deployment environment

---

### Stage 3 – Build Docker Image

Builds application image.

```bash
docker build -t ai-study-buddy-pro .
```

Output:

```text
Docker Image Created Successfully
```

---

### Stage 4 – Stop Existing Container

Stops previously deployed container.

```bash
docker stop ai-study-buddy-container
```

---

### Stage 5 – Remove Existing Container

Removes old container.

```bash
docker rm ai-study-buddy-container
```

---

### Stage 6 – Deploy New Container

Launches latest application version.

```bash
docker run -d \
--name ai-study-buddy-container \
-p 8501:8501 \
--env-file .env \
ai-study-buddy-pro
```

---

### Stage 7 – Deployment Verification

Verifies successful deployment.

Checks:

* Container running
* Port exposed
* Application accessible

---

# Jenkins Pipeline Flow

```text
Code Push
    │
    ▼
GitHub
    │
    ▼
Jenkins Trigger
    │
    ▼
Checkout Repository
    │
    ▼
Build Docker Image
    │
    ▼
Deploy Container
    │
    ▼
Verify Deployment
    │
    ▼
Application Live
```

---

# Jenkins Commands Used

View Running Containers:

```bash
docker ps
```

Access Jenkins Container:

```bash
docker exec -it jenkins-container bash
```

View Jenkins Logs:

```bash
docker logs jenkins-container
```

Restart Jenkins:

```bash
docker restart jenkins-container
```

---

# 🏗 Infrastructure as Code (Terraform)

Infrastructure provisioning was automated using Terraform.

Terraform allows infrastructure resources to be defined and managed through code instead of manual AWS configuration.

---

# Why Terraform?

Without Terraform:

```text
AWS Console
     │
Manual Resource Creation
     │
Manual Configuration
```

Problems:

* Time consuming
* Difficult to reproduce
* Error prone

---

With Terraform:

```text
Terraform Code
        │
        ▼
terraform apply
        │
        ▼
AWS Infrastructure
```

Benefits:

* Automation
* Repeatability
* Version Control
* Consistency

---

# Terraform Folder Structure

```text
terraform/
│
├── provider.tf
├── main.tf
├── variables.tf
├── outputs.tf
└── terraform.tfvars
```

---

# Terraform Components

## provider.tf

Responsible for AWS provider configuration.

Purpose:

* Connect Terraform to AWS
* Configure deployment region

---

## variables.tf

Stores reusable variables.

Examples:

* Region
* Instance Type
* Key Pair Name

---

## terraform.tfvars

Contains actual values.

Examples:

```text
Region = ap-south-1
Instance Type = t3.small
```

---

## main.tf

Creates AWS resources.

Resources include:

* EC2 Instance
* Security Groups
* Network Configuration

---

## outputs.tf

Displays deployment information.

Examples:

* Public IP
* Instance Details

---

# Terraform Workflow

```text
Terraform Files
       │
       ▼
terraform init
       │
       ▼
terraform validate
       │
       ▼
terraform plan
       │
       ▼
terraform apply
       │
       ▼
AWS Infrastructure
```

---

# Terraform Commands Used

Initialize:

```bash
terraform init
```

Validate:

```bash
terraform validate
```

Execution Plan:

```bash
terraform plan
```

Provision Resources:

```bash
terraform apply
```

Destroy Infrastructure:

```bash
terraform destroy
```

---

# AWS Infrastructure Provisioned

The project was deployed on:

| Resource        | Details          |
| --------------- | ---------------- |
| Cloud Provider  | AWS              |
| Compute Service | EC2              |
| Instance Type   | t3.small         |
| Region          | ap-south-1       |
| OS              | Ubuntu 24.04 LTS |

---

# ☸ Kubernetes Configuration

Kubernetes manifests were created to demonstrate container orchestration and production deployment readiness.

Although the primary deployment was Docker-based on AWS EC2, Kubernetes resources were configured and tested locally.

---

# Kubernetes Folder Structure

```text
kubernetes/
│
├── namespace.yaml
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
└── service.yaml
```

---

# Kubernetes Resources

### Namespace

Provides resource isolation.

File:

```text
namespace.yaml
```

---

### ConfigMap

Stores application configuration.

File:

```text
configmap.yaml
```

---

### Secret

Stores sensitive values.

File:

```text
secret.yaml
```

Examples:

* API Keys
* Tokens
* Credentials

---

### Deployment

Manages application Pods.

File:

```text
deployment.yaml
```

Responsibilities:

* Pod creation
* Replica management
* Rolling updates

---

### Service

Exposes application to users.

File:

```text
service.yaml
```

Responsibilities:

* Stable endpoint
* Internal communication
* Load balancing

---

# Kubernetes Architecture

```text
Namespace
     │
     ▼
Deployment
     │
     ▼
Pods
     │
     ▼
Service
     │
     ▼
Users
```

---

# Kubernetes Commands Used

Check Nodes:

```bash
kubectl get nodes
```

Check Pods:

```bash
kubectl get pods
```

Check Deployments:

```bash
kubectl get deployments
```

Check Services:

```bash
kubectl get services
```

Apply Namespace:

```bash
kubectl apply -f namespace.yaml
```

Apply Deployment:

```bash
kubectl apply -f deployment.yaml
```

Apply Service:

```bash
kubectl apply -f service.yaml
```

---

# 📸 Screenshots to Include

### Jenkins

* Jenkins Dashboard
* Successful Build
* Pipeline Stages

### Terraform

* terraform apply Output
* AWS EC2 Instance Dashboard

### Kubernetes

* kubectl get nodes
* kubectl get deployments
* kubectl get services

### Docker

* docker ps Output showing:

  * ai-study-buddy-container
  * jenkins-container
  * prometheus-container
  * grafana-container
  * node-exporter

---

# 📊 Monitoring & Observability

Monitoring is a critical component of modern DevOps practices. After deployment, applications and infrastructure must be continuously monitored to ensure reliability, performance, and availability.

For this project, a complete monitoring stack was implemented using:

* Prometheus
* Grafana
* Node Exporter

These tools provide real-time visibility into system performance and application health.

---

# Monitoring Architecture

```text
AWS EC2 (t3.small)
        │
        ▼
  Node Exporter
        │
        ▼
   Prometheus
        │
        ▼
    Grafana
        │
        ▼
 Monitoring Dashboard
```

---

# Why Monitoring?

Monitoring helps answer important operational questions:

### Infrastructure Monitoring

* Is CPU usage increasing?
* Is memory sufficient?
* Is disk space running low?
* Is network traffic normal?

### Application Monitoring

* Is the application running?
* Are containers healthy?
* Are services reachable?

### Performance Analysis

* Resource utilization trends
* System bottlenecks
* Capacity planning

---

# 📈 Prometheus

Prometheus is an open-source monitoring and alerting toolkit used for collecting and storing metrics.

In this project, Prometheus acts as the central metrics collection system.

---

# Prometheus Responsibilities

* Metrics Collection
* Time-Series Data Storage
* Target Monitoring
* Query Processing
* Integration with Grafana

---

# Prometheus Container

| Property       | Value                |
| -------------- | -------------------- |
| Container Name | prometheus-container |
| Image          | prom/prometheus      |
| Port           | 9090                 |

Access URL:

```text
http://<EC2_PUBLIC_IP>:9090
```

---

# Prometheus Configuration

Configuration File:

```text
monitoring/prometheus/prometheus.yml
```

The configuration defines:

* Scrape intervals
* Target endpoints
* Monitoring jobs

Example Targets:

```yaml
scrape_configs:

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

---

# Target Monitoring

Configured targets:

| Target             | Purpose                    |
| ------------------ | -------------------------- |
| localhost:9090     | Prometheus Self Monitoring |
| node-exporter:9100 | System Metrics Collection  |

---

# Useful Prometheus Queries

Check Target Status:

```promql
up
```

CPU Metrics:

```promql
rate(node_cpu_seconds_total[5m])
```

Memory Metrics:

```promql
node_memory_MemAvailable_bytes
```

---

# 📡 Node Exporter

Node Exporter exposes Linux system metrics to Prometheus.

---

# Node Exporter Container

| Property       | Value              |
| -------------- | ------------------ |
| Container Name | node-exporter      |
| Image          | prom/node-exporter |
| Port           | 9100               |

---

# Metrics Collected

### CPU Metrics

* CPU Utilization
* CPU Load
* CPU Time

### Memory Metrics

* RAM Usage
* Available Memory
* Cached Memory

### Disk Metrics

* Disk Utilization
* Free Space
* Filesystem Information

### Network Metrics

* Incoming Traffic
* Outgoing Traffic
* Interface Statistics

---

# Node Exporter Verification

Verify metrics:

```bash
docker exec -it prometheus-container \
wget -qO- http://node-exporter:9100/metrics
```

Expected Output:

```text
# HELP go_gc_duration_seconds
# TYPE go_gc_duration_seconds summary
...
```

---

# 📊 Grafana

Grafana is an open-source analytics and visualization platform used to display monitoring metrics.

Grafana retrieves data from Prometheus and presents it through interactive dashboards.

---

# Grafana Container

| Property       | Value             |
| -------------- | ----------------- |
| Container Name | grafana-container |
| Image          | grafana/grafana   |
| Port           | 3000              |

Access URL:

```text
http://<EC2_PUBLIC_IP>:3000
```

---

# Grafana Dashboard Features

The monitoring dashboard provides:

### CPU Monitoring

* CPU Utilization
* CPU Load
* Historical Trends

### Memory Monitoring

* Used Memory
* Available Memory
* Memory Trends

### Disk Monitoring

* Disk Usage
* Free Space
* Filesystem Health

### Network Monitoring

* Network Throughput
* Interface Statistics

### System Health

* Host Status
* Uptime
* Resource Availability

---

# Monitoring Stack Summary

| Component     | Purpose                |
| ------------- | ---------------------- |
| Node Exporter | Collect System Metrics |
| Prometheus    | Store Metrics          |
| Grafana       | Visualize Metrics      |

---

# 🐳 Containers Used in Project

The following containers were deployed during project implementation.

| Container Name           | Purpose                |
| ------------------------ | ---------------------- |
| ai-study-buddy-container | Main Application       |
| jenkins-container        | CI/CD Pipeline         |
| prometheus-container     | Monitoring             |
| grafana-container        | Visualization          |
| node-exporter            | Infrastructure Metrics |

---

# Docker Network Configuration

Container communication was enabled through Docker networking.

Useful Commands:

List Networks:

```bash
docker network ls
```

Inspect Network:

```bash
docker network inspect bridge
```

Purpose:

* Prometheus ↔ Node Exporter Communication
* Grafana ↔ Prometheus Communication
* Service Discovery

---

# ⚠ Challenges Faced During Development

Real-world projects often encounter deployment and configuration challenges.

Several issues were encountered and resolved during implementation.

---

# Challenge 1: Jenkins Build Failure

Issue:

```text
.env file not found
```

Cause:

Jenkins workspace did not contain required environment variables.

Solution:

* Created .env file in deployment environment
* Updated deployment configuration

Result:

Successful build and deployment.

---

# Challenge 2: Docker Container Conflict

Issue:

```text
Container name already in use
```

Cause:

Existing container with identical name.

Solution:

```bash
docker stop container-name

docker rm container-name
```

Result:

Container recreated successfully.

---

# Challenge 3: Prometheus Target DOWN

Issue:

Node Exporter target showing DOWN.

Cause:

Network communication issue between containers.

Solution:

* Verified Docker network
* Updated Prometheus configuration
* Restarted monitoring containers

Result:

Target status changed to UP.

---

# Challenge 4: Grafana No Data

Issue:

Dashboard displaying:

```text
No Data
```

Cause:

Prometheus datasource misconfiguration.

Solution:

* Verified datasource URL
* Tested Prometheus connectivity
* Reloaded dashboards

Result:

Metrics displayed correctly.

---

# Challenge 5: Kubernetes Resources Not Visible

Issue:

```bash
kubectl get pods
```

Output:

```text
No resources found
```

Cause:

Manifests had not been applied.

Solution:

```bash
kubectl apply -f deployment.yaml
```

Result:

Resources created successfully.

---

# 🏆 Project Outcomes

The project successfully achieved all planned objectives.

---

## Application Outcomes

✅ AI Study Buddy Application Developed

✅ Interactive Streamlit Interface

✅ Cloud Deployment Successful

---

## DevOps Outcomes

✅ Git & GitHub Integration

✅ Docker Containerization

✅ Jenkins CI/CD Automation

✅ Terraform Infrastructure Provisioning

✅ Kubernetes Configuration

---

## Monitoring Outcomes

✅ Prometheus Operational

✅ Node Exporter Metrics Collection

✅ Grafana Dashboard Visualization

✅ Real-Time Monitoring Enabled

---

# 📸 Screenshots Section

Add screenshots for:

### Application

* Home Page
* User Interface

### AWS

* EC2 Dashboard
* Security Group Configuration

### Docker

* docker ps Output
* Running Containers

### Jenkins

* Jenkins Dashboard
* Successful Build

### Terraform

* terraform apply Output

### Kubernetes

* kubectl get nodes
* kubectl get deployments
* kubectl get services

### Prometheus

* Target Status Page
* Metrics Queries

### Grafana

* Node Exporter Dashboard
* System Monitoring Dashboard

---

# 🚀 Future Enhancements

The project can be extended with:

### Application Improvements

* User Authentication
* Learning Analytics
* Progress Tracking
* AI Chatbot Integration

### DevOps Enhancements

* GitHub Actions
* SonarQube Integration
* Automated Testing
* Container Registry Integration

### Cloud Enhancements

* AWS ECS
* Amazon EKS
* Application Load Balancer
* Auto Scaling Groups

### Monitoring Enhancements

* AlertManager
* Email Notifications
* Slack Alerts
* Centralized Logging

---

# 👨‍💻 Author

**Rahul Tyagi**

Computer Science Student | DevOps Enthusiast | Cloud Learner

### Skills Demonstrated

* Python
* Streamlit
* Git & GitHub
* Docker
* Docker Compose
* Jenkins
* Terraform
* Kubernetes
* AWS EC2
* Prometheus
* Grafana
* Linux Administration

---

# 📄 License

This project is developed for:

* Academic Learning
* DevOps Practice
* Cloud Computing Demonstration
* Portfolio Development

Feel free to explore, learn, and extend the project.

---

# ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 📢 Share it with others

---

# 🎯 Conclusion

AI Study Buddy demonstrates the complete software delivery lifecycle using modern DevOps tools and practices. The project integrates application development, cloud deployment, automation, infrastructure provisioning, container orchestration, and monitoring into a single end-to-end solution.

By combining Python, Streamlit, Docker, Jenkins, Terraform, Kubernetes, AWS, Prometheus, Grafana, and Node Exporter, the project showcases practical implementation of industry-standard DevOps workflows and serves as a strong academic and professional portfolio project.