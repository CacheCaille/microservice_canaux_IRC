# microservice_canaux_IRC

## Objectifs du service

Ce microservice gère les canaux de discussion d’un système de type IRC. Il permet :

- La création, modification et suppression de canaux
- La gestion des utilisateurs dans un canal (invitation, bannissement, rôles)
- Le paramétrage du sujet et des modes de fonctionnement (lecture seule, privé/public)
- L’interfaçage avec d’autres services via JWT pour l’authentification

## Routes du service

Les routes principales sont décrites ci-dessous. La documentation complète (paramètres, réponses, types) est accessible via Swagger à l’URL : http://localhost:5000/apidocs

| Méthode | Endpoint                | Description                                     |
| ------- | ----------------------- | ----------------------------------------------- |
| GET     | `/channel`              | Liste des canaux publics                        |
| POST    | `/channel`              | Créer un nouveau canal                          |
| GET     | `/channel/<nom>/users`  | Liste des utilisateurs d’un canal               |
| PATCH   | `/channel/<nom>`        | Modifier le sujet / mode du canal               |
| POST    | `/channel/<nom>/topic`  | Modifier uniquement le sujet                    |
| POST    | `/channel/<nom>/mode`   | Modifier les modes (lecture seule, privé, etc.) |
| GET     | `/channel/<nom>/config` | Récupérer toute la config d’un canal            |
| POST    | `/channel/<nom>/invite` | Inviter un utilisateur                          |
| POST    | `/channel/<nom>/ban`    | Bannir un utilisateur                           |
| DELETE  | `/channel/<nom>`        | Supprimer un canal (OWNER uniquement)           |


## Instructions de lancement
```
cd microservice_canaux_IRC/service_canal
docker compose build flask_app
docker compose up --build
```
## Exemple(s) d'appel (avec JWT si besoin)

Créer un canal public :

    curl -X POST http://localhost:5000/channel \
      -H "Authorization: Bearer <TOKEN>" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "général",
        "private": false
      }'

