# 🚀 Quick Start: Deploy AI Manus to Google Cloud (5 Minutes)

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed:
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Or download: https://cloud.google.com/sdk/docs/install
   ```
3. **Your Gemini API Key**: `AIzaSyC7pKCPc9dInPlk9u-84qi2yYOE4HuZaDE`

## Deployment (One Command!)

```bash
# 1. Authenticate with Google Cloud
gcloud auth login

# 2. Run deployment script
./deploy-gcp.sh
```

### What Gets Deployed

- ✅ **Frontend**: React app on Cloud Run (auto-scaling 1-10 instances)
- ✅ **Backend**: Python/FastAPI with Gemini 2.5 Pro
- ✅ **Security**: API keys stored in Secret Manager
- ✅ **HTTPS**: Automatic SSL certificates
- ✅ **CDN**: Global content delivery

### Expected Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         Deployment Complete! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Frontend URL: https://manus-frontend-xxxxx-uc.a.run.app
✅ Backend URL: https://manus-backend-xxxxx-uc.a.run.app
✅ AI Model: Gemini 2.5 Pro (gemini-2.0-flash-exp)
```

## Post-Deployment (Optional)

### Add MongoDB (Recommended for Production)

1. Create free cluster at [MongoDB Atlas](https://cloud.mongodb.com)
2. Get connection string
3. Update secret:
   ```bash
   echo -n "YOUR_MONGODB_URI" | \
     gcloud secrets versions add mongodb-uri --data-file=-
   ```
4. Redeploy backend:
   ```bash
   gcloud run deploy manus-backend --region=us-central1
   ```

### Test Your Deployment

Visit your Frontend URL and:
1. Create an account
2. Start a conversation
3. Ask: "Search for the latest AI research papers"
4. Watch AI Manus use Gemini 2.5 Pro to complete the task!

## Cost Estimate

**Free Tier (First Month)**:
- Cloud Run: 2M requests free
- MongoDB Atlas: 512MB free forever
- **Total: $0-5/month**

**Production**:
- ~$60-100/month for moderate usage

## Troubleshooting

**"Permission denied"**
```bash
gcloud auth login
gcloud auth application-default login
```

**"API not enabled"**
Script automatically enables all required APIs. If issues persist:
```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

**"Build failed"**
Ensure Docker is running locally for image builds.

## What's Next?

- 📖 Read full guide: `DEPLOYMENT-GCP.md`
- 🔐 Configure authentication
- 🗄️ Set up production database
- 📊 Monitor at: https://console.cloud.google.com/run
- 🎨 Customize frontend
- 🔧 Add custom tools/integrations

## Support

- **GitHub**: https://github.com/simpleyyt/ai-manus/issues
- **Docs**: https://docs.ai-manus.com
- **QQ Group**: 1005477581

---

**That's it!** Your AI Agent system is now running on Google Cloud with Gemini 2.5 Pro. 🎉
