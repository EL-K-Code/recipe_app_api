En Django REST Framework (DRF), les classes **`APIView`** et **`ViewSet`** permettent de créer des API, mais elles sont utilisées de manières différentes selon ton besoin de **contrôle** vs **automatisation**.

---

## ⚖️ `APIView` vs `ViewSet` — Résumé global

| Critère                 | `APIView`                           | `ViewSet`                            |
| ----------------------- | ----------------------------------- | ------------------------------------ |
| 🧠 Niveau d'abstraction | Bas (plus de code à écrire)         | Élevé (DRF génère beaucoup pour toi) |
| 🎛 Contrôle             | Maximal (tu codes chaque méthode)   | Plus automatique, moins de contrôle  |
| 🔄 Routing / URLs       | Manuellement dans `urls.py`         | Automatiquement via `routers`        |
| 🔧 Méthodes à définir   | `get`, `post`, `put`, `patch`, etc. | `list`, `retrieve`, `create`, etc.   |

---

## 🔍 1. `APIView` – plus **classique et explicite**

Tu dois écrire **toi-même** les méthodes HTTP (`get`, `post`, `put`, etc.).

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloAPIView(APIView):

    def get(self, request):
        return Response({'message': 'Hello, GET!'})

    def post(self, request):
        return Response({'message': 'Hello, POST!'}, status=status.HTTP_201_CREATED)
```

➡️ Tu déclares **chaque méthode** manuellement. Tu as un **contrôle total**, mais c’est plus de travail.

---

## 🔍 2. `ViewSet` – plus **automatisé et structuré**

Avec un `ViewSet`, tu écris des méthodes comme `list`, `retrieve`, `create` et **le router s'occupe de générer les routes automatiquement**.

```python
from rest_framework import viewsets
from rest_framework.response import Response

class HelloViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response({'message': 'Hello from list'})

    def create(self, request):
        return Response({'message': 'Hello from create'})
```

Et dans `urls.py` :

```python
from rest_framework.routers import DefaultRouter
from .views import HelloViewSet

router = DefaultRouter()
router.register('hello', HelloViewSet, basename='hello')

urlpatterns = router.urls
```

➡️ DRF va créer automatiquement des routes comme :

* `/hello/` (GET → list, POST → create)
* `/hello/{id}/` (GET → retrieve, PUT/PATCH → update, DELETE → destroy)

---

## 🎯 Quand utiliser quoi ?

| Tu veux...                                      | Utilise... |
| ----------------------------------------------- | ---------- |
| Un **contrôle fin** sur les requêtes            | `APIView`  |
| Écrire une API **simple et rapide**             | `ViewSet`  |
| Personnaliser à fond le comportement des routes | `APIView`  |
| Générer automatiquement toutes les routes REST  | `ViewSet`  |

---

## 🧠 Résumé en une phrase

> `APIView` = tu contrôles tout manuellement.
> `ViewSet` = tu profites de la puissance du router pour suivre automatiquement les conventions REST.

---


On va créer un **mini projet DRF** avec une API pour gérer des livres, en **deux versions** :

1. 📘 **Avec `APIView`** (manuelle)
2. 📗 **Avec `ViewSet` + Router** (automatique)

---

## 📘 1. Version APIView (manuelle)

### ✅ Objectif : Gérer une liste de livres (`GET`, `POST`)

### **models.py**

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title
```

---

### **serializers.py**

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

---

### **views.py** (avec `APIView`)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

### **urls.py**

```python
from django.urls import path
from .views import BookListCreateAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
]
```

---

## 📗 2. Version ViewSet + Router (automatique)

### **views.py** (avec `ViewSet`)

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

### **urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register('books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

---

## 📊 Résultat comparatif

| Action                 | APIView route      | ViewSet route (auto)    |
| ---------------------- | ------------------ | ----------------------- |
| Liste des livres (GET) | `/books/`          | `/books/`               |
| Créer un livre (POST)  | `/books/`          | `/books/`               |
| Détail d’un livre      | ❌ (non implémenté) | `/books/<id>/`          |
| Supprimer (DELETE)     | ❌                  | `/books/<id>/` (DELETE) |
| Mettre à jour (PATCH)  | ❌                  | `/books/<id>/` (PATCH)  |

---



---

## 📘 Avec `APIView` :

Tu dois **toi-même implémenter chaque méthode HTTP** que tu veux supporter.

Par exemple, si tu veux gérer un livre avec :

* `GET` (lister ou récupérer),
* `POST` (créer),
* `PATCH` (mettre à jour),
* `DELETE` (supprimer),

👉 Tu dois **écrire chaque méthode manuellement** dans ta classe `APIView` :

```python
class BookDetailView(APIView):
    def get(self, request, pk):
        ...

    def patch(self, request, pk):
        ...

    def delete(self, request, pk):
        ...
```

🔧 **Tu as un contrôle total, mais c’est plus de code.**

---

## 📗 Avec `ViewSet` :

Tu écris **zéro méthode HTTP directement**.

Tu définis simplement :

* le **queryset** (ce que tu veux manipuler),
* le **serializer**.

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

Ensuite :

* Django REST Framework crée automatiquement les routes REST (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, etc.)
* Tu peux surcharger les méthodes **seulement si besoin** (`create`, `update`, `destroy`, etc.).

---

## 🧠 En résumé :

| 🔍 Tu veux…                          | Choix recommandé |
| ------------------------------------ | ---------------- |
| Simplicité + rapidité                | `ViewSet`        |
| Contrôle fin + logique personnalisée | `APIView`        |


