# CI/CD Pipeline - GitHub Actions to AWS EC2 with Docker

Automated deployment pipeline that builds and deploys a Dockerized application to AWS EC2 on every push to main branch.

### Architecture

Git Push (main) -> GitHub Actions -> SSH -> AWS EC2 -> Docker Build & Run -> Live on Port 80


### Tech Stack
- **Cloud:** AWS EC2 (t2.micro), IAM
- **CI/CD:** GitHub Actions, GitHub Secrets
- **Containers:** Docker
- **App:** Python Flask
- **OS:** Ubuntu 22.04

### How It Works
1. Code is pushed to the `main` branch
2. Workflow `.github/workflows/deploy.yml` triggers
3. GitHub Actions connects to EC2 via SSH using stored secrets
4. EC2 executes:
```bash
git pull origin main
docker build -t myapp .
docker stop myapp || true
docker rm myapp || true
docker run -d -p 80:5000 --name myapp myapp

Project Structure
.
├── app.py
├── Dockerfile
├── requirements.txt
└──.github/
    └── workflows/
        └── deploy.yml
```

### Features
- No manual deployment via SSH
- Secure secret management with GitHub Secrets
- IAM best practices - No root account usage
- Containerized deployment for consistency

### Required Secrets
Configure these in GitHub > Settings > Secrets and variables > Actions:
- `EC2_HOST` - EC2 public IP address
- `EC2_USER` - EC2 username (ubuntu)
- `EC2_SSH_KEY` - Private SSH key (.pem file content)

### Roadmap
- ✅ Level 1: Automated EC2 deployment - DONE
- ⏳ Level 2: Nginx reverse proxy
- ⏳ Level 3: Infrastructure as Code with Terraform
- ⏳ Level 4: Monitoring with CloudWatch
