# Ido-Esperanto Web Translator

A modern web application for translating between Ido and Esperanto, powered by Apertium machine translation. Features text translation and full webpage translation with side-by-side comparison.

## 🌟 Features

- **Text Translation**: Translate phrases and sentences between Ido and Esperanto
- **URL Translation**: Translate entire webpages (e.g., Wikipedia articles) with side-by-side comparison
- **Bidirectional**: Switch translation direction with one click
- **Admin Panel**: Manual rebuild and deployment of updated translation dictionaries
- **Modern UI**: Beautiful, responsive interface built with React and TailwindCSS

## 🏗️ Architecture

```
┌──────────────────────────────────────────────┐
│     Firebase Hosting (Static Frontend)      │
│     - React + TypeScript + TailwindCSS       │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│     Firebase Cloud Functions (API)          │
│     - Translation endpoints                  │
│     - URL fetching and processing            │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│     Cloud Run (APy Server)                   │
│     - Docker container with Apertium         │
│     - apertium-ido + apertium-ido-epo        │
└──────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Node.js 18+ and npm
- Docker and Docker Compose
- Firebase CLI: `npm install -g firebase-tools`
- Google Cloud Platform account
- Firebase project created

## 🚀 Quick Start (Local Development)

### 1. Clone and Install Dependencies

```bash
cd ido-epo-translator-web

# Install frontend dependencies
npm install

# Install functions dependencies
cd functions
npm install
cd ..
```

### 2. Start the APy Server Locally

```bash
cd apy-server
docker-compose up -d
cd ..
```

Wait for the server to build and start (first time takes 10-15 minutes).

### 3. Start the Development Server

```bash
# In the project root
npm run dev
```

Open http://localhost:5173 in your browser.

## 🔧 Configuration

### Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com
2. Enable Cloud Functions and Hosting
3. Update `.firebaserc` with your project ID:

```json
{
  "projects": {
    "default": "your-project-id"
  }
}
```

### Environment Variables

Create `functions/.env` for local development:

```env
APY_SERVER_URL=http://localhost:2737
ADMIN_PASSWORD=your-secure-password
```

For production, set these in Firebase Functions config:

```bash
firebase functions:config:set apy.server_url="YOUR_CLOUD_RUN_URL"
firebase functions:config:set admin.password="YOUR_SECURE_PASSWORD"
```

## 📦 Deployment

### Step 1: Deploy APy Server to Cloud Run

```bash
cd apy-server

# Build and push to Google Container Registry
PROJECT_ID="your-firebase-project-id"
docker build -t gcr.io/$PROJECT_ID/ido-epo-apy .
docker push gcr.io/$PROJECT_ID/ido-epo-apy

# Deploy to Cloud Run
gcloud run deploy ido-epo-apy \
  --image gcr.io/$PROJECT_ID/ido-epo-apy \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 2737 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300

# Get the service URL
gcloud run services describe ido-epo-apy --region us-central1 --format="value(status.url)"
```

### Step 2: Configure Firebase Functions

Update the APy server URL in Firebase Functions:

```bash
firebase functions:config:set apy.server_url="YOUR_CLOUD_RUN_URL"
firebase functions:config:set admin.password="YOUR_SECURE_PASSWORD"
```

### Step 3: Deploy Frontend and Functions

```bash
# Build and deploy everything
npm run deploy

# Or deploy separately
firebase deploy --only hosting
firebase deploy --only functions
```

## 🔄 Updating Translation Dictionaries

### Option 1: Via Admin Panel (Manual Trigger)

1. Navigate to the Admin tab in the web app
2. Enter the admin password
3. Click "Rebuild & Deploy"
4. Wait for the rebuild to complete

### Option 2: Via Docker (Local Development)

```bash
# Rebuild inside the container
docker exec ido-epo-apy /opt/apertium-ido-epo-local/rebuild.sh

# Restart the container
docker-compose restart
```

### Option 3: Rebuild and Redeploy Cloud Run

```bash
cd apy-server

# Copy your latest local repos (optional)
cp -r ../../apertium-ido ./apertium-ido-local
cp -r ../../apertium-ido-epo ./apertium-ido-epo-local

# Rebuild and push
docker build --no-cache -t gcr.io/$PROJECT_ID/ido-epo-apy .
docker push gcr.io/$PROJECT_ID/ido-epo-apy

# Update Cloud Run service (triggers rolling update)
gcloud run services update ido-epo-apy --region us-central1
```

## 🧪 Testing

### Test APy Server

```bash
# List available language pairs
curl http://localhost:2737/listPairs

# Translate Ido to Esperanto
curl -X POST http://localhost:2737/translate \
  -d "q=Me amas vu" \
  -d "langpair=ido|epo"

# Translate Esperanto to Ido
curl -X POST http://localhost:2737/translate \
  -d "q=Mi amas vin" \
  -d "langpair=epo|ido"
```

### Test Firebase Functions Locally

```bash
cd functions
npm run serve
```

Then test the endpoints:

```bash
# Test translation
curl -X POST http://localhost:5001/your-project-id/us-central1/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Me amas vu","direction":"ido-epo"}'
```

## 📁 Project Structure

```
ido-epo-translator-web/
├── src/                      # React frontend source
│   ├── components/           # React components
│   │   ├── TextTranslator.tsx
│   │   ├── UrlTranslator.tsx
│   │   └── AdminPanel.tsx
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Tailwind styles
├── functions/               # Firebase Cloud Functions
│   └── src/
│       └── index.ts         # API endpoints
├── apy-server/              # Docker setup for APy
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── rebuild.sh
├── public/                  # Static assets
├── firebase.json           # Firebase configuration
├── package.json            # Frontend dependencies
└── README.md               # This file
```

## 💰 Cost Estimate (Firebase Free Tier)

- **Firebase Hosting**: 10 GB storage, 360 MB/day transfer (FREE)
- **Cloud Functions**: 2M invocations/month, 400K GB-seconds (FREE)
- **Cloud Run**: 2M requests/month, 360K GB-seconds (FREE)

**Estimated monthly cost for low usage: $0-5/month**

For moderate usage (1000 translations/day), expect $5-15/month.

## 🛠️ Development

### Frontend Development

```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Functions Development

```bash
cd functions
npm run build        # Compile TypeScript
npm run serve        # Run locally with emulator
npm run deploy       # Deploy functions only
```

## 🐛 Troubleshooting

### APy Server Won't Start

Check Docker logs:
```bash
docker-compose logs -f apy-server
```

Common issues:
- Compilation errors: Check Apertium dependency versions
- Out of memory: Increase Docker memory allocation
- Port conflict: Change port in docker-compose.yml

### Translation Returns Empty

1. Verify APy server is running: `curl http://localhost:2737/listPairs`
2. Check if language pair is installed
3. Test with simple text first

### Firebase Deployment Fails

1. Ensure you're logged in: `firebase login`
2. Verify project ID: `firebase projects:list`
3. Check quota limits in Firebase console

## 📚 Resources

- [Apertium Documentation](https://wiki.apertium.org)
- [Apertium APy Repository](https://github.com/apertium/apertium-apy)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

## 📄 License

This project uses Apertium, which is licensed under the GPL. See individual component licenses for details.

## 🤝 Contributing

Contributions to the translation dictionaries should be made to:
- [apertium-ido](https://github.com/apertium/apertium-ido)
- [apertium-ido-epo](https://github.com/apertium/apertium-ido-epo)

For web app improvements, please open issues or pull requests in this repository.

