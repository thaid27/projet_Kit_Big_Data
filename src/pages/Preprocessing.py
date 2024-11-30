import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import ast
import nltk
import re

from utils.dbapi import DBapi

db = DBapi()
with db:
    df = pd.DataFrame(db.get_percentage_documents(per=0.0005))

# Variables globales pour simuler les données
PATH_DATA = "../data/"
RAW_RECIPE = "RAW_recipes_sample.csv"
RAW_INTERACTIONS = "RAW_interactions_sample.csv"


# ---- Page Streamlit ----
st.set_page_config(page_title="Explication Prétraitement", layout="wide")

# --- Titre et Introduction ---
st.title("🌟 Explication du Prétraitement des Données")
st.write(
    """
Cette page présente les étapes de prétraitement appliquées aux données, 
ainsi que des visualisations pour mieux comprendre leur impact.
"""
)

# --- Chargement des données ---
st.header("Chargement des Données")
st.write(
    """
Les données brutes sont chargées à partir de fichiers CSV. Voici un aperçu des fichiers utilisés :
- `RAW_recipes.csv` : Données des recettes brutes.
- `RAW_interactions.csv` : Interactions des utilisateurs avec les recettes.
"""
)


# Exemple de chargement fictif
@st.cache_data
def load_data(file_name):
    path = os.path.join(PATH_DATA, file_name)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()  # Placeholder si le fichier est manquant


raw_recipes = load_data(RAW_RECIPE)
raw_interactions = load_data(RAW_INTERACTIONS)

# Afficher les données brutes si elles existent
if not raw_recipes.empty:
    st.write("Exemple de données brutes de RAW_recipe:")
    st.dataframe(raw_recipes.head(5))
else:
    st.warning("Fichier RAW_recipes_sample.csv introuvable.")


# Afficher les données brutes si elles existent
if not raw_recipes.empty:
    st.write("Exemple de données brutes de RAW_interactions:")
    st.dataframe(raw_interactions.head(5))
else:
    st.warning("Fichier RAW_interactions_sample.csv introuvable.")


# --- Transformation des Données ---
st.header("2️⃣ Transformation des Données")
st.write(
    """
Plusieurs transformations sont appliquées pour préparer les données :
1. Les datasets doivent être nétoyés.
    Pour cela, les recettes avec des valeurs manquantes sont supprimées.
    Les recettes avec des valeurs aberrantes sont également supprimées.
    Notamment celles avec un temps de cuisson excessif ou un nombre de steps nul.
    Les 'Description' manquantes sont remplies avec le contenu de 'Name' pour combler les vides.
    
2. Les données de RAW_interactions devaient être fusionnées avec RAW_recipes. Pour cela, les deux dataframes ont été merge sur la colonne `recipe_id`.
Les colonnes de interactions ont été transformées en listes pour faire correspondre chaque recette avec ses interactions, ses commentaires, ses reviews, etc.

3. Fusion des datasets `RAW_recipes` et `RAW_interactions`.

4. Nettoyage des descriptions et des noms.
   Dans le but de réaliser un clustering, les descriptions et les noms des recettes sont nettoyés et tokenisés.
   Les stopwords sont supprimés des textes.

"""
)

# Exemple visuel avant/après nettoyage
if not raw_recipes.empty:
    # Conversion fictive
    raw_recipes["submitted"] = pd.to_datetime(
        raw_recipes.get("submitted", pd.Series([]))
    )
    st.write(
        "**Avant conversion de la colonne `submitted` :**",
        raw_recipes["tags"].dtype,
    )
    st.write("**Après conversion :**", raw_recipes["tags"].dtype)

# --- Nettoyage des Données ---
st.header("1️⃣ Nettoyage des Données")
st.write(
    """
Les colonnes contenant des valeurs manquantes sont remplacées ou supprimées :
- La colonne `description` est remplie avec le contenu de `name` si elle est vide.
- Les lignes avec `name` manquant sont supprimées.
"""
)

# Visualisation des valeurs manquantes
if not raw_recipes.empty:
    st.write("Visualisation des valeurs manquantes dans les données brutes :")
    missing_data = raw_recipes.isna().sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(missing_data.index, missing_data.values)
    ax.set_title("Valeurs manquantes par colonne")
    ax.set_xlabel("Nombre de valeurs manquantes")
    st.pyplot(fig)

st.header("2️⃣ Préparation à la fusion des Données")

st.write(
    """
Les données de `RAW_interactions` sont fusionnées avec `RAW_recipes` :
- Les deux datasets sont joints sur la colonne `recipe_id`.
- Les colonnes de `RAW_interactions` sont transformées en listes.
"""
)

st.header("3️⃣ Visualisation de la Fusion")

# --- Suppression des Valeurs Aberrantes ---
st.header("4️⃣ Suppression des Valeurs Aberrantes")
st.write(
    """
Certaines recettes troll ou mal renseignées sont supprimées :
- Les recettes avec un temps de cuisson excessif.
- Les recettes avec un nombre de steps ou d'ingrédients nul.
"""
)

# Exemple fictif
if not raw_recipes.empty:
    cleaned_recipes = raw_recipes[raw_recipes["minutes"] < 300]
    st.write(f"Recettes avant nettoyage : {len(raw_recipes)}")
    st.write(f"Recettes après nettoyage : {len(cleaned_recipes)}")

# --- Nettoyage des Textes ---
st.header("5️⃣ Nettoyage et Tokenisation des Textes")
st.write(
    """
Les descriptions et noms des recettes sont nettoyés et tokenisés :
- Suppression des stopwords.
- Tokenisation des phrases en mots.
"""
)

# Afficher des exemples fictifs
example_text = "This is a recipe with a lot of unnecessary words and punctuation!!!"
stopwords = {"this", "is", "a", "and"}
cleaned_text = " ".join(
    [word for word in example_text.lower().split() if word not in stopwords]
)
st.write(f"**Texte brut** : {example_text}")
st.write(f"**Texte nettoyé** : {cleaned_text}")

# --- Pipeline de Prétraitement ---
st.header("6️⃣ Visualisation du Pipeline")
from graphviz import Digraph

dot = Digraph()
dot.node("A", "Chargement")
dot.node("B", "Fusion")
dot.node("C", "Nettoyage")
dot.node("D", "Suppression des Outliers")
dot.node("E", "Tokenisation")
dot.edges(["AB", "BC", "CD", "DE"])
st.graphviz_chart(dot)

# TODO : Raconter mieux lhistoire du pretaitement