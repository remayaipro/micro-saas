#!/usr/bin/env python3
"""Image Optimizer Web Service - Flask API"""

import os
import uuid
import tempfile
from flask import Flask, request, send_file, jsonify, render_template_string
from PIL import Image

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Optimizer Pro</title>
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
            max-width: 500px;
            width: 100%;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        }
        h1 { color: #1a1a2e; margin-bottom: 10px; text-align: center; }
        .tagline { color: #666; text-align: center; margin-bottom: 30px; }
        
        .upload-area {
            border: 3px dashed #ddd;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        .upload-area:hover { border-color: #4f46e5; background: #f8f9fa; }
        .upload-area.dragover { border-color: #4f46e5; background: #eef2ff; }
        
        .file-input { display: none; }
        .upload-icon { font-size: 48px; margin-bottom: 10px; }
        
        .options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        .option-group { display: flex; flex-direction: column; }
        .option-group label { font-size: 12px; color: #666; margin-bottom: 5px; }
        .option-group input, .option-group select {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
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
            margin-top: 20px;
            padding: 20px;
            background: #f0fdf4;
            border-radius: 10px;
            display: none;
        }
        .result.show { display: block; }
        .result-img {
            width: 100%;
            max-height: 300px;
            object-fit: contain;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            text-align: center;
        }
        .stat { padding: 10px; background: white; border-radius: 8px; }
        .stat-value { font-size: 18px; font-weight: bold; color: #1a1a2e; }
        .stat-label { font-size: 11px; color: #666; }
        .savings { color: #16a34a; font-weight: bold; }
        
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
        
        .error {
            background: #fef2f2;
            color: #dc2626;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
        .error.show { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Image Optimizer</h1>
        <p class="tagline">Compress images without losing quality</p>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <p>Drop image here or click to upload</p>
            <p style="font-size: 12px; color: #999; margin-top: 5px;">PNG, JPG up to 16MB</p>
        </div>
        <input type="file" class="file-input" id="fileInput" accept="image/*">
        
        <div class="options">
            <div class="option-group">
                <label>Quality (1-100)</label>
                <input type="number" id="quality" value="75" min="1" max="100">
            </div>
            <div class="option-group">
                <label>Max Width (px)</label>
                <input type="number" id="maxWidth" placeholder="Optional">
            </div>
            <div class="option-group">
                <label>Max Height (px)</label>
                <input type="number" id="maxHeight" placeholder="Optional">
            </div>
            <div class="option-group">
                <label>Output Format</label>
                <select id="format">
                    <option value="original">Keep Original</option>
                    <option value="jpeg">JPEG</option>
                    <option value="png">PNG</option>
                    <option value="webp">WebP</option>
                </select>
            </div>
        </div>
        
        <button class="btn" id="optimizeBtn" onclick="optimizeImage()">Optimize Image</button>
        
        <div class="error" id="error"></div>
        
        <div class="result" id="result">
            <img class="result-img" id="resultImg" src="" alt="Optimized">
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="originalSize">-</div>
                    <div class="stat-label">Original</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="optimizedSize">-</div>
                    <div class="stat-label">Optimized</div>
                </div>
                <div class="stat">
                    <div class="stat-value savings" id="savings">-</div>
                    <div class="stat-label">Saved</div>
                </div>
            </div>
            <a class="download-btn" id="downloadBtn" href="" download>Download Optimized Image</a>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFileSelect();
            }
        });
        
        fileInput.addEventListener('change', handleFileSelect);
        
        function handleFileSelect() {
            if (fileInput.files.length) {
                uploadArea.innerHTML = '<div class="upload-icon">✅</div><p>' + fileInput.files[0].name + '</p>';
            }
        }
        
        async function optimizeImage() {
            if (!fileInput.files.length) {
                showError('Please select an image first');
                return;
            }
            
            const btn = document.getElementById('optimizeBtn');
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('quality', document.getElementById('quality').value);
            formData.append('max_width', document.getElementById('maxWidth').value);
            formData.append('max_height', document.getElementById('maxHeight').value);
            formData.append('format', document.getElementById('format').value);
            
            btn.disabled = true;
            btn.textContent = 'Optimizing...';
            hideError();
            
            try {
                const response = await fetch('/optimize', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Optimization failed');
                }
                
                document.getElementById('resultImg').src = data.download_url + '?t=' + Date.now();
                document.getElementById('originalSize').textContent = formatSize(data.original_size);
                document.getElementById('optimizedSize').textContent = formatSize(data.optimized_size);
                document.getElementById('savings').textContent = data.savings + '%';
                document.getElementById('downloadBtn').href = data.download_url;
                document.getElementById('result').classList.add('show');
                
            } catch (err) {
                showError(err.message);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Optimize Image';
            }
        }
        
        function formatSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + ' KB';
            return (bytes/(1024*1024)).toFixed(2) + ' MB';
        }
        
        function showError(msg) {
            const el = document.getElementById('error');
            el.textContent = msg;
            el.classList.add('show');
        }
        
        function hideError() {
            document.getElementById('error').classList.remove('show');
        }
    </script>
</body>
</html>
'''

def optimize_image_file(input_path, quality=75, max_width=None, max_height=None, output_format=None):
    """Optimize image and return output path"""
    
    filename = str(uuid.uuid4())
    
    try:
        with Image.open(input_path) as img:
            # Handle RGBA to RGB for JPEG
            if img.mode in ('RGBA', 'LA') and (not output_format or output_format in ('jpeg', 'original')):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Resize if needed
            if max_width or max_height:
                width, height = img.size
                new_width, new_height = width, height
                
                if max_width and width > max_width:
                    ratio = max_width / width
                    new_width = max_width
                    new_height = int(height * ratio)
                
                if max_height and new_height > max_height:
                    ratio = max_height / new_height
                    new_height = max_height
                    new_width = int(new_width * ratio)
                
                if new_width != width or new_height != height:
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Determine format
            ext = 'jpg'
            if output_format and output_format != 'original':
                ext = output_format
            elif input_path.lower().endswith('.png'):
                ext = 'png'
            elif input_path.lower().endswith('.webp'):
                ext = 'webp'
            
            output_path = os.path.join(UPLOAD_FOLDER, f"{filename}.{ext}")
            
            save_kwargs = {'quality': quality, 'optimize': True}
            
            if ext == 'png':
                img.save(output_path, 'PNG', **save_kwargs)
            elif ext == 'webp':
                img.save(output_path, 'WEBP', quality=quality, optimize=True)
            else:
                img.save(output_path, 'JPEG', **save_kwargs)
            
            return output_path
            
    except Exception as e:
        raise Exception(f"Failed to optimize image: {str(e)}")


@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/optimize', methods=['POST'])
def optimize():
    """Handle image optimization request"""
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    
    if not image_file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    quality = int(request.form.get('quality', 75))
    max_width = request.form.get('max_width')
    max_height = request.form.get('max_height')
    output_format = request.form.get('format', 'original')
    
    if max_width:
        max_width = int(max_width)
    if max_height:
        max_height = int(max_height)
    
    # Save uploaded file
    input_filename = str(uuid.uuid4()) + '_' + image_file.filename
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    image_file.save(input_path)
    
    try:
        # Optimize
        output_path = optimize_image_file(
            input_path, quality, max_width, max_height, output_format
        )
        
        original_size = os.path.getsize(input_path)
        optimized_size = os.path.getsize(output_path)
        savings = round(((original_size - optimized_size) / original_size) * 100, 1)
        
        return jsonify({
            'success': True,
            'download_url': f'/download/{os.path.basename(output_path)}',
            'original_size': original_size,
            'optimized_size': optimized_size,
            'savings': savings
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up input
        if os.path.exists(input_path):
            os.remove(input_path)


@app.route('/download/<filename>')
def download(filename):
    """Serve optimized image"""
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)