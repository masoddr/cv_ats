# 📝 Optimise-ton-CV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-%2335495e.svg?style=flat&logo=vuedotjs&logoColor=%234FC08D)](https://vuejs.org/)
[![Nuxt](https://img.shields.io/badge/Nuxt-002E3B?style=flat&logo=nuxtdotjs&logoColor=#00DC82)](https://nuxt.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-%2338B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

Application web qui analyse et optimise automatiquement les CV pour les systèmes ATS (Applicant Tracking Systems) en utilisant l'intelligence artificielle.

🌐 [Voir la démo](https://optimise-ton-cv.fr)

## ✨ Fonctionnalités

- 📊 Analyse complète du CV avec notation détaillée
- 🔍 Détection des mots-clés importants
- 🎯 Compatibilité avec les offres d'emploi
- 💡 Suggestions d'amélioration personnalisées
- 📝 Export du CV optimisé
- 🌙 Mode sombre

## 🛠️ Technologies

- **Backend**: FastAPI + Groq API (LLaMA)
- **Frontend**: Nuxt.js 3 + Vue.js 3
- **Styles**: Tailwind CSS
- **Infrastructure**: Docker + Traefik

## 🚀 Installation

1. Clonez le repository :
```bash
git clone https://github.com/masoddr/cv_ats.git
cd cv_ats
```

2. Créez un fichier `.env` dans le dossier `backend` :
```env
GROQ_API_KEY=votre_clé_api_groq
```

3. Lancez avec Docker Compose :
```bash
docker-compose up -d
```

L'application sera disponible sur `http://localhost:3002`

## 📖 Documentation

### Structure du projet
```
cv_ATS/
├── backend/         # API FastAPI
├── frontend/        # Application Nuxt.js
├── docker/          # Configurations Docker
└── docs/           # Documentation
```

### API Endpoints

- `POST /api/analyze-cv` : Analyse un CV
  - Accepte du texte ou un fichier PDF
  - Retourne une analyse détaillée

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amélioration`)
3. Commit vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Push sur la branche (`git push origin feature/amélioration`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Massyl OUADDOUR**
- 📧 Email : ouaddour.massyl@gmail.com
- 🌐 LinkedIn : [Massyl Ouaddour](https://www.linkedin.com/in/massylouaddour/)

## 🙏 Remerciements

- [Groq](https://groq.com/) pour leur API performante
- [Meta AI](https://ai.meta.com/) pour le modèle LLaMA
- La communauté open source pour leurs contributions inestimables 
