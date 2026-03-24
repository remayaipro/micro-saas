/**
 * AI Image Generator using Cloudflare Workers AI
 * Model: FLUX.2 [klein] 9B
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET") {
      return new Response(html, {
        headers: { "Content-Type": "text/html" }
      });
    }

    if (request.method === "POST") {
      return await handleGenerate(request, env);
    }

    return new Response("Method not allowed", { status: 405 });
  }
};

async function handleGenerate(request, env) {
  try {
    const formData = await request.formData();
    const prompt = formData.get("prompt");
    const width = parseInt(formData.get("width") || "1024");
    const height = parseInt(formData.get("height") || "1024");

    if (!prompt) {
      return jsonError("Please enter a prompt");
    }

    const accountId = "ba4047b60c7a96d74233b69c46831a61";
    const apiToken = env.CF_API_TOKEN || "cfat_iYnIArpG1S1p1ejLNkN9JoFf94T8weVbBH8IfcUHef5691f5";

    const form = new FormData();
    form.append('prompt', prompt);
    form.append('width', width.toString());
    form.append('height', height.toString());

    const formResponse = new Response(form);
    const stream = formResponse.body;
    const contentType = formResponse.headers.get('content-type');

    const response = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${accountId}/ai/run/@cf/black-forest-labs/flux-2-klein-9b`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiToken}`,
          'Content-Type': contentType
        },
        body: stream
      }
    );

    const result = await response.json();

    if (!result.success) {
      return jsonError(result.errors?.[0]?.message || 'AI generation failed');
    }

    return JSON.stringify({
      success: true,
      image: `data:image/png;base64,${result.result.image}`
    });

  } catch (e) {
    return jsonError(e.message);
  }
}

function jsonError(msg) {
  return new Response(JSON.stringify({ error: msg }), {
    status: 400,
    headers: { "Content-Type": "application/json" }
  });
}

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Image Generator</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .container {
      background: white;
      border-radius: 20px;
      padding: 40px;
      max-width: 600px;
      width: 100%;
      box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    h1 { color: #1a1a2e; margin-bottom: 5px; text-align: center; }
    .tagline { color: #666; text-align: center; margin-bottom: 30px; font-size: 14px; }
    .model-badge {
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      color: white;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      display: inline-block;
      margin-bottom: 20px;
    }
    .input-group { margin-bottom: 20px; }
    .input-group label { 
      display: block; 
      font-size: 12px; 
      color: #666; 
      margin-bottom: 8px; 
    }
    textarea {
      width: 100%;
      padding: 15px;
      border: 2px solid #e5e7eb;
      border-radius: 12px;
      font-size: 14px;
      resize: vertical;
      min-height: 80px;
      font-family: inherit;
    }
    textarea:focus { outline: none; border-color: #4f46e5; }
    .options {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-bottom: 20px;
    }
    .option-group label { 
      display: block; 
      font-size: 12px; 
      color: #666; 
      margin-bottom: 8px; 
    }
    .option-group select, .option-group input {
      width: 100%;
      padding: 10px;
      border: 2px solid #e5e7eb;
      border-radius: 8px;
      font-size: 14px;
      background: white;
    }
    .btn {
      width: 100%;
      padding: 15px;
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .btn:hover { transform: translateY(-2px); }
    .btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .result {
      margin-top: 30px;
      display: none;
    }
    .result.show { display: block; }
    .result-img {
      width: 100%;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .download-btn {
      display: block;
      width: 100%;
      padding: 12px;
      background: #16a34a;
      color: white;
      text-align: center;
      text-decoration: none;
      border-radius: 8px;
      margin-top: 15px;
      font-weight: 600;
    }
    .loading {
      text-align: center;
      padding: 40px;
      color: #666;
    }
    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid #e5e7eb;
      border-top-color: #4f46e5;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 15px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .error {
      background: #fef2f2;
      color: #dc2626;
      padding: 15px;
      border-radius: 8px;
      margin-top: 15px;
    }
    .pricing {
      font-size: 11px;
      color: #999;
      text-align: center;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div style="text-align: center;">
      <span class="model-badge">FLUX.2 [klein] 9B</span>
    </div>
    <h1>🎨 AI Image Generator</h1>
    <p class="tagline">Create stunning images with AI</p>
    
    <div class="input-group">
      <label>Describe your image</label>
      <textarea id="prompt" placeholder="A serene sunset over mountains with pink clouds..."></textarea>
    </div>
    
    <div class="options">
      <div class="option-group">
        <label>Width</label>
        <select id="width">
          <option value="512">512px</option>
          <option value="768">768px</option>
          <option value="1024" selected>1024px</option>
          <option value="1536">1536px</option>
        </select>
      </div>
      <div class="option-group">
        <label>Height</label>
        <select id="height">
          <option value="512">512px</option>
          <option value="768">768px</option>
          <option value="1024" selected>1024px</option>
          <option value="1536">1536px</option>
        </select>
      </div>
    </div>
    
    <button class="btn" id="generateBtn" onclick="generateImage()">Generate Image</button>
    
    <div class="error" id="error" style="display: none;"></div>
    
    <div class="result" id="result">
      <img class="result-img" id="resultImg" src="" alt="Generated Image">
      <a class="download-btn" id="downloadBtn" href="" download="ai-image.png">Download Image</a>
    </div>
    
    <p class="pricing">Pricing: $0.015/first MP, $0.002/subsequent MP</p>
  </div>

  <script>
    async function generateImage() {
      const prompt = document.getElementById('prompt').value.trim();
      if (!prompt) {
        showError('Please enter a prompt');
        return;
      }
      
      const btn = document.getElementById('generateBtn');
      const result = document.getElementById('result');
      const resultImg = document.getElementById('resultImg');
      
      btn.disabled = true;
      btn.textContent = 'Generating... (this may take up to 30s)';
      hideError();
      result.classList.remove('show');
      
      // Show loading
      result.innerHTML = '<div class="loading"><div class="spinner"></div><p>Creating your image...</p></div>';
      result.classList.add('show');
      
      try {
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('width', document.getElementById('width').value);
        formData.append('height', document.getElementById('height').value);
        
        const response = await fetch('/', { method: 'POST', body: formData });
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.error || 'Generation failed');
        
        result.innerHTML = \`
          <img class="result-img" src="\${data.image}" alt="Generated Image">
          <a class="download-btn" href="\${data.image}" download="ai-image.png">Download Image</a>
        \`;
        
      } catch (err) {
        showError(err.message);
        result.classList.remove('show');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Generate Image';
      }
    }
    
    function showError(msg) {
      const el = document.getElementById('error');
      el.textContent = msg;
      el.style.display = 'block';
    }
    
    function hideError() {
      document.getElementById('error').style.display = 'none';
    }
  </script>
</body>
</html>`;
