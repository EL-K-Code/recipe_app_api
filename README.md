
# 🍽️ Recipe App API

API de gestion de recettes de cuisine, construite avec **Django REST Framework**, **Docker**, et documentée via **drf-spectacular (OpenAPI/Swagger)**.

---

## 📦 Fonctionnalités

- 🔐 Authentification par token
- 👨‍🍳 CRUD pour les recettes
- 🏷️ Ajout de tags et d’ingrédients
- 📁 Upload d’images pour les recettes
- 📊 Filtres (tags, ingrédients, assignés uniquement)
- 📄 Documentation Swagger / Redoc
- 🐳 Dockerized (prêt pour la production)
- ✅ Tests automatisés (Pytest / Django)

---

## 🚀 Stack technique

- Python 3.9
- Django & Django REST Framework
- drf-spectacular
- Postgres
- Docker / Docker Compose
- Nginx (proxy)
- Gunicorn (serveur WSGI)

---

## 🧑‍💻 Développement local

### 1. Cloner le repo

```bash
git clone https://github.com/EL-K-Code/recipe-app-api.git
cd recipe-app-api
````

### 2. Démarrer avec Docker

```bash
docker-compose up --build
```

> L’API sera disponible sur `http://localhost:8000/api/`

### 3. Créer un superuser

```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

---

## 🧪 Lancer les tests

```bash
docker-compose run --rm app sh -c "python manage.py test"
```

---

## 🖼️ Accès à la documentation de l’API

Une fois le serveur lancé :

* 📚 Swagger UI : [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
* 📘 Redoc : [http://localhost:8000/api/schema/redoc](http://localhost:8000/api/schema/redoc)

---

## 📁 Structure des fichiers importants

```
app/
├── core/              # Modèles de base (User, Tags, Ingredients, etc.)
├── recipe/            # Logique métier autour des recettes
├── user/              # Authentification / gestion utilisateur
requirements.txt       # Dépendances principales
docker-compose.yml     # Définition des services Docker
Dockerfile             # Image pour l'app Django
```

---

## 🌐 Déploiement sur serveur (ex : AWS EC2)

1. Installer Docker & Docker Compose
2. Copier les fichiers de config (env, nginx, etc.)
3. Lancer `docker-compose up -d`
4. Configurer un domaine + SSL avec Nginx / Certbot (optionnel)

---

## 📄 Licence

Ce projet est sous licence MIT – voir le fichier [LICENSE](./LICENSE) pour plus de détails.


---

## 🙌 Crédits

Développé avec ❤️ par Komla Alex LABOU.


