
---

## À quoi sert la méthode HTTP **PATCH** ?

* **PATCH** est une méthode HTTP utilisée pour faire une **mise à jour partielle** d’une ressource sur un serveur.

---

### Différence entre PATCH et PUT :

| Méthode   | Fonctionnement                                                                                                   |
| --------- | ---------------------------------------------------------------------------------------------------------------- |
| **PUT**   | Remplace **complètement** la ressource existante par les données envoyées. Tous les champs doivent être fournis. |
| **PATCH** | Met à jour **seulement certains champs** spécifiés dans la requête, sans toucher aux autres.                     |

---

### Exemple concret :

Imaginons une ressource utilisateur :

```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "password": "oldpassword"
}
```

* Si tu envoies un **PUT** avec seulement `{"name": "Bob"}`, le serveur pourrait remplacer toute la ressource par cet objet incomplet, supprimant les autres champs.
* Avec **PATCH**, tu peux envoyer seulement `{"name": "Bob"}`, et seuls le nom sera changé, le reste (email, password) restera intact.

---

### Pourquoi utiliser PATCH ?

* Plus sûr pour modifier **partiellement** les données.
* Évite de renvoyer tous les champs si on veut juste changer un ou deux.
* Moins de risque d’écraser des données non voulues.

---

### Dans Django REST Framework :

* `PATCH` est souvent utilisé dans les vues pour **mettre à jour partiellement** un objet.
* Ex: modifier juste le mot de passe ou le nom d’un utilisateur sans toucher aux autres données.

---

