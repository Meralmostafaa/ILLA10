from main import query_documents, generate_response
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

def chatbot_response(question):
    relevant_chunks = query_documents(question)
    answer = generate_response(question, relevant_chunks)
    return answer 

@app.route('/chatbot', methods=['POST']) 
def chatbot():
    try:
        data = request.json
        question = data.get("question")
        
        if not question:
            return jsonify({"error": "No question provided."}), 400

        # Generate chatbot response
        answer = chatbot_response(question)
        
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/message_received', methods=['POST'])
def message_received():
    try:
        data = request.json
        message_id = data.get("message_id")
        conversation_id = data.get("conversation_id")
        message_text = data.get("message_text")
        
        if not message_text or not conversation_id:
            return jsonify({"error": "Missing message or conversation ID."}), 400

        # Process the message and generate a response
        response_text = chatbot_response(message_text)
        
        # Send the response back to Crisp
        send_response_to_crisp(conversation_id, response_text)
        
        return jsonify({"status": "success"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_response_to_crisp(conversation_id, response_text):
    url = f"https://api.crisp.chat/v1.0/conversations/{conversation_id}/messages"
    headers = {
        "Authorization": "Bearer YOUR_CRISP_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "text",
        "content": response_text
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from .env or default to 5000
    app.run(host='0.0.0.0', port=port)
