# CI/CD Update Plan

**Status:** DRAFT  
**Date:** October 20, 2025  
**Purpose:** Plan all CI/CD path updates for restructured repository

## Current CI/CD Setup

### Web App Workflows
- **Location:** `ido-epo-translator-web/.github/workflows/`
- **Files:**
  - `deploy-worker.yml` - Cloudflare Workers deployment (ACTIVE)
  - `deploy-firebase.yml` - Firebase deployment (DISABLED)

### Current assumptions:
- Web app is at root of its own repo or at `ido-epo-translator-web/`
- No submodule dependencies
- Build artifacts in `dist/`
- Worker deployed from `_worker.js`

---

## Required Updates After Restructure

### 1. Web App Workflows

**New location:** `tools/web/ido-epo-translator-web/.github/workflows/`

#### deploy-worker.yml updates:

**Before:**
```yaml
- name: Checkout
  uses: actions/checkout@v4

- name: Setup Node
  uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm"
    cache-dependency-path: "package-lock.json"

- name: Install deps
  run: npm ci --no-audit --no-fund

- name: Build
  run: npm run build
```

**After:**
```yaml
- name: Checkout
  uses: actions/checkout@v4
  with:
    submodules: recursive  # Initialize submodules

- name: Setup Node
  uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm"
    cache-dependency-path: "tools/web/ido-epo-translator-web/package-lock.json"

- name: Install deps
  working-directory: tools/web/ido-epo-translator-web
  run: npm ci --no-audit --no-fund

- name: Read app version
  id: version
  working-directory: tools/web/ido-epo-translator-web
  run: echo "app_version=$(jq -r .version package.json)" >> $GITHUB_OUTPUT

- name: Build
  working-directory: tools/web/ido-epo-translator-web
  run: npm run build

- name: Deploy with Wrangler
  working-directory: tools/web/ido-epo-translator-web
  env:
    CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
  run: |
    npx wrangler --version
    npx wrangler deploy --env="" --var APP_VERSION=${{ steps.version.outputs.app_version }}
```

### 2. Apertium Pair Build Workflow (NEW)

**Create:** `.github/workflows/build-apertium-pair.yml`

```yaml
name: Build and Test Apertium Pair

on:
  push:
    branches: [ main, feature/* ]
    paths:
      - 'apertium/**'
      - '.github/workflows/build-apertium-pair.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'apertium/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
      
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            autoconf automake libtool \
            pkg-config flex bison \
            libxml2-dev libxml2-utils \
            xsltproc
      
      - name: Cache vendor builds
        uses: actions/cache@v3
        with:
          path: apertium/vendor/installed
          key: vendor-${{ runner.os }}-${{ hashFiles('apertium/vendor/*/configure.ac') }}
      
      - name: Build vendor dependencies
        working-directory: apertium/apertium-dev
        run: make vendor
      
      - name: Build Ido-Esperanto pair
        working-directory: apertium/apertium-dev
        run: make pair
      
      - name: Run tests
        working-directory: apertium/apertium-dev
        run: make test
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: apertium-ido-epo-binaries
          path: apertium/build/*.bin
          retention-days: 7
```

### 3. Extractor Pipeline Workflow (NEW)

**Create:** `.github/workflows/run-extractor.yml`

```yaml
name: Run Dictionary Extractor

on:
  workflow_dispatch:
    inputs:
      force_rebuild:
        description: 'Force full rebuild'
        required: false
        default: 'false'
  schedule:
    # Run weekly on Sundays at 2 AM UTC
    - cron: '0 2 * * 0'

jobs:
  extract:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
      
      - name: Install Python dependencies
        run: |
          pip install -r tools/extractor/ido-esperanto-extractor/requirements.txt
      
      - name: Run extractor pipeline
        working-directory: tools/extractor/ido-esperanto-extractor
        run: make all
      
      - name: Generate reports
        working-directory: tools/extractor/ido-esperanto-extractor
        run: make reports
      
      - name: Upload extraction results
        uses: actions/upload-artifact@v3
        with:
          name: extractor-output
          path: |
            tools/extractor/ido-esperanto-extractor/output/**
            tools/extractor/ido-esperanto-extractor/reports/**
          retention-days: 30
      
      - name: Create PR if changes detected
        if: github.event_name == 'schedule'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Check if dictionaries have changes
          if [ -n "$(git status --porcelain apertium/apertium-ido-epo/*.dix)" ]; then
            git config user.name "Extractor Bot"
            git config user.email "bot@apertium-ido-epo"
            git checkout -b extractor-update-$(date +%Y%m%d)
            git add apertium/apertium-ido-epo/*.dix
            git commit -m "chore: Update dictionaries from extractor pipeline"
            git push origin extractor-update-$(date +%Y%m%d)
            
            gh pr create \
              --title "Dictionary update from extractor pipeline" \
              --body "Automated dictionary update from weekly extractor run" \
              --label "automated,extractor"
          fi
```

### 4. Root-level Build Workflow (OPTIONAL)

**Create:** `.github/workflows/build-all.yml`

```yaml
name: Build All Subprojects

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-core:
    uses: ./.github/workflows/build-apertium-pair.yml
  
  build-web:
    uses: ./.github/workflows/deploy-worker.yml
    secrets: inherit
```

---

## Webhook and EC2 Updates

### Current setup:
- Webhook server on EC2 listens for GitHub pushes
- Rebuilds Apertium pair on main branch updates
- Scripts at `ido-epo-translator-web/apy-server/rebuild.sh`

### Required updates:

#### 1. Update webhook paths in `webhook-server.js`

**Location:** `tools/web/ido-epo-translator-web/webhook-server.js`

**Before:**
```javascript
const APERTIUM_PAIR_DIR = '/path/to/apertium-ido-epo';
```

**After:**
```javascript
const APERTIUM_PAIR_DIR = '/path/to/apertium/apertium-ido-epo';
const VENDOR_DIR = '/path/to/apertium/vendor';
```

#### 2. Update rebuild scripts

**Location:** `tools/web/ido-epo-translator-web/apy-server/rebuild.sh`

**Before:**
```bash
cd /path/to/apertium-ido-epo
make clean
make
```

**After:**
```bash
cd /path/to/apertium/apertium-dev
make vendor  # Ensure vendor is built
make pair    # Build the pair
```

#### 3. Update EC2 deployment scripts

**Files to update:**
- `tools/web/ido-epo-translator-web/setup-ec2.sh`
- `tools/web/ido-epo-translator-web/update-ec2-docker.sh`
- `tools/web/ido-epo-translator-web/update-ec2-webhook.sh`

**Add submodule initialization:**
```bash
# In all EC2 scripts, after git pull:
git submodule update --init --recursive
```

---

## Documentation Updates Required

### README files to update:

1. **Root README.md**
   - Update build instructions
   - Update directory structure section
   - Add submodule initialization steps

2. **apertium/README.md**
   - New file with pair-specific docs
   - Reference vendor submodules

3. **tools/web/ido-epo-translator-web/README.md**
   - Update paths in examples
   - Update deployment instructions

4. **tools/extractor/ido-esperanto-extractor/README.md**
   - Update output paths
   - Reference new structure

---

## GitHub Secrets Verification

Ensure these secrets are configured:

### For Web deployment:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

### For automated PRs:
- `GITHUB_TOKEN` (automatically provided)

### Optional (if using Firebase):
- `FIREBASE_TOKEN`
- `FIREBASE_PROJECT_ID`

---

## Migration Checklist

### Phase 1: Preparation
- [ ] Update all workflow files with new paths
- [ ] Add submodule initialization to all workflows
- [ ] Update webhook scripts
- [ ] Update EC2 deployment scripts
- [ ] Test workflows on feature branch

### Phase 2: Testing
- [ ] Create test PR with restructured layout
- [ ] Verify all workflows run successfully
- [ ] Test webhook triggers
- [ ] Test manual deployments

### Phase 3: Deployment
- [ ] Merge restructuring PR
- [ ] Verify CI passes on main
- [ ] Update EC2 server paths
- [ ] Restart webhook server
- [ ] Test end-to-end deployment

### Phase 4: Cleanup
- [ ] Remove old workflow files
- [ ] Update documentation links
- [ ] Archive old deployment scripts
- [ ] Notify team of new structure

---

## Rollback Plan

If CI/CD breaks after restructure:

1. **Immediate:** Revert PR that changed structure
2. **Short-term:** Use manual deployment while fixing
3. **Testing:** Use feature branch to test fixes
4. **Recovery:** Restore from backup or git history

---

## Testing Strategy

### Local testing before committing:

```bash
# Test vendor build
cd apertium/apertium-dev
make vendor

# Test pair build
make pair

# Test tests
make test

# Test web build
cd ../../tools/web/ido-epo-translator-web
npm install
npm run build

# Test extractor
cd ../../extractor/ido-esperanto-extractor
# Run extractor commands
```

### CI testing on feature branch:

1. Create feature branch with all changes
2. Push to GitHub
3. Observe workflow runs
4. Fix any path issues
5. Iterate until all green
6. Then merge to main

---

## Estimated Timeline

- **Workflow updates:** 2 hours
- **Testing on feature branch:** 2-3 hours
- **EC2 updates:** 1 hour
- **Documentation updates:** 1 hour
- **Verification and monitoring:** 1 hour

**Total:** ~7-8 hours

---

## Questions Before Proceeding

1. Should we keep old workflow files as `.disabled` or delete them?
2. Do we want to cache vendor builds in CI (faster but uses cache storage)?
3. Should extractor run automatically on schedule, or manual only?
4. Do we need notification webhooks for failed builds?

---

**Status:** Ready for implementation after user approval

