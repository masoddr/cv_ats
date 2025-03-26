# Analyseur de CV avec IA
## 🎯 Vue d'ensemble

Application web permettant d'analyser automatiquement des CV via l'intelligence artificielle, en simulant le comportement des ATS (Applicant Tracking Systems).

## 💡 Fonctionnalités principales

- Upload de CV au format PDF
- Analyse complète du CV :
  - Lisibilité et structure
  - Détection des mots-clés importants
  - Optimisation SEO pour les recruteurs
  - Compatibilité avec une offre d'emploi (optionnel)
- Suggestions d'amélioration personnalisées
- Export du CV optimisé

## 🛠 Architecture technique

| Composant | Technologie |
|-----------|-------------|
| API Backend | FastAPI |
| Modèle IA | Groq API (Mixtral) |
| Parser PDF | PyMuPDF |
| Frontend | Nuxt 3 |
| Infrastructure | Docker + Traefik |

## 🔄 Processus d'analyse

1. **Réception du CV**
   - Upload du fichier PDF
   - Saisie optionnelle d'une offre d'emploi

2. **Extraction et validation**
   - Conversion PDF vers texte
   - Vérification du format et de la lisibilité
   - Détection des éléments problématiques

3. **Analyse IA**
   - Génération d'un prompt contextualisé
   - Appel à l'API Groq (modèle Mixtral)
   - Analyse ATS complète

4. **Présentation des résultats**
   - Score détaillé par critère
   - Recommandations d'amélioration
   - Version optimisée du CV

## 📡 API Backend

### Analyse simple