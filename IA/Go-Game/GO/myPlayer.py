# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import importlib
import Goban 
from random import choice
from playerInterface import *
from utils import *
from numpy.random import normal
from alphabeta import *
class myPlayer(PlayerInterface):
	''' Example of a random player for the go. The only tricky part is to be able to handle
	the internal representation of moves given by legal_moves() and used by push() and 
	to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

	'''

	def __init__(self):
		self._board = Goban.Board()
		self._mycolor = None
		self.corner=[19,11,25,15,55,65,61,69,40]


	def evaluate(self,board) :
		b=list(board)
		#start with corner to get more score
		score_win=100-b.count(0)
		
		for i in self.corner:
			if b[i]==self._mycolor :
				self.corner.remove(i)
				return(2000000) #corner

		
		# Score for win or lose
		score_black, score_white = self._board.compute_score()
		if (self._mycolor==1):
			score_self, score_oppo = self._board.compute_score()
		else :
			score_oppo,score_self  = self._board.compute_score()
		if ((score_self)>=(score_oppo*2) and score_oppo >4):
			#print("here !!!")
			return(2000000)

		
		# Score for endangered groups
		oppo_color=self._board.flip(self._mycolor)
		groups_self,groups_oppo=getGroups(b,self._mycolor,oppo_color)
		groups_liberties_self=libertiesOfGroups(b,groups_self,oppo_color)
		groups_liberties_oppo=libertiesOfGroups(b,groups_oppo,self._mycolor)
		
		for k in groups_liberties_self :
			if k<=1 : 
				return((score_win-10000) / 2) #lose
			
		ko=0
		for k in groups_liberties_oppo :
			if k==1 : 
				score_win=score_win +50
			if k==0 :
				ko+=1
				if (ko==2) :
					return(200000) #win
				else :
					score_win+=100
		for i in range(len(groups_self)) :
			if len(groups_self[i])>=2 :
				score_win+=len(groups_self[i])*groups_liberties_self[i]+groups_liberties_self[i]*5+20
		for i in range(len(groups_oppo)) :
			score_win=score_win-len(groups_oppo[i])*groups_liberties_oppo[i] 
		 # Score for groups
		num_groups_2lbt_self=groups_liberties_self.count(2)
		num_groups_2lbt_oppo = groups_liberties_oppo.count(2)
		score_groups = num_groups_2lbt_oppo - num_groups_2lbt_self
		# Score for liberties
		score_liberties=sum(groups_liberties_self)-sum(groups_liberties_oppo)

		
		return score_win + score_groups * normal(1, 0.1) + score_liberties * normal(1, 0.1)
	def getPlayerName(self):
		return "Team 41"

	def getPlayerMove(self):
		if self._board.is_game_over():
			print("Referee told me to play but the game is over!")
			return "PASS"
		
		ai = AI(self._mycolor,self.evaluate)
		move=ai.chooseMove(self._board)
		self._board.push(move)


		# move is an internal representation. To communicate with the interface I need to change if to a string
		return Goban.Board.flat_to_name(move) 

	def playOpponentMove(self, move):
		print("Opponent played ", move) # New here
		# the board needs an internal represetation to push the move.  Not a string
		self._board.push(Goban.Board.name_to_flat(move)) 

	def newGame(self, color):
		self._mycolor = color
		self._opponent = Goban.Board.flip(color)
	def endGame(self, winner):
		if self._mycolor == winner:
			print("I won!!!")
		else:
			print("I lost :(!!")



