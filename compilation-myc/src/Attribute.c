#include "Attribute.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

static int int_reg = 1;

int new_int_reg(){
  return int_reg++;
}

static int float_reg = 1;

int new_float_reg(){
  return float_reg++;
}

attribute new_attribute () {
  attribute r;
  r = malloc (sizeof (struct ATTRIBUTE));
  r->pointer_lvl = 0;
  r->label = 0;
  r->is_param = 0;
  r->is_fun = 0;
  return r;
};

void print_reg(FILE *f, attribute x){
    /*for(int i = 0; i < x->pointer_lvl; i++){
			  fprintf(f, "*");
		}*/
    fprintf(f, "r%s%d", x->type_val == INT ? "i" : "f", x->reg_number);
}


// table des registres pour reconsituer le .h 
// avec les niveaux de pointeurs associés
struct data_int_reg{
  int r;
  int p;
  struct data_int_reg * next;
};
struct data_float_reg{
  int r;
  int p;
  struct data_float_reg * next;
};

struct data_int_reg *table_int_reg = NULL;
struct data_float_reg *table_float_reg = NULL;

void add_int_reg(int r, int p){
  struct data_int_reg *e = malloc(sizeof(struct data_int_reg));
  e->r = r;
  e->p = p;
  e->next = table_int_reg;
  table_int_reg = e;
}

void add_float_reg(int r, int p){
  struct data_float_reg *e = malloc(sizeof(struct data_float_reg));
  e->r = r;
  e->p = p;
  e->next = table_float_reg;
  table_float_reg = e;
}

void print_registers(FILE *f){
  struct data_int_reg * tracker;
	tracker = table_int_reg;
	while(tracker){
		fprintf(f, "int");
		for(int i = 0; i < tracker->p; i++){
			fprintf(f, "*");
		}
		fprintf(f, " ri%d;\n", tracker->r);
		tracker = tracker -> next;
	}
  struct data_float_reg * tracker2;
	tracker2 = table_float_reg;
	while(tracker2){
		fprintf(f, "float");
		for(int i = 0; i < tracker2->p; i++){
			fprintf(f, "*");
		}
		fprintf(f, " rf%d;\n", tracker2->r);
		tracker2 = tracker2 -> next;
	}
}

attribute dereferencer(FILE *f, attribute x){
  while (x->pointer_lvl > 0){
    attribute y = new_attribute();
    y->reg_number = new_int_reg();
    y->pointer_lvl = x->pointer_lvl - 1;
    y->block = x->block;
    add_int_reg(y->reg_number, y->pointer_lvl);
    fprintf(f, "ri%d = *ri%d;\n", y->reg_number, x->reg_number);
    x = y;
  }
  return x;
}

attribute op_attribute(attribute x, attribute y, char * op, FILE* f) {
  attribute r = new_attribute();
  
    if (x->type_val == INT && y->type_val == INT){
      r->type_val = INT;
      r->reg_number = new_int_reg();
      add_int_reg(r->reg_number, 0);
    }
    else if (x->type_val == INT && y->type_val == FLOAT){
        attribute tmp = new_attribute();
        tmp->type_val = FLOAT;
        tmp->reg_number = new_float_reg();
        r->type_val = FLOAT;
        r->reg_number = new_float_reg();
        print_reg(f, tmp); fprintf(f, " = (float) "); print_reg(f, x); fprintf(f, ";\n");
        add_float_reg(tmp->reg_number, 0);
        add_float_reg(r->reg_number, 0);
        x = tmp;
    }
    else if (x->type_val == FLOAT && y->type_val == INT){
        attribute tmp = new_attribute();
        tmp->type_val = FLOAT;
        tmp->reg_number = new_float_reg();
        r->type_val = FLOAT;
        r->reg_number = new_float_reg();
        print_reg(f, tmp); fprintf(f, " = (float) "); print_reg(f, y); fprintf(f,";\n");
        add_float_reg(tmp->reg_number, 0);
        add_float_reg(r->reg_number, 0);
        y = tmp;
    }
    else{
        r->type_val = FLOAT;
        r->reg_number = new_float_reg();
        add_float_reg(r->reg_number, 0);
    }
    r->block = get_block_courant();
    print_reg(f, r);      fprintf(f, " = ");
    print_reg(f, x);      fprintf(f, " %s ", op);
    print_reg(f, y);      fprintf(f, ";\n");
    return r;
};

attribute neg_attribute(attribute x, FILE *f){
  attribute r = new_attribute();
  if (x->type_val == INT){
    r->type_val = INT;
    r->reg_number = new_int_reg();
    add_int_reg(r->reg_number, 0);
  }
  else{
    r->type_val = FLOAT;
    r->reg_number = new_float_reg();
    add_float_reg(r->reg_number, 0);
  }
  print_reg(f, r); fprintf(f, " = - "); print_reg(f, x); fprintf(f, ";\n");
  r->block = x->block;
  return r;
};


// gestion des labels :
int new_label(){
  return label++;
}


// gestion des block :
int new_block(){
  return block++;
}

int get_block_courant(){
  //return block_courant;
  return pile_block[hauteur];
}

void empiler_block(){
  //printf("/* empile */");
  hauteur++;
  pile_block[hauteur] = new_block();
}

void depiler_block(){
  //printf("/* depile */");
  hauteur--;
  if (hauteur < 0){
    perror("trop de } !\n");
  }
}

int get_pile_block(int i){
  return pile_block[i];
}

int get_hauteur(){
  return hauteur;
}

// gestion des fonctions
int nb_param_fun=0;
attribute Pile_Param_Fun[100];

void ajout_param_fun(attribute a){
  Pile_Param_Fun[nb_param_fun] = a;
  nb_param_fun++;
}

void set_a_zero_nb_param_fun(){
  nb_param_fun=0;
}

void print_param(FILE *f,int type){
//type si c'est une func decl ou appel func
  if (type){
    fprintf(f, "%s %s", Pile_Param_Fun[nb_param_fun-1]->type_val == 0 ? "int" : "float",Pile_Param_Fun[nb_param_fun-1]->name);
    for (int i = nb_param_fun-2; i >=0; i--) {
        fprintf(f, ",%s %s",Pile_Param_Fun[i]->type_val == 0 ? "int" : "float",Pile_Param_Fun[i]->name );
    }
  }
  else {
    print_reg(f, Pile_Param_Fun[nb_param_fun-1]);
    for (int i = nb_param_fun-2; i >=0; i--) {
        fprintf(f, ", ");
        print_reg(f, Pile_Param_Fun[i]);
    }
  }
}