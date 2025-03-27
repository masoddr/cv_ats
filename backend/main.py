from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF
from typing import Optional
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
import logging

# Chargement des variables d'environnement
load_dotenv()

# Vérification de la présence de la clé API
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")

# Initialisation du client OpenAI avec l'API Groq
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration CORS plus détaillée avec logs
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",  # Ajout de votre port 3001
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CVAnalysisResponse(BaseModel):
    hasTitle: bool
    titleFeedback: str
    hasGoodStructure: bool
    structureFeedback: str
    missingKeywords: list[str]
    alerts: list[str]
    optimizedVersion: str

@app.post("/analyze-cv", response_model=CVAnalysisResponse)
async def analyze_cv(
    request: Request,
    file: Optional[UploadFile] = File(None),
    cv_content: Optional[str] = Form(None),
    job_offer: Optional[str] = Form(None)
):
    logger.info(f"Requête reçue - Origin: {request.headers.get('origin')}")
    logger.info(f"Headers reçus: {request.headers}")
    
    # Récupération du contenu du CV
    if file:
        # Lecture du PDF
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        cv_text = ""
        for page in doc:
            cv_text += page.get_text()
    else:
        cv_text = cv_content if cv_content else ""

    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="CV content is required")

    # Construction du prompt
    prompt = f"""Tu es un expert ATS qui analyse les CV. Analyse ce CV et réponds UNIQUEMENT en JSON valide selon le format spécifié.

CV à analyser :
{cv_text}

{f'Offre d\'emploi :\n{job_offer}\n' if job_offer else ''}

IMPORTANT: La version optimisée doit être une chaîne de caractères avec des retours à la ligne \\n.

Format STRICT de réponse (exemple) :
{{
    "hasTitle": true,
    "titleFeedback": "Le titre est clair et bien visible",
    "hasGoodStructure": true,
    "structureFeedback": "La structure est bien organisée avec des sections distinctes",
    "missingKeywords": ["java", "agile", "scrum"],
    "alerts": ["Attention aux abréviations comme API"],
    "optimizedVersion": "John Doe\\nDéveloppeur Full Stack Senior\\n\\nEXPÉRIENCE PROFESSIONNELLE\\n..."
}}

Assure-toi que :
1. La réponse est un JSON valide
2. optimizedVersion est une chaîne de caractères avec des \\n pour les retours à la ligne
3. Pas de texte avant ou après le JSON"""

    try:
        # Appel à l'API via le client OpenAI
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "system",
                "content": "Tu es un expert ATS qui répond uniquement en JSON valide. La version optimisée du CV doit être une chaîne de caractères avec des retours à la ligne \\n."
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=4000
        )

        # Parsing de la réponse
        response_content = completion.choices[0].message.content.strip()
        
        # Debug: afficher la réponse brute
        print("Réponse brute de l'API :", response_content)
        
        # Nettoyage supplémentaire pour s'assurer que c'est du JSON valide
        if response_content.startswith("```json"):
            response_content = response_content.replace("```json", "").replace("```", "")
        
        response_content = response_content.strip()
        
        try:
            analysis_result = json.loads(response_content)
            # Vérification supplémentaire
            if not isinstance(analysis_result["optimizedVersion"], str):
                raise HTTPException(
                    status_code=500,
                    detail="optimizedVersion must be a string"
                )
            logger.info("Analyse du CV réussie")
            return CVAnalysisResponse(**analysis_result)
        except json.JSONDecodeError as e:
            print(f"Contenu de la réponse : {response_content}")
            raise HTTPException(
                status_code=500,
                detail=f"Error parsing JSON response: {str(e)}"
            )

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during CV analysis: {str(e)}"
        ) 