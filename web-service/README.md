# 🖼️ Image Optimizer Pro - Web Service

A beautiful, production-ready image optimization web service that lets users upload, compress, and download images with adjustable quality and dimensions.

## Features

- 📤 Drag & drop image upload
- 🎚️ Adjustable quality (1-100)
- 📐 Max width/height constraints
- 🖼️ Output format conversion (JPEG, PNG, WebP)
- 📊 Real-time size savings display
- 📱 Mobile responsive

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Open http://localhost:5000
```

## Deploy to Render.com (Free)

### Step 1: Prepare Your Code

```bash
# Navigate to web-service folder
cd ~/ai-side-hustles/micro-saas/web-service

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Push to GitHub

```bash
# Create a new GitHub repo, then:
git remote add origin https://github.com/YOUR_USERNAME/image-optimizer.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your repo
5. Configure:
   - **Name:** image-optimizer-pro
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Click **"Create Web Service"**

### Step 4: Wait for Deployment

- Build takes ~2-3 minutes
- First deploy is free
- Your app will be at: `https://image-optimizer-pro.onrender.com`

## How to Make Money 💰

### Option 1: Free + Paid Tier
- Free: 10 images/day, max 2MB
- Paid ($5/month): Unlimited, max 16MB, batch processing

### Option 2: API Access
- Sell API access to developers
- $10/month for 1000 API calls
- Include in documentation

### Option 3: White Label
- Customize for businesses (logo, colors)
- Charge $50-200 for setup + $20/month

### Option 4: Add More Features
- Before/after comparison slider
- Bulk upload
- AI-powered background removal
- Premium filters

## API Usage (Optional)

You can also use as a simple API:

```bash
curl -X POST https://your-app.onrender.com/optimize \
  -F "image=@photo.jpg" \
  -F "quality=75"
```

## Files

```
web-service/
├── app.py          # Main Flask application
├── requirements.txt # Python dependencies
├── Procfile        # Render deployment config
└── README.md       # This file
```

## Support

For issues or questions, open an issue on GitHub or reach out!