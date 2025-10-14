# Ido-Esperanto Web Translator

A modern web application for translating between Ido and Esperanto, powered by Apertium machine translation. Features text translation and full webpage translation with side-by-side comparison.

> Current deployment: Cloudflare Worker (static assets + API) + EC2 APy server
>
> - Set `APY_SERVER_URL` in the Worker to your APy base URL (e.g., `http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com`)
> - Set `REBUILD_WEBHOOK_URL` to `http://<ec2-hostname>/rebuild` to enable the Rebuild button

## 🌟 Features

- **Text Translation**: Translate phrases and sentences between Ido and Esperanto
- **URL Translation**: Translate entire webpages (e.g., Wikipedia articles) with side-by-side comparison
- **Bidirectional**: Switch translation direction with one click
- **Rebuild Button**: Trigger idempotent dictionary updates on EC2 (no password)
- **Modern UI**: Beautiful, responsive interface built with React and TailwindCSS

## 🏗️ Architecture

```
┌──────────────────────────────────────────────┐
│        Cloudflare Worker (Frontend + API)    │
│  - React + TypeScript + TailwindCSS          │
│  - Worker handles /api/* and serves assets   │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│        EC2 (APy Server + Apertium)          │
│  - Dockerized APy HTTP server                │
│  - apertium-ido + apertium-ido-epo           │
│  - Exposes port 2737                         │
└──────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Node.js 18+ and npm
- Docker and Docker Compose (for EC2 build)

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

### Cloudflare Worker Setup

1. Build locally: `npm run build`
2. Deploy: `npm run cf:deploy`
3. Set Worker variables (Dashboard → Settings → Variables):
   - `APY_SERVER_URL = http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com`
   - `REBUILD_WEBHOOK_URL = http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com/rebuild`
4. GitHub Actions deploys on push to `main` (`.github/workflows/deploy-worker.yml`).

### Environment Variables

Local development (wrangler / Pages dev): set in `wrangler.toml`

```toml
[vars]
APY_SERVER_URL = "http://localhost:2737"
REBUILD_WEBHOOK_URL = "http://localhost/rebuild"
```

Production (Worker → Settings → Variables):

```text
APY_SERVER_URL = http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com
REBUILD_WEBHOOK_URL = http://ec2-52-211-137-158.eu-west-1.compute.amazonaws.com/rebuild
```

## 📦 Deployment

### Option A (Recommended): Cloudflare Worker + EC2

1) Deploy APy to EC2

```bash
ssh ubuntu@<YOUR_EC2_IP>
curl -o setup-ec2.sh https://raw.githubusercontent.com/komapc/ido-epo-translator-web/main/setup-ec2.sh
chmod +x setup-ec2.sh
./setup-ec2.sh
# After build (10–15 min)
curl http://localhost:2737/listPairs
```

2) Configure Cloudflare Worker env

```text
APY_SERVER_URL = http://ec2-<YOUR_EC2_IP with dashes>.<your-aws-region>.compute.amazonaws.com
ADMIN_PASSWORD = <your-strong-secret>
```

3) Deploy Worker with `wrangler deploy` or merge PR to `main`.

### Option B: Firebase + Cloud Run (Legacy)
If you prefer this path, see the older instructions in git history or `PROJECT_SUMMARY.md`. Current stack favors Cloudflare Pages + EC2.

## 🔄 Updating Translation Dictionaries

### Option 1: Via Rebuild Button (Manual Trigger)

1. Open the web app
2. Click "Rebuild"
3. The EC2 webhook will run `update-dictionaries.sh` and rebuild only if changes are detected

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

### Test Worker locally

Use Wrangler dev:

```bash
# Health
curl http://127.0.0.1:8787/api/health

# Translate
curl -X POST http://127.0.0.1:8787/api/translate \
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
│   │   └── AdminPanel.tsx  # shows a single Rebuild button
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

# Trigger redeploy
