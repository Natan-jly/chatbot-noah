Un projet de chatbot simple qui répond aux questions basées sur une FAQ qu'on lui donne. Utilise Flask pour le serveur et Google Gemini pour l'IA.

J'ai utilisé Flask pour le serveur en Python, l'API Google pour l'IA (gratuite), l'interface est en HTML/CSS, et du JS écrit par Claude.
La FAQ est stockée en JSON

Notes:
La clé API Google est dans .env (pas pushée sur GitHub), faut la refaire avec la vôtre (ça prend 5 minutes sur aistudio.google.com).
Elle est enregistrée sous le format suivant: GOOGLE_API_KEY="clé google
