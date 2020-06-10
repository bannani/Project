# -*- coding: utf-8 -*-
''' This is the famous random player whici (almost) always looses.
'''

import time
import Goban 
from random import *
from playerInterface import *

def _isOnBoard(x,y):
        return x >= 0 and x < 9 and y >= 0 and y < 9


def flatten(coord) :
    return 9 * coord[0] + coord[1]


def voisin(i) :
    d = divmod(i, 9)
    neighbors = ((d[0]+1, d[1]), (d[0]-1, d[1]), (d[0], d[1]+1), (d[0], d[1]-1))
    v=[]
    for c in neighbors :
        if _isOnBoard(c[0], c[1]) :
            v.append(flatten(c))
    return(v)


def getGroup(l,i,color,done,v):
    v.append(i)
    neighbors=voisin(i)
    neighbors=list(set(neighbors) - set(done))
    for c in neighbors :
        done = list(dict.fromkeys(done))
        if l[c]==color  :
            done.append(c)
            getGroup(l,c,color,done,v)
        else : 
            done.append(c)
    v = list(dict.fromkeys(v))
    return (v)


def getGroups(l,color_self,color_oppo):
    g_self=[]
    g_oppo=[]
    for i in range(81) :
        if l[i]==color_self :
            fait=False
            for h in g_self :
                if i in h :
                    fait=True
                    break
            if fait==False :
                v=getGroup(l,i,color_self,[i],[])
                g_self.append(v)
        elif l[i]==color_oppo :
            fait=False
            for h in g_oppo :
                if i in h :
                    fait=True
                    break
            if fait==False :
                v=getGroup(l,i,color_oppo,[i],[])
                g_oppo.append(v)
    return(g_self,g_oppo)

def libertiesOfGroup (l,g,oppo,i=0) :
    k=[]
    for i in g :
        v=voisin(i)
        v=list(set(v) - set(g))
        k=k+v
    k = list(dict.fromkeys(k))
    liberties=0
    opp_neighbor=0
    for i in k :
        if l[i]==oppo :
            opp_neighbor+=1
        elif l[i]==0 :
            liberties+=1
    return (liberties)
def libertiesOfGroups(l,groups,oppo) :
    v=[]
    for group in groups :
        v.append(libertiesOfGroup(l,group,oppo))
    return v

def isMyMove(b,color):
    if b._nextPlayer==color :
        return False
    else :
        return True
