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

    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')

    cloudinary.config(
      cloud_name = cloud_name,  
      api_key = api_key,  
      api_secret = api_secret  
    )

    try:
        upload_result = cloudinary.uploader.upload(url, resource_type="video")
        width = upload_result['width']
        height = upload_result['height']

        # Do two transformations
        result_anticlockwise = cloudinary.uploader.upload(url, resource_type="video", angle=-90) if width > height else upload_result
        result_clockwise = cloudinary.uploader.upload(url, resource_type="video", angle=90) if width > height else upload_result

        https_url_anticlockwise = result_anticlockwise['url'].replace("http://", "https://")
        https_url_clockwise = result_clockwise['url'].replace("http://", "https://")

        return {'transformedUrlAnticlockwise': https_url_anticlockwise, 'transformedUrlClockwise': https_url_clockwise}
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
