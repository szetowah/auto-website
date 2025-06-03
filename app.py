from flask import Flask, request, send_from_directory, jsonify
import os
import logging
import secrets

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
HTML_FILE = 'index.html'

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/generate', methods=['POST'])
def generate_site():
    try:
        data = request.get_json()
        if not data or 'html' not in data:
            logger.error('缺少 html 参数')
            return jsonify({'error': '缺少 html 参数'}), 400
        html_content = data['html']
        if not isinstance(html_content, str):
            logger.error('html 参数必须为字符串')
            return jsonify({'error': 'html 参数必须为字符串'}), 400
        hash_str = secrets.token_urlsafe(8)
        site_dir = os.path.join(STATIC_DIR, hash_str)
        os.makedirs(site_dir, exist_ok=True)
        file_path = os.path.join(site_dir, HTML_FILE)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f'网站已生成: {hash_str}')
        return jsonify({'message': '网站已生成', 'url': f'/site/{hash_str}'}), 200
    except Exception as e:
        logger.exception('生成网站时发生错误')
        return jsonify({'error': '生成网站时发生错误', 'details': str(e)}), 500

@app.route('/site/<hash_str>', methods=['GET'])
def serve_site(hash_str):
    site_dir = os.path.join(STATIC_DIR, hash_str)
    file_path = os.path.join(site_dir, HTML_FILE)
    if not os.path.exists(file_path):
        return '<h1>未找到该网站</h1>', 404
    return send_from_directory(site_dir, HTML_FILE)

@app.route('/', methods=['GET'])
def root_info():
    return '<h1>请通过 /generate 接口生成网站</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 