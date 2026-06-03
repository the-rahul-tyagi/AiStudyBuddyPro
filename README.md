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

> *Bridging AI-powered education with production-grade DevOps — from code to cloud, fully automated.*

<br/>

[Features](#-features) · [Architecture](#-system-architecture) · [Setup](#-local-development-setup) · [Deployment](#-aws-deployment) · [Monitoring](#-monitoring--observability) · [Roadmap](#-future-enhancements)

</div>

---

## 📖 Overview

**AI Study Buddy Pro** is a cloud-native educational platform that delivers personalized learning assistance through an intelligent AI interface. Beyond the application itself, this project is a complete showcase of modern DevOps practices — covering Infrastructure as Code, CI/CD automation, containerization, Kubernetes orchestration, and real-time observability.

This project serves dual purposes:

- 🤖 **An AI-powered educational platform** — interactive, personalized, and accessible
- ⚙️ **A production-grade DevOps implementation** — automated, monitored, and cloud-deployed

---

## ✨ Features

### Application

| Feature | Description |
|---|---|
| 📚 Personalized Learning | AI-tailored educational assistance for individual learners |
| 🎨 Modern Interface | Clean, interactive UI built with Streamlit |
| ⚡ Lightweight Deployment | Containerized architecture for portability and speed |
| ☁️ Cloud Hosted | Deployed on AWS EC2 for scalability and availability |

### DevOps

| Feature | Description |
|---|---|
| 🔄 CI/CD Automation | Jenkins pipeline — push code, get deployed automatically |
| 🐳 Containerization | Full Docker and Docker Compose setup |
| ☸️ Kubernetes Ready | Deployment manifests for production-grade orchestration |
| 🏗️ Infrastructure as Code | AWS resources provisioned via Terraform |
| 📊 Real-Time Monitoring | Prometheus + Node Exporter metrics collection |
| 📈 Visualization | Grafana dashboards for infrastructure insights |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Developer Machine                    │
│                    Code → Git Push                       │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   GitHub Repository                      │
└───────────────────────────┬─────────────────────────────┘
                            │  Webhook Trigger
                            ▼
┌─────────────────────────────────────────────────────────┐
│                Jenkins CI/CD Pipeline                    │
│    Checkout → Build Image → Deploy Container             │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   AWS EC2 (t3.small)                    │
│                                                         │
│  ┌────────────────┐      ┌──────────────────────────┐   │
│  │  AI Study Buddy│      │   Monitoring Stack       │   │
│  │  (Streamlit)   │      │                          │   │
│  │  :8501         │      │  Node Exporter  :9100    │   │
│  └────────────────┘      │  Prometheus     :9090    │   │
│                          │  Grafana        :3000    │   │
│  ┌────────────────┐      └──────────────────────────┘   │
│  │    Jenkins     │                                     │
│  │    :8081       │                                     │
│  └────────────────┘                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.11 |
| Frontend | Streamlit |
| Version Control | Git & GitHub |
| Containerization | Docker & Docker Compose |
| CI/CD | Jenkins |
| Infrastructure as Code | Terraform |
| Container Orchestration | Kubernetes |
| Cloud Platform | AWS EC2 (ap-south-1) |
| Monitoring | Prometheus + Node Exporter |
| Visualization | Grafana |

---

## 📂 Repository Structure

```
AI_STUDY_BUDDY_PRO/
│
├── app/                        # Application source code
│
├── jenkins/                    # Jenkins pipeline configuration
│
├── kubernetes/                 # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── deployment.yaml
│   └── service.yaml
│
├── monitoring/
│   ├── grafana/                # Grafana dashboard configs
│   └── prometheus/             # Prometheus scrape configs
│
├── terraform/                  # Infrastructure as Code
│
├── .streamlit/                 # Streamlit configuration
├── .env                        # Environment variables (not committed)
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # Container image definition
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 💻 Local Development Setup

### Prerequisites

Ensure the following are installed before proceeding:

| Tool | Version |
|---|---|
| Python | 3.10+ |
| Git | Latest |
| Docker | Latest |
| Docker Compose | Latest |
| Terraform | Latest |
| AWS CLI | Latest |
| kubectl | Latest |
| Jenkins | LTS |

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

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
APP_ENV=development
```

> ⚠️ Never commit the `.env` file to version control.

### Step 5 — Run the Application

```bash
streamlit run app/app.py
```

Open your browser at: **http://localhost:8501**

---

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t ai-study-buddy-pro .
```

### Run the Container

```bash
docker run -d \
  --name ai-study-buddy-container \
  -p 8501:8501 \
  --env-file .env \
  ai-study-buddy-pro
```

### Useful Docker Commands

```bash
docker ps                                # List running containers
docker logs ai-study-buddy-container     # View logs
docker restart ai-study-buddy-container  # Restart container
docker stop ai-study-buddy-container     # Stop container
docker rm ai-study-buddy-container       # Remove container
```

---

## 🐙 Docker Compose

Docker Compose manages all project services simultaneously.

| Service | Container Name | Port |
|---|---|---|
| Application | ai-study-buddy-container | 8501 |
| Jenkins | jenkins-container | 8081 |
| Prometheus | prometheus-container | 9090 |
| Grafana | grafana-container | 3000 |
| Node Exporter | node-exporter | 9100 |

```bash
docker compose up -d     # Start all services
docker compose down      # Stop all services
docker compose ps        # Check service status
docker compose logs      # View all logs
```

---

## ☁️ AWS Deployment

### Infrastructure Details

| Parameter | Value |
|---|---|
| Cloud Provider | AWS |
| Service | EC2 |
| Instance Type | t3.small (2 vCPU, 2 GB RAM) |
| Operating System | Ubuntu 24.04 LTS |
| Region | ap-south-1 (Mumbai) |

> The `t3.small` instance was selected to support multiple simultaneous containers at a cost-effective price point for this project.

### Connect to the Instance

```bash
ssh -i ai-study-buddy-key.pem ubuntu@<PUBLIC_IP>
```

### Deploy on EC2

```bash
git clone https://github.com/the-rahul-tyagi/AiStudyBuddyPro.git
cd AiStudyBuddyPro
docker compose up -d
```

### Security Group Rules

| Port | Protocol | Purpose |
|---|---|---|
| 22 | TCP | SSH Access |
| 8081 | TCP | Jenkins Dashboard |
| 8501 | TCP | AI Study Buddy App |
| 9090 | TCP | Prometheus |
| 3000 | TCP | Grafana |
| 9100 | TCP | Node Exporter |

### Service Endpoints

Replace `<EC2_PUBLIC_IP>` with your instance's public IP.

| Service | URL |
|---|---|
| Application | `http://<EC2_PUBLIC_IP>:8501` |
| Jenkins | `http://<EC2_PUBLIC_IP>:8081` |
| Prometheus | `http://<EC2_PUBLIC_IP>:9090` |
| Grafana | `http://<EC2_PUBLIC_IP>:3000` |

---

## 🔄 CI/CD Pipeline — Jenkins

Jenkins automates the full build-and-deploy cycle on every Git push, eliminating manual steps and ensuring consistent releases.

### Pipeline Stages

```
Git Push
   │
   ▼
Stage 1: Checkout Repository      ← Pulls latest code from GitHub
   │
   ▼
Stage 2: Verify Environment       ← Confirms Docker availability
   │
   ▼
Stage 3: Build Docker Image       ← docker build -t ai-study-buddy-pro .
   │
   ▼
Stage 4: Stop Existing Container  ← docker stop ai-study-buddy-container
   │
   ▼
Stage 5: Remove Old Container     ← docker rm ai-study-buddy-container
   │
   ▼
Stage 6: Deploy New Container     ← docker run -d ... ai-study-buddy-pro
   │
   ▼
Stage 7: Verify Deployment        ← Confirms container is running & reachable
   │
   ▼
Application Live ✅
```

### Jenkins Container Details

| Property | Value |
|---|---|
| Container Name | jenkins-container |
| Image | jenkins/jenkins:lts |
| Port | 8081:8080 |

### Useful Jenkins Commands

```bash
docker exec -it jenkins-container bash   # Access Jenkins shell
docker logs jenkins-container            # View logs
docker restart jenkins-container         # Restart Jenkins
```

---

## 🏗 Infrastructure as Code — Terraform

All AWS infrastructure is defined and provisioned through Terraform, enabling repeatable, version-controlled deployments.

### Folder Structure

```
terraform/
├── provider.tf      # AWS provider and region config
├── main.tf          # EC2 instance and security group definitions
├── variables.tf     # Reusable input variables
├── terraform.tfvars # Actual variable values
└── outputs.tf       # Displays public IP and instance info post-deploy
```

### Terraform Workflow

```bash
terraform init      # Initialize providers and modules
terraform validate  # Check configuration syntax
terraform plan      # Preview changes before applying
terraform apply     # Provision AWS infrastructure
terraform destroy   # Tear down all resources
```

---

## ☸️ Kubernetes Configuration

Kubernetes manifests are included to demonstrate production-grade container orchestration. The manifests were configured and tested locally while Docker-on-EC2 served as the primary deployment.

### Manifest Overview

| File | Purpose |
|---|---|
| `namespace.yaml` | Isolates resources in a dedicated namespace |
| `configmap.yaml` | Stores non-sensitive application configuration |
| `secret.yaml` | Stores sensitive values (API keys, tokens) |
| `deployment.yaml` | Manages pods, replicas, and rolling updates |
| `service.yaml` | Exposes the app with stable endpoints and load balancing |

### Common Commands

```bash
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## 📊 Monitoring & Observability

A full monitoring stack gives real-time visibility into application health and infrastructure performance.

### Stack Overview

```
AWS EC2 Instance
      │
      ▼
Node Exporter  ──────────────────────────────────┐
(System Metrics: CPU, RAM, Disk, Network)        │
                                                 ▼
                                           Prometheus
                                      (Metrics Storage & Querying)
                                                 │
                                                 ▼
                                             Grafana
                                      (Interactive Dashboards)
```

### Prometheus

Prometheus collects and stores time-series metrics from all configured targets.

**Configuration** (`monitoring/prometheus/prometheus.yml`):
```yaml
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

**Useful Queries:**
```promql
up                                        # Target health status
rate(node_cpu_seconds_total[5m])          # CPU usage rate
node_memory_MemAvailable_bytes            # Available memory
```

### Node Exporter

Collects Linux system-level metrics exposed to Prometheus.

| Metric Category | Examples |
|---|---|
| CPU | Utilization, load, time per core |
| Memory | Used, available, cached |
| Disk | Usage, free space, filesystem info |
| Network | Incoming/outgoing traffic, interface stats |

### Grafana

Grafana visualizes Prometheus data through interactive, real-time dashboards covering CPU, memory, disk, network, and overall system health.

| Container | Port | Image |
|---|---|---|
| prometheus-container | 9090 | prom/prometheus |
| node-exporter | 9100 | prom/node-exporter |
| grafana-container | 3000 | grafana/grafana |

---

## ⚠️ Challenges & Solutions

Real-world deployments rarely go smoothly. Here are the key issues encountered and how they were resolved:

| # | Challenge | Root Cause | Solution |
|---|---|---|---|
| 1 | Jenkins build failure — `.env` not found | Missing env file in Jenkins workspace | Created `.env` in deployment environment |
| 2 | Docker container name conflict | Existing container using the same name | Stopped and removed old container before redeployment |
| 3 | Prometheus target showing `DOWN` | Network communication failure between containers | Verified Docker network, updated Prometheus config, restarted containers |
| 4 | Grafana showing `No Data` | Prometheus datasource misconfigured | Verified datasource URL, tested connectivity, reloaded dashboards |
| 5 | `kubectl get pods` returning no resources | Manifests not applied to the cluster | Applied manifests with `kubectl apply -f` |

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
- ✅ Prometheus collecting metrics
- ✅ Node Exporter exposing system-level data
- ✅ Grafana dashboards live with real-time visualization

---

## 🚀 Future Enhancements

### Application
- User authentication and session management
- Learning progress tracking and analytics
- AI chatbot integration for conversational tutoring

### DevOps
- GitHub Actions as an alternative/parallel CI pipeline
- SonarQube for static code quality analysis
- Automated test suite with coverage reporting
- Private container registry integration

### Cloud
- Migration to AWS ECS or Amazon EKS
- Application Load Balancer + Auto Scaling Groups
- Multi-region deployment for high availability

### Monitoring
- AlertManager with email and Slack notifications
- Centralized logging (ELK / Loki)
- Uptime and SLA dashboards

---

## 👨‍💻 Author

**Rahul Tyagi** — Computer Science Student · DevOps Enthusiast · Cloud Learner

*Skills demonstrated in this project: Python · Streamlit · Git & GitHub · Docker · Docker Compose · Jenkins · Terraform · Kubernetes · AWS EC2 · Prometheus · Grafana · Linux Administration*

---

## 📄 License

This project was developed for academic learning, DevOps practice, and portfolio development. Feel free to explore, learn from, and extend it.

---

<div align="center">

If this project was useful to you, consider giving it a ⭐ — it helps others discover it too.

**[⭐ Star](https://github.com/the-rahul-tyagi/AiStudyBuddyPro) · [🍴 Fork](https://github.com/the-rahul-tyagi/AiStudyBuddyPro/fork) · [📢 Share](https://github.com/the-rahul-tyagi/AiStudyBuddyPro)**

</div>
