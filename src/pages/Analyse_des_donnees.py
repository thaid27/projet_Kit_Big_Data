"""
Page de l'application dédiée à l'analyse des données.
"""

import os
import logging
import streamlit as st
from utils.bivariate_study import BivariateStudy
from utils.univariate_study import UnivariateStudy
from pandas import Timestamp
from utils.load_functions import compute_trend, load_df, initialize_recipes_df, load_css

st.set_page_config(page_title="MangeTaData", page_icon="images/favicon_mangetadata.png", layout="wide")

logger = logging.getLogger(os.path.basename(__file__))


if "recipes_df" not in st.session_state:
    st.session_state["recipes_df"] = initialize_recipes_df("data/clean_cloud_df.csv")

if "first_load" not in st.session_state:
    st.session_state["first_load"] = True

if "locked_graphs" not in st.session_state:
    st.session_state["locked_graphs"] = {}


def main():
    """
    Fonction principale de la page Analyse des données.
    """
    st.title("Analyse des data")
    load_css("src/style.css")

    try:
        # Creation of all the graphs displayed in the page
        if st.session_state["first_load"]:
            trend = compute_trend(st.session_state["recipes_df"])
            logger.info("Tendance calculee avec succes.")

            nb_recette_par_annee_study = BivariateStudy(
                dataframe=trend,
                key="Moyenne glissante du nombre de recettes par mois",
                name="Moyenne glissante du nombre de recettes du temps",
                axis_x="Date",
                axis_y="Moyenne glissante",
                plot_type="plot",
                default_values={
                    "Date": (
                        Timestamp("1999-08-01 00:00:00"),
                        Timestamp("2018-12-1 00:00:00"),
                    ),
                    "Moyenne glissante": (3, 2268),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"] = nb_recette_par_annee_study

            nb_recette_temps_study = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de recettes par an",
                name="Nombre de recettes par an",
                axis_x="Date de publication de la recette",
                filters=[],
                plot_type="histogram",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Date de publication de la recette": (
                        Timestamp("2000-01-01 00:00:00"),
                        Timestamp("2018-01-01 00:00:00"),
                    ),
                    "chosen_filters": [],
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Nombre de recettes par an"] = nb_recette_temps_study

            

            nb_commentaire_par_annee_study = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de commentaires par recette en fonction du temps",
                name="Nombre de commentaires par recette en fonction du temps",
                axis_x="Date de publication de la recette",
                axis_y="Nombre de commentaires",
                filters=[],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=True,
                default_values={
                    "Date de publication de la recette": (
                        Timestamp("1999-08-06 00:00:00"),
                        Timestamp("2018-12-04 00:00:00"),
                    ),
                    "Nombre de commentaires": (1, 1613),
                    "chosen_filters": [],
                },
            )
            st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"] = nb_commentaire_par_annee_study

            nb_recette_temps_active_study = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de recettes durant le pic d'activité du site",
                name="Nombre de recettes durant le pic d'activité du site",
                axis_x="Date de publication de la recette", 
                filters=[],
                plot_type="histogram", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "Date de publication de la recette": 
                    (Timestamp('2002-01-01 00:00:00'), 
                     Timestamp('2010-01-01 00:00:00')), 
                     "chosen_filters":[]
                },
                graph_pad=1,
                
            )
            st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"] = nb_recette_temps_active_study

            comment_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution du nombre de commentaires par recette",
                name="Distribution du nombre de commentaires par recette",
                axis_x="Nombre de commentaires",
                filters=[],
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "Nombre de commentaires": (0, 1613), 
                },
            )
            st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"] = comment_box_blot

            mean_rating_box_blot = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Distribution de la note moyenne des recettes",
                name="Distribution de la note moyenne des recettes",
                axis_x="Note moyenne", 
                filters=[], 
                plot_type="boxplot", 
                log_axis_x=True, 
                log_axis_y=False, 
                default_values={
                    "Note moyenne": (0, 5), 
                },
            )
            st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"] = mean_rating_box_blot

            min_popular_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Durée des recettes populaires",
                name="Durée recettes populaires",
                axis_x="Durée de la recette (minutes)",
                axis_y="Nombre de commentaires", filters=['Note moyenne'],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=True,
                default_values={
                    "Durée de la recette (minutes)": (1, 1750),
                    "Nombre de commentaires": (5, 1613),
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Durée des recettes populaires"] = min_popular_recipes

            nb_steps_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'étapes des recettes populaires",
                name="Nombre d'étapes des recettes populaires",
                axis_x="Nombre d'étapes",
                axis_y="Nombre de commentaires",
                filters=['Note moyenne'],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Nombre d'étapes": (3, 37),
                    "Nombre de commentaires": (5, 1613),
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                },
                graph_pad=1,
                
            )
            st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"] = nb_steps_recipes

            nb_ing_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre d'ingrédients par recette",
                name="Nombre d'ingrédients par recette",
                axis_x="Nombre d'ingrédients", 
                axis_y="Nombre de commentaires", 
                filters=['Note moyenne'], 
                plot_type="density map", 
                log_axis_x=False, 
                log_axis_y=False, 
                default_values={
                    "Nombre d'ingrédients": (4, 20), 
                    "Nombre de commentaires": (5, 1613), 
                    "Note moyenne":(4, 5), 
                    "chosen_filters":['Note moyenne'],
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Nombre d'ingrédients par recette"] = nb_ing_recipes

            popular_ing = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Ingrédients les plus populaires",
                name="Ingrédients les plus populaires",
                axis_x="Ingrédients",
                filters=['Note moyenne',"Nombre de commentaires"],
                plot_type="bar_ingredients",
                log_axis_x=False, log_axis_y=False,
                default_values={
                    "Ingrédients": 10,
                    "Note moyenne":(4, 5),
                    "Nombre de commentaires": (5, 1613),
                    "chosen_filters":['Note moyenne',"Nombre de commentaires"]
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Ingrédients les plus populaires"] = popular_ing

            calories_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Calories des recettes populaires",
                name="Calories des recettes populaires",
                axis_x="Calories",
                axis_y="Nombre de commentaires",
                filters=['Note moyenne'], plot_type="density map",
                log_axis_x=True, log_axis_y=True,
                default_values={
                    "Calories": (1, 19383),
                    "Nombre de commentaires": (5, 1613), 
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                },
            )
            st.session_state["locked_graphs"]["Calories des recettes populaires"] = calories_recipes

            popular_techniques = UnivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Techniques de cuisine les plus populaires",
                name="Techniques de cuisine les plus populaires",
                axis_x="Techniques utilisées",
                filters=['Note moyenne',"Nombre de commentaires"],
                plot_type="bar_techniques",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Techniques utilisées": 10,
                    "Nombre de commentaires": (5, 1613),
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne',"Nombre de commentaires"]
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Techniques de cuisine les plus populaires"] = popular_techniques

            nb_techniques_recipes = BivariateStudy(
                dataframe=st.session_state["recipes_df"],
                key="Nombre de techniques de cuisine différentes par recettes",
                axis_x="Nombre de techniques utilisées",
                axis_y="Nombre de commentaires",
                filters=['Note moyenne'],
                plot_type="density map",
                log_axis_x=False,
                log_axis_y=False,
                default_values={
                    "Nombre de techniques utilisées": (0, 14),
                    "Nombre de commentaires": (5, 1613),
                    "Note moyenne":(4, 5),
                    "chosen_filters":['Note moyenne']
                },
                graph_pad=1,
            )
            st.session_state["locked_graphs"]["Nombre de techniques de cuisine différentes par recettes"] = nb_techniques_recipes 

            st.session_state["first_load"] = False
            logger.info("Graphiques initialises avec succes.")

            
        st.write("""Dans cette page, diverses analyses seront effectuées sur les données sur les recettes fournies par le site MangeTaMain, 
                 notamment le nombre de recettes publiées, leur note moyenne et le nombre de commentaires,
                 les ingrédients ou techniques de cuisine utilisés, etc. 
                 Le but de cette étude est d'évaluer les performances du site au cours du temps et de comprendre les facteurs de succès 
                 des recettes les plus populaires, afin de déterminer le type de recettes à partager et à promouvoir afin de redynamiser l'activité sur la plateforme.""")

        # Page layout 
        st.header("1️⃣ Analyse de la fréquentation du site")

        st.write("""Tout d'abord, il s'agira d'étudier la fréquentation du site au cours des années 
                 à travers l'évolution du nombre de recettes ainsi que le nombre de commentaires par recette.""")

        explanation_graph_1 = """
        **Observations :**
        - Ce graphe représente la moyenne glissante par mois du nombre de recettes entre 2000 et 2018
        - Une forte croissance des contributions est visible entre 2000 et 2002, puis une stagnation entre 2002 et 2004 suivie d'une deuxième phase de croissance en 2008, 
        - Le pic d'activité maximale est atteint autour de 2007 et 2008 avec plus de 2000 recettes par mois.
        - À partir de 2008, une chute significative et prolongée est observée, atteignant presque zéro entre 2016 et 2018."""

        
        st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"].display_graph(
            explanation=explanation_graph_1
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Moyenne glissante du nombre de recettes"].name}")

        col1, col2 = st.columns(2)
        with col1 :
            st.session_state["locked_graphs"]["Nombre de recettes par an"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de recettes par an"].name}")
        with col2 :
            st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de recettes durant le pic d'activité du site"].name}")
        
        with st.container(border=True):
            explanation_graph_2 = """
            **Observations :**
            - Ces deux graphes représentent le nombre de recettes publiées par an sur deux plages d'années différentes :
            1.Celui de droite offrant une vue d'ensemble sur toute la période couverte par les données, entre 2000 et 2018
            (Les recettes en bordure, fin 1999 et début 2018 sont omises pour avoir des intervalles correspondant à des années entières, 
            mais ces recettes restent consultables en changeant les dates des filtres)
            2.Celui de gauche se focalise sur la phase de plus grande affluence du site entre 2002 et 2010. 
            - La tendance du nombre de publications de recettes précedemment observée est en accord avec ces graphes avec 
            comme années culminantes 2007 et 2008 comptant respectivement 26 539 et 23 238 recettes, puis une chute de l'activité après 2008.
            - De plus, il est intéressant de noter que le pic d'activité représente 151 367 recettes sur 176 287 au total, soit 
            environ 85 % de toutes les recettes publiées.
            """
            st.write(explanation_graph_2)
            

        explanation_graph_3 ="""
        **Observations :**
        - Ce graphe est une carte de densité représentant l'évolution du nombre de commentaires par recette sur la période étudiée.
        Une forte activité des utilisateurs se traduisant par un nombre de commentaires par recette peut être observée dès 2000 jusqu'en 2009, 
        ce qui est une plage temporelle plus étendue comparée au pic d'activité du nombre de recettes publiées.
        - Sur cette période un grand nombre de recettes dépasse les 20 commentaires et 
        les records de nombre de commentaires sont établis pour les recettes publiées dans cet intervalle, 
        atteignant plus de 1600 commentaires pour les meilleures recettes.
        - De plus, une concentration très importante de recettes publiées à ce moment ont entre 1 et 20 commentaires (en jaune et cyan sur le graphe),
        notamment entre 2006 et 2009 avec la plus forte concentration recette à 1 commentaires. Cette tendance montre une effervescence de recettes, 
        mais que ces recettes n'attirent pas forcément beaucoup de personnes, remettant en cause la qualité des recettes.
        """

        st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"].display_graph(
            explanation=explanation_graph_3
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de commentaires par recette en fonction du temps"].name}")

        conclusion_part_1 = """
        **Interprétation :**
        - Après une forte croissance jusqu'en 2009, Le site a connu un fort déclin jusqu'à aujourd'hui, illustré par la diminution marquée de l'activité des utilisateurs
        dans la création de recettes et de l'engagement des utilisateurs dans l'espace commentaire.  

        - Cette baisse d'activité peut être expliquée par plusieurs facteurs :
          1. **Concurrence croissante** : Avec l'émergence de plateformes sociales comme YouTube, Instagram, et des sites concurrents, le site aurait pu perdre son attractivité.
          2. **Fatigue des contributeurs** : Les créateurs pourraient avoir perdu intérêt ou ne pas être suffisamment motivés pour continuer à enrichir la plateforme.
          3. **Manque d'innovation** : Si le site n'a pas évolué pour répondre aux nouvelles attentes des utilisateurs (fonctionnalités modernes, gamification, etc.), il aurait pu perdre de l'engagement.
          4. **Facteurs externes** : La crise économique de 2008 a pu engendrer un manque de moyens pour s'investir dans la cuisine maison. 
        
        - La question des solutions pour remédier à cette tendance et revitaliser le site peut se poser.
          La démarche proposée dans la suite de l'étude est d'analyser en profondeur les recettes les plus populaires ayant porté 
          le site durant son âge d'or, engendrant de l'attractivité et de l'engagement de la part de ses utilisateurs.
        """
        with st.container(border=True):
            st.write(conclusion_part_1)
        

        st.header("2️⃣ Définition d'une recette de populaire")

        st.write("""Dans cette deuxième partie, il conviendra de comprendre ce qui définit la popularité d'une recette
                 Deux axes principaux seront explorés : la note moyenne et le nombre de commentaires des recettes""")

        explanation_graph_4 = """
        **Observations :**
        Ce graphe de type boîte à moustaches illustre la distribution du nombre de commentaires par recette. 
        Plus précisément, d'après celui-ci, on observe :
        - une médianne située aux alentours de 2 commentaires par recettes
        - 25% des meilleurs recettes en termes de nombre de commentaires ont 5 ou plus de commentaires (Troisième quartile).

        La distribution du nombre de commentaires par recette est très polarisée en faveur des recettes avec peu de commentaires
        avec la grande majorité des recettes ayant en dessous de 5 commentaires, 
        une médiane situé à 2 commentaires et un grand nombre à 1 commentaire (63 084 recettes, soit 35 %).
        Cette analyse confirme le rapport quantité/attractivité à améliorer, évoqué dans la première partie.
        """

        st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"].display_graph(
            explanation=explanation_graph_4
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Distribution du nombre de commentaires par recette"].name}")

        explanation_graph_5 = """
        **Observations :**
        Ce graphe de type boîte à moustaches représente la distribution des notes moyennes des recettes. 
        Plus précisément, d'après celui-ci, on observe :
        - une médianne située aux alentours de la note moyenne de 4,6 par recette
        - seulement 25% des recettes sont notés 4 ou moins (1er quartile).

        Ce critère est moins représentatif des meilleures recettes car la majorité des recettes sont notées 4 ou plus. 
        De plus, des exemples de recettes très populaires, mais avec notes en dessous de la médiane sont présents dans la dataframe ci-dessus
        (par exemple : la recette "best banana bread" est notée 4,186 en moyenne).
        """

        st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"].display_graph(
            explanation=explanation_graph_5
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Distribution de la note moyenne des recettes"].name}")

        conclusion_part_2 = """
        **Interprétation :**
        D'après cette analyse, deux critères peuvent définir la popularité d'une recette. 
        Tout d'abord, l'élément le plus discriminant est le nombre de commentaires par recette 
        car seulement très peu de recettes réussissent à attirer l'engagement des utilisateurs.
         
        Un second élément moins représentatif est la note moyenne sui permet de supprimer les recettes dépréciées, 
        mais qui ne permet pas de juger à lui seul l'attractivité d'une recette.

        Dans le reste de cette étude on se placera dans ces conditions : 
        - nombre de commentaires par recette : supérieur ou égal à 5
        - note moyenne : supérieure ou égale à 4
        Avec ces filtres, 38 918 recettes sont considérées comme populaires et seront étudiées. 
        """

        with st.container(border=True):
            st.write(conclusion_part_2)

        

        st.header("3️⃣ Caractéristiques des recettes populaires")
        
        st.write("""Après avoir déterminé les critères définissant les recettes populaires, leurs caractéristiques internes peuvent être explicitées 
                    afin de comprendre la source de leur popularité. En effet, des analyses seront effectuées sur la logistique, les ingrédients et 
                    les techniques employées pour identifier les facteurs de succès d'une recette.""")
    

        explanation_graph_6 = """
        **Observations :**
        Concernant le graphe sur la durée des recettes populaires :
        - La majorité des recettes populaires sont relativement courtes, avec une durée de préparation inférieure à 100 minutes.
        Ces recettes ont tendance à avoir un nombre de commentaires plus élevé, avec une grande concentration de recettes à plus de 50 commentaires (log Nombre de commentaires = 4) 
        ainsi que presque toutes les recettes à plus de 400 commentaires (log Nombre de commentaires = 6).
        - Cependant certaines recettes longues restent populaires en moins grande proportion entre 200 et 750 minutes, et un pic peut être observé aux alentours de 1000 minutes.
        Enfin, certaines recettes très longues ont un bon nombre de commentaires observables en élargissant le filtre sur la durée de la recette. 

        Concernant le graphe sur le nombre d'étapes des recettes populaires :
        - Une très grande concentration de recettes populaires peut être observée pour un nombre d'étapes inférieurs à 17, 
        puis une baisse entre 17 et 25 et au-delà, les recettes ont peu de commentaires.

        **Interprétations :**
        Les recettes relativement courtes et avec peu d'étapes semblent être **plus populaires**
        Une interprétation possible car elles sont **plus simples et rapides à réaliser** ne nécessitant pas un investissement temporel
        ou une aptitude à exécuter une procédure complexe.
        Ces recettes sont alors plus faciles d'accès et s'adressent à un plus grand public, d'où leur popularité.
        """

        col1, col2 = st.columns(2)
        with col1:
            st.session_state["locked_graphs"]["Durée des recettes populaires"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Durée des recettes populaires"].name}")
        with col2:
            st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre d'étapes des recettes populaires"].name}")

        with st.container(border=True):
            st.write(explanation_graph_6)

        explication_graph_7 = """
        **Observations**
        Concernant le nombre d'ingrédients par recette :
        - Les recettes populaires ont un nombre d'ingrédients situé entre 4 et 16 ingrédients. 
        Cette plage de valeurs, bien que relativement large, permet tout de même d'inférer que les recettes populaires ont moins de 16 ingrédients.

        Concernant la nature de leurs ingrédients :
        - Dans le top 10, des ingrédients on retrouve les condiments ordinaires tels que le sel, le sucre, l'huile et l'eau 
        - D'autres ingrédients moins ordinaires mais tout de même communs, se retrouve dans les ingrédients les plus utilisés
        comme les oeufs, les gousses d'ail et oignons à tendance salée (les oeufs se trouvant aussi dans les recettes sucrées)

        **Interprétations**
        Le nombre et la nature des ingrédients semblent jouer un rôle dans la popularité d'une recette. 
        En effet, un nombre d'ingrédients non excessif ainsi que des ingrédients communs peuvent être
        des indicateurs d'une recette populaire. Cette observation rejoint la notion d'accessibilité des recettes 
        leur permettant d'attirer un large éventail d'utilisateurs, ne nécessitant qu'un nombre limité d'ingrédients,
        généralement présents dans la plupart des cuisines.
        """
        

        col1, col2 = st.columns(2)
        with col1:
            st.session_state["locked_graphs"]["Nombre d'ingrédients par recette"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre d'ingrédients par recette"].name}")
        with col2:
            st.session_state["locked_graphs"]["Ingrédients les plus populaires"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Ingrédients les plus populaires"].name}")

        with st.container(border=True):
            st.write(explication_graph_7)

        explication_graph_8 ="""
        **Observation :**
        Le graphe montre une concentration des recettes populaires pour un nombre de calories situé 
        entre 54 (log Calories = 4) et 1100 (log Calories = 7). En effet, cet intervalle compte environ 35000 recettes, 
        soit environ 95% des recettes
        - Plus particulièrement, une forte densité de recettes populaires est remarquée entre 190 (log Calories = 5,25) et 
        520 (log Calories = 6,25) calories, correspondant à des repas sains ou à des snacks. Dans cet intervalle se trouvent 
        19344 des recettes soit 50 % des recettes.

        Cette analyse calorique permet de conclure que les recettes à faible apport calorique sont les plus populaires notamment entre 190 et 520 calories.
        """

        st.session_state["locked_graphs"]["Calories des recettes populaires"].display_graph(
            explanation=explication_graph_8
        )
        logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Calories des recettes populaires"].name}")

        explication_graph_9 = """
        **Observation :**
        Les graphes analysent le nombre et le type des techniques de cuisine utilisées dans les recettes populaires.

        Concernant le nombre de techniques par recette, un grand nombre de recettes utilise au plus 6 techniques, dont les plus commentées (avec plus de 400 commentaires).
        Ensuite, une baisse de popularité peut être constatée jusqu'à 10 techniques par recettes et au-delà, les recettes sont peu commentées.

        Concernant les techniques employées, la "cuisson au four" et "combiner" semblent être proéminente par rapport aux autres avec plus de 50 000 recettes.
        Puis "verser", "faire bouillir", "faire fondre". La plupart de ces techniques sont basiques mais ne permettent pas de différencier un type de recettes particulier 
        car elles sont trop génériques. Cependant, la "cuisson au four" étant en tête des réponses semble indiquer que les recettes au four sont particulièrement appréciées.

        Donc, les recettes populaires utilisent peu de technique de cuisine différentes et notamment la cuisson au four. Cette tendance réaffirme que la popularité 
        est liée à l'accessibilité de la recette utilisant peu de techniques, lesquelles sont simples. 
        """
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["locked_graphs"]["Nombre de techniques de cuisine différentes par recettes"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Nombre de techniques de cuisine différentes par recettes"].name}")
        with col2:
            st.session_state["locked_graphs"]["Techniques de cuisine les plus populaires"].display_graph()
            logger.info(f"Graphique affiche : {st.session_state["locked_graphs"]["Techniques de cuisine les plus populaires"].name}")

        with st.container(border=True):
            st.write(explication_graph_9)

        conclusion = """
        **Conclusion :**
        Dans cette étude, l'évolution de la tendance a indiqué que le site, ayant connu une période de haute fréquentation entre 2002 et 2010, 
        semble aujourd'hui en manque d'activité. Pour tenter de redynamiser le site, une analyse sur la popularité des recettes a été effectuée et 
        a permis de déterminer les facteurs de succès d'une recette, à savoir une note moyenne d'au moins 4 et un nombre de commentaires d'au moins 5. 
        Enfin, les caractéristiques des recettes ainsi défini ont été examinées, permettant d'extraire les points clés de la popularité d'une recette.
        Ainsi une recette populaire doit être accessible au plus grand nombre d'utilisateurs en étant rapide, simple et peu calorique utilsant des techniques et ingrédients
        basiques et suivant un protocole concis. 

        Plus précisement, les recettes les plus populaires présentent ces caractéristiques :
        - moins de 100 minutes et moins de 17 étapes
        - entre 4 et 16 ingrédients, de préférence communs
        - moins de 6 techniques de cuisine, de préférence basiques
        - entre 190 et 520 calories

        Une deuxième étude utilisant le topic modeling est disponible dans la page "Clustering".
        Celle-ci se concentre plus sur le rapprochement des recettes populaires pour fournir des exemples et types 
        concrets de recettes. 
        """

        with st.container(border=True):
            st.write(conclusion)
        
        
    except Exception as e:
        logger.exception(f"Erreur dans la fonction principale : {e}")
        st.error("Une erreur est survenue lors de l'execution de l'application.")


if __name__ == "__main__":
    main()
