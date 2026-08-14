# DevOps EC2 Deploy - Level 2: Manual EC2 + Nginx + CI/CD

> Branch: `level-2-nginx` | Tag: `level-2-complete`

This branch represents Level 2 milestone - Manual EC2 provisioning with Nginx reverse proxy and GitHub Actions.

## What was built in Level 2

- **EC2:** Ubuntu 22.04, t2.micro, manually created via AWS Console
- **Security Group:** Ports 22 (SSH), 80 (HTTP), 5000 (app)
- **On EC2:** Docker, Nginx, Git installed manually
- **App:** `app.py` (Python Flask) + `Dockerfile` + `requirements.txt`
- **Nginx:** Reverse proxy `80 -> 5000` to avoid exposing Docker directly

## CI/CD (Level 2)

`.github/workflows/deploy.yml`:
- Trigger: push to `level-2-nginx` / `main`
- SSH via appleboy/ssh-action
- Steps: `git pull` → `docker build -t myapp` → `docker run -p 5000:5000`

## How to use this branch

```bash
git checkout level-2-nginx
# EC2_HOST must point to manual EC2 IP
