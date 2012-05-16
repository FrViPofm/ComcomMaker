ComcomMaker v° 0.3
Vincent Pottier
2011-12-09
Licence GPL 3.0

***************
Installation

Mettre quelque part sur un serveur.
Chez moi c'est en mod_py.

Paramétrer l'accès à une base postGis modèle osm2pgsql
dans le fichier settings.py
***************
Notes

Si les colonnes "local_authority:FR" et "election" existent dans la base, les options de menu peuvent être dé-commentées dans index.html.

comcommaker.py peut s'utiliser en ligne de commande.
./comcommaker.py -h pour plus d'informations

***************
Issues

Des erreurs peuvent se produire si les clefs demandées dans la requête ne correspondent pas à des champs en base de donnée.
***************
*TODO
** Ajouter une bbox dans le fichier .osm transmis à JOSM
** Ajouter un contrôle "keep in mind" de la zone ouverte précédemment.

* 10 mai 2012
** ''bug'' : correction d'une régression, non export des tags du select ''in'' dans la textarea

* 21 avril 2012
** ''bug'' : correction d'une régression, non détection de clic ; ''comcom.js''
** ''bug'' : mise à zéro du compteur de process lors de l'effacement de la liste ; ''comcom.js

* 14 avril 2012
** ''ajout'' : permalink; ''comcom.js''
** ''mise à jour'' : ''render.js''

* 13 avril 2012
** ''ajout'' : édition des tags en mode ''basic''; overlays.js, comcom.js, index.html, style.css
** ''bug'' : mise à zéro du compteur de process à l'effacement.

*25 mars 2012
** ''mise à jour'' : '''overlays.js''' mise à jour de la table des overlays sur ''layers.openstreetmap.fr''

*16 mars 2012
**  ''bug'' : correction d'une régression dans la sélection des tags out ; ''comcom.js''

*15 mars 2012
** ''bugs'' :
*** adaptation du code à python 2.6 (version production) pour l'analyse des tags ; ''comcommaker.py : ''
*** correction d'adresse de serveur pour le remotecontrol ; ''comcom.js''

*14 mars 2012
** ''maintenance'' : nettoyage de fichiers
** ''mise à jour'' : adresses des overlays sur beta.letuffe ; ''overlays.js''

*5 mars 2012
** '''Ajout d'un overlay''' pour l'affichage des entités existantes avec sélection automatique de l'overlay selon le type d'entitée.

*24 février 2012
** '''Ajout d'un compteur d'entités'''.
** ''Correction d'un bug sur chemins sélectionnés'' : l'identifiant n'était pas précédé de 'w' dans la liste.
** '''Ajout au menu ''out'' d'une entrée''' ''Circonscription législative''

