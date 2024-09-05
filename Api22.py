from main import query_documents
from main import generate_response
from flask import Flask, request, jsonify
import os

#CHATTRACE_TOKEN = "1535842.PGZdZtgv2JnlbgTL0922Zrleq21txrhyf"

def chatbot_response(question):
    relevant_chunks = query_documents(question)
    answer = generate_response(question, relevant_chunks)
    return answer 

app = Flask(__name__)

@app.route('/chatbot', methods=['POST']) 
def chatbot():

    #token = request.headers.get('Authorization')
    #if token != f"Bearer {CHATTRACE_TOKEN}":
        #return jsonify({"error": "Unauthorized access"}), 403

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from .env or default to 5000
    app.run(host='0.0.0.0', port=port)
