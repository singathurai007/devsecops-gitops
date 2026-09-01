# DevSecOps GitOps CI/CD Pipeline

## 📌 Project Overview

This project implements an end-to-end DevSecOps and GitOps CI/CD pipeline for deploying a Flask application on Kubernetes.

The pipeline automatically builds, scans, analyzes, publishes, and deploys the application using Jenkins, Docker, Trivy, SonarQube, Docker Hub, GitHub, Kubernetes, and ArgoCD.

---

## 🏗️ Architecture

Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
Docker Build
    ↓
Trivy Security Scan
    ↓
SonarQube Code Analysis
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

---

## 🛠️ Technologies Used

- AWS EC2
- Ubuntu
- Git & GitHub
- Jenkins
- Docker
- Docker Hub
- Trivy
- SonarQube
- Kubernetes
- ArgoCD
- Flask
- Python

---

## 🔄 CI/CD Workflow

### 1. Developer

The developer modifies the Flask application code and pushes the changes to GitHub.

### 2. Jenkins

Jenkins performs the CI/CD pipeline.

Pipeline stages include:

- Checkout source code
- Build Docker image
- Run Trivy security scan
- Run SonarQube analysis
- Test application
- Push Docker image to Docker Hub
- Update Kubernetes deployment manifest
- Push updated manifest to GitHub

### 3. Docker

Jenkins builds the Flask application into a Docker image.

Example:

```text
singathurai/devsecops-app:67
