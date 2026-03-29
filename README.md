# 🌍 Observatoire Spatial de la Chlordécone - Analyse et Aide à la Décision


## 📌 Contexte du Projet
La chlordécone est un insecticide organochloré utilisé massivement dans les bananeraies des Antilles françaises jusqu'en 1993. Sa très forte persistance dans l'environnement pose aujourd'hui un enjeu sanitaire et agronomique majeur. 

Ce projet a pour objectif d'analyser une base de données de plus de 30 000 prélèvements de sols afin d'identifier les zones à risque et de fournir un **outil d'aide à la décision publique** pour prioriser les actions sanitaires.

## 🚀 Méthodologie et Pipeline de Données

Le projet est divisé en trois grands volets analytiques :

1. **Nettoyage et Analyse Exploratoire (EDA)** : 
   - Traitement des valeurs manquantes et aberrantes (erreurs de laboratoire).
   - Étude des distributions temporelles et spatiales de la contamination.

2. **Machine Learning Non Supervisé (Clustering)** :
   - **Analyse en Composantes Principales (ACP)** : Mise en évidence de la forte corrélation entre la topographie (pente, rugosité), l'historique de culture bananière et le taux de chlordécone.
   - **K-Means & CAH** : Segmentation du territoire en profils de risque. Validation croisée par Classification Ascendante Hiérarchique (Dendrogramme).

3. **Dashboard Interactif (Streamlit)** :
   - Interface décisionnelle permettant de filtrer les données par commune, par année et par profil de risque.
   - Cartographie spatiale interactive (Plotly) avec identification instantanée des zones critiques.

## 📊 Principaux Résultats (Profils de Territoires)
L'algorithme de Machine Learning a permis d'isoler 3 grands profils agronomiques (et un cluster technique) :
* 🟢 **Zone Saine (Cluster 0)** : ~48% des parcelles. Contamination quasi-nulle, très faible historique bananier.
* 🟠 **Zone Pentue (Cluster 1)** : ~19% des parcelles. Risque modéré, forte contrainte topographique.
* 🔴 **Zone Critique (Cluster 2)** : ~32% des parcelles. **Haut risque sanitaire**. Fort historique bananier, très forte contamination, localisée principalement au Nord/Nord-Ouest (ex: Saint-Pierre, Grand'Rivière).
* ⚫ **Anomalies (Cluster 3)** : < 1% des parcelles. Isolement automatique par l'algorithme des erreurs de mesure résiduelles.

## 📁 Structure du Dépôt
```text
├── 01_EDA.ipynb                  # Analyse Exploratoire des Données
├── 02_Cleaning.ipynb             # Nettoyage et préparation des données
├── 03_ACP.ipynb                  # Analyse en Composantes Principales
├── 04_Clustering_KMeans.ipynb    # Segmentation K-Means et Méthode du Coude
├── 05_Clustering_CAH.ipynb       # Validation par CAH (Dendrogramme)
├── app.py                        # Code source du Dashboard Streamlit
├── chlordecone_clustered.csv     # Jeu de données final (généré post-ML)
└── README.md                     # Documentation du projet