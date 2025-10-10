# Quick Start Guide

Get up and running in minutes!

## 🎯 Goal

This guide will help you:
1. Test the application locally
2. Deploy to Firebase (production)

## 📋 Prerequisites

```bash
# Install required tools
npm install -g firebase-tools
# Install Docker Desktop (for APy server)
# Install Google Cloud SDK from https://cloud.google.com/sdk/install
```

## 🚀 Local Development (5 minutes)

### Step 1: Install Dependencies

```bash
cd /home/mark/apertium-dev/ido-epo-translator-web

# Install frontend dependencies
npm install

# Install functions dependencies
cd functions && npm install && cd ..
```

### Step 2: Start APy Server

```bash
cd apy-server
docker-compose up -d
cd ..
```

⏱️ First build takes 10-15 minutes. Get a coffee! ☕

### Step 3: Start Development Server

```bash
npm run dev
```

Open http://localhost:5173 in your browser!

### Step 4: Test Everything Works

```bash
./scripts/test-local.sh
```

## 🌍 Production Deployment (15 minutes)

### Step 1: One-Time Setup

```bash
# Login to Google Cloud
gcloud auth login

# Login to Firebase
firebase login

# Create Firebase project (or use existing)
firebase use --add
# Select your project ID: ido-epo-translator (or create new)

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Configure Environment

```bash
# Set your Firebase project ID
export FIREBASE_PROJECT_ID="ido-epo-translator"

# Set admin password for the admin panel
firebase functions:config:set admin.password="YOUR_SECURE_PASSWORD"
```

### Step 3: Deploy Everything

```bash
# One command to deploy everything!
./scripts/deploy-all.sh
```

This will:
1. Build APy Docker image with your latest translations
2. Deploy to Cloud Run
3. Build and deploy Firebase frontend
4. Build and deploy Firebase functions

### Step 4: Update Firebase Functions Config

After APy deployment, you'll get a URL. Set it:

```bash
firebase functions:config:set apy.server_url="YOUR_CLOUD_RUN_URL"

# Redeploy functions with new config
firebase deploy --only functions
```

### Step 5: Test Production

Visit: `https://YOUR_PROJECT_ID.web.app`

## 🔄 Updating Translations

When you make changes to your Apertium dictionaries:

### Option 1: Automated Script (Recommended)

```bash
./scripts/update-translations.sh
```

This will:
- Pull latest from your Apertium repos
- Rebuild locally
- Ask if you want to deploy

### Option 2: Manual via Admin Panel

1. Go to your website
2. Click "Admin" tab
3. Enter admin password
4. Click "Rebuild & Deploy"

### Option 3: Manual Deployment

```bash
./scripts/deploy-apy.sh v1.0.1
```

## 📊 Common Commands

```bash
# Local development
npm run dev                    # Start dev server
./scripts/test-local.sh       # Test locally

# Deployment
./scripts/deploy-all.sh       # Deploy everything
./scripts/deploy-apy.sh       # Deploy APy server only
./scripts/deploy-firebase.sh  # Deploy frontend/functions only

# Monitoring
firebase functions:log        # View function logs
gcloud run services logs read ido-epo-apy  # View APy logs

# Cost tracking
gcloud billing budgets list   # View budgets
```

## 🐛 Troubleshooting

### APy server won't start

```bash
docker-compose logs -f apy-server
```

Common fixes:
- Increase Docker memory (Settings > Resources)
- Wait longer (first build is slow)
- Check disk space

### "Permission denied" on scripts

```bash
chmod +x scripts/*.sh
```

### Firebase deploy fails

```bash
# Make sure you're on the right project
firebase use

# Clear cache
rm -rf node_modules functions/node_modules
npm install
cd functions && npm install && cd ..
```

### Translation returns empty

```bash
# Test APy server directly
curl http://localhost:2737/listPairs
```

## 💰 Cost Estimate

**Free Tier**: $0/month for low usage
- Firebase Hosting: Free up to 10GB
- Cloud Functions: Free up to 2M invocations
- Cloud Run: Free up to 2M requests

**Moderate Usage**: $5-15/month (1000 translations/day)

## 📚 Next Steps

1. ✅ Test locally
2. ✅ Deploy to production
3. ⬜ Set up custom domain
4. ⬜ Configure monitoring alerts
5. ⬜ Add usage analytics

## 🆘 Getting Help

- **Apertium**: https://wiki.apertium.org
- **Firebase**: https://firebase.google.com/docs
- **Cloud Run**: https://cloud.google.com/run/docs

---

**That's it!** You now have a production-ready translation website! 🎉

