# main.py
from flask import Flask, request, render_template
from flask_cors import CORS
import cloudinary.uploader
import os  # Import the os module

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    url = request.json['url']
    angle = request.json.get('angle', 0)
    flip = request.json.get('flip', False)

    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')

    cloudinary.config(
      cloud_name = cloud_name,  
      api_key = api_key,  
      api_secret = api_secret  
    )

    try:
        transformations = []
        if flip:
            transformations.append({"angle": "hflip"})
        if angle != 0:
            transformations.append({"angle": angle})

        result = cloudinary.uploader.upload(url, resource_type="video", transformation=transformations)

        https_url = result['url'].replace("http://", "https://")  # Replace http with https
        return {'transformedUrl': https_url}
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
