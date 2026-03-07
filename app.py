from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

app = Flask(__name__)

# Configure l'API Google avec ta clé
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("ERREUR: GOOGLE_API_KEY non trouvée dans .env")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

# Charge la FAQ depuis le fichier JSON
def load_faq():
    try:
        with open('faq.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['faq']
    except FileNotFoundError:
        print("ERREUR: faq.json non trouvé")
        return []

faq = load_faq()

# Formate la FAQ pour l'envoyer à l'API
def format_faq_for_prompt():
    faq_text = "Voici la FAQ de notre entreprise:\n\n"
    for item in faq:
        faq_text += f"Q: {item['question']}\nA: {item['answer']}\n\n"
    return faq_text

# Route 1 : Affiche la page d'accueil
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route 2 : Reçoit une question et retourne une réponse basée sur la FAQ
@app.route('/ask', methods=['POST'])
def ask_chatbot():
    try:
        # Récupère la question envoyée par le navigateur
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'answer': 'Veuillez poser une question'}), 400
        
        # Prépare le prompt avec la FAQ
        faq_context = format_faq_for_prompt()
        prompt = f"""{faq_context}
        
L'utilisateur pose la question suivante: {question}

Réponds à cette question basé uniquement sur la FAQ ci-dessus. Si la réponse n'est pas dans la FAQ, dis poliment que tu ne sais pas."""
        
        # Appelle l'API Google
        response = model.generate_content(prompt)
        answer = response.text
        
        # Retourne la réponse
        return jsonify({'answer': answer})
    
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        return jsonify({'answer': f'Erreur: {str(e)}'}), 500

# Route 3 : Vérifie que le serveur marche
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Serveur OK'})

# Route 4 (optionnel) : Retourne la FAQ complète
@app.route('/faq', methods=['GET'])
def get_faq():
    return jsonify({'faq': faq})

if __name__ == '__main__':
    app.run(debug=True, port=5000)