# 🚀 Streamlit Deployment Guide

Complete guide for deploying the Poverty Dashboard to various platforms.

## Table of Contents

1. [Streamlit Community Cloud (Easiest)](#1-streamlit-community-cloud)
2. [Docker Deployment](#2-docker-deployment)
3. [Heroku](#3-heroku)
4. [AWS EC2](#4-aws-ec2)
5. [Google Cloud Platform](#5-google-cloud-platform)
6. [Azure](#6-azure)
7. [Local Production Server](#7-local-production-server)

---

## 1. Streamlit Community Cloud

**Best for:** Quick, free deployment with GitHub integration

### Prerequisites
- GitHub account
- Project pushed to GitHub repository

### Steps

1. **Push your code to GitHub** (already done)
   ```bash
   git push origin main
   ```

2. **Visit Streamlit Community Cloud**
   - Go to: https://share.streamlit.io
   - Sign in with GitHub

3. **Deploy your app**
   - Click "New app"
   - Select your repository: `anonymous-pxe/anonymous-pxe`
   - Branch: `feature/poverty-dashboard` (or `main` after merging)
   - Main file path: `Poverty_dashboard/app.py`
   - Click "Deploy"

4. **Configuration** (Optional)
   - Click "Advanced settings"
   - Add environment variables if needed
   - Set Python version: 3.9

5. **Your app will be live at:**
   ```
   https://your-app-name.streamlit.app
   ```

### Managing Your App

- **View logs**: Click on the app → "Manage app" → "Logs"
- **Reboot app**: "Manage app" → "Reboot app"
- **Update**: Just push to GitHub, auto-deploys
- **Delete**: "Manage app" → "Delete app"

### Streamlit Cloud Limitations

- Free tier: Limited resources, public apps only
- Private apps: Requires paid plan
- No persistent storage (use external database)

---

## 2. Docker Deployment

**Best for:** Consistent deployment across platforms

### Create Dockerfile

Already included in the project, or create:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build the Docker image
docker build -t poverty-dashboard .

# Run the container
docker run -p 8501:8501 poverty-dashboard

# Run with environment variables
docker run -p 8501:8501 \
  -e WB_API_KEY=your_key \
  poverty-dashboard

# Run in background
docker run -d -p 8501:8501 --name poverty-app poverty-dashboard
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - WB_API_KEY=${WB_API_KEY}
    volumes:
      - ./reports:/app/reports
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

---

## 3. Heroku

**Best for:** Quick cloud deployment with add-ons

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

1. **Create `Procfile`**
   ```bash
   web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/

   echo "\
   [general]\n\
   email = \"your-email@example.com\"\n\
   " > ~/.streamlit/credentials.toml

   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

3. **Make setup.sh executable**
   ```bash
   chmod +x setup.sh
   ```

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create poverty-dashboard-app

# Set Python buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku feature/poverty-dashboard:main

# Or from main branch
git push heroku main

# Open app
heroku open

# View logs
heroku logs --tail

# Scale dynos
heroku ps:scale web=1
```

### Heroku Configuration

```bash
# Set environment variables
heroku config:set WB_API_KEY=your_key

# View config
heroku config

# Add PostgreSQL (if needed)
heroku addons:create heroku-postgresql:hobby-dev
```

---

## 4. AWS EC2

**Best for:** Full control, scalable deployment

### Launch EC2 Instance

1. **Create EC2 instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t2.medium (or larger)
   - Security group: Allow ports 22 (SSH), 8501 (Streamlit)

2. **Connect to instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3-pip python3-venv -y

   # Install git
   sudo apt install git -y
   ```

4. **Clone and setup project**
   ```bash
   # Clone repository
   git clone https://github.com/anonymous-pxe/anonymous-pxe.git
   cd anonymous-pxe/Poverty_dashboard

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install requirements
   pip install -r requirements.txt
   ```

5. **Run with systemd (production)**

   Create `/etc/systemd/system/poverty-dashboard.service`:
   ```ini
   [Unit]
   Description=Poverty Dashboard Streamlit App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/anonymous-pxe/Poverty_dashboard
   Environment="PATH=/home/ubuntu/anonymous-pxe/Poverty_dashboard/venv/bin"
   ExecStart=/home/ubuntu/anonymous-pxe/Poverty_dashboard/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable poverty-dashboard
   sudo systemctl start poverty-dashboard
   sudo systemctl status poverty-dashboard
   ```

6. **Setup Nginx reverse proxy** (optional)
   ```bash
   sudo apt install nginx -y
   ```

   Create `/etc/nginx/sites-available/poverty-dashboard`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/poverty-dashboard /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## 5. Google Cloud Platform

**Best for:** Google ecosystem integration

### Using Cloud Run

1. **Enable Cloud Run API**
   ```bash
   gcloud services enable run.googleapis.com
   ```

2. **Create Dockerfile** (use the one from Docker section)

3. **Build and deploy**
   ```bash
   # Set project
   gcloud config set project YOUR_PROJECT_ID

   # Build image
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/poverty-dashboard

   # Deploy to Cloud Run
   gcloud run deploy poverty-dashboard \
     --image gcr.io/YOUR_PROJECT_ID/poverty-dashboard \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Using Compute Engine

Similar to AWS EC2 - follow the EC2 instructions but use GCP console to create VM.

---

## 6. Azure

**Best for:** Microsoft ecosystem

### Using Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name poverty-dashboard-rg --location eastus

# Create container
az container create \
  --resource-group poverty-dashboard-rg \
  --name poverty-dashboard \
  --image your-dockerhub-username/poverty-dashboard \
  --dns-name-label poverty-dashboard-app \
  --ports 8501

# Get public IP
az container show \
  --resource-group poverty-dashboard-rg \
  --name poverty-dashboard \
  --query ipAddress.fqdn \
  --output tsv
```

### Using Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name poverty-dashboard-plan \
  --resource-group poverty-dashboard-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group poverty-dashboard-rg \
  --plan poverty-dashboard-plan \
  --name poverty-dashboard-app \
  --deployment-container-image-name your-dockerhub-username/poverty-dashboard
```

---

## 7. Local Production Server

**Best for:** On-premise deployment

### Using tmux (simple)

```bash
# Start tmux session
tmux new -s poverty-dashboard

# Navigate to project
cd Poverty_dashboard

# Activate venv and run
source venv/bin/activate
streamlit run app.py --server.port=8501

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t poverty-dashboard
```

### Using PM2 (Node.js process manager)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem.config.js
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'poverty-dashboard',
    script: 'streamlit',
    args: 'run app.py --server.port=8501',
    interpreter: 'python3',
    cwd: '/path/to/Poverty_dashboard',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
}
EOF

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 config
pm2 save

# Setup startup script
pm2 startup
```

---

## Environment Variables

For all deployment methods, you may need to set environment variables:

```bash
# World Bank API key
WB_API_KEY=your_world_bank_api_key

# India data API key
INDIA_API_KEY=your_india_api_key

# Custom settings
CACHE_TTL=3600
DEBUG=false
```

### In Streamlit Cloud
- Go to app settings
- Add secrets in `.streamlit/secrets.toml` format:
  ```toml
  WB_API_KEY = "your_key"
  INDIA_API_KEY = "your_key"
  ```

### In Docker
```bash
docker run -e WB_API_KEY=your_key -e INDIA_API_KEY=your_key ...
```

### In Heroku
```bash
heroku config:set WB_API_KEY=your_key
```

---

## Performance Optimization

### 1. Caching
All major data functions already use `@st.cache_data`

### 2. Resource Limits
Adjust in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false
```

### 3. Connection Pooling
For database connections, use connection pooling.

### 4. CDN for Static Assets
Host large files (GeoJSON, images) on CDN.

---

## Monitoring

### Streamlit Cloud
- Built-in logs and metrics
- Check "Manage app" → "Logs"

### Other Platforms
- Use application monitoring services:
  - Datadog
  - New Relic
  - Prometheus + Grafana

### Health Checks
Add health check endpoint if needed (Streamlit has built-in at `/_stcore/health`)

---

## SSL/HTTPS

### Streamlit Cloud
- Automatically provided

### Custom Domain + Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find and kill process
   lsof -ti:8501 | xargs kill -9
   ```

2. **Memory errors**
   - Increase instance size
   - Optimize data caching
   - Reduce batch sizes

3. **Slow loading**
   - Check cache configuration
   - Optimize data queries
   - Use CDN for static files

4. **Module not found**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

---

## Cost Estimates

| Platform | Free Tier | Paid (monthly) |
|----------|-----------|----------------|
| Streamlit Cloud | ✅ Limited | $20+ |
| Heroku | ❌ | $7-50 |
| AWS EC2 | ❌ | $10-100+ |
| GCP Cloud Run | ✅ Limited | $10-50 |
| Azure | ✅ Limited | $15-100 |

---

## Recommended Deployment

For this project, I recommend:

1. **Development/Testing**: Streamlit Community Cloud (free, easy)
2. **Production (Small)**: Docker on AWS EC2 t2.small ($10-15/month)
3. **Production (Large)**: Docker on AWS ECS or GCP Cloud Run (auto-scaling)

---

## Quick Deploy Commands Summary

### Streamlit Cloud
```bash
# Just push to GitHub, deploy via web UI
git push origin main
# Visit share.streamlit.io
```

### Docker
```bash
docker build -t poverty-dashboard .
docker run -p 8501:8501 poverty-dashboard
```

### Heroku
```bash
heroku create poverty-dashboard
git push heroku main
```

### AWS EC2
```bash
ssh -i key.pem ubuntu@instance-ip
git clone repo
cd Poverty_dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## Support

For deployment issues:
- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Forum: https://discuss.streamlit.io/
- GitHub Issues: Create issue in repository

---

**Last Updated**: 2024
**Maintained By**: Poverty Dashboard Team
