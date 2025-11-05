# AI Manus - Google Cloud Deployment Guide

Deploy AI Manus to Google Cloud Platform with Gemini 2.5 Pro integration.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Google Cloud account with billing enabled
- `gcloud` CLI installed ([Download](https://cloud.google.com/sdk/docs/install))
- Gemini API Key: `AIzaSyC7pKCPc9dInPlk9u-84qi2yYOE4HuZaDE`

### One-Command Deployment

```bash
./deploy-gcp.sh
```

The script will:
1. ✅ Enable required Google Cloud APIs
2. ✅ Store Gemini API key in Secret Manager
3. ✅ Build Docker images for frontend and backend
4. ✅ Deploy to Cloud Run with auto-scaling
5. ✅ Provide URLs for your deployed application

**That's it!** Your AI Manus will be running on Google Cloud with Gemini 2.5 Pro.

---

## 📋 Detailed Setup

### Step 1: Prerequisites

1. **Install Google Cloud SDK**
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. **Create or Select Project**
   ```bash
   # Create new project
   gcloud projects create ai-manus-prod --name="AI Manus Production"

   # Or use existing
   gcloud config set project YOUR_PROJECT_ID
   ```

### Step 2: Set Environment Variables

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"  # Or your preferred region
```

### Step 3: Run Deployment

```bash
chmod +x deploy-gcp.sh
./deploy-gcp.sh
```

The script will prompt you for:
- Google Cloud Project ID (if not set)
- MongoDB URI (optional - can add later)

### Step 4: Access Your Application

After deployment completes, you'll see:

```
✅ Frontend URL: https://manus-frontend-xxxxx-uc.a.run.app
✅ Backend URL: https://manus-backend-xxxxx-uc.a.run.app
✅ AI Model: Gemini 2.5 Pro
```

Visit the Frontend URL to start using AI Manus!

---

## 🔧 Configuration

### Gemini 2.5 Pro Integration

The deployment automatically configures:
- **API Key**: `AIzaSyC7pKCPc9dInPlk9u-84qi2yYOE4HuZaDE`
- **Model**: `gemini-2.0-flash-exp` (Gemini 2.5 Pro Flash)
- **API Base**: `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Format**: OpenAI-compatible API

### Database Options

#### Option 1: MongoDB Atlas (Recommended)

1. Create free cluster at [MongoDB Atlas](https://cloud.mongodb.com)
2. Get connection string
3. Update secret:
   ```bash
   echo -n "mongodb+srv://user:pass@cluster.mongodb.net" | \
     gcloud secrets versions add mongodb-uri --data-file=-
   ```

#### Option 2: Google Cloud MongoDB

Use [MongoDB Atlas on GCP Marketplace](https://console.cloud.google.com/marketplace/product/mongodb/mdb-atlas-gcp)

### Redis Configuration (Optional)

For session management:

```bash
# Create Redis instance
gcloud redis instances create manus-redis \
  --size=1 \
  --region=$GCP_REGION \
  --redis-version=redis_7_0

# Get Redis host
REDIS_HOST=$(gcloud redis instances describe manus-redis \
  --region=$GCP_REGION \
  --format="value(host)")

# Create secret
echo -n "$REDIS_HOST" | gcloud secrets create redis-config --data-file=-
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Google Cloud Platform                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  Cloud Run       │         │  Cloud Run       │     │
│  │  (Frontend)      │◄────────┤  (Backend)       │     │
│  │  React + Nginx   │         │  Python/FastAPI  │     │
│  └──────────────────┘         └────────┬─────────┘     │
│                                         │               │
│                                         │               │
│  ┌──────────────────┐         ┌────────▼─────────┐    │
│  │  MongoDB Atlas   │◄────────┤ Gemini 2.5 Pro   │    │
│  │  (Database)      │         │ API              │    │
│  └──────────────────┘         └──────────────────┘    │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │  Secret Manager  │         │  Cloud Build     │    │
│  │  (API Keys)      │         │  (CI/CD)         │    │
│  └──────────────────┘         └──────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Key Components

- **Cloud Run Frontend**: Auto-scaling React app (1-10 instances)
- **Cloud Run Backend**: FastAPI server with Gemini integration
- **Secret Manager**: Secure storage for API keys and credentials
- **MongoDB Atlas**: Managed database for task/session storage
- **Gemini 2.5 Pro**: Google's latest AI model via API

---

## 🔐 Security

### API Key Management

All sensitive data is stored in Google Secret Manager:

```bash
# View secrets
gcloud secrets list

# Update Gemini API key
echo -n "NEW_API_KEY" | gcloud secrets versions add gemini-api-key --data-file=-

# Access secret
gcloud secrets versions access latest --secret="gemini-api-key"
```

### Authentication

Default auth provider: `password`

To configure:
1. Set `AUTH_PROVIDER` environment variable
2. Configure JWT secrets
3. (Optional) Set up email for password resets

---

## 📈 Monitoring & Logs

### View Logs

```bash
# Backend logs
gcloud run logs read manus-backend --region=$GCP_REGION

# Frontend logs
gcloud run logs read manus-frontend --region=$GCP_REGION

# Live tail
gcloud run logs tail manus-backend --region=$GCP_REGION
```

### Monitoring Dashboard

Access at: https://console.cloud.google.com/run

Monitor:
- Request count
- Latency
- Error rate
- Instance count
- CPU/Memory usage

---

## 💰 Cost Estimation

### Free Tier (Month 1-2)

- **Cloud Run**: 2M requests free
- **MongoDB Atlas**: 512MB free forever
- **Secret Manager**: 6 active secrets free
- **Estimated**: **$0-5/month**

### Production Usage

- **Cloud Run**: ~$0.40 per GB-second
- **MongoDB Atlas**: ~$57/month (M10 cluster)
- **Egress**: ~$0.12 per GB
- **Estimated**: **$60-100/month**

---

## 🛠️ Advanced Configuration

### Custom Domain

```bash
gcloud run domain-mappings create \
  --service=manus-frontend \
  --domain=yourdomain.com \
  --region=$GCP_REGION
```

### CI/CD Integration

Create `cloudbuild.yaml`:

```yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/manus-backend', './backend']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/manus-backend']
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: gcloud
  args: ['run', 'deploy', 'manus-backend',
         '--image', 'gcr.io/$PROJECT_ID/manus-backend',
         '--region', 'us-central1']
```

### Environment-Specific Deployments

```bash
# Development
./deploy-gcp.sh --env=dev

# Staging
./deploy-gcp.sh --env=staging

# Production
./deploy-gcp.sh --env=prod
```

---

## 🐛 Troubleshooting

### Issue: "Permission Denied"

```bash
# Grant required permissions
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/run.admin"
```

### Issue: "API Not Enabled"

```bash
# Enable all required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  containerregistry.googleapis.com secretmanager.googleapis.com
```

### Issue: "Build Timeout"

```bash
# Increase timeout
gcloud builds submit --timeout=30m
```

### Issue: "Gemini API Error"

Check API key validity:
```bash
curl -H "x-goog-api-key: AIzaSyC7pKCPc9dInPlk9u-84qi2yYOE4HuZaDE" \
  "https://generativelanguage.googleapis.com/v1beta/models"
```

---

## 📚 Additional Resources

- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [MongoDB Atlas Setup](https://docs.atlas.mongodb.com/getting-started/)
- [AI Manus Documentation](https://docs.ai-manus.com/)

---

## 🆘 Support

Need help?
- GitHub Issues: https://github.com/simpleyyt/ai-manus/issues
- QQ Group: 1005477581
- Documentation: https://docs.ai-manus.com

---

**Deployment created by Claude Code** ✨
