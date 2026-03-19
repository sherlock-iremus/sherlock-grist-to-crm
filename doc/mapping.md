# 🔮 Mapper les patterns spécifiques du CIDOC CRM

## Conventions

## Problématique

Le CRM génère beaucoup de sous-entités. Par exemple, si on veut exprimer que la période Tokugawa s'étend de 1603 à 1868, cela doit passer par une instance de la classe `crm:E52_Time-Span` :

```mermaid
flowchart TB
    E4[Instance de<br>crm:E4_Period]
    E52[Instance de<br>crm:E52_Time-Span]
    P1[« Période Tokugawa »]

    E4 -->|crm:P1_is_identified_by| P1
    E4 -->|crm:P4_has_time-span| E52
    E52 -->|crm:P82a_begin_of_the_begin| 1603
    E52 -->|crm:P82b_end_of_the_end| 1868

    style P1 color:deeppink
    style 1603 color:deeppink
    style 1868 color:deeppink
```

Mais dans une interface tabulaire, on aimerait simplement saisir les données de cette façon :

| Nom              | Début | Fin  |
| ---------------- | ----- | ---- |
| Période Tokugawa | 1603  | 1868 |

Comment préserver cette ergonomie, tout en réalisant la structure CRM souhaitée, et en s'assurant que l'on contrôle bien l'URL des sous-entités qui doivent être générées ?

| Colonne (Label) | Colonne (Id)  | Record 1         | Cachable à l'utilisateur ? |
| --------------- | ------------- | ---------------- | :------------------------: |
| UUID            | `UUID`        | `UUID-1`         |           ✅<tr/>           |
| Nom             | `P1`          | Période Tokugawa |           <tr/>            |
| E52             | `P4___E52a`   | `UUID-2`         |           ✅<tr/>           |
| Début           | `E52a___P82a` | 1603             |           <tr/>            |
| Fin             | `E52a___P82b` | 1868             |           <tr/>            |

## 🧑‍🎤 Modèle de composition de DOREMUS

Le modèle [DOREMUS](https://data.doremus.org/ontology/) (basé sur une ancienne
version de [LRMoo](https://cidoc-crm.org/lrmoo/fm_releases)) génère beaucoup de
sous-entités pour établir des faits comme : « Dan Terminus et Perturbator ont
composé _The Wrath of Code_. ». Le modèle de composition est illustré
[ici](https://data.doremus.org/ontology/img/model.composition.png) et
[là](https://repository.ifla.org/rest/api/core/bitstreams/29ee4904-34e2-4ee7-a129-3bebda2f369b/content#page=12).
Il repose sur l'idée qu'une expression (F2) résulte d'un événement de création
(F28) qui agrège l'ensemble des activités (E7) qui établissent les différents
rôles tenus dans la création de l'expression.

```mermaid
flowchart TB
    F2[lrmoo:F2_Expression<br>« The Wrath of Code »]
    F28[lrmoo:F28_Expression_Creation]
    E7a[crm:E7_Activity]
    E7b[crm:E7_Activity]
    E21a[crm:E21_Person<br>« Dan Terminus »]
    E21b[crm:E21_Person<br>« Perturbator »]
    E55[crm:E55_Type<br>« Compositeur »]
    
    F2 -->|lrmoo:R17i_was_created_by| F28
    F28 -->|crm:P9_consists_of| E7a
    F28 -->|crm:P9_consists_of| E7b
    E7a -->|crm:P14_carried_out_by| E21a
    E7a -->|doremus:U31_had_function| E55
    E7b -->|crm:P14_carried_out_by| E21b
    E7b -->|doremus:U31_had_function| E55
```

### 🗃️🧑‍🎤 Table de `E21_Person`

| Colonne (Id) | Record 1     | Record 2          |
| ------------ | ------------ | ----------------- |
| `UUID`       | `UUID-1`     | `UUID-2`    <tr/> |
| `P1`         | Dan Terminus | Perturbator <tr/> |

### 🗃️🎶 Table de `F2_Expression`

| Colonne (Label)                   | Colonne (Id)      | Record 1                                                     | Cachable à l'utilisateur ? | Note    |
| --------------------------------- | ----------------- | ------------------------------------------------------------ | :------------------------: | ------- |
| Identifiant                       | `UUID`            | `UUID-3`                                                     |             ✅              | <tr/>   |
| Titre                             | `P1`              | The Wrath of Code                                            |                            | <tr/>   |
| Identifiant du F28                | `R17i___F28a`     | `UUID-4`                                                     |             ✅              | ♈ <tr/> |
| 1<sup>ère</sup> E7                | `F28a___P9___E7a` | `UUID-5`                                                     |             ✅              | ♊ <tr/> |
| Fonction de la 1<sup>ère</sup> E7 | `E7a___U31`       | [`aat:300025671`](http://vocab.getty.edu/page/aat/300025671) |                            | <tr/>   |
| Auteur de la 1<sup>ère</sup> E7   | `E7a___P14`       | `UUID-1`                                                     |                            | <tr/>   |
| 2<sup>ème</sup> E7                | `F28a___P9___E7b` | `UUID-6`                                                     |             ✅              | ♊ <tr/> |
| Fonction de la 2<sup>ème</sup> E7 | `E7b___U31`       | [`aat:300025671`](http://vocab.getty.edu/page/aat/300025671) |                            | <tr/>   |
| Auteur de la 2<sup>ème</sup> E7   | `E7b___P14`       | `UUID-2`                                                     |                            | <tr/>   |


♈ On exprime ici que la `F2` est connectée à une `F28` via `R17i`. On définit l'UUID de la sous-entité `F28` souhaité dans la cellule.
<br>
♊ On exprime ici que les `E7` sont connectés à la `F28` via `P9`. On définit les UUID des sous-entité `E7` souhaités dans la cellule.

<!--

-->

Cette approche convient quand on a un nombre « raisonnable » de E7 rattachés au F28, et qu'il est possible de créer un jeu de colonnes pour chacun d'entre eux. Dans le cas où ce nombre de E7 pourrait être important et non déterminable en amont, ils devraient être définis dans une table à part.