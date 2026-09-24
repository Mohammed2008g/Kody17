from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Google Maps Scraper API is Live!"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json() or {}
    keyword = data.get('keyword')
    
    if not keyword:
        return jsonify({"status": "error", "message": "Please provide a keyword"}), 400

    # استعلام مجاني لسحب بيانات الأماكن والأرقام
    url = f"https://nominatim.openstreetmap.org/search?q={keyword}&format=json&addressdetails=1&extratags=1"
    headers = {'User-Agent': 'n8n-scraper-app/1.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        places = response.json()
        
        results = []
        for place in places:
            extratags = place.get('extratags', {})
            phone = extratags.get('phone') or extratags.get('contact:phone') or "N/A"
            
            results.append({
                "name": place.get('display_name', '').split(',')[0],
                "full_address": place.get('display_name'),
                "phone": phone,
                "lat": place.get('lat'),
                "lon": place.get('lon')
            })
            
        return jsonify({
            "status": "success",
            "count": len(results),
            "keyword": keyword,
            "data": results
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
