/*
 *  Attribute.h
 *
 *  Created by Janin on 10/2019
 *  Copyright 2018 LaBRI. All rights reserved.
 *
 *  Module for a clean handling of attibutes values
 *
 */
#ifndef ATTRIBUTE_H
#define ATTRIBUTE_H

#include <stdlib.h>
#include <stdio.h>

typedef enum {INT, FLOAT} type;

struct ATTRIBUTE {
  char * name;
  int int_val;
  float float_val;
  type type_val;
  int reg_number;
  
  /* other attribute's fields can goes here */ 
  int pointer_lvl;  // nombre d'étoiles
  int label;
  int block;
  int is_fun; // pour les noms de fonctions
  int is_param; // pour empecher de ecrire dans .h
};

typedef struct ATTRIBUTE * attribute;

attribute new_attribute ();
/* returns the pointeur to a newly allocated (but uninitialized) attribute value structure */


attribute op_attribute(attribute x, attribute y, char * op, FILE* f);
attribute neg_attribute(attribute x, FILE *f);

// gestion des registres :
int new_int_reg();
int new_float_reg();
void print_reg(FILE*f, attribute x);
attribute dereferencer(FILE * f, attribute x);
void add_int_reg(int r, int p);
void add_float_reg(int r, int p);
void print_registers(FILE *f);

// gestion des blocs :
static int pile_block[100] = {0};
static int hauteur = 0;
static int block = 1;
int new_block();
void empiler_block();
void depiler_block(); 
int get_block_courant();

int get_pile_block(int i);

int get_hauteur();
// gestion des labels :
static int label = 1;
int new_label();
void ajout_param_fun(attribute a);
void set_a_zero_nb_param_fun();
void print_param(FILE *f,int type);
#endif

