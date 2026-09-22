# 🌧️ Radar — détection de pluie par capteur à auget

![MicroPython](https://img.shields.io/badge/MicroPython-2B2728?style=flat-square&logo=micropython&logoColor=white)
![Électronique](https://img.shields.io/badge/Électronique-GPIO-2563EB?style=flat-square)
![Wokwi](https://img.shields.io/badge/Simulation-Wokwi-7C3AED?style=flat-square)
![Système embarqué](https://img.shields.io/badge/Système-embarqué-059669?style=flat-square)

**Détecter la pluie pour permettre à un radar pédagogique de tenir compte des conditions météorologiques.**

Dans ce projet collectif, j'ai travaillé sur la détection de pluie à l'aide d'un **capteur à auget**, d'un **interrupteur à lames souples (ILS)** et d'un programme **MicroPython**. Le basculement du mécanisme produit un changement d'état électrique, que le programme détecte pour activer et maintenir un état « mode pluie ».

Le projet s'appuie sur un radar pédagogique existant. Mon travail porte sur le module de détection de pluie et son intégration au prototype : lorsqu'un basculement est détecté, le mode pluie adapte la vitesse limite du radar pendant une durée déterminée. Un nouveau basculement relance cette temporisation.

## 🎬 Démonstration

<p align="center">
  <a href="https://github.com/D-Berat/radar-pluie/raw/refs/heads/main/docs/videos/test-auget.mov"><img src="docs/images/test-auget.jpg" alt="Essai du mécanisme à auget avec de l'eau" width="230"></a>
  <img src="docs/images/radar.jpg" alt="Radar pédagogique utilisé comme support du projet" width="230">
</p>

**[Télécharger la vidéo de l'essai du capteur à auget](https://github.com/D-Berat/radar-pluie/raw/refs/heads/main/docs/videos/test-auget.mov)** — versement d'eau dans le mécanisme et observation des messages du programme. Vidéo originale au format MOV, à lire avec un lecteur compatible.

La photo du radar provient du site de présentation réalisé autour du même équipement. Ce site apporte du contexte sur le matériel ; il ne constitue pas une interface de pilotage du capteur.

**Repère dans la vidéo :** le capteur ILS se trouve sous l'étiquette jaune, à l'intérieur du mécanisme blanc. Les deux aimants sont placés sous les extrémités de l'auget : à chaque basculement, l'un d'eux s'approche du capteur et déclenche la détection.

## ⚙️ Principe de fonctionnement

1. L'eau s'accumule dans le mécanisme à auget.
2. L'auget bascule : l'un des deux aimants placés sous ses extrémités s'approche suffisamment de l'ILS pour le déclencher.
3. Le changement d'état est lu sur une entrée numérique.
4. Le programme incrémente un compteur et active `mode_pluie`.
5. Chaque nouvelle détection renouvelle la temporisation ; sans nouvelle détection, le mode pluie se désactive à son échéance.

```mermaid
flowchart LR
    A[Pluie] --> B[Basculement de l'auget]
    B --> C[Aimant et contact ILS]
    C --> D[Entrée GPIO 2]
    D --> E[Programme MicroPython]
    E --> F[Compteur et temporisation]
    F --> G[État mode pluie]
```

Dans le prototype intégré, ce mode adapte la vitesse limite du radar aux conditions de pluie. Les deux fichiers MicroPython documentent la partie acquisition et temporisation ; la liaison avec la commande du radar n'est pas incluse dans ces fichiers.

## 🛠️ Technologies & matériel

| Élément | Rôle |
|---|---|
| **MicroPython** | Lecture de l'entrée, compteur, temporisation et interruption |
| **`machine.Pin`** | Configuration de GPIO 2 et gestion du contact ILS |
| **ILS et deux aimants** | Détection magnétique à chaque basculement de l'auget |
| **Mécanisme à auget** | Conversion de l'accumulation d'eau en mouvement |
| **Raspberry Pi Pico W** | Carte représentée dans le schéma de simulation |
| **Wokwi** | Schéma du montage de simulation |
| **diagrams.net** | Logigramme du fonctionnement |

## 🔎 Choix du capteur

J'ai comparé un bouton, un microrupteur et un **capteur ILS**, selon leur efficacité, leur faisabilité et leur durabilité. L'ILS obtient le meilleur total dans cette grille de choix : **7,5**, contre **6,5** pour le bouton et **6** pour le microrupteur.

![Comparaison des composants pour le capteur à auget](docs/images/choix-capteur.png)

La détection magnétique permet d'actionner le contact sans appui mécanique de l'auget sur le capteur. Le positionnement des aimants est donc essentiel. Les prix figurant dans ce tableau sont ceux relevés pendant le projet.

## 💻 Deux versions du programme

| Version | Acquisition | Traitement |
|---|---|---|
| [ILS avec compteur](src/Radar%20-%20ILS_Compteur_%21.py) | Lecture de l'entrée toutes les 10 ms environ | Détection de chaque changement d'état, compteur et temporisation |
| [Code post-projet](src/Radar%20Code%20Post-Projet.py) | Interruption sur front descendant | Filtrage temporel de 200 ms et traitement de l'événement dans la boucle principale |

Dans les deux fichiers, `durée_pluie = 10 * 60` maintient le mode pluie pendant **10 minutes après la dernière détection**. La vidéo montre un essai avec une temporisation raccourcie.

La première version compte les **changements d'état** du contact : une fermeture puis une ouverture peuvent donc produire deux incréments. La version post-projet se concentre sur les fronts descendants et filtre les événements trop rapprochés. Le compteur affiché doit être interprété selon la version utilisée ; il ne constitue pas, à lui seul, une mesure calibrée de précipitations.

## 👤 Ma contribution

- Comparaison des solutions de détection et **choix du capteur ILS**.
- Programmation de l'acquisition du **capteur ILS** et du compteur associé au mécanisme à auget.
- **Positionnement précis des deux aimants** sous les extrémités de l'auget pour obtenir le déclenchement de l'ILS lors du basculement.
- Gestion du **mode pluie** et de sa temporisation réinitialisée à chaque détection.
- Travail sur les schémas du montage et le **logigramme** du fonctionnement.
- Intégration du capteur au mécanisme et essais avec de l'eau sur le prototype.
- Exploration d'une version utilisant les **interruptions** et un **filtrage anti-rebond**.

Le projet a été mené en équipe, avec des contributions complémentaires en électronique, programmation et conception mécanique. Le radar pédagogique sert de support matériel au prototype.

## 🔌 Schéma & documentation

![Schéma de simulation du capteur avec une Raspberry Pi Pico W](docs/images/schema-wokwi.png)

Le schéma représente le montage de simulation. Les éléments dessinés ne sont pas tous pilotés par les deux programmes : ceux-ci utilisent uniquement l'entrée `Pin(2, Pin.IN)`.

- [Logigramme du capteur à auget — fichier diagrams.net](docs/schemas/capteur-auget.drawio)
- [Vidéo du test avec de l'eau](https://github.com/D-Berat/radar-pluie/raw/refs/heads/main/docs/videos/test-auget.mov)

## 🧩 Logigramme

<p align="center"><img src="docs/images/logigramme.png" alt="Logigramme du capteur à auget" width="428"></p>

Ce logigramme présente la logique envisagée lors de la conception, avec une temporisation de **15 minutes**. Les deux programmes disponibles sont réglés sur **10 minutes**. Pour le comportement exécuté, se référer aux fichiers MicroPython : la désactivation intervient à l'expiration du délai après la dernière détection, même si cette condition n'est pas explicitée dans le dessin.

## 📚 Documents techniques

- [Présentation individuelle finale — PowerPoint avec vidéos](https://github.com/D-Berat/radar-pluie/releases/download/documentation/Projet.Revue.Finale.pptx)
- [Guide du module ILS ST013 — GoTronic](docs/technique/guide-ils-st013.pdf)
- [Logigramme modifiable — diagrams.net](docs/schemas/capteur-auget.drawio)

Le guide GoTronic décrit un exemple de montage sur **Arduino Uno en 5 V**. Il sert de documentation du module ; son câblage ne doit pas être repris tel quel pour la carte MicroPython du projet. Les niveaux électriques et les broches doivent correspondre à la carte utilisée.

## 📝 Retour d'expérience

Les essais avec de l'eau ont permis de vérifier le fonctionnement de la détection. Ma présentation finale souligne aussi la **fragilité de l'ILS**, qui demande du soin lors de la manipulation et du montage, ainsi que l'importance de choisir le bon environnement : **Python sur ordinateur et MicroPython sur microcontrôleur n'offrent pas les mêmes modules matériels**.

## 🚀 Exécuter le programme

Les fichiers utilisent **MicroPython** et son module `machine`. Ils sont destinés à une carte compatible, avec le capteur raccordé à **GPIO 2** et un niveau électrique au repos défini par le montage.

1. Préparer une carte avec MicroPython et le montage du capteur ILS.
2. Ouvrir l'un des deux fichiers de `src/` dans un éditeur connecté à la carte, par exemple Thonny.
3. Exécuter le fichier sur la carte et observer la console.
4. Actionner le capteur pour vérifier la détection, l'incrémentation et la réinitialisation de la temporisation.

Un lancement avec Python classique sur ordinateur ne fournit pas le module `machine`. La version post-projet utilise également `time.ticks_ms()` et `time.ticks_diff()`.

## 📁 Organisation

```text
src/                 Programmes MicroPython
docs/images/         Montage, radar et aperçu du test
docs/videos/         Vidéo de démonstration
docs/schemas/        Logigramme du capteur
docs/technique/      Documentation du module ILS
```

Projet réalisé en **STI2D, spécialité Systèmes d'information et numérique**, dans le cadre d'un prototype collectif de radar adaptatif aux conditions météorologiques.
