from flask import Flask, request, jsonify
from flask_cors import CORS  # Handle Cross-Origin Requests
from chatbot import get_chatbot_response  # Import your chatbot function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get user message from request
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get response from your chatbot
        bot_response = get_chatbot_response(user_message)
        
        return jsonify({
            'reply': bot_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)