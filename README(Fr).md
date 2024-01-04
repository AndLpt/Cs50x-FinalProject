# CS50X - NOTE KEEPING web app avec Flask

# Vidéo démo: https://www.youtube.com/watch?v=KoBVqtJ_5zE

# Description
Ceci est mon projet final pour le cours CS50X de Harvard. J'ai conçu cette application web pour aider les étudiants dont les écoles ne proposent pas de plateforme de conservation des notes. Ils peuvent ainsi garder toutes leurs notes au même endroit et y avoir facilement accès.

## Architecture projet final
- **Flask session**

- **static**
  - fichier.js
  - IMG_0535.pdf
  - mahbod-akhzami-Fe3xy9C9wow-unsplash.jpg
  - note.png
  - pexels-jess-bailey-designs-743986.jpg
  - style.css
- **templates**
  - grades.html
  - index.html
  - layout.html
  - login.html
  - passwordchanging.html
  - register.html
  - settings.html
- **app.py**
- **helpers.py**
- **README.md**
- **requirements.txt**
- **users.db**

## **Outils utilisés** : Python, Flask, SQLite3, Bootstrap, HTML, Jinja2, CSS, JavaScript

## Frontend/ Côté utilisateur
Une fois qu'il a créé son compte et s'est connecté, l'utilisateur aura la possibilité d'effectuer plusieurs actions grâce à une succession ordonnée de pages contenues dans **templates**:
* **layout.html** c'est la page de base dont les autres sont des extensions.
* la page **register.html** permet la création d'un compte
* la page **login.html** implémente l'ouverture d'une session pour un utilisateur enregistré, et permet également à celui-ci de solliciter un changement de mot de passe.
* **passwordchanging.html** est la page depuis laquelle l'utilisateur peut changer son mot de passe lorsqu'il ne s'en rappelle plus. Il n'est pas nécessaire qu'il soit connecté par contre il doit répondre aux questions de sécurité.

  **Pour toutes pages suivantes, l'utilisateur doit être connecté pour y avoir accès.**
* la page **index.html** sert de page d'accueil depuis laquelle l'utilisateur peut ajouter ou supprimer une année de son profil.
* la page **grades.html** est la page depuis laquelle l'utilisateur peut rajouter ou supprimer un cours en indiquant la session et l'année pour plus de précision. Il peut en rajouter autant qu'il veut car l'application est conçue pour être dynamique et réactive.
* **settings.html** cette page n'est accessible que pour un utilisateur déjà connecté et lui permet de changer ses questions de sécurité et son mot de passe.
* **results.html** est la page qui retournent les résultats de ses différentes recherches à l'utilisateur.
L'application est conçue pour faciliter le plus possible la manipulation des données. En quelques clics l'utilisateur peut ajouter, supprimer ou modifier des données et la mise à jour est faite immédiatement après soumission.
L'utilisateur a également accès en tout temps à une barre de recherche qui lui permet d'accéder rapidement aux données d'un cours en particulier.

## Backend/ Côté serveur
Chaque action côté utilisateur déclenche une réaction côté serveur. J'ai fait en sorte de couvrir le plus de scénarios possibles grâce aux fichiers **app.py** et **helpers.py**. **app.py** est le cœur du projet et contrôle la quasi-totalité des réactions côté serveur grâce à l'implémentation de route. Tandis que **helpers.py** est un fichier dans lequel j'ai stocké des fonctions dont je me suis aidé pour faire rouler mon serveur. Grâce à ces deux fichiers je peux implémenter les actions suivantes :
* Contrôler comment est-ce que l'utilisateur crée un compte et se connecte à l'application.
* Définir les conditions qui doivent être remplies pour déclencher des changements précis.
* La façon de répondre à une requête de l'utilisateur à une base de données uniquement accessible côté serveur.
* Les mécanismes qui me permettent de sélectionner et de manipuler les données relatives au bon utilisateur.
* Les conditions de modification de ma base de données ainsi que l'ordre des opérations.
* Gestion de l'ouverture et de la fermeture d'une session.
* Mise à jour de la base de données quand nécessaire.

## Structure base de données
J'ai conçu une base de données pour gérer le stockage et la restitution des données aux utilisateurs. **Toutes les tables de cette base de données sont extensibles selon les besoins de l'utilisateur.**
![databasestructure](/FinalProject/static/IMG_0535-1.png)

# Améliorations possibles
En développant cette application, je me suis fixé des objectifs atteignables au vu de mes connaissances et dans un laps de temps que je m'étais donné. Et donc, plusieurs points peuvent être améliorés et le seront dans le futur.
- Vue que l'utilisateur peut rajouter autant de matières et d'examens qu'il veut, implémenter un moyen de supprimer les colonnes vides en cas de retrait de notes permettrait d'avoir une base de données moins volumineuse.
- Améliorer le style visuel de l'application en utilisant CSS afin de proposer une interface plus agréable à l'utilisateur.
- Améliorer les options de suppression notamment en permettant à l'utilisateur de supprimer uniquement certaines périodes de certains cours.
- L'expérience utilisateur de façon globale peut être améliorer en utilisant Ajax pour limiter le rafraichissement des pages lors des échanges client/serveur.


