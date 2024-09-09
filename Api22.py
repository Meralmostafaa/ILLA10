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
    print("this is nessage received")
    try:
        response = request.json
        content = response.get("data").get("content")
        #conversation_id = data.get("conversation_id")
        #message_text = data.get("message_text")
        print(f"content is: {content}")
       

        # Process the message and generate a response
        response_text = chatbot_response(content)
        print(f"response: {response_text}")
        
        # Send the response back to Crisp
        #send_response_to_crisp(conversation_id, response_text)
        
        return jsonify({"status": "success", "content":content, "our response": response_text}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_response_to_crisp(conversation_id, response_text):
    url = f"https://api.crisp.chat/v1.0/conversations/{conversation_id}/messages"
    headers = {
        "Authorization": "NzE2ZmM3YjktOTI4ZC00MDFkLWEwOTYtMTBkY2FiZmZjZDE5OmYxOTczZjljLTlhMzctNDE3ZS05NmU2LWIzMzMwM2I0OGFkZQ==",
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
