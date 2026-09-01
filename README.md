# 🚀 DevSecOps & GitOps CI/CD Pipeline

An end-to-end **DevSecOps and GitOps CI/CD project** that automates application build, security scanning, code quality analysis, container publishing, and Kubernetes deployment.

---

## 📌 Project Overview

This project demonstrates a complete modern DevOps workflow using:

- Jenkins
- GitHub
- Docker
- Docker Hub
- Trivy
- SonarQube
- Kubernetes
- ArgoCD
- Python Flask
- AWS EC2

The pipeline follows:

```text
Code
  ↓
GitHub
  ↓
Jenkins
  ↓
Docker Build
  ↓
Trivy Security Scan
  ↓
SonarQube Analysis
  ↓
Application Test
  ↓
Docker Hub
  ↓
GitOps Repository
  ↓
ArgoCD
  ↓
Kubernetes
  ↓
Flask Application
```

---

# 🏗️ Architecture

```text
                         Developer
                             │
                             ▼
                      ┌─────────────┐
                      │   GitHub    │
                      └──────┬──────┘
                             │
                             ▼
                      ┌─────────────┐
                      │   Jenkins   │
                      └──────┬──────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        Docker Build      Trivy        SonarQube
                         Security        Code
                           Scan         Analysis
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                      Application Test
                             │
                             ▼
                      ┌─────────────┐
                      │ Docker Hub  │
                      └──────┬──────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │ GitOps Repository│
                   └────────┬─────────┘
                            │
                            ▼
                      ┌─────────────┐
                      │   ArgoCD    │
                      │ Auto Sync   │
                      │ Self Heal   │
                      └──────┬──────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Kubernetes    │
                    │                 │
                    │  ┌──────────┐   │
                    │  │  Pod 1   │   │
                    │  └──────────┘   │
                    │                 │
                    │  ┌──────────┐   │
                    │  │  Pod 2   │   │
                    │  └──────────┘   │
                    └────────┬────────┘
                             │
                             ▼
                    Flask Application
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| AWS EC2 | Cloud infrastructure |
| Ubuntu | Server operating system |
| Git | Version control |
| GitHub | Source code and GitOps repository |
| Jenkins | CI/CD automation |
| Docker | Containerization |
| Docker Hub | Container image registry |
| Trivy | Container vulnerability scanning |
| SonarQube | Static code analysis |
| Kubernetes | Container orchestration |
| ArgoCD | GitOps continuous delivery |
| Python | Application development |
| Flask | Web application framework |

---

# 🔄 CI/CD Pipeline

## 1. GitHub

Developer pushes application changes to GitHub.

```text
Developer
    ↓
GitHub
```

Jenkins retrieves the latest source code from the repository.

---

## 2. Jenkins

Jenkins executes the complete CI/CD pipeline.

### Pipeline stages

```text
Checkout
   ↓
Build Docker Image
   ↓
Trivy Security Scan
   ↓
SonarQube Analysis
   ↓
Application Test
   ↓
Docker Hub Push
   ↓
Update Kubernetes Manifest
   ↓
Push GitOps Changes
```

---

# 🐳 Docker

The Flask application is packaged into a Docker image.

Example image:

```text
singathurai/devsecops-app:67
```

Latest tag:

```text
singathurai/devsecops-app:latest
```

Versioned Docker tags are generated using the Jenkins build number.

Example:

```text
:63
:65
:66
:67
```

This provides traceability between Jenkins builds and Docker images.

---

# 🔐 Trivy Security Scan

Trivy is integrated into the Jenkins pipeline to scan the Docker image for vulnerabilities.

The pipeline checks for:

- HIGH vulnerabilities
- CRITICAL vulnerabilities

Example:

```text
Docker Image
     ↓
   Trivy
     ↓
Security Scan
```

This ensures security is considered during the CI process.

---

# 📊 SonarQube

SonarQube performs static code analysis on the application source code.

It helps identify:

- Bugs
- Vulnerabilities
- Code smells
- Code quality issues

Workflow:

```text
Source Code
    ↓
SonarQube
    ↓
Code Analysis
```

---

# 🧪 Application Testing

Jenkins runs an application health check before publishing the image.

The Flask application provides:

```text
/health
```

Expected response:

```text
OK
```

Example:

```bash
curl http://localhost:5001/health
```

Expected:

```text
OK
```

---

# 📦 Docker Hub

After successful build, security scan, code analysis, and testing, Jenkins pushes the Docker image to Docker Hub.

Example:

```text
singathurai/devsecops-app:67
singathurai/devsecops-app:latest
```

---

# 🌿 GitOps

The Kubernetes configuration is maintained in the GitOps repository.

Kubernetes deployment:

```text
k8s/deployment.yaml
```

Jenkins updates the Docker image tag in the Kubernetes manifest.

Example:

```yaml
image: singathurai/devsecops-app:67
```

Then Jenkins commits the change:

```text
Update image to 67 [skip ci]
```

and pushes the updated manifest to GitHub.

---

# 🚀 ArgoCD

ArgoCD monitors the GitOps repository and keeps the Kubernetes cluster synchronized with Git.

Current configuration:

```text
Automated Sync: Enabled
Prune: Enabled
Self Heal: Enabled
```

ArgoCD status:

```text
Synced | Healthy
```

### GitOps flow

```text
GitHub
   ↓
Updated Kubernetes Manifest
   ↓
ArgoCD
   ↓
Automatic Sync
   ↓
Kubernetes
```

---

# ☸️ Kubernetes

The application is deployed to Kubernetes using a Deployment.

Current configuration:

```text
Application: devsecops-app
Replicas: 2
Container Port: 5000
Service Type: NodePort
```

Two replicas provide basic application availability:

```text
             Deployment
                  │
          ┌───────┴───────┐
          ▼               ▼
       Pod 1            Pod 2
      Running           Running
```

---

# ❤️ Kubernetes Health Probes

The deployment uses both readiness and liveness probes.

## Readiness Probe

Endpoint:

```text
/health
```

Purpose:

```text
Determines whether the application is ready
to receive traffic.
```

## Liveness Probe

Endpoint:

```text
/health
```

Purpose:

```text
Determines whether the application is still healthy.
```

---

# 🌐 Kubernetes Service

The application is exposed using a Kubernetes `NodePort` service.

Example:

```text
Service Port: 5000
NodePort: 32106
Target Port: 5000
```

Service:

```text
devsecops-app
```

Check using:

```bash
kubectl get svc devsecops-app
```

---

# 🧪 Verification Commands

## Check Kubernetes Pods

```bash
kubectl get pods
```

Expected:

```text
devsecops-app-xxxxx   1/1   Running
devsecops-app-yyyyy   1/1   Running
```

---

## Check Deployment

```bash
kubectl get deployment devsecops-app
```

---

## Check Current Docker Image

```bash
kubectl get deployment devsecops-app \
-o=jsonpath='{.spec.template.spec.containers[0].image}'; echo
```

Example:

```text
singathurai/devsecops-app:67
```

---

## Check Deployment Rollout

```bash
kubectl rollout status deployment/devsecops-app
```

Expected:

```text
deployment "devsecops-app" successfully rolled out
```

---

## Check ArgoCD Sync Status

```bash
kubectl -n argocd get application devsecops-app \
-o jsonpath='{.status.sync.status}{" | "}{.status.health.status}{"\n"}'
```

Expected:

```text
Synced | Healthy
```

---

## Check ArgoCD Auto Sync

```bash
kubectl -n argocd get application devsecops-app \
-o jsonpath='{.spec.syncPolicy.automated}{"\n"}'
```

Expected:

```text
{"prune":true,"selfHeal":true}
```

---

## Check Kubernetes Service

```bash
kubectl get svc devsecops-app
```

---

## Test Application

```bash
curl http://localhost:5001/
```

Expected:

```text
DevSecOps boys daa - Application is Running! Hello from devsecops v3
```

---

## Test Health Endpoint

```bash
curl http://localhost:5001/health
```

Expected:

```text
OK
```

---

# 🔐 Jenkins Credentials

Sensitive credentials are stored in Jenkins Credentials instead of being hardcoded in the pipeline.

Credentials used:

```text
dockerhub-credentials
github-token
github-credentials
sonarqube-token
ec2-ssh
```

These credentials are used for authentication with the required services.

---

# 📁 Project Structure

```text
devsecops-gitops/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── Jenkinsfile
│
└── README.md
```

---

# 🎯 Key DevOps Concepts Demonstrated

- Continuous Integration
- Continuous Delivery
- DevSecOps
- GitOps
- Docker containerization
- Docker image versioning
- Jenkins pipeline automation
- Trivy container security scanning
- SonarQube static code analysis
- Docker Hub image publishing
- Kubernetes Deployment
- Kubernetes Service
- Kubernetes health probes
- ArgoCD automated synchronization
- ArgoCD self-healing
- Git-based deployment
- Cloud infrastructure using AWS EC2

---

# 📈 Deployment Flow

A typical application change follows this process:

```text
1. Developer changes code
          ↓
2. Push to GitHub
          ↓
3. Jenkins starts pipeline
          ↓
4. Docker image is built
          ↓
5. Trivy scans image
          ↓
6. SonarQube analyzes code
          ↓
7. Application is tested
          ↓
8. Image pushed to Docker Hub
          ↓
9. Kubernetes manifest updated
          ↓
10. GitOps change pushed to GitHub
          ↓
11. ArgoCD detects Git change
          ↓
12. ArgoCD synchronizes Kubernetes
          ↓
13. Kubernetes performs rolling update
          ↓
14. New application version becomes healthy
```

---

# 🏆 Project Validation

The complete pipeline has been successfully tested.

Current validated configuration:

```text
Docker Image:
singathurai/devsecops-app:67

Kubernetes Replicas:
2

Pods:
Running

ArgoCD Sync:
Synced

ArgoCD Health:
Healthy

ArgoCD Auto Sync:
Enabled

ArgoCD Prune:
Enabled

ArgoCD Self Heal:
Enabled
```

Application test:

```text
DevSecOps boys daa - Application is Running! Hello from devsecops v3
```

Health test:

```text
OK
```

---

# 💡 What This Project Demonstrates

This project demonstrates how development, security, CI/CD, containers, GitOps, and Kubernetes can work together in a modern software delivery workflow.

The main principle is:

```text
Build
  ↓
Test
  ↓
Secure
  ↓
Analyze
  ↓
Package
  ↓
Publish
  ↓
GitOps
  ↓
Deploy
  ↓
Monitor
  ↓
Self-Heal
```

---

# 👨‍💻 Author

## Singathurai

GitHub:

https://github.com/singathurai007

---

# ⭐ Conclusion

This project implements an automated **DevSecOps + GitOps delivery pipeline** using Jenkins, Docker, Trivy, SonarQube, Docker Hub, GitHub, ArgoCD, and Kubernetes.

It demonstrates the complete journey from source code commit to secure container build and automated Kubernetes deployment.

**Build → Secure → Analyze → Test → Publish → GitOps → Deploy → Self-Heal**
