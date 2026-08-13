# DevOps EC2 Deploy - Production Grade CI/CD

A project where I rebuild a production deployment pipeline from scratch, Level by Level in public.

Live Demo: `http://YOUR_EC2_IP` -> Replace with your IP

## Architecture Evolution

### Level 1: Basic Automation
User -> EC2 (Port 80) -> Docker App (Port 5000)
- Direct exposure of app container
- Manual SSH deployment problem solved with GitHub Actions

### Level 2: Reverse Proxy (Current) ✅
User -> Nginx (Port 80) -> Docker App (Port 5000)
- Nginx as Reverse Proxy - App never exposed directly to internet
- Decoupled Web Server and Application
- Production-ready with auto-restart and auto-boot

## Tech Stack

- **Cloud:** AWS EC2 (Ubuntu), IAM with MFA
- **Containers:** Docker
- **Web Server:** Nginx (Reverse Proxy)
- **CI/CD:** GitHub Actions + GitHub Secrets + SSH
- **OS:** Linux

## What I Learned in Level 2

- Why we never expose app containers directly on port 80
- How Nginx reverse proxy works (`proxy_pass`)
- Port mapping: `5000:5000` for internal app, `80` for Nginx
- Updating CI/CD to handle infra changes (`systemctl restart nginx`)
- Production essentials: `--restart unless-stopped` and `systemctl enable`

## Project Roadmap

- ✅ **Level 1: Automated Deployment** - CI/CD with GitHub Actions (Tag: `level-1-complete`)
- ✅ **Level 2: Nginx Reverse Proxy** - Production-grade architecture (Tag: `level-2-complete`)
- [ ] **Level 3: Terraform - Infra as Code** - Recreate entire infra with `terraform apply` (Next)
- [ ] **Level 4: Monitoring & SSL** - CloudWatch + Let's Encrypt HTTPS

## Deployment Flow

Push to `main` -> GitHub Actions connects via SSH -> Pulls code on EC2 -> Builds Docker image -> Runs on 5000 -> Restarts Nginx -> Live in ~40 seconds.

No manual SSH needed.

## How to Run Locally

```bash
docker build -t myapp .
docker run -d -p 5000:5000 --restart unless-stopped --name myapp myapp
```

**IMPORTANT:** Replace `http://YOUR_EC2_IP` with your actual EC2 IP before committing.
