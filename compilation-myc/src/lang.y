%code requires{
#include "Table_des_symboles.h"
#include "Attribute.h"
 }

%{

#include <stdio.h>

#include <stdlib.h>
  
extern int yylex();
extern int yyparse();

void yyerror (char* s) {
  printf ("something went wrong : %s\n",s);
  
}
FILE *f_main = NULL;
FILE *f_h = NULL;
FILE *f_fun = NULL;
FILE *current = NULL;


%}

%union { 
	attribute val;
}
%token <val> NUMI NUMF
%token <val>TINT TFLOAT STRUCT
%token <val> ID
%token AO AF PO PF PV VIR
%token RETURN VOID EQ
%token <val> IF ELSE WHILE

%token <val> AND OR NOT DIFF EQUAL SUP INF
%token <val> PLUS MOINS STAR DIV
%token DOT ARR

%left DIFF EQUAL SUP INF       // low priority on comparison
%left PLUS MOINS               // higher priority on + - 
%left STAR DIV                 // higher priority on * /
%left OR                       // higher priority on ||
%left AND                      // higher priority on &&
%left DOT ARR                  // higher priority on . and -> 
%nonassoc UNA                  // highest priority on unary operator

%type <val> vlist vir typename type exp pointer block inst_list inst bool_cond cond stat else while while_cond loop params fun fun_head fun_body app args arglist aff
 
%start prog  
 


%%

prog : block                   { fprintf(current, "return d;\n}\n"); }
;

block:
decl_list inst_list            { ; } 
;

// I. Declarations

decl_list : decl decl_list     { ; }
|                              { ; }
;

decl: var_decl PV              { ; }
| struct_decl PV               {}
| fun_decl                     {}
;

// I.1. Variables
var_decl : type vlist          { ; }
;

// I.2. Structures
struct_decl : STRUCT ID struct {}
;

struct : AO attr AF            {}
;

attr : type ID                 {}
| type ID PV attr              {}

// I.3. Functions

fun_decl : type fun            { ; }
;

fun : fun_head fun_body        { fprintf(current,";\n}\n");
                                current = f_main; }
;

fun_head : ID PO PF            { }
| ID PO params PF              {  $1->is_fun = 1;
                                  $1->type_val = $<val>0->type_val;
                                  set_symbol_value($1->name, $1);
                                 fprintf(f_h,"%s %s (",$<val>0->type_val == 0 ? "int" : "float",$1->name);
                                 print_param(f_h,1);
                                 fprintf(f_h,");\n");
                                 current = f_fun;
                                 fprintf(current,"%s %s (",$<val>0->type_val == 0 ? "int" : "float",$1->name);
                                 print_param(current,1);
                                 fprintf(current,"){\n");
                                 set_a_zero_nb_param_fun();
                                }
;

params: type ID vir params     {$2->type_val=$1->type_val;
                                $2->is_param = 1;
                                set_symbol_value($2->name, $2);
                                ajout_param_fun($2); }
| type ID                      { $$=new_attribute();
                                  $$->name=$2->name;
                                  $$->type_val=$1->type_val;
                                  $$->is_param = 1;
                                  set_symbol_value($$->name, $$);
                                   ajout_param_fun($$);}

vlist: ID vir vlist            {  if (!valid($1->name)){
                                    $1->type_val = $<val>0->type_val;
                                    $1->block = get_block_courant();
                                    $1->pointer_lvl = $<val>0->pointer_lvl;
                                    $$ = set_symbol_value($1->name, $1); 
                                  }
                                  else{
                                    printf("variable deja declaree ! %s\n", $1->name);
                                  } }
| ID                           {  if (!valid($1->name)){
                                    $1->type_val = $<val>0->type_val;
                                    $1->block = get_block_courant();
                                    $1->pointer_lvl = $<val>0->pointer_lvl;
                                    $$ = set_symbol_value($1->name, $1); 
                                  }
                                  else{
                                    printf("variable deja declaree ! %s\n", $1->name);
                                  } }
;

vir : VIR                      { $$ = $<val>-1; }
;

fun_body : AO block AF         { ; }
;

// I.4. Types
type
: typename pointer             { $$ = $1; $$->pointer_lvl = $2->pointer_lvl; }
| typename                     { $$ = $1; }
;

typename
: TINT                          { $$ = $1; }
| TFLOAT                        { $$ = $1; }
| VOID                          {}
| STRUCT ID                     {}
;

pointer
: pointer STAR                 { $$ = $1; $$->pointer_lvl = $$->pointer_lvl + 1; }
| STAR                         { $$ = $1; $$->pointer_lvl = $$->pointer_lvl + 1; }
;


// II. Intructions

inst_list: inst PV inst_list   {if ($3->label != 0){
                                  fprintf(current, "label%d :\n", $3->label);
                                  $1->label = 0;
                                }
                                else if ($1->label != 0){
                                  $1->label = 0;
                                }
                                $$ = $1;} 
| inst                         { ; } 
;

inst:
exp                           {}
| AO block AF                 { depiler_block(); } 
| aff                         {}
| ret                         {}
| cond                        { ; }
| loop                        {}
| PV                          { ; }
;


// II.1 Affectations

aff : ID EQ exp               { $$=$1;
                                if (valid($1->name)){
                                  attribute a = get_symbol_value($1->name);
                                  if (a != NULL){
                                    //$3 = dereferencer(current, $3);
                                    if (a->type_val == $3->type_val){
                                      fprintf(current, "%s = ", a->name); print_reg(current, $3); fprintf(current, ";\n");
                                    }
                                    else{
                                      if (a->type_val == FLOAT){
                                        fprintf(current, "%s = (float) ri%d;", a->name, $3->reg_number);
                                      }
                                      else{
                                        fprintf(current, "%s = (int) rf%d;", a->name, $3->reg_number);
                                      }
                                    }
                                  }
                                  else{
                                    printf("variable non declaree ! %s\n", $1->name);
                                  } }
                                  else{
                                    printf("variable non accessible ici %s\n", $1->name);
                                  } }
| STAR exp EQ exp             {   fprintf(current, "*");
                                  if ($1->type_val == $4->type_val){
                                    print_reg(current, $2); fprintf(current, " = "); print_reg(current, $4); fprintf(current, ";\n");
                                  }
                                  else{
                                    if ($1->type_val == FLOAT){
                                      print_reg(current, $2); fprintf(current, " = (float) "); print_reg(current, $4); fprintf(current, ";\n");
                                    }
                                    else{
                                      print_reg(current, $2); fprintf(current, " = (int) "); print_reg(current, $4); fprintf(current, ";\n");
                                    }
                                  }
                              }
;


// II.2 Return
ret : RETURN PO ID PF              {   attribute a = get_symbol_value($3->name);
                                        if (a != NULL){
                                          attribute b = new_attribute(); // on a besoin d'un attribut à afficher
                                          b->name = a->name;
                                          b->reg_number = a->type_val == INT ? new_int_reg() : new_float_reg();
                                          b->type_val = a->type_val;
                                          if (a->type_val == INT){
                                            add_int_reg(b->reg_number, a->pointer_lvl);
                                          }
                                          else{
                                            add_float_reg(b->reg_number, a->pointer_lvl);
                                          }
                                          print_reg(current, b); fprintf(current, " = %s;\n", a->name);
                                          fprintf(current,"return "); print_reg(current, b); fprintf(current, ";\n");
                                        }
                                        else{
                                          printf("variable non declaree !\n");
                                        } }
| RETURN PO PF                { fprintf(current,"return;"); }
;

// II.3. Conditionelles
cond :
if bool_cond stat else stat   { $$=$4;
                                fprintf(current, "label%d :", $4->label);
                                $$->label=0;}
|  if bool_cond stat          { $$=$2;
                                fprintf(current, "label%d :", $2->label);
                                $$->label=0;}
;

stat:
AO block AF                   { $$=$<val>2 ;
                                }
;



bool_cond : PO exp PF         { fprintf(current, "if (!"); print_reg(current, $2);
                                int l1 = new_label();
                                $$ = new_attribute();
                                $$->label = l1;
                                fprintf(current, ") goto label%d;\n", l1); }
;

if : IF                       { ; }
;

else : ELSE                   { int l2 = new_label();
                                fprintf(current, "goto label%d;\n",l2);
                                fprintf(current, "label%d :\n", $<val>-1->label); 
                                $<val>-1->label = 0; // desactivation pour empecher la remontée en double !
                                $$ = new_attribute();
                                $$->label = l2; }
;

// II.4. Iterations

loop : while while_cond inst  { fprintf(current, "goto label%d;\n", $1->label);
                                fprintf(current, "label%d :\n", $2->label);
                                $$ = new_attribute(); }
;

while_cond : PO exp PF        { int label = new_label();
                                fprintf(current, "if (!"); print_reg(current, $2); fprintf(current, ") goto label%d;\n", label);
                                $$ = new_attribute();
                                $$->label = label; }

while : WHILE                 { $$ = new_attribute();
                                $$->label = new_label();
                                fprintf(current, "label%d : \n", $$->label); }
;


// II.3 Expressions
exp
// II.3.0 Exp. arithmetiques
: MOINS exp %prec UNA         { $$ = neg_attribute($2, current); }
| exp PLUS exp                { $$ = op_attribute($1,$3, "+", current); }
| exp MOINS exp               { $$ = op_attribute($1,$3, "-", current); }
| exp STAR exp                { $$ = op_attribute($1,$3, "*", current); }
| exp DIV exp                 { $$ = op_attribute($1,$3, "/", current); }
| PO exp PF                   { $$ = $2; }
| ID                          { if (valid($1->name)){
                                  attribute a = get_symbol_value($1->name);
                                  if (a != NULL){
                                    $$ = new_attribute();
                                    $$->name = a->name;
                                    $$->reg_number = a->type_val == INT ? new_int_reg() : new_float_reg();
                                    $$->type_val = a->type_val;
                                    if (a->type_val == INT){
                                      add_int_reg($$->reg_number, a->pointer_lvl);
                                    }
                                    else{
                                      add_float_reg($$->reg_number, a->pointer_lvl);
                                    }
                                    print_reg(current, $$); fprintf(current, " = %s;\n", $1->name);
                                    $$->pointer_lvl = a->pointer_lvl;
                                  }
                                  else{
                                    perror("variable non declaree !\n");
                                  } }
                                  else{
                                    perror("variable non accessible ici ! \n");
                                  } }
| NUMI                        { $$ = $1;
                                $$->reg_number = new_int_reg();
                                add_int_reg($$->reg_number, 0);
                                print_reg(current, $$); fprintf(current, " = %d;\n", $1->int_val); }
| NUMF                        { $$ = $1;
                                $$->reg_number = new_float_reg();
                                add_float_reg($$->reg_number, 0);
                                print_reg(current, $$); fprintf(current, " = %f;\n", $1->float_val); }

// II.3.1 Déréférencement

| STAR exp %prec UNA          { $$ = new_attribute();
                                $$->type_val = $2->type_val;
                                $$->reg_number = ($$->type_val == INT ? new_int_reg() : new_float_reg());
                                $$->pointer_lvl = $2->pointer_lvl - 1;
                                $$->block = $2->block;
                                if ($$->type_val == INT){
                                  add_int_reg($$->reg_number, $$->pointer_lvl);
                                }
                                else{
                                  add_float_reg($$->reg_number, $$->pointer_lvl);
                                }
                                print_reg(current, $$); fprintf(current, " = *"); 
                                print_reg(current, $2); fprintf(current, ";\n"); } 
                      

// II.3.2. Booléens

| NOT exp %prec UNA           {}
| exp INF exp                 { $$ = op_attribute($1,$3, "<", current);}
| exp SUP exp                 { $$ = op_attribute($1,$3, ">", current);}
| exp EQUAL exp               { $$ = op_attribute($1,$3, "==", current);}
| exp DIFF exp                { $$ = op_attribute($1,$3, "!=", current);}
| exp AND exp                 { $$ = op_attribute($1,$3, "&&", current);}
| exp OR exp                  { $$ = op_attribute($1,$3, "||", current);}

// II.3.3. Structures

| exp ARR ID                  {}
| exp DOT ID                  {}

| app                         {}
;
       
// II.4 Applications de fonctions

app : ID PO args PF           { attribute a = get_symbol_value($1->name);
                                if (a != NULL){
                                  $$ = new_attribute();
                                  $$->type_val = a->type_val;
                                  if ($$->type_val == INT){
                                    $$->reg_number = new_int_reg();
                                    add_int_reg($$->reg_number, 0);
                                  }
                                  else{
                                    $$->reg_number = new_float_reg();
                                    add_float_reg($$->reg_number, 0);
                                  }
                                  print_reg(current, $$);
                                  fprintf(current," = %s(", $1->name); 
                                  print_param(current,0);
                                  fprintf(current,");\n"); 
                                  set_a_zero_nb_param_fun();
                                }
                                else{
                                  printf("error : fonction non declaree\n");
                                }  }
;

args :  arglist               {  }
|                             {}
;

arglist : exp VIR arglist     { ajout_param_fun($1); }
| exp                         { ajout_param_fun($1); }
;



%% 
int main () {
  f_main = fopen("main.c", "w");
  f_h = fopen("main.h", "w");
  f_fun = fopen("fun.c", "w");
  current = f_main;

  fprintf(f_main, "\nint main(){\n");
  fprintf(f_h, "#ifndef TEST_H\n#define TEST_H\n\n");
  int r = yyparse ();
  print_table(f_h);
  print_registers(f_h);
  fprintf(f_h, "#endif\n");

  fclose(f_main);
  fclose(f_h);
  fclose(f_fun);
  return r;
} 

