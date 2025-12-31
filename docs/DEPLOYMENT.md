# GitHub Actions CI/CD Pipeline - Setup Guide

## Prerequisites

### 1. VPS Setup

Your VPS should have:
- ✅ Docker installed
- ✅ Docker Compose installed
- ✅ Git installed
- ✅ Project cloned to VPS
- ✅ SSH access configured

### 2. GitHub Secrets

Configure these secrets in your GitHub repository:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `VPS_HOST` | VPS IP address or domain | `123.45.67.89` or `vps.example.com` |
| `VPS_PORT` | SSH port (usually 22) | `22` |
| `VPS_USER` | SSH username with Docker access | `deploy` |
| `VPS_SSH_KEY` | Private SSH key for authentication | Contents of `~/.ssh/id_rsa` |

---

## Setup Steps

### Step 1: Generate SSH Key (if not exists)

On your **local machine**:

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "github-actions-deploy" -f ~/.ssh/github_deploy

# Copy public key to VPS
ssh-copy-id -i ~/.ssh/github_deploy.pub -p YOUR_PORT YOUR_USER@YOUR_VPS_IP
```

### Step 2: Add SSH Key to GitHub

1. Copy private key content:
   ```bash
   cat ~/.ssh/github_deploy
   ```

2. Go to GitHub: **Settings → Secrets → New secret**
3. Name: `VPS_SSH_KEY`
4. Value: Paste the entire private key (including `-----BEGIN` and `-----END` lines)

### Step 3: Configure VPS User

On your **VPS**, ensure the deploy user has Docker permissions:

```bash
# Add user to docker group
sudo usermod -aG docker YOUR_USER

# Verify
docker ps  # Should work without sudo
```

### Step 4: Set Project Directory

On your **VPS**, ensure project is in one of these locations:
- `~/Invisibilidown`
- `/home/YOUR_USER/Invisibilidown`
- `/var/www/Invisibilidown`

Or update the workflow to match your path.

### Step 5: Test SSH Connection

From your **local machine**:

```bash
ssh -i ~/.ssh/github_deploy -p YOUR_PORT YOUR_USER@YOUR_VPS_IP "docker ps"
```

Should show running containers without password prompt.

---

## Deployment Workflow

### Automatic Deployment

Every push to `main` branch triggers deployment:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

GitHub Actions will:
1. ✅ Connect to VPS via SSH
2. ✅ Pull latest code
3. ✅ Build Docker images
4. ✅ Stop containers
5. ✅ Run migrations
6. ✅ Collect static files
7. ✅ Start containers
8. ✅ Clean up old images

### Manual Deployment

Go to GitHub: **Actions → Deploy to VPS → Run workflow**

---

## Monitoring Deployment

### View Logs in GitHub

1. Go to **Actions** tab
2. Click on latest workflow run
3. Click on **Deploy to Production** job
4. View detailed logs

### Check VPS Status

SSH into VPS:

```bash
ssh -p YOUR_PORT YOUR_USER@YOUR_VPS_IP

# Check containers
docker-compose ps

# View logs
docker-compose logs -f web

# Check recent deployments
git log --oneline -5
```

---

## Troubleshooting

### Issue: "Permission denied (publickey)"

**Solution:**
```bash
# Verify SSH key is correct
cat ~/.ssh/github_deploy.pub

# Ensure it's in VPS authorized_keys
ssh YOUR_USER@YOUR_VPS_IP "cat ~/.ssh/authorized_keys"
```

### Issue: "Docker: permission denied"

**Solution:**
```bash
# On VPS
sudo usermod -aG docker $USER
newgrp docker
```

### Issue: "Project directory not found"

**Solution:**
Update workflow with correct path:
```yaml
cd /your/actual/project/path
```

### Issue: "Migrations failed"

**Solution:**
```bash
# On VPS, run manually
cd ~/Invisibilidown
docker-compose run --rm web python manage.py migrate --fake-initial
```

---

## Advanced Configuration

### Deploy to Staging First

Create `.github/workflows/deploy-staging.yml`:

```yaml
on:
  push:
    branches:
      - develop  # Deploy staging on develop branch
```

### Add Health Check

Add to workflow after deployment:

```yaml
- name: Health Check
  run: |
    sleep 10
    curl -f https://your-domain.com/health/ || exit 1
```

### Slack Notifications

Add to workflow:

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Security Best Practices

1. ✅ Use separate SSH key for deployments
2. ✅ Restrict SSH key to specific commands (optional)
3. ✅ Use GitHub Environments for production
4. ✅ Enable branch protection on `main`
5. ✅ Review deployment logs regularly

---

## Rollback Procedure

If deployment fails:

```bash
# SSH to VPS
ssh -p PORT USER@VPS_IP

# Go to project
cd ~/Invisibilidown

# Rollback to previous commit
git reset --hard HEAD~1

# Rebuild and restart
docker-compose build
docker-compose up -d
```

---

## Next Steps

1. ✅ Configure all GitHub secrets
2. ✅ Test SSH connection
3. ✅ Push to main branch
4. ✅ Monitor deployment in Actions tab
5. ✅ Verify application is running

**Your CI/CD pipeline is ready!** 🚀
