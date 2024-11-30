from pymongo import MongoClient, errors
import dotenv
import os
import logging
import pandas as pd

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

# TODO : Commentaires à avoir en liste : Importer la liste de tout les commentaires et
# pas la liste des caractères des commentaires


class DBapi:
    def __init__(self):
        self.client = None
        try:
            self.URI = os.getenv("URI_DB")
            if not self.URI:
                raise ValueError(
                    "URI_DB n'est pas défini dans les variables d'environnement."
                )
            self.client = MongoClient(self.URI)
            self.db = self.client["MangaTaMainDF"]
            self.collection = self.db["Food.com"]
            logging.info("Connexion à la base de données établie avec succès.")
        except errors.ConfigurationError as e:
            logging.error(f"Erreur de connexion à la base de données : {e}")
        except Exception as e:
            logging.error(f"Une erreur est survenue : {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def find_by(self, colonne: str, value, nb=0):
        """
        Trouve des documents par colonne et valeur avec une limite optionnelle.
        """
        if self.client:
            try:
                cursor = self.collection.find({colonne: value})
                if nb > 0:
                    cursor = cursor.limit(nb)
                result = list(cursor)
                logging.info(
                    f"{len(result)} documents trouvés pour {colonne} = {value}."
                )
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la recherche des documents : {e}")
        return []

    def find_by_columns(self, columns: list, nb=0):
        """
        Find documents by a value in a specific column, returning only specified columns, with an optional limit.
        :param columns: List of columns to be included in the result.
        :param value: Value to filter by (default is None, meaning no filter).
        :param nb: Maximum number of documents to retrieve (default is 0, meaning no limit).
        """
        if self.client:
            try:
                # Constructing projection dynamically based on the list of columns
                projection = {column: 1 for column in columns}
                projection["_id"] = 0  # Exclude the '_id' field

                # Filter: If value is None, select all documents
                filter_query = {}  # Default filter selects all documents

                # Fetch the documents and convert to DataFrame
                documents = list(
                    self.collection.find(filter_query, projection).limit(nb)
                )
                return pd.DataFrame(documents)
            except errors.PyMongoError as e:
                print(f"Error finding documents: {e}")
                return pd.DataFrame()
        return pd.DataFrame()

    def find_range_submitted(self, begin, end):
        """
        Trouve des documents dont le champ 'submitted' est dans la plage donnée.
        """
        if self.client:
            try:
                query = {"submitted": {"$gte": begin, "$lt": end}}
                result = list(self.collection.find(query))
                logging.info(
                    f"{len(result)} documents trouvés avec 'submitted' entre {begin} et {end}."
                )
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la recherche des documents : {e}")
        return []

    def use_query(self, query):
        """
        Exécute une requête personnalisée sur la collection.
        """
        if self.client:
            try:
                result = list(self.collection.find(query))
                logging.info(
                    f"{len(result)} documents trouvés pour la requête personnalisée."
                )
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de l'exécution de la requête : {e}")
        return []

    def get_all_from(self, colonne: str):
        """
        Récupère toutes les données du champ spécifié 'colonne', en incluant 'recipe_id'.
        """
        if self.client:
            try:
                # Définir la projection pour inclure 'recipe_id' et 'colonne', exclure '_id'
                projection = {"_id": 0, "recipe_id": 1, colonne: 1}
                cursor = self.collection.find({}, projection)
                result = list(cursor)
                logging.info(
                    f"{len(result)} documents trouvés pour {colonne} avec 'recipe_id'."
                )
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la récupération des documents : {e}")
        return []

    def get_percentage(self, colonne: str, per=1):
        """
        Renvoi un pourcentage de documents aléatoires de la colone spécifiée.

        Args:
            colonne (str): Nom de la colonne.
            per (int): Pourcentage de documents à renvoyer entre 0 et 1.

        """
        if self.client:
            try:
                cursor = self.collection.aggregate(
                    [
                        {
                            "$sample": {
                                "size": int(per * self.collection.count_documents({}))
                            }
                        },
                        {"$project": {"_id": 0, colonne: 1}},
                    ]
                )
                result = list(cursor)
                logging.info(
                    f"{len(result)} documents trouvés pour {colonne} avec un pourcentage de {per}."
                )
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la récupération des documents : {e}")
        return []

    def get_percentage_documents(self, colonnes=None, per=1):
        """
        Renvoie un pourcentage de documents aléatoires avec les colonnes spécifiées.

        Args:
            colonnes (list or None): Liste des colonnes à inclure dans le résultat.
                                    Si None, toutes les colonnes sont incluses.
            per (int): Pourcentage de documents à renvoyer entre 0 et 1.

        Returns:
            list: Liste des documents correspondant au critère.
        """
        if self.client:
            try:

                projection = {"_id": 0}
                if colonnes:
                    projection.update({col: 1 for col in colonnes})

                # Créer l'agrégation
                cursor = self.collection.aggregate(
                    [
                        {
                            "$sample": {
                                "size": int(per * self.collection.count_documents({}))
                            }
                        },
                        {"$project": projection},
                    ]
                )

                result = list(cursor)
                logging.info(
                    f"{len(result)} documents trouvés avec un pourcentage de {per}."
                )
                return result
            except errors.PyMongoError as e:
                logging.error(f"Erreur lors de la récupération des documents : {e}")
        return []

    def close_connection(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.client:
            self.client.close()
            self.client = None
            logging.info("Connexion à la base de données fermée.")