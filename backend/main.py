from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF
from typing import Optional, List, Dict, Union, Any
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
import logging
from httpx import HTTPStatusError

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
    topKeywords: List[str]
    presentKeywords: List[str]
    missingKeywords: List[str]
    keywordSuggestions: Dict[str, List[str]]
    alerts: List[str]
    contentFeedback: Dict[str, List[str]]
    optimizedVersion: str
    scores: Dict[str, float]
    totalScore: float
    jobMatch: Optional[Dict[str, Union[float, List[str]]]] = None

    class Config:
        arbitrary_types_allowed = True

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

    # Définition du template pour jobMatch
    job_match_template = 'null' if not job_offer else '''{
        "score": 85.5,
        "technicalMatch": 90.0,
        "experienceMatch": 80.0,
        "softSkillsMatch": 85.0,
        "strengths": [
            "Expertise technique en accord avec les besoins",
            "Expérience en management d'équipe"
        ],
        "gaps": [
            "Pas d'expérience mentionnée avec Kubernetes",
            "Certification cloud manquante"
        ],
        "recommendations": [
            "Mettre en avant votre expérience DevOps",
            "Obtenir une certification AWS/Azure"
        ]
    }'''

    # Construction du prompt en plusieurs parties
    compatibility_text = ' et sa compatibilité avec l\'offre d\'emploi' if job_offer else ''
    prompt_header = f"Tu es un expert ATS qui analyse les CV. Fais une analyse approfondie de ce CV{compatibility_text}.\n\n"
    prompt_header += "CV à analyser :\n"
    prompt_header += cv_text + "\n\n"
    
    if job_offer:
        prompt_header += "Offre d'emploi à analyser :\n"
        prompt_header += job_offer + "\n\n"

    prompt_instructions = """Réalise l'analyse suivante :

1. MOTS-CLÉS (40 mots-clés essentiels)
   - Liste les 40 mots-clés les plus importants pour ce type de poste
   - Identifie ceux présents dans le CV
   - Identifie ceux manquants
   - Suggère des formulations alternatives pour les mots-clés manquants

2. STRUCTURE ET FORMAT
   - Vérifie la présence et la clarté du titre
   - Analyse la hiérarchie des sections
   - Vérifie la cohérence du formatage
   - Identifie les éventuels problèmes de mise en page

3. LISIBILITÉ ATS
   - Détecte les abréviations à expliciter
   - Identifie les éléments potentiellement illisibles
   - Vérifie la compatibilité du format avec les ATS

4. CONTENU ET IMPACT
   - Évalue la pertinence des expériences décrites
   - Vérifie la présence de résultats quantifiables
   - Analyse l'utilisation de verbes d'action
   - Identifie les réalisations clés"""

    prompt_compatibility = """5. ANALYSE DE COMPATIBILITÉ AVEC L'OFFRE
   - Évalue la correspondance technique (technologies, outils)
   - Analyse l'adéquation de l'expérience
   - Vérifie la correspondance des soft skills
   - Identifie les points forts et les écarts
   - Propose des recommandations spécifiques""" if job_offer else "5. NOTATION DÉTAILLÉE"

    prompt_important = """
IMPORTANT : 
- Le score total doit être sur 20 points maximum
- Chaque score individuel doit être sur 5 points maximum
- Les scores de compatibilité doivent être en pourcentage (0-100%)"""

    response_format = {
        "hasTitle": True,
        "titleFeedback": "Le titre est clair et bien visible",
        "hasGoodStructure": True,
        "structureFeedback": "La structure est bien organisée",
        "topKeywords": ["mot1", "mot2", "mot3"],
        "presentKeywords": ["mot1", "mot3"],
        "missingKeywords": ["mot2", "mot4"],
        "keywordSuggestions": {
            "mot_manquant1": ["alternative1", "alternative2"],
            "mot_manquant2": ["alternative1", "alternative2"]
        },
        "alerts": [
            "Attention aux abréviations",
            "Suggestion d'amélioration 1"
        ],
        "contentFeedback": {
            "points_forts": ["point1", "point2", "point3"],
            "points_amelioration": ["suggestion1", "suggestion2"]
        },
        "optimizedVersion": "Version optimisée du CV\n avec des retours à la ligne\n",
        "scores": {
            "titre": 4.5,
            "structure": 4.0,
            "mots_cles": 3.5,
            "lisibilite": 4.0,
            "impact_contenu": 4.2
        },
        "totalScore": 16.0,
        "jobMatch": json.loads(job_match_template)
    }

    prompt_format = f"\nFormat STRICT de réponse :\n{json.dumps(response_format, indent=2, ensure_ascii=False)}"

    # Assemblage du prompt final
    prompt = "\n".join([
        prompt_header,
        prompt_instructions,
        prompt_compatibility,
        prompt_important,
        prompt_format
    ])

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
            
            # Vérification et limitation du score total
            if "totalScore" in analysis_result:
                analysis_result["totalScore"] = min(20.0, float(analysis_result["totalScore"]))
            
            # Vérification des scores individuels
            if "scores" in analysis_result:
                for key in analysis_result["scores"]:
                    analysis_result["scores"][key] = min(5.0, float(analysis_result["scores"][key]))

            # Vérification des scores de compatibilité seulement si jobMatch existe et n'est pas null
            if job_offer and analysis_result.get("jobMatch"):
                if isinstance(analysis_result["jobMatch"], (int, float)):
                    # Si jobMatch est un nombre, le convertir en structure complète
                    score = float(analysis_result["jobMatch"])
                    analysis_result["jobMatch"] = {
                        "score": min(100.0, score),
                        "technicalMatch": min(100.0, score),
                        "experienceMatch": min(100.0, score),
                        "softSkillsMatch": min(100.0, score),
                        "strengths": [],
                        "gaps": [],
                        "recommendations": []
                    }
                elif isinstance(analysis_result["jobMatch"], dict):
                    # Si jobMatch est un dictionnaire, limiter les scores à 100
                    for key in ["score", "technicalMatch", "experienceMatch", "softSkillsMatch"]:
                        if key in analysis_result["jobMatch"]:
                            analysis_result["jobMatch"][key] = min(100.0, float(analysis_result["jobMatch"][key]))
            else:
                # Si pas d'offre d'emploi ou jobMatch est null
                analysis_result["jobMatch"] = None

            # Autres vérifications...
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

    except HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Limite de requêtes atteinte. Veuillez réessayer dans quelques minutes."
            )
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de l'analyse"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur inattendue est survenue"
        ) 