<div align="center">

# 🎓 AI Study Buddy Pro

**An AI-Powered Personalized Learning Platform with End-to-End DevOps Automation**

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white)](https://jenkins.io)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://terraform.io)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![AWS](https://img.shields.io/badge/AWS_EC2-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)](https://grafana.com)

<br/>

> _Bridging AI-powered education with production-grade DevOps — from code to cloud, fully automated._

<br/>

[Overview](#-overview) · [Features](#-features) · [Architecture](#-system-architecture) · [Tech Stack](#-technology-stack) · [Setup](#-local-development-setup) · [Docker](#-docker-deployment) · [AWS](#️-aws-deployment) · [Jenkins](#-cicd-pipeline--jenkins) · [Terraform](#-infrastructure-as-code--terraform) · [Kubernetes](#️-kubernetes-configuration) · [Monitoring](#-monitoring--observability) · [Roadmap](#-future-enhancements)

</div>

---

## 📖 Overview

**AI Study Buddy Pro** is a cloud-native educational platform that delivers personalized learning assistance through an intelligent AI interface. Beyond the application itself, this project is a complete showcase of modern DevOps practices — covering Infrastructure as Code, CI/CD automation, containerization, Kubernetes orchestration, and real-time observability.

This project serves dual purposes:

- 🤖 **An AI-powered educational platform** — interactive, personalized, and accessible
- ⚙️ **A production-grade DevOps implementation** — automated, monitored, and cloud-deployed

---

## ✨ Features

### Application Features

| Feature                            | Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------ |
| 📚 Personalized Learning Support   | Intelligent educational assistance tailored to individual learning needs |
| 🎨 Interactive User Interface      | Clean, modern UI built with Streamlit                                    |
| ⚡ Fast and Lightweight Deployment | Containerized architecture ensures efficient deployment and portability  |
| ☁️ Cloud Hosted                    | Deployed on AWS EC2 for accessibility and scalability                    |

### DevOps Features

| Feature                     | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| 🔄 CI/CD Automation         | Automated build and deployment using Jenkins              |
| 🐳 Docker Containerization  | Application packaged into portable Docker containers      |
| ☸️ Kubernetes Configuration | Deployment manifests prepared for container orchestration |
| 🏗️ Infrastructure as Code   | AWS infrastructure provisioned using Terraform            |
| 📊 Real-Time Monitoring     | Prometheus and Node Exporter collect metrics              |
| 📈 Dashboard Visualization  | Grafana dashboards provide infrastructure insights        |

---

## 🏗 System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Developer Machine                    │
│                    Code  →  Git Push                     │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
└────────────────────────────┬─────────────────────────────┘
                             │  Webhook Trigger
                             ▼
┌──────────────────────────────────────────────────────────┐
│                  Jenkins CI/CD Pipeline                  │
│       Checkout  →  Build Image  →  Deploy Container      │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                    AWS EC2 (t3.small)                    │
│                                                          │
│  ┌──────────────────┐      ┌──────────────────────────┐  │
│  │  AI Study Buddy  │      │    Monitoring Stack      │  │
│  │   (Streamlit)    │      │                          │  │
│  │     :8501        │      │  Node Exporter  :9100    │  │
│  └──────────────────┘      │  Prometheus     :9090    │  │
│                            │  Grafana        :3000    │  │
│  ┌──────────────────┐      └──────────────────────────┘  │
│  │    Jenkins       │                                    │
│  │    :8081         │                                    │
│  └──────────────────┘                                    │
└──────────────────────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

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

## 📂 Repository Structure

```
AI_STUDY_BUDDY_PRO/
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
│   ├── grafana/                 # Grafana dashboard configs
│   └── prometheus/              # Prometheus scrape configs
│
├── terraform/                   # Infrastructure as Code files
│
├── .dockerignore
├── .env                         # Environment variables (not committed)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── Project_Presentation.pptx
├── Project_Report.pdf
└── README.md
```

---

## 🔄 Complete DevOps Workflow

```
Code Development
      │
      ▼
Git Commit & Push
      │
      ▼
GitHub Repository
      │
      ▼
Jenkins CI/CD Pipeline
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

## ☁ Cloud Infrastructure

### Deployment Environment

| Component        | Details             |
| ---------------- | ------------------- |
| Cloud Provider   | AWS                 |
| Compute Service  | EC2                 |
| Instance Type    | t3.small            |
| Operating System | Ubuntu 24.04 LTS    |
| Region           | ap-south-1 (Mumbai) |
| Access Method    | SSH                 |

---

## 💻 Local Development Setup

### Prerequisites

Ensure the following are installed before proceeding:

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

### Step 1 — Clone the Repository

```bash
git clone https://github.com/the-rahul-tyagi/AiStudyBuddyPro.git
cd AiStudyBuddyPro
```

### Step 2 — Create a Virtual Environment

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, your terminal prompt will show:

```
(.venv)
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Create a `.env` file at `AI_STUDY_BUDDY_PRO/.env`:

```env
OPENAI_API_KEY=your_api_key_here
APP_ENV=development
```

> **Why environment variables?** They secure sensitive information, separate configuration from code, and support multiple deployment environments without code changes.

> ⚠️ Never commit the `.env` file to version control.

### Step 5 — Run the Application

```bash
streamlit run app/app.py
```

Open your browser at: **`http://localhost:8501`**

---

## 🐳 Docker Deployment

### Why Docker?

Docker packages the application into a portable container, providing:

- Consistent execution environment across all machines
- Easy and repeatable deployment
- Simplified dependency management
- Platform independence

### Docker Architecture

```
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

### Dockerfile Overview

The Dockerfile defines how the application image is built. Its responsibilities:

- Select the Python base image
- Install all required dependencies
- Copy application source files
- Configure Streamlit settings
- Launch the application on container start

### Build the Docker Image

```bash
docker build -t ai-study-buddy-pro .
```

Verify the image was created:

```bash
docker images
```

Expected output includes: `ai-study-buddy-pro`

### Run the Container

```bash
docker run -d \
  --name ai-study-buddy-container \
  -p 8501:8501 \
  --env-file .env \
  ai-study-buddy-pro
```

### Manage the Container

```bash
# Verify container is running
docker ps

# View container logs
docker logs ai-study-buddy-container

# Restart container
docker restart ai-study-buddy-container

# Stop container
docker stop ai-study-buddy-container

# Remove container
docker rm ai-study-buddy-container
```

---

## 🐙 Docker Compose Setup

Docker Compose manages all project services simultaneously.

### Services Managed

| Service       | Container Name           | Port |
| ------------- | ------------------------ | ---- |
| Application   | ai-study-buddy-container | 8501 |
| Jenkins       | jenkins-container        | 8081 |
| Prometheus    | prometheus-container     | 9090 |
| Grafana       | grafana-container        | 3000 |
| Node Exporter | node-exporter            | 9100 |

```bash
docker compose up -d     # Start all services
docker compose down      # Stop all services
docker compose ps        # Check service status
docker compose logs      # View all logs
```

---

## ☁️ AWS Deployment

### Instance Details

| Parameter        | Value               |
| ---------------- | ------------------- |
| Cloud Provider   | AWS                 |
| Service          | EC2                 |
| Instance Type    | t3.small            |
| Operating System | Ubuntu 24.04 LTS    |
| Region           | ap-south-1 (Mumbai) |

### Why t3.small?

The `t3.small` instance provides:

- 2 vCPUs and 2 GB RAM
- Better performance than t2.micro
- Ability to run multiple containers simultaneously
- Cost-effective pricing for academic projects

### Connect to the EC2 Instance

```bash
ssh -i ai-study-buddy-key.pem ubuntu@<PUBLIC_IP>
```

### Clone and Deploy on EC2

```bash
git clone https://github.com/the-rahul-tyagi/AiStudyBuddyPro.git
cd AiStudyBuddyPro
docker compose up -d
```

### Verify Running Containers

```bash
docker ps
```

Expected containers:

```
ai-study-buddy-container
jenkins-container
prometheus-container
grafana-container
```

### Security Group Configuration

| Port | Protocol | Purpose                    |
| ---- | -------- | -------------------------- |
| 22   | TCP      | SSH Access                 |
| 8081 | TCP      | Jenkins Dashboard          |
| 8501 | TCP      | AI Study Buddy Application |
| 9090 | TCP      | Prometheus                 |
| 3000 | TCP      | Grafana                    |
| 9100 | TCP      | Node Exporter              |

### Service Endpoints

Replace `<EC2_PUBLIC_IP>` with your instance's public IP address.

| Service            | URL                           |
| ------------------ | ----------------------------- |
| AI Study Buddy App | `http://<EC2_PUBLIC_IP>:8501` |
| Jenkins            | `http://<EC2_PUBLIC_IP>:8081` |
| Prometheus         | `http://<EC2_PUBLIC_IP>:9090` |
| Grafana            | `http://<EC2_PUBLIC_IP>:3000` |

---

## 🔄 CI/CD Pipeline — Jenkins

One of the primary goals of this project was to automate the software delivery process using Continuous Integration and Continuous Deployment. Jenkins was integrated to automatically build and deploy the application on every GitHub push, eliminating manual steps and ensuring consistent releases.

### Traditional vs Automated Deployment

| ❌ Traditional (Manual)       | ✅ Automated (Jenkins)                      |
| ----------------------------- | ------------------------------------------- |
| Manual build on every change  | Git push triggers pipeline automatically    |
| Prone to human errors         | Consistent, scripted execution              |
| Time-consuming and repetitive | Fast delivery with zero manual intervention |
| Inconsistent deployments      | Repeatable and auditable releases           |

### Jenkins Architecture

```
GitHub Repository
       │
       ▼
    Jenkins
       │
  ┌────┼──────────┐
  │    │          │
  ▼    ▼          ▼
Build Deploy   Verify
       │
       ▼
Docker Container
       │
       ▼
AWS EC2 Server
```

### Jenkins Container Details

| Property       | Value               |
| -------------- | ------------------- |
| Container Name | jenkins-container   |
| Image          | jenkins/jenkins:lts |
| Port Mapping   | 8081:8080           |

**Access Jenkins:** `http://<EC2_PUBLIC_IP>:8081`

### Pipeline Stages

```
Git Push
   │
   ▼
Stage 1 — Source Code Checkout
   │       Fetches the latest commit from GitHub
   ▼
Stage 2 — Verify Environment
   │       Confirms Docker availability: docker --version
   ▼
Stage 3 — Build Docker Image
   │       docker build -t ai-study-buddy-pro .
   ▼
Stage 4 — Stop Existing Container
   │       docker stop ai-study-buddy-container
   ▼
Stage 5 — Remove Old Container
   │       docker rm ai-study-buddy-container
   ▼
Stage 6 — Deploy New Container
   │       docker run -d -p 8501:8501 --env-file .env ai-study-buddy-pro
   ▼
Stage 7 — Verify Deployment
   │       Confirms container running, port exposed, app reachable
   ▼
Application Live ✅
```

### Useful Jenkins Commands

```bash
docker exec -it jenkins-container bash   # Access Jenkins container shell
docker logs jenkins-container            # View Jenkins logs
docker restart jenkins-container         # Restart Jenkins
```

---

## 🏗 Infrastructure as Code — Terraform

All AWS infrastructure is defined and provisioned through Terraform, enabling repeatable, version-controlled deployments without touching the AWS console.

### Without vs With Terraform

| ❌ Without Terraform                     | ✅ With Terraform                             |
| ---------------------------------------- | --------------------------------------------- |
| Manual resource creation via AWS Console | `terraform apply` provisions everything       |
| Difficult to reproduce setup             | Fully repeatable from version-controlled code |
| Error-prone and time-consuming           | Automated, consistent, and auditable          |

### Folder Structure

```
terraform/
├── provider.tf       # AWS provider configuration and deployment region
├── main.tf           # EC2 instance, security groups, network resources
├── variables.tf      # Reusable input variables (region, instance type, key pair)
├── terraform.tfvars  # Actual variable values
└── outputs.tf        # Displays public IP and instance info after deploy
```

### Terraform Workflow

```bash
terraform init       # Initialize providers and backend
terraform validate   # Check configuration syntax
terraform plan       # Preview changes before applying
terraform apply      # Provision AWS infrastructure
terraform destroy    # Tear down all resources
```

### AWS Resources Provisioned

| Resource         | Details          |
| ---------------- | ---------------- |
| Cloud Provider   | AWS              |
| Compute Service  | EC2              |
| Instance Type    | t3.small         |
| Region           | ap-south-1       |
| Operating System | Ubuntu 24.04 LTS |

---

## ☸️ Kubernetes Configuration

Kubernetes manifests were created to demonstrate production-grade container orchestration. The manifests were configured and tested locally while Docker-on-EC2 served as the primary deployment target.

### Folder Structure

```
kubernetes/
├── namespace.yaml    # Isolates resources in a dedicated namespace
├── configmap.yaml    # Stores non-sensitive application configuration
├── secret.yaml       # Stores sensitive values: API keys, tokens, credentials
├── deployment.yaml   # Manages pod creation, replicas, and rolling updates
└── service.yaml      # Exposes the app with stable endpoints and load balancing
```

### Kubernetes Architecture

```
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

### Common kubectl Commands

```bash
# Inspect cluster resources
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services

# Apply manifests
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## 📊 Monitoring & Observability

Monitoring is a critical component of modern DevOps. After deployment, applications and infrastructure must be continuously observed for reliability, performance, and availability. This project implements a full monitoring stack using **Prometheus**, **Node Exporter**, and **Grafana**.

### Why Monitoring?

| Infrastructure Questions   | Application Questions       | Performance Questions       |
| -------------------------- | --------------------------- | --------------------------- |
| Is CPU usage increasing?   | Is the application running? | Resource utilization trends |
| Is memory sufficient?      | Are containers healthy?     | System bottlenecks          |
| Is disk space running low? | Are services reachable?     | Capacity planning           |
| Is network traffic normal? |                             |                             |

### Monitoring Architecture

```
AWS EC2 (t3.small)
       │
       ▼
 Node Exporter         ← Collects Linux system-level metrics
       │
       ▼
  Prometheus           ← Stores and queries time-series data
       │
       ▼
   Grafana             ← Visualizes metrics on interactive dashboards
       │
       ▼
Monitoring Dashboard
```

---

### 📈 Prometheus

Prometheus is the central metrics collection system responsible for scraping, storing, and querying time-series data from all configured targets.

**Responsibilities:** Metrics collection · Time-series storage · Target monitoring · Query processing · Grafana integration

| Property       | Value                |
| -------------- | -------------------- |
| Container Name | prometheus-container |
| Image          | prom/prometheus      |
| Port           | 9090                 |

**Access:** `http://<EC2_PUBLIC_IP>:9090`

**Configuration** (`monitoring/prometheus/prometheus.yml`):

```yaml
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

**Monitored Targets:**

| Target             | Purpose                    |
| ------------------ | -------------------------- |
| localhost:9090     | Prometheus self-monitoring |
| node-exporter:9100 | System metrics collection  |

**Useful PromQL Queries:**

```promql
up                                      # Target health status
rate(node_cpu_seconds_total[5m])        # CPU usage rate
node_memory_MemAvailable_bytes          # Available memory
```

---

### 📡 Node Exporter

Node Exporter exposes Linux system-level metrics to Prometheus.

| Property       | Value              |
| -------------- | ------------------ |
| Container Name | node-exporter      |
| Image          | prom/node-exporter |
| Port           | 9100               |

**Metrics Collected:**

| Category | Metrics                                    |
| -------- | ------------------------------------------ |
| CPU      | Utilization, load, time per core           |
| Memory   | Used, available, cached RAM                |
| Disk     | Usage, free space, filesystem info         |
| Network  | Incoming/outgoing traffic, interface stats |

**Verify Node Exporter metrics:**

```bash
docker exec -it prometheus-container \
  wget -qO- http://node-exporter:9100/metrics
```

Expected output:

```
# HELP go_gc_duration_seconds
# TYPE go_gc_duration_seconds summary
...
```

---

### 📊 Grafana

Grafana retrieves data from Prometheus and presents it through interactive, real-time dashboards.

| Property       | Value             |
| -------------- | ----------------- |
| Container Name | grafana-container |
| Image          | grafana/grafana   |
| Port           | 3000              |

**Access:** `http://<EC2_PUBLIC_IP>:3000`

**Dashboard Panels:**

| Panel              | Metrics Shown                              |
| ------------------ | ------------------------------------------ |
| CPU Monitoring     | Utilization, load, historical trends       |
| Memory Monitoring  | Used memory, available memory, trends      |
| Disk Monitoring    | Usage, free space, filesystem health       |
| Network Monitoring | Throughput, interface statistics           |
| System Health      | Host status, uptime, resource availability |

---

### All Containers at a Glance

| Container Name           | Purpose                    |
| ------------------------ | -------------------------- |
| ai-study-buddy-container | Main Application           |
| jenkins-container        | CI/CD Pipeline             |
| prometheus-container     | Metrics Storage & Querying |
| grafana-container        | Dashboard Visualization    |
| node-exporter            | Infrastructure Metrics     |

### Docker Network Configuration

Container-to-container communication is enabled through Docker networking, allowing Prometheus to reach Node Exporter and Grafana to query Prometheus.

```bash
docker network ls                        # List all Docker networks
docker network inspect bridge            # Inspect network details
```

---

## ⚠️ Challenges & Solutions

Real-world deployments always surface unexpected issues. Here are the key challenges encountered during this project and how each was resolved:

| #   | Challenge                                 | Root Cause                                       | Solution                                                                            | Result                           |
| --- | ----------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Jenkins build failure — `.env not found`  | Missing env file in Jenkins workspace            | Created `.env` in deployment environment, updated config                            | Successful build and deployment  |
| 2   | Docker container name conflict            | Existing container using identical name          | Ran `docker stop` + `docker rm` before redeploying                                  | Container recreated successfully |
| 3   | Prometheus target showing `DOWN`          | Network communication failure between containers | Verified Docker network, updated Prometheus config, restarted monitoring containers | Target status changed to `UP`    |
| 4   | Grafana showing `No Data`                 | Prometheus datasource misconfigured              | Verified datasource URL, tested connectivity, reloaded dashboards                   | Metrics displayed correctly      |
| 5   | `kubectl get pods` returning no resources | Manifests had not been applied to the cluster    | Applied manifests with `kubectl apply -f deployment.yaml`                           | Resources created successfully   |

---

## 🏆 Project Outcomes

### Application

- ✅ AI Study Buddy application developed and deployed
- ✅ Interactive Streamlit interface live on AWS

### DevOps

- ✅ Git & GitHub version control integrated
- ✅ Docker containerization complete
- ✅ Jenkins CI/CD pipeline operational
- ✅ Terraform infrastructure provisioning automated
- ✅ Kubernetes manifests configured and tested

### Monitoring

- ✅ Prometheus collecting metrics from all targets
- ✅ Node Exporter exposing system-level infrastructure data
- ✅ Grafana dashboards live with real-time visualization

---

## 🚀 Future Enhancements

### Application Improvements

- User authentication and session management
- Learning analytics and progress tracking
- AI chatbot integration for conversational tutoring

### DevOps Enhancements

- GitHub Actions as an alternative CI pipeline
- SonarQube for static code quality analysis
- Automated test suite with coverage reporting
- Private container registry integration

### Cloud Enhancements

- Migration to AWS ECS or Amazon EKS
- Application Load Balancer + Auto Scaling Groups
- Multi-region deployment for high availability

### Monitoring Enhancements

- AlertManager with email and Slack notifications
- Centralized logging (ELK stack / Grafana Loki)
- Uptime and SLA dashboards

---

## 👨‍💻 Author

**Rahul Tyagi** — Computer Science Student · DevOps Enthusiast · Cloud Learner

**Skills demonstrated:** Python · Streamlit · Git & GitHub · Docker · Docker Compose · Jenkins · Terraform · Kubernetes · AWS EC2 · Prometheus · Grafana · Linux Administration

---

## 📄 License

This project was developed for academic learning, DevOps practice, cloud computing demonstration, and portfolio development. Feel free to explore, learn from, and extend it.

---

<div align="center">

**If this project was useful, consider giving it a ⭐ — it helps others discover it too.**

[⭐ Star this repo](https://github.com/the-rahul-tyagi/AiStudyBuddyPro) · [🍴 Fork it](https://github.com/the-rahul-tyagi/AiStudyBuddyPro/fork) · [📢 Share it](https://github.com/the-rahul-tyagi/AiStudyBuddyPro)

</div>
