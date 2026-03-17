# 🌃 sherlock-grist-to-crm

## 🤖 Trois types de données

### Métadonnées de mapping Grist → CRM

Les métadonnées permettant d'exploiter les conventions utilisées dans les colonnes des tables Grist. Ce sont des types (`crm:E55_Type`) de titres (`crm:E35_Title`), d'appellation (`crm:E41_Appellation`), d'identifiants (`crm:E42_Identifier`) et d'annotations (`crm:P177_assigned_property_of_type`), ainsi que les prédicats RDF non CRM utilisés.

### Données d'administration des projets

Les liste des projets, personnes, collections et fichiers des projets.

### Données utilisateurs des tables Grist

Les données des tables Grist, pour lesquelles chaque ligne donne lieu à la création d'une ressource identifiée par un UUID. Pour chacune de ces ressources, il faut pouvoir spécifier :

- quel est le `rdf:type` des ressources (éventuellement avec une surcharge par ligne via une colonne `rdf:type`) ;
- à quelle `sherlock:collection` appartiennent (`sherlock:hasMember`) les ressources ;
- les différents types métiers que doit recevoir la ressource (des `crm:E55_Type` liés à la ressource par le prédicat `crm:P2_has_type`) ;
- s'il y a des annotations `crm:E13_Attribbute_Assignment`, quels en sont les auteurs (des `crm:E21_Person` via la prédicat `crm:P14_carried_out_by`) ;
- le projet (`crm:E7_Activity`) dans le contexte duquel (`sherlock:has_context_project`) la ressource a été produite ;
- si nécessaire, comment générer (à partir de quelles colonnes) un `rdfs:label`.

## 🎆 Remarques techniques

- Le graphe dans lequel iront les données est hors du périmètre de sherlock-grist-to-crm, qui ne génère que des triplets et non des quads.

## 🔮 Mapper les patterns spécifiques du CIDOC CRM

### 🧑‍🎤 Modèle de composition de DOREMUS

Le modèle [DOREMUS](https://data.doremus.org/ontology/) (basé sur une ancienne version de [LRMoo](https://cidoc-crm.org/lrmoo/fm_releases)) génère beaucoup de sous-entités pour établir des faits comme : « Dan Terminus et Perturbator ont composé *The Wrath of Code*. ». Le modèle de composition est illustré [ici](https://data.doremus.org/ontology/img/model.composition.png) et [là](https://repository.ifla.org/rest/api/core/bitstreams/29ee4904-34e2-4ee7-a129-3bebda2f369b/content#page=12). Il repose sur l'idée qu'une expression (F2) résulte d'un événement de création (F28) qui agrège l'ensemble des activités (E7) qui établissent les différents rôles tenus dans la création de l'expression.

```mermaid
flowchart TB
    F2_Expression[F2_Expression<br>« The Wrath of Code »] -->|R17i_was_created_by| F28_Expression_Creation
    F28_Expression_Creation -->|P9_consists_of| E7a
    F28_Expression_Creation -->|P9_consists_of| E7b
    E7a[E7_Activity]
    E7b[E7_Activity]
    E55_compositeur[E55_Type<br>« Compositeur »]
    E21a[E21_Person<br>« Dan Terminus »]
    E21b[E21_Person<br>« Perturbator »]
    E7a -->|P14_carried_out_by| E21a
    E7a -->|U31_has_function| E55_compositeur
    E7b -->|P14_carried_out_by| E21b
    E7b -->|U31_has_function| E55_compositeur
```

🧑‍🎤 Table des personnes :

|   UUID   | P1_is_identified_by |
| :------: | :-----------------: |
| `UUID-1` |    Dan Terminus     |
| `UUID-2` |     Perturbator     |

🎶 Table des expressions :

|   UUID   | P1_is_identified_by | 0SEa0_U31_has_function_of_type | 0SEa0_P14 | 0SEa0_UUID | 0SEb0_U31_has_function_of_type | 0SEb0_P14 | 0SEb0_UUID |
| :------: | :-----------------: | :----------------------------: | :-------: | :--------: | :----------------------------: | :-------: | :--------: |
| `UUID-3` |  The Wrath of Code  |        `aat:300025671`         | `UUID-1`  |  `UUID-4`  |        `aat:300025671`         | `UUID-2`  |  `UUID-5`  |

Le problème avec cette approche, c'est que nous ne pouvons pas connaître le nombre de E7 par F28, et qu'il faut créer autant de jeux de colonnes qu'il y a de E7.

TODO : reste à connecter les n E7 à l'unique F28.