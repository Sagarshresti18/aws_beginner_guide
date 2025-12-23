from flask import Flask, render_template, request, jsonify
import boto3
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Connect to AWS DynamoDB
print("🔄 Connecting to AWS...")
try:
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_DEFAULT_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    table = dynamodb.Table('UserInputs')
    print("✅ Connected to DynamoDB successfully!")
except Exception as e:
    print(f"❌ Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        user_name = data.get('user_name')
        user_number = data.get('user_number')
        user_photo = data.get('user_photo')

        if not user_name or not user_number or not user_photo:
            return jsonify({"message": "All fields are required"}), 400

        # Save to DynamoDB
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'name': user_name,
                'number': int(user_number),
                'photo': user_photo,  # Base64 encoded image
                'timestamp': datetime.now().isoformat()
            }
        )

        return jsonify({"message": "✅ Data with photo stored successfully in AWS!"})
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/view-all')
def view_all():
    try:
        # Get all items from DynamoDB
        response = table.scan()
        items = response['Items']
        
        return render_template('view_all.html', items=items)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    app.run(debug=True)