# Micro-SaaS Starter Kit

3 simple Python tools for passive income on Render.com free tier.

## Tools

### 1. URL Shortener with AI Summarization
- Shortens URLs with unique codes
- Generates AI summary of target pages
- In-memory storage (upgrade to Redis for production)

### 2. Image Optimizer ⭐ (Ready to Deploy)
- Compress images (JPEG/PNG/WebP)
- Resize to max dimensions
- CLI interface with quality control
- **Web UI ready** → Deploy to Render.com and start charging!

### 3. JSON Formatter/Validator
- Pretty-print JSON
- Validate JSON syntax
- Minify JSON

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Requirements

```
# requirements.txt
Pillow>=10.0.0
requests>=2.31.0
```

## Local Testing

```bash
# URL Shortener
python tools/url_shortener.py shorten --url https://example.com
python tools/url_shortener.py resolve --code abc123
python tools/url_shortener.py list

# Image Optimizer
python tools/image_optimizer.py photo.jpg -q 80 -w 800 -o photo_small.jpg

# JSON Tool
python tools/json_tool.py data.json -i 4
python tools/json_tool.py data.json --minify
python tools/json_tool.py data.json --validate
echo '{"a":1}' | python tools/json_tool.py -
```

---

## Deploy on Render.com (Free Tier)

### Option A: Web Service (for URL Shortener)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   # Push to GitHub repository
   ```

2. **Create Render Web Service**
   - Go to [render.com](https://render.com) → New → Web Service
   - Connect GitHub repo
   - Settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python tools/url_shortener.py` (or create web wrapper)
     - Free Instance Type

3. **Add Environment Variables**
   - `PYTHON_VERSION: 3.11`
   - Optional: `OPENAI_API_KEY` (for real AI summaries)

### Option B: Background Worker (for Image Optimizer)

For image processing, use a **Background Service**:
1. Create new → Background Service
2. Upload your tool
3. Use Cloud Storage (AWS S3, Cloudinary) for file I/O

### Option C: Cron Job (for JSON Tool)

For scheduled JSON processing:
1. Create new → Cron Job
2. Set schedule (e.g., `*/5 * * * *`)
3. Run: `python tools/json_tool.py input.json --output result.json`

## Production Tips

1. **URL Shortener**: Add Redis for persistence, use real AI API
2. **Image Optimizer**: Integrate Cloudinary/AWS S3 for file storage
3. **JSON Tool**: Can be called via webhooks from other services

## License

MIT