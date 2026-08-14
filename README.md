# DevOps EC2 Deploy - CI/CD with Terraform IaC

> Real DevOps progression: Level 1 Docker → Level 2 Manual EC2+Nginx → Level 3 Terraform (eu-north-1 t3.micro)

![Deploy](https://github.com/anuzdevops/devops-ec2-deploy/actions/workflows/deploy.yml/badge.svg)
![Terraform](https://img.shields.io/badge/IaC-Terraform-623CE4?logo=terraform)
![AWS](https://img.shields.io/badge/AWS-eu--north--1-FF9900?logo=amazonec2)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)

**Current Branch:** `main` (Level 3) | **Level 2 Branch:** `level-2-nginx` | **Release:** `level-1-complete` | **Live:** `http://<EC2_IP>` from `terraform output`

## Architecture

Git Push to main → GitHub Actions (appleboy/ssh-action) → EC2 t3.micro (Terraform provisioned in eu-north-1) → Docker (app.py:5000) → Nginx Reverse Proxy (80 → 5000)

## Structure
```
.
├── app.py # Python Flask app
├── Dockerfile # EXPOSE 5000
├── requirements.txt
├──.github/workflows/deploy.yml # CI/CD for Level 2 & 3
└── terraform/ # Level 3
    ├── main.tf # aws_instance + aws_security_group
    ├── variables.tf # region, ami, instance_type
    ├── outputs.tf # public_ip
    ├── user_data.sh # Bootstrap docker, nginx, git
    └── (ignored).terraform/, *.tfstate, *.lock.hcl
```
## Level 1: Dockerization [Release: level-1-complete]

- Dockerized Python app
- `docker build -t myapp. && docker run -p 5000:5000 myapp`

## Level 2: Manual EC2 + Nginx + CI/CD [Branch: level-2-nginx]

**Goal:** Deploy to manually created EC2

- EC2: Ubuntu 22.04, t2.micro, created via console
- SG: 22, 80, 5000
- Manual install on EC2: docker.io, nginx, git, git clone
- Nginx: /etc/nginx/sites-available/default → proxy_pass http://127.0.0.1:5000
- CI/CD: deploy.yml → `cd ~/devops-ec2-deploy && git pull && docker build/run && systemctl restart nginx`
- Limitation: Not reproducible, folder missing on fresh instance causes 502

View Level 2 code: `git checkout level-2-nginx`

## Level 3: Terraform IaC [Branch: main - Current] eu-north-1 t3.micro

**Goal:** Infrastructure as Code, 40 sec reproducible infra

main.tf:
- aws_security_group.app_sg (ingress 22,80,5000)
- aws_instance.app_server (t3.micro, Ubuntu 22.04, user_data = file("user_data.sh"))

Commands:
terraform init
terraform plan
terraform apply # get IP → update EC2_HOST secret
terraform destroy # save cost

### Critical Production Fixes in Level 3

| Issue | Root Cause | Fix |
|---|---|---|
| GH001: Large file 838MB push failed, provider binary 171MiB detected | Committed `.terraform/` folder | Added terraform/.gitignore + root.gitignore with `.terraform/`, `*.tfstate*`, `*.lock.hcl`. Cleaned history via `git reset --hard 2c4290d`, push became 2.45 KiB |
| 502 Bad Gateway, `docker ps` empty on Terraform EC2 | deploy.yml only `cd ~/devops-ec2-deploy && git pull` → folder doesn't exist on new EC2 | Fixed deploy.yml: Added clone-if-not-exists logic `if [! -d ~/devops-ec2-deploy ]; then git clone https://github.com/anuzdevops/devops-ec2-deploy.git; fi` before pull. Now IaC-compatible |
| `terraform state list` empty after cleanup | Deleted `terraform.tfstate` while fixing GH001 | Terminated manually via console. Lesson → Level 4 will use S3 Remote State + DynamoDB locking with versioning |

**CI/CD Fix for IaC (main branch deploy.yml):**
```bash
if [ ! -d ~/devops-ec2-deploy ]; then
  cd ~; git clone https://github.com/anuzdevops/devops-ec2-deploy.git
fi
cd ~/devops-ec2-deploy && git pull origin main
sudo docker build -t myapp .
sudo docker rm -f myapp || true
sudo docker run -d -p 5000:5000 --restart unless-stopped --name myapp myapp
```

## How to Run (Level 3)

git checkout main
cd terraform
terraform init && terraform apply -auto-approve
# terraform output → set GitHub Secret EC2_HOST = IP
git push origin main # auto deploy

## Best Practices

- Never commit.terraform/ or.tfstate
-.gitignore enforced
- Idempotent deploy (rm -f || true)
- SSH key only

## Roadmap

- Level 1 Docker - release level-1-complete ✅
- Level 2 Manual EC2+Nginx - branch level-2-nginx ✅
- Level 3 Terraform IaC eu-north-1 t3.micro - branch main ✅
- Level 4 S3 Backend + DynamoDB Locks [ ]

Author: Anuj Yadav (@anuzdevops) - Mumbai, IN
