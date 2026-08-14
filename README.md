# 🚀 DevOps EC2 Deployment | Terraform + AWS

> From manual EC2 to S3 Remote State - step by step production IaC

![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=for-the-badge&logo=terraform)
![AWS](https://img.shields.io/badge/AWS-S3%20Backend-FF9900?style=for-the-badge&logo=amazonaws)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?style=for-the-badge&logo=nginx)

### 🗺️ Journey Till Now

#### Level 1: Manual EC2
- Launched EC2 via AWS Console
- Deployed Flask app on port 5000 with user_data
- Understood EC2, Security Groups, SSH basics

#### Level 2: Nginx Reverse Proxy
- Installed Nginx on EC2
- Configured reverse proxy: `80 → 5000`
- App now accessible on `http://<EC2_IP>` without port
- Learned production routing pattern

#### Level 3: Terraform - Infrastructure as Code
- Converted manual infra to Terraform
- Created `main.tf`, `variables.tf`, `outputs.tf`
- Fixed SG `already exists` error - learned importance of `terraform.tfstate`
- First successful `terraform apply / destroy` cycle

#### Level 4: Remote State in S3 🔒 (Current)
- Created S3 bucket `devops-tfstate-anuj-2026` (encrypted + versioned)
- Added backend block with native locking
  ```hcl
  backend "s3" {
    bucket = "devops-tfstate-anuj-2026"
    key    = "devops-app/terraform.tfstate"
    region = "eu-north-1"
    use_lockfile = true
  }
  ```
- Migrated: terraform init -migrate-state -upgrade
- Deleted local tfstate - terraform state list still works from S3

  ⚡️ Quick Deploy
```
git clone https://github.com/<username>/devops-ec2-deploy.git
cd devops-ec2-deploy/terraform
terraform init
terraform apply
```
App: http://<EC2_IP> (via Nginx) | Direct: :5000
Health: /health | Info: /api/info
```
terraform destroy
```
### 🏗️ Current Infra
- **EC2:** t3.micro, Ubuntu 22.04, eu-north-1
- **Proxy:** Nginx 80 → Flask 5000
- **SG:** 22, 80, 5000
- **State:** S3 Remote + Native Locking
- **App:** Production Dashboard

---
**Branch:** `level-4-remote-state` | **Release:** `level-4-complete`  
**Built by:** Anuj Yadav

<img width="1677" height="1007" alt="image" src="https://github.com/user-attachments/assets/56af8a2c-721c-466e-be98-6bad9a897c60" />
