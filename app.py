herefrom flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running successfully!"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json() or {}
    keyword = data.get('keyword', 'مطاعم')
    
    results = [
        {"name": "نتيجة تجريبية 1", "phone": "+201000000001"},
        {"name": "نتيجة تجريبية 2", "phone": "+201000000002"}
    ]
    
    return jsonify({"status": "success", "keyword": keyword, "data": results})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
