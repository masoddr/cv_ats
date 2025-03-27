<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Hero Section -->
      <div class="text-center py-16 md:py-24">
        <h1 class="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Optimisez votre CV pour l'ère digitale
        </h1>
        <p class="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
          Notre IA analyse votre CV et vous guide pour maximiser vos chances face aux systèmes de recrutement modernes.
        </p>
        
        <!-- Stats -->
        <div class="grid grid-cols-2 md:grid-cols-3 gap-8 max-w-3xl mx-auto mb-16">
          <div class="text-center">
            <div class="text-3xl font-bold text-blue-600 mb-2">98%</div>
            <div class="text-gray-600">Taux de détection</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-indigo-600 mb-2">40+</div>
            <div class="text-gray-600">Mots-clés analysés</div>
          </div>
          <div class="text-center hidden md:block">
            <div class="text-3xl font-bold text-purple-600 mb-2">2min</div>
            <div class="text-gray-600">Temps d'analyse</div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="bg-white rounded-2xl shadow-xl p-8 mb-16 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent opacity-50"></div>
          
          <!-- Import Tabs -->
          <div class="relative">
            <div class="flex justify-center space-x-4 mb-8">
              <button 
                @click="importMode = 'text'"
                :class="[
                  'px-6 py-3 rounded-full text-sm font-medium transition-all duration-200',
                  importMode === 'text' 
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-200'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                ]"
              >
                Copier-coller
              </button>
              <button 
                @click="importMode = 'file'"
                :class="[
                  'px-6 py-3 rounded-full text-sm font-medium transition-all duration-200',
                  importMode === 'file' 
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-200'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                ]"
              >
                Upload PDF
              </button>
            </div>

            <!-- Import Content -->
            <div class="max-w-3xl mx-auto">
              <div v-if="importMode === 'text'" class="mb-6">
                <textarea
                  v-model="cvContent"
                  rows="12"
                  class="w-full px-6 py-4 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none shadow-sm transition-all duration-200"
                  placeholder="Copiez-collez le texte de votre CV ici..."
                ></textarea>
              </div>

              <div v-else class="mb-6">
                <div 
                  class="border-2 border-dashed border-gray-200 rounded-xl p-12 text-center hover:border-blue-500 transition-all duration-200 cursor-pointer bg-gray-50"
                  @dragover.prevent
                  @drop.prevent="handleFileDrop"
                  @click="$refs.fileInput.click()"
                >
                  <input
                    ref="fileInput"
                    type="file"
                    accept=".pdf"
                    class="hidden"
                    @change="handleFileSelect"
                  >
                  <div v-if="selectedFile">
                    <div class="text-blue-600 font-medium mb-2">{{ selectedFile.name }}</div>
                    <button 
                      @click.stop="selectedFile = null"
                      class="text-red-500 text-sm hover:text-red-600"
                    >
                      Supprimer
                    </button>
                  </div>
                  <div v-else>
                    <div class="mx-auto w-16 h-16 mb-4 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
                      <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <p class="text-gray-600 mb-1">Glissez votre fichier ici ou cliquez pour sélectionner</p>
                    <p class="text-gray-400 text-sm">Format PDF uniquement</p>
                  </div>
                </div>
              </div>

              <!-- Job Offer Input -->
              <div class="mb-8">
                <textarea
                  v-model="jobOffer"
                  rows="4"
                  class="w-full px-6 py-4 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none shadow-sm transition-all duration-200"
                  placeholder="Pour une analyse plus pertinente, collez l'offre d'emploi ici (optionnel)..."
                ></textarea>
              </div>

              <!-- Analyze Button -->
              <button
                @click="analyzeCV"
                :disabled="!canAnalyze || isAnalyzing"
                class="w-full md:w-auto px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-200/50 hover:shadow-xl hover:shadow-blue-300/50 transform hover:-translate-y-0.5"
              >
                <span v-if="isAnalyzing" class="flex items-center justify-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyse en cours...
                </span>
                <span v-else>Analyser mon CV</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Results Section -->
        <div v-if="analysisResults" class="bg-white p-6 rounded-xl shadow-lg animate-fadeIn">
          <h2 class="text-2xl font-bold mb-6 text-gray-800">Résultats de l'analyse</h2>
          
          <!-- Format et Structure -->
          <div class="mb-8">
            <div class="flex items-center mb-4">
              <h3 class="text-xl font-semibold text-gray-700">Format et Structure</h3>
              <div class="relative ml-2 group">
                <span class="cursor-help text-gray-400 hover:text-gray-600">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                  </svg>
                </span>
                <div class="opacity-0 group-hover:opacity-100 transition-opacity bg-gray-800 text-sm text-white rounded-md absolute z-10 px-4 py-2 w-64 bottom-full left-1/2 transform -translate-x-1/2 -translate-y-2">
                  La structure de votre CV est cruciale pour les systèmes ATS.
                  <div class="absolute w-2 h-2 bg-gray-800 transform rotate-45 left-1/2 -translate-x-1/2 -bottom-1"></div>
                </div>
              </div>
            </div>

            <!-- Titre et Structure -->
            <div class="space-y-4">
              <div class="flex items-start">
                <div :class="analysisResults.hasTitle ? 'text-green-500' : 'text-red-500'" class="mr-2 mt-1">
                  {{ analysisResults.hasTitle ? '✓' : '✗' }}
                </div>
                <div>
                  <p class="font-medium">Titre</p>
                  <p class="text-gray-600 text-sm">{{ analysisResults.titleFeedback }}</p>
                </div>
              </div>
              
              <div class="flex items-start">
                <div :class="analysisResults.hasGoodStructure ? 'text-green-500' : 'text-red-500'" class="mr-2 mt-1">
                  {{ analysisResults.hasGoodStructure ? '✓' : '✗' }}
                </div>
                <div>
                  <p class="font-medium">Structure</p>
                  <p class="text-gray-600 text-sm">{{ analysisResults.structureFeedback }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Mots-clés manquants -->
          <div v-if="analysisResults.missingKeywords.length" class="mb-8">
            <div class="flex items-center mb-4">
              <h3 class="text-xl font-semibold text-gray-700">Mots-clés manquants</h3>
              <div class="relative ml-2 group">
                <span class="cursor-help text-gray-400 hover:text-gray-600">ℹ️</span>
                <div class="opacity-0 group-hover:opacity-100 transition-opacity bg-gray-800 text-sm text-white rounded-md absolute z-10 px-4 py-2 w-64">
                  Ces mots-clés sont fréquemment recherchés par les recruteurs.
                </div>
              </div>
            </div>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="keyword in analysisResults.missingKeywords" 
                :key="keyword"
                class="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm"
              >
                {{ keyword }}
              </span>
            </div>
          </div>

          <!-- Alertes -->
          <div v-if="analysisResults.alerts.length" class="mb-8">
            <h3 class="text-xl font-semibold text-gray-700 mb-4">Points d'attention</h3>
            <div class="space-y-2">
              <div 
                v-for="(alert, index) in analysisResults.alerts" 
                :key="index"
                class="flex items-start bg-red-50 p-4 rounded-lg"
              >
                <span class="text-red-500 mr-2">⚠️</span>
                <p class="text-red-700">{{ alert }}</p>
              </div>
            </div>
          </div>

          <!-- Version optimisée -->
          <div class="mb-8">
            <h3 class="text-xl font-semibold text-gray-700 mb-4">Version optimisée suggérée</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
              <pre class="whitespace-pre-wrap text-sm text-gray-700 font-mono">{{ analysisResults.optimizedVersion }}</pre>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="text-blue-600 text-2xl mb-3">🎯</div>
            <h3 class="text-lg font-semibold mb-2">Analyse ATS</h3>
            <p class="text-gray-600">Vérification de la compatibilité avec les systèmes de recrutement</p>
          </div>
          
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="text-blue-600 text-2xl mb-3">💡</div>
            <h3 class="text-lg font-semibold mb-2">Recommandations</h3>
            <p class="text-gray-600">Suggestions d'amélioration personnalisées</p>
          </div>
          
          <div class="bg-white p-6 rounded-xl shadow-md">
            <div class="text-blue-600 text-2xl mb-3">⚡</div>
            <h3 class="text-lg font-semibold mb-2">Instantané</h3>
            <p class="text-gray-600">Résultats en quelques secondes</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'default'
})

const importMode = ref('text')
const cvContent = ref('')
const jobOffer = ref('')
const selectedFile = ref(null)
const fileInput = ref(null)
const isAnalyzing = ref(false)
const analysisResults = ref(null)

const canAnalyze = computed(() => {
  return importMode.value === 'text' ? cvContent.value.trim() !== '' : selectedFile.value !== null
})

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
  }
}

const handleFileDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
  }
}

const analyzeCV = async () => {
  if (!canAnalyze.value) return
  
  console.log('Début de l\'analyse...')
  isAnalyzing.value = true
  
  try {
    const formData = new FormData()
    
    if (importMode.value === 'file') {
      formData.append('file', selectedFile.value)
      console.log('Fichier ajouté:', selectedFile.value.name)
    } else {
      formData.append('cv_content', cvContent.value)
      console.log('Contenu CV ajouté, longueur:', cvContent.value.length)
    }
    
    if (jobOffer.value.trim()) {
      formData.append('job_offer', jobOffer.value)
      console.log('Offre d\'emploi ajoutée')
    }

    console.log('Envoi de la requête à:', 'http://localhost:8000/analyze-cv')
    const response = await fetch('http://localhost:8000/analyze-cv', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Origin': window.location.origin
      },
      body: formData,
      credentials: 'include'  // Ajout pour les cookies si nécessaire
    })

    console.log('Statut de la réponse:', response.status)
    console.log('Headers de la réponse:', Object.fromEntries(response.headers))

    if (!response.ok) {
      const error = await response.json()
      console.error('Erreur serveur:', error)
      throw new Error(error.detail || 'Erreur lors de l\'analyse')
    }

    const data = await response.json()
    console.log('Réponse du backend:', data)
    analysisResults.value = data

  } catch (error) {
    console.error('Erreur détaillée:', error)
    // TODO: Afficher le toast d'erreur
  } finally {
    isAnalyzing.value = false
    console.log('Fin de l\'analyse')
  }
}
</script>

<style>
.shadow-md {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.shadow-md:hover {
  transform: translateY(-2px);
}

/* Ajout d'animations subtiles */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-out forwards;
}
</style> 