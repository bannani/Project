import random
from time import time
from utils import isMyMove
from math import *
class AI() :
    def __init__(self,color,evaluate) :
        self.TIME_LIMIT = 0.5

        self.winCutoff = 20000 
        self.searchCutoff = False
        self.color=color
        self.evaluate=evaluate
    def chooseMove(self,b):
        startTime = time()
        maxScore =float("-inf")
        bestMove = None
        moves = b.generate_legal_moves()
        moves.remove(-1)
        # i have discovered a weak points in simple IA implementation they can sometimes pass even a losing position 
        # so i exploited this weak point if i'm winnig 
        if (len(moves)<81) :
            score_black, score_white = b.compute_score()
            if (self.color==1) :
                if b._lastPlayerHasPassed and score_black> score_white :
                    return -1
            if (self.color==2) :
                if b._lastPlayerHasPassed and score_black< score_white :
                    return -1
            if len(moves)==0 :
                return -1
        if len(moves)>0 :
            for move in moves :
                b.push(move)
                start = time()
                # Compute how long to spend looking at each move 
                searchTimeLimit =((self.TIME_LIMIT) / len(moves))
                score = self.iterativeDeepeningSearch(b, searchTimeLimit)
                #If the search finds a winning move
                b.pop()
                if (score >= self.winCutoff) :
                    return (move)
                if (score > maxScore) :
                    maxScore = score
                    bestMove = move
                
                #print("this move take:",time()-start)
          
        else :
            bestMove=-1
        print("time taked to move :",time()-startTime, "with score=",maxScore)
        return bestMove
    #Run an iterative deepening search on a game state, taking no longrer than the given time limit
    def iterativeDeepeningSearch(self,b,timeLimit):
        startTime = time()
        endTime = startTime + timeLimit
        depth = 1
        score = 0
        self.searchCutoff = False
        while 1:
            currentTime =time()
            if (currentTime >= endTime) :
                break
            searchResult = self.search(b, depth, float("-inf"),  float("inf"), currentTime, endTime - currentTime)
            #If the search finds a winning move, stop searching
            if (searchResult >= self.winCutoff) :
                return searchResult
            #if not (self.searchCutoff) :
            score = searchResult
            depth+=1
            
            
        return score
    # search() will perform minimax search with alpha-beta pruning on a game state, and will cut off if the given time
    # limit has elapsed since the beginning of the search
    def search(self,b, depth,alpha,beta,startTime,timeLimit) :
        moves = b.generate_legal_moves()
        myMove = isMyMove(b,self.color)
        
        score = self.evaluate(b)
        currentTime =time()
        elapsedTime = (currentTime - startTime)
        if (elapsedTime >= timeLimit) :
            self.searchCutoff = True
            return score
        #If this is a terminal node or a win for either player, abort the search
        if (self.searchCutoff or b.is_game_over() or (depth == 0) or (len(moves) == 0) or (score >= self.winCutoff) or (score <= -self.winCutoff)) :
            return score
        if (myMove):
            for move in moves :
                b.push(move)
                alpha = max([alpha, self.search(b, depth - 1, alpha, beta, startTime, timeLimit)])
                b.pop()
                if (beta <= alpha) :
                    break
            return alpha

        else :
            for move in moves :
                b.push(move)
                beta = min([beta, self.search(b, depth - 1, alpha, beta, startTime, timeLimit)])
                b.pop()
                if (beta <= alpha) :
                    break
            return beta

