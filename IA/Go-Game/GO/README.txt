utils.py 
---------
le fichier Utilis.py contient des fonctions qu'on utilise dans la fonction heuristique :
Ces fonctions nous aide à déterminer les groupe dans le groupe et leur degré de liberté
Getgroups: va parcourir tout le board et elle fait l'appel à la fonction getgroup qui determine le groupe d'une stone donnée
Getlibertiesofgroups :determine le degré de liberté pour chaque groupe donné



alphabeta.py
--------

Fichier contenant une classe qui contient les focntions de l'itérative deepning et le minmax.
En effet, pour chaque move de legal_moves, on fix un temps d'exécution pour chaque noeud et puis on fait le minmax.
Du coup chaque sous arbre de legal_moves à un temps fix d'exécution et aussi on fixe un score (wincutoff) qui va nous amener à gagner donc c'est pas necessaire de déterminer le parcours

myPlayer.py
-------------

ce fichier contient la fonction heuristique qui permet de calculer le score d'un plateau donné.
cette fonction permet de repondre à plusieurs objectifs :
1- Au départ du match, on fixe les pieces dans les coins pour controler cette zone
2- On calcule le score et si on a un score égale à 2 fois le score de l'enemie, donc on est sure qu'on va gagner et du coup, on envoie un wincutoff
3- on ajoute la taille des groupes multuplier par leur degré de liberté
4- si on a une degré de liberté=0 donc on va perdu le match
5- si l'enemie à une degré de liberté=0, peut etre on va gagner
6- puis on ajoute le score de groupe et le score des libertés





