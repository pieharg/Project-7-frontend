# Projet-7-frontend

Ce répertoire regroupe les fichiers nécessaires au frontend du projet OpenClassrooms numéro 7, du parcous Data Scientist, "Implémentez un modèle de scoring".
On y retrouve le fichier permettant de générer le dashboard en utilisant la librairie Streamlit ainsi qu'un fichier requirements.txt pour les dépendances.

## Fonctionnement du dashboard

Le dashboard est hebergée gratuitement sur le cloud Streamlit et référence l'API présente sur Heroku pour son fonctionnement. Il est divisé en 3 parties distinctes :
* Obtention de prêt
* Comparaison
* Page d'informations

Le fonctionnement du dashboard et de ses différents onglets sont accessibles dans la *Page d'informations*.

## Concernant l'environnement de travail

### Dépendances

* Streamlit
* Matplotlib
* Seaborn
* Requests

### Installation dans un environnement Linux

Le dashboard est destiné, comme l'API à laquelle il est associé, à être hébergé sur un serveur cloud. Voici cependant la démarche à suivre pour un déploiement en local dans un environnement Linux.

Commencer par créer un environnement spécifique au front-end :
```sh
python3 -m venv name_environment
```

Activer ensuite l'environnement :
```sh
source name_environment/bin/activate
```

Installer les librairies nécessaires grâce au fichier requirements.txt préalablement copié dans le dossier de travail :
```sh
pip install -r requirements.txt
```

Vérifier le bon déroulé du processus :
```sh
pip list
```

La commande à effectuer pour déployer le dashboard en local est :
```sh
streamlit run dashboard.py
```

Si une fenêtre ne s'ouvre pas automatiquement, simplement recopier le lien *localhost* dans un navigateur.