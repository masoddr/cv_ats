<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Hero Section -->
      <div class="text-center py-16 md:py-24">
        <h1 class="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Optimisez votre CV 
        </h1>
        <p class="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
          Notre IA analyse votre CV et vous guide pour maximiser vos chances face aux ATS (Applicant Tracking Systems) qui filtrent automatiquement les candidatures.
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
            <div class="text-3xl font-bold text-purple-600 mb-2">1min</div>
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
              <!-- Reset Button -->
              <div class="flex justify-end mb-4">
                <button
                  @click="resetForm"
                  class="flex items-center px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors duration-200"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Réinitialiser
                </button>
              </div>

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
                <span v-else class="flex items-center">
                  <svg 
                    class="w-5 h-5 mr-2" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      stroke-linecap="round" 
                      stroke-linejoin="round" 
                      stroke-width="2" 
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                    />
                  </svg>
                  {{ jobOffer.trim() 
                    ? 'Analyser mon CV et sa compatibilité' 
                    : 'Analyser mon CV' 
                  }}
                </span>
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

          <!-- Analyse des mots-clés -->
          <div class="mb-8">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-semibold text-gray-700">Analyse des mots-clés</h3>
              <div class="flex gap-2">
                <button
                  @click="copyMissingKeywords"
                  class="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                  </svg>
                  Copier les mots-clés
                </button>
                <button
                  @click="exportKeywords"
                  class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Exporter l'analyse
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <!-- Statistiques -->
              <div class="bg-white p-6 rounded-lg shadow">
                <h4 class="font-medium text-gray-800 mb-4">Vue d'ensemble</h4>
                <div class="grid grid-cols-3 gap-4">
                  <div class="text-center p-4 bg-blue-50 rounded-lg">
                    <div class="text-2xl font-bold text-blue-600">{{ analysisResults.topKeywords.length }}</div>
                    <div class="text-sm text-gray-600">Total</div>
                  </div>
                  <div class="text-center p-4 bg-green-50 rounded-lg">
                    <div class="text-2xl font-bold text-green-600">{{ analysisResults.presentKeywords.length }}</div>
                    <div class="text-sm text-gray-600">Présents</div>
                  </div>
                  <div class="text-center p-4 bg-yellow-50 rounded-lg">
                    <div class="text-2xl font-bold text-yellow-600">{{ analysisResults.missingKeywords.length }}</div>
                    <div class="text-sm text-gray-600">Manquants</div>
                  </div>
                </div>
              </div>

              <!-- Mots-clés manquants -->
              <div class="bg-yellow-50 p-6 rounded-lg">
                <h4 class="font-medium text-yellow-800 mb-4 flex items-center">
                  <span class="text-xl mr-2">⚠️</span>
                  Mots-clés manquants prioritaires
                </h4>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="keyword in analysisResults.missingKeywords" 
                    :key="keyword"
                    class="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm flex items-center group relative"
                  >
                    {{ keyword }}
                    <span class="ml-2 cursor-pointer hover:text-yellow-600" @click="copyKeyword(keyword)">📋</span>
                    <span class="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded whitespace-nowrap transition-opacity">
                      Cliquer pour copier
                    </span>
                  </span>
                </div>
              </div>
            </div>

            <!-- Suggestions de formulation -->
            <div class="bg-white p-6 rounded-lg shadow">
              <h4 class="font-medium text-gray-800 mb-4">Suggestions de formulation alternatives</h4>
              <div class="space-y-4">
                <div 
                  v-for="(alternatives, keyword) in analysisResults.keywordSuggestions" 
                  :key="keyword"
                  class="bg-gray-50 p-4 rounded-lg"
                >
                  <div class="font-medium text-gray-700 mb-2">{{ keyword }}</div>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      v-for="(alt, index) in alternatives" 
                      :key="index"
                      class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm cursor-pointer hover:bg-blue-200 transition-colors duration-200"
                      @click="copyKeyword(alt)"
                    >
                      {{ alt }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Scores d'évaluation -->
          <div class="mb-8">
            <h3 class="text-xl font-semibold text-gray-700 mb-4">Scores d'évaluation</h3>
            <div class="bg-white rounded-lg shadow overflow-hidden">
              <table class="min-w-full">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Critère</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Note sur 5</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Barre de progression</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(score, criterion) in analysisResults.scores" :key="criterion">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ criterion.charAt(0).toUpperCase() + criterion.slice(1).replace('_', ' ') }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ score.toFixed(1) }}/5
                    </td>
                    <td class="px-6 py-4">
                      <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div class="bg-blue-600 h-2.5 rounded-full" 
                             :style="{ width: `${(score/5)*100}%` }"
                             :class="{
                               'bg-red-600': score < 2.5,
                               'bg-yellow-600': score >= 2.5 && score < 3.5,
                               'bg-green-600': score >= 3.5
                             }">
                        </div>
                      </div>
                    </td>
                  </tr>
                  <!-- Score total -->
                  <tr class="bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Score Total</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">
                      {{ analysisResults.totalScore.toFixed(1) }}/20
                    </td>
                    <td class="px-6 py-4">
                      <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div class="bg-blue-600 h-2.5 rounded-full" 
                             :style="{ width: `${(analysisResults.totalScore/20)*100}%` }"
                             :class="{
                               'bg-red-600': analysisResults.totalScore < 10,
                               'bg-yellow-600': analysisResults.totalScore >= 10 && analysisResults.totalScore < 14,
                               'bg-green-600': analysisResults.totalScore >= 14
                             }">
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Points forts et améliorations -->
          <div class="mb-8">
            <h3 class="text-xl font-semibold text-gray-700 mb-4">Analyse du contenu</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Points forts -->
              <div class="bg-green-50 p-6 rounded-lg">
                <h4 class="font-medium text-green-800 mb-4 flex items-center">
                  <span class="text-xl mr-2">💪</span>
                  Points forts
                </h4>
                <ul class="space-y-2">
                  <li 
                    v-for="(point, index) in analysisResults.contentFeedback.points_forts" 
                    :key="index"
                    class="flex items-start"
                  >
                    <span class="text-green-600 mr-2">✓</span>
                    <span class="text-green-900">{{ point }}</span>
                  </li>
                </ul>
              </div>

              <!-- Points d'amélioration -->
              <div class="bg-yellow-50 p-6 rounded-lg">
                <h4 class="font-medium text-yellow-800 mb-4 flex items-center">
                  <span class="text-xl mr-2">💡</span>
                  Suggestions d'amélioration
                </h4>
                <ul class="space-y-2">
                  <li 
                    v-for="(point, index) in analysisResults.contentFeedback.points_amelioration" 
                    :key="index"
                    class="flex items-start"
                  >
                    <span class="text-yellow-600 mr-2">→</span>
                    <span class="text-yellow-900">{{ point }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Section de compatibilité - affichée uniquement si une offre est fournie -->
          <div v-if="analysisResults.jobMatch && jobOffer" class="mb-8">
            <h3 class="text-xl font-semibold text-gray-700 mb-4">Compatibilité avec l'offre</h3>
            
            <!-- Scores de compatibilité -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div class="bg-white p-4 rounded-lg shadow">
                <div class="text-2xl font-bold text-blue-600 mb-1">{{ analysisResults.jobMatch.score }}%</div>
                <div class="text-sm text-gray-600">Score global</div>
              </div>
              <div class="bg-white p-4 rounded-lg shadow">
                <div class="text-2xl font-bold text-green-600 mb-1">{{ analysisResults.jobMatch.technicalMatch }}%</div>
                <div class="text-sm text-gray-600">Technique</div>
              </div>
              <div class="bg-white p-4 rounded-lg shadow">
                <div class="text-2xl font-bold text-purple-600 mb-1">{{ analysisResults.jobMatch.experienceMatch }}%</div>
                <div class="text-sm text-gray-600">Expérience</div>
              </div>
              <div class="bg-white p-4 rounded-lg shadow">
                <div class="text-2xl font-bold text-indigo-600 mb-1">{{ analysisResults.jobMatch.softSkillsMatch }}%</div>
                <div class="text-sm text-gray-600">Soft Skills</div>
              </div>
            </div>

            <!-- Analyse détaillée -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Points forts -->
              <div class="bg-green-50 p-6 rounded-lg">
                <h4 class="font-medium text-green-800 mb-4 flex items-center">
                  <span class="text-xl mr-2">💪</span>
                  Points forts
                </h4>
                <ul class="space-y-2">
                  <li 
                    v-for="(strength, index) in analysisResults.jobMatch.strengths" 
                    :key="index"
                    class="flex items-start"
                  >
                    <span class="text-green-600 mr-2">✓</span>
                    <span class="text-green-900">{{ strength }}</span>
                  </li>
                </ul>
              </div>

              <!-- Écarts -->
              <div class="bg-yellow-50 p-6 rounded-lg">
                <h4 class="font-medium text-yellow-800 mb-4 flex items-center">
                  <span class="text-xl mr-2">⚠️</span>
                  Points à améliorer
                </h4>
                <ul class="space-y-2">
                  <li 
                    v-for="(gap, index) in analysisResults.jobMatch.gaps" 
                    :key="index"
                    class="flex items-start"
                  >
                    <span class="text-yellow-600 mr-2">→</span>
                    <span class="text-yellow-900">{{ gap }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Recommandations -->
            <div class="mt-6 bg-blue-50 p-6 rounded-lg">
              <h4 class="font-medium text-blue-800 mb-4 flex items-center">
                <span class="text-xl mr-2">💡</span>
                Recommandations pour cette offre
              </h4>
              <ul class="space-y-2">
                <li 
                  v-for="(rec, index) in analysisResults.jobMatch.recommendations" 
                  :key="index"
                  class="flex items-start"
                >
                  <span class="text-blue-600 mr-2">•</span>
                  <span class="text-blue-900">{{ rec }}</span>
                </li>
              </ul>
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
    <Toast v-bind="toast" />
    <ProgressSteps 
      :steps="steps"
      :currentStep="currentStep"
    />

    <!-- Footer -->
    <footer class="bg-gray-50 border-t border-gray-200 mt-16">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <!-- À propos -->
          <div>
            <h3 class="text-gray-900 font-semibold mb-4">À propos</h3>
            <p class="text-gray-600 text-sm">
              CV ATS Optimizer vous aide à optimiser votre CV pour les systèmes de suivi des candidatures (ATS) grâce à l'intelligence artificielle.
            </p>
          </div>
          
          <!-- Liens utiles -->
          <div>
            <h3 class="text-gray-900 font-semibold mb-4">Liens utiles</h3>
            <ul class="space-y-2">
              <li>
                <NuxtLink to="/guide" class="text-gray-600 hover:text-blue-600 text-sm transition-colors duration-200">
                  Guide d'utilisation
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/faq" class="text-gray-600 hover:text-blue-600 text-sm transition-colors duration-200">
                  FAQ
                </NuxtLink>
              </li>
            </ul>
          </div>
          
          <!-- Légal -->
          <div>
            <h3 class="text-gray-900 font-semibold mb-4">Informations légales</h3>
            <ul class="space-y-2">
              <li>
                <NuxtLink to="/cgu" class="text-gray-600 hover:text-blue-600 text-sm transition-colors duration-200">
                  Conditions générales d'utilisation
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/privacy" class="text-gray-600 hover:text-blue-600 text-sm transition-colors duration-200">
                  Politique de confidentialité
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/legal" class="text-gray-600 hover:text-blue-600 text-sm transition-colors duration-200">
                  Mentions légales
                </NuxtLink>
              </li>
            </ul>
          </div>
          
          <!-- Contact -->
          <div>
            <h3 class="text-gray-900 font-semibold mb-4">Contact</h3>
            <!-- Formulaire de contact -->
            <form @submit.prevent="sendContactForm" class="space-y-4">
              <div>
                <input
                  v-model="contactForm.name"
                  type="text"
                  placeholder="Votre nom"
                  class="w-full px-4 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <input
                  v-model="contactForm.email"
                  type="email"
                  placeholder="Votre email"
                  class="w-full px-4 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <textarea
                  v-model="contactForm.message"
                  placeholder="Votre message"
                  rows="3"
                  class="w-full px-4 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  required
                ></textarea>
              </div>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="w-full px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50"
              >
                {{ isSubmitting ? 'Envoi...' : 'Envoyer' }}
              </button>
            </form>

            <!-- Informations de contact -->
            <div class="mt-4 space-y-2">
              <li class="flex items-center text-gray-600 text-sm">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <a href="mailto:ouaddour.massyl@gmail.com" class="hover:text-blue-600 transition-colors duration-200">
                  ouaddour.massyl@gmail.com
                </a>
              </li>
              <li class="flex items-center text-gray-600 text-sm">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Toulouse, France
              </li>
            </div>
          </div>
        </div>
        
        <!-- Copyright -->
        <div class="border-t border-gray-200 mt-8 pt-8 text-center">
          <p class="text-gray-500 text-sm">
            © {{ new Date().getFullYear() }} CV ATS Optimizer. Tous droits réservés.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Toast from '~/components/Toast.vue'
import ProgressSteps from '~/components/ProgressSteps.vue'

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

const toast = ref({
  isVisible: false,
  type: 'info',
  message: ''
})

const showToast = (type, message) => {
  toast.value = { isVisible: true, type, message }
  setTimeout(() => {
    toast.value.isVisible = false
  }, 3000)
}

const steps = [
  'Import du CV',
  'Analyse ATS',
  'Résultats'
]

const currentStep = ref(0)

const resetForm = () => {
  // Réinitialisation des champs
  cvContent.value = ''
  jobOffer.value = ''
  selectedFile.value = null
  analysisResults.value = null
  currentStep.value = 0

  // Réinitialisation du mode d'import si nécessaire
  importMode.value = 'text'

  // Notification à l'utilisateur
  showToast('info', 'Formulaire réinitialisé')
}

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
  currentStep.value = 1
  
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
    currentStep.value = 2
    showToast('success', 'Analyse terminée avec succès !')

  } catch (error) {
    console.error('Erreur détaillée:', error)
    showToast('error', 'Une erreur est survenue lors de l\'analyse')
  } finally {
    isAnalyzing.value = false
    console.log('Fin de l\'analyse')
  }
}

const exportOptimizedVersion = () => {
  if (!analysisResults.value?.optimizedVersion) return

  // Création du blob avec le contenu
  const blob = new Blob([analysisResults.value.optimizedVersion], { type: 'text/plain' })
  
  // Création de l'URL du blob
  const url = window.URL.createObjectURL(blob)
  
  // Création d'un lien temporaire pour le téléchargement
  const link = document.createElement('a')
  link.href = url
  link.download = 'cv_optimise.txt'
  
  // Ajout du lien au document et simulation du clic
  document.body.appendChild(link)
  link.click()
  
  // Nettoyage
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}

const exportKeywords = () => {
  if (!analysisResults.value) return

  const content = `ANALYSE DÉTAILLÉE DES MOTS-CLÉS DE VOTRE CV

STATISTIQUES
-----------
Total mots-clés importants : ${analysisResults.value.topKeywords.length}
Mots-clés présents : ${analysisResults.value.presentKeywords.length}
Mots-clés manquants : ${analysisResults.value.missingKeywords.length}

MOTS-CLÉS PRÉSENTS
-----------------
${analysisResults.value.presentKeywords.join(', ')}

MOTS-CLÉS MANQUANTS
-----------------
${analysisResults.value.missingKeywords.join(', ')}

SUGGESTIONS DE FORMULATION
------------------------
${Object.entries(analysisResults.value.keywordSuggestions)
  .map(([keyword, alternatives]) => `${keyword}:\n  - ${alternatives.join('\n  - ')}`)
  .join('\n\n')}

POINTS FORTS
-----------
${analysisResults.value.contentFeedback.points_forts.map(point => `- ${point}`).join('\n')}

SUGGESTIONS D'AMÉLIORATION
------------------------
${analysisResults.value.contentFeedback.points_amelioration.map(point => `- ${point}`).join('\n')}

SCORE GLOBAL: ${analysisResults.value.totalScore.toFixed(1)}/20`

  const blob = new Blob([content], { type: 'text/plain' })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'analyse_complete_cv.txt'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}

const copyKeyword = async (keyword) => {
  try {
    await navigator.clipboard.writeText(keyword)
    showToast('success', 'Mot-clé copié !')
  } catch (err) {
    showToast('error', 'Erreur lors de la copie')
  }
}

const copyMissingKeywords = async () => {
  if (!analysisResults.value?.missingKeywords) return
  
  try {
    const keywords = analysisResults.value.missingKeywords.join(', ')
    await navigator.clipboard.writeText(keywords)
    showToast('success', 'Mots-clés copiés !')
  } catch (err) {
    showToast('error', 'Erreur lors de la copie')
  }
}

const contactForm = ref({
  name: '',
  email: '',
  message: ''
})

const isSubmitting = ref(false)

const sendContactForm = async () => {
  isSubmitting.value = true
  try {
    // Création du contenu de l'email avec mailto
    const subject = `Contact CV ATS Optimizer - ${contactForm.value.name}`
    const body = `Message de : ${contactForm.value.name}\nEmail : ${contactForm.value.email}\n\n${contactForm.value.message}`
    const mailtoLink = `mailto:ouaddour.massyl@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
    
    // Ouverture du client mail
    window.location.href = mailtoLink
    
    // Réinitialisation du formulaire
    contactForm.value = {
      name: '',
      email: '',
      message: ''
    }
    
    showToast('info', 'Votre client mail a été ouvert. N\'oubliez pas d\'envoyer le message !')
  } catch (error) {
    showToast('error', 'Erreur lors de l\'ouverture de votre client mail')
  } finally {
    isSubmitting.value = false
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