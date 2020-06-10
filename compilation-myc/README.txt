Ce projet réalise un compilateur du langage "myc" vers un code C 3 adresses
recompilable avec gcc.

il permet de :
* déclarer des variables
* affecter des variables
* faire des opérations arithmétiques
* gérer les types int/float
* gestion de bloc
* gérer des pointeurs
* faire des conditions if/else
* faire des boucles while
* fonctions
* fonctions récursives

==============================================================================
Remarques :

Les variables sont stockées au fur et à mesure et afficher d'un coup à la fin.
La table des symboles contient à la fin l'ensemble des variables à afficher.
La table des registres contient à la fin l'ensemble des registres utilisés.

==============================================================================
On peut lancer une série de tests via la commande : 
make && ./test.sh

Les tests compilent un programme myc en code 3 adresses puis compilent ce code 
avec gcc.
Le test consiste alors à vérifier la valeur de retour du programme, celle-ci 
dépendant du bon déroulement des opérations réalisées par le code.