# Deployment Guide

Complete step-by-step guide to deploy the Ido-Esperanto translator to production.

## Prerequisites Checklist

- [ ] Google Cloud Platform account created
- [ ] Firebase project created
- [ ] Billing enabled (required for Cloud Run, but free tier is generous)
- [ ] Firebase CLI installed: `npm install -g firebase-tools`
- [ ] Google Cloud SDK installed
- [ ] Docker installed locally
- [ ] Domain name (optional, for custom domain)

## Part 1: Initial Setup

### 1. Create Firebase Project

```bash
# Login to Firebase
firebase login

# Create new project (or use existing)
firebase projects:create ido-epo-translator

# List projects to verify
firebase projects:list

# Set the project as default
firebase use ido-epo-translator
```

### 2. Enable Required APIs

Go to Google Cloud Console and enable:
- Cloud Run API
- Cloud Build API
- Container Registry API
- Firebase Hosting API

Or via command line:

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Configure GCloud

```bash
# Set your project
gcloud config set project ido-epo-translator

# Set default region
gcloud config set run/region us-central1
```

## Part 2: Deploy APy Translation Server

### 1. Build Docker Image with Your Local Repos

```bash
cd /home/mark/apertium-dev/ido-epo-translator-web/apy-server

# Create directory for local repos
mkdir -p apertium-ido-epo-local

# Copy your latest Ido-Esperanto translation files
cp -r /home/mark/apertium-dev/apertium-ido ./apertium-ido-local
cp -r /home/mark/apertium-dev/apertium-ido-epo ./apertium-ido-epo-local

# Build the Docker image
docker build -t gcr.io/ido-epo-translator/ido-epo-apy:v1 .
```

### 2. Push to Google Container Registry

```bash
# Configure Docker to use gcloud credentials
gcloud auth configure-docker

# Push the image
docker push gcr.io/ido-epo-translator/ido-epo-apy:v1
```

### 3. Deploy to Cloud Run

```bash
gcloud run deploy ido-epo-apy \
  --image gcr.io/ido-epo-translator/ido-epo-apy:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 2737 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 3 \
  --min-instances 0

# Get the service URL
APY_URL=$(gcloud run services describe ido-epo-apy --region us-central1 --format="value(status.url)")
echo "APy Server URL: $APY_URL"
```

**Note**: Save this URL - you'll need it for Firebase Functions configuration.

### 4. Test the APy Server

```bash
# Test if server is running
curl $APY_URL/listPairs

# Test translation
curl -X POST $APY_URL/translate \
  -d "q=Me amas vu" \
  -d "langpair=ido|epo"
```

## Part 3: Deploy Firebase Functions

### 1. Install Dependencies

```bash
cd /home/mark/apertium-dev/ido-epo-translator-web/functions
npm install
```

### 2. Configure Environment Variables

```bash
# Set the APy server URL
firebase functions:config:set apy.server_url="YOUR_CLOUD_RUN_URL"

# Set admin password
firebase functions:config:set admin.password="your-secure-password-here"

# View configuration
firebase functions:config:get
```

### 3. Deploy Functions

```bash
cd /home/mark/apertium-dev/ido-epo-translator-web
firebase deploy --only functions
```

## Part 4: Deploy Frontend

### 1. Build Frontend

```bash
cd /home/mark/apertium-dev/ido-epo-translator-web

# Install dependencies
npm install

# Build for production
npm run build
```

### 2. Deploy to Firebase Hosting

```bash
firebase deploy --only hosting
```

### 3. Get Your Website URL

```bash
firebase hosting:sites:list
```

Your site will be available at: `https://ido-epo-translator.web.app`

## Part 5: Post-Deployment Configuration

### 1. Set Up Custom Domain (Optional)

```bash
# Add custom domain
firebase hosting:sites:create your-domain.com

# Follow the instructions to verify domain ownership
```

### 2. Configure Security Rules

Update `firebase.json` to add security headers:

```json
{
  "hosting": {
    "headers": [
      {
        "source": "**",
        "headers": [
          {
            "key": "X-Content-Type-Options",
            "value": "nosniff"
          },
          {
            "key": "X-Frame-Options",
            "value": "DENY"
          }
        ]
      }
    ]
  }
}
```

### 3. Set Up Monitoring

Enable Cloud Monitoring for Cloud Run:

```bash
# Install monitoring agent
gcloud monitoring channels create \
  --display-name="Email Alerts" \
  --type=email \
  --channel-labels=email_address=your-email@example.com
```

## Part 6: Updating Translations

### Method 1: Manual Update via Admin Panel

1. Go to `https://your-site.web.app`
2. Click "Admin" tab
3. Enter admin password
4. Click "Rebuild & Deploy"

**Note**: This requires implementing the rebuild script in Cloud Run.

### Method 2: Rebuild and Redeploy Docker Image

```bash
cd /home/mark/apertium-dev/ido-epo-translator-web/apy-server

# Copy latest repos
cp -r /home/mark/apertium-dev/apertium-ido ./apertium-ido-local
cp -r /home/mark/apertium-dev/apertium-ido-epo ./apertium-ido-epo-local

# Increment version number
docker build -t gcr.io/ido-epo-translator/ido-epo-apy:v2 .
docker push gcr.io/ido-epo-translator/ido-epo-apy:v2

# Deploy new version
gcloud run deploy ido-epo-apy \
  --image gcr.io/ido-epo-translator/ido-epo-apy:v2 \
  --region us-central1

# Cloud Run will do a rolling update (zero downtime)
```

### Method 3: Automated CI/CD (Advanced)

Create `.github/workflows/deploy.yml` in your Apertium repos:

```yaml
name: Deploy Updated Translations

on:
  push:
    branches: [ master ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and Push Docker Image
        run: |
          # Your build and deploy commands
          
      - name: Deploy to Cloud Run
        run: |
          # Update Cloud Run service
```

## Part 7: Monitoring and Maintenance

### View Cloud Run Logs

```bash
gcloud run services logs read ido-epo-apy --region us-central1
```

### View Firebase Functions Logs

```bash
firebase functions:log
```

### Check Usage and Costs

```bash
# View Cloud Run metrics
gcloud run services describe ido-epo-apy --region us-central1

# View in console
open https://console.cloud.google.com/run
open https://console.firebase.google.com
```

### Set Budget Alerts

```bash
# Create budget alert in Google Cloud Console
# Billing > Budgets & Alerts
# Set alert at $10, $20, $50
```

## Troubleshooting

### Cloud Run Deploy Fails

```bash
# Check build logs
gcloud builds list
gcloud builds log BUILD_ID

# Common fixes:
# 1. Increase timeout: --timeout 900
# 2. Increase memory: --memory 4Gi
# 3. Check image exists: gcloud container images list
```

### Functions Deploy Fails

```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and rebuild
cd functions
rm -rf node_modules lib
npm install
npm run build

# Deploy with verbose logging
firebase deploy --only functions --debug
```

### APy Server Returns 500 Errors

```bash
# Check if language pairs are installed
curl $APY_URL/listPairs

# Exec into Cloud Run (if supported) or check logs
gcloud run services logs read ido-epo-apy --region us-central1 --limit 100
```

## Cost Optimization

### 1. Set Minimum Instances to 0

```bash
gcloud run services update ido-epo-apy \
  --region us-central1 \
  --min-instances 0
```

### 2. Enable Cloud CDN (for static assets)

Already enabled with Firebase Hosting automatically.

### 3. Set Appropriate Timeouts

```bash
gcloud run services update ido-epo-apy \
  --region us-central1 \
  --timeout 60  # Shorter timeout = lower costs
```

## Security Checklist

- [ ] Admin password set to strong value
- [ ] Cloud Run allows unauthenticated (public access needed)
- [ ] Firebase Functions properly configured
- [ ] Environment variables not committed to Git
- [ ] HTTPS enforced (automatic with Firebase)
- [ ] CORS configured correctly

## Rollback Procedure

### Rollback Cloud Run

```bash
# List revisions
gcloud run revisions list --service ido-epo-apy --region us-central1

# Rollback to previous revision
gcloud run services update-traffic ido-epo-apy \
  --region us-central1 \
  --to-revisions PREVIOUS_REVISION=100
```

### Rollback Firebase Hosting

```bash
firebase hosting:rollback
```

## Next Steps

1. Set up custom domain
2. Configure automated backups
3. Implement usage analytics
4. Add rate limiting for API endpoints
5. Set up automated testing
6. Create monitoring dashboards

## Support

- Cloud Run: https://cloud.google.com/run/docs
- Firebase: https://firebase.google.com/support
- Apertium: https://wiki.apertium.org

