from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import re

app = Flask(__name__)
CORS(app)

def normalize_url(url):
    parts = urlparse(url.strip().lower())
    return f"{parts.scheme}://{parts.netloc}{parts.path}".rstrip('/')

def load_phishing_urls():
    try:
        with open('phishing_urls.txt', 'r', encoding='utf-8') as f:
            return set(normalize_url(line) for line in f if line.strip())
    except FileNotFoundError:
        print("❌ phishing_urls.txt not found.")
        return set()

phishing_urls = load_phishing_urls()

def uses_ip_address(url):
    parsed = urlparse(url)
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return bool(ip_pattern.match(parsed.netloc))

def suspicious_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.count('-') > 2 or any(char.isdigit() for char in domain):
        return True
    return False


def url_too_long(url, max_length=75):
    return len(url) > max_length

def has_at_symbol(url):
    return '@' in url

def is_valid_url(url):
    try:
        parts = urlparse(url)
        return parts.scheme in ('http', 'https') and parts.netloc != ''
    except:
        return False

@app.route('/check', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not is_valid_url(url):
        url = 'http://' + url
        if not is_valid_url(url):
            return jsonify({'valid': False, 'phishing': False, 'message': 'Invalid URL format'}), 400

    norm = normalize_url(url)

    
    if uses_ip_address(url):
        return jsonify({'valid': True, 'phishing': True, 'message': '⚠️ Warning: URL uses suspicious IP address!'})
    if suspicious_domain(url):
        return jsonify({'valid': True, 'phishing': True, 'message': '⚠️ Warning: Suspicious domain detected!'})
    if url_too_long(url):
        return jsonify({'valid': True, 'phishing': True, 'message': '⚠️ Warning: URL is unusually long!'})
    if has_at_symbol(url):
        return jsonify({'valid': True, 'phishing': True, 'message': '⚠️ Warning: URL contains "@" symbol!'})

    
    if norm in phishing_urls:
        return jsonify({'valid': True, 'phishing': True, 'message': '⚠️ Warning: Phishing URL detected!'})

    return jsonify({'valid': True, 'phishing': False, 'message': '✅ URL looks safe.'})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
