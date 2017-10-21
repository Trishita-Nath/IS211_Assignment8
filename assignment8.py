#~ ASSIGNMENT 8

#~ input argument format:

#~ for timed version: $python assignment8.py --player1 [arg] --player2 [arg] --timed
#~ for normal version: $python assignment8.py --player1 [arg] --player2 [arg] 

#~ for the players, [arg] should be "human" or "computer"

#~ eg: $python assignment8.py --player1 human --player2 computer --timed

import random
import time
import sys
import argparse


class TimedProxy:
	
	def __init__(self, time_limit = 60):
		self.start_time = time.time()
		self.time_limit = time_limit
		
	def check_time(self):
		elapsed_time = time.time() - self.start_time
		if elapsed_time > self.time_limit:
			return True
		else:
			return False
	
	def reset_time(self):
		self.start_time = time.time()	

class GameBase:
	
	@classmethod
	def play(self):
		pass	
	
	@classmethod
	def roll(self):
		pass
	
	@classmethod
	def print_scores(self):
		pass
		
	@classmethod
	def reset_game(self):
		pass
	
	@classmethod
	def check_win(self):
		pass
	
class Game(GameBase):
	
	players = []
	num_players = 2
	game_limit = 100
	timed_game = True
	proxy = None
	
	def __init__(self, player1, player2, timed = False):
		
		self.players.append(player1)
		self.players.append(player2)
		self.current_player = 0
		self.sum_roll = 0
		self.timed = timed
		if self.timed:
			self.proxy = TimedProxy(time_limit = 60)
		random.seed(0)
		self.play()
		
		
	def play(self):
		end_game = False
		while(not(end_game)):
			self.roll()
			if self.players[0].get_score() > self.players[1].get_score():
				winner = 0
			else:
				winner = 1
			
			for i in range(0, 4):
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
				
			self.print_scores()
			print "Game won by Player{}".format(winner)
			time.sleep(1)
			print "Enter 'quit' to exit or Press any key to play again."
			s = raw_input()
			if s == 'quit':
				end_game = True
			else:
				self.reset_params()
				for i in range(0, 4):
					sys.stdout.write("\033[F")
					sys.stdout.write("\033[K")


	def roll(self):
		while(True):
			self.current_player = self.current_player % self.num_players
			self.print_scores()
			print "Player {} Enter command(r/h):".format(self.current_player),
			s = self.players[self.current_player].get_roll_state(self.sum_roll)
			if s == 'r':
				die_value = (random.randint(1, 100) % 6) + 1
				print "Player {} rolled a value of {}".format(self.current_player, die_value)
				if die_value == 1:
					self.sum_roll = 0
					self.current_player = self.current_player + 1
				else:
					self.sum_roll = self.sum_roll + die_value
					if self.check_win():
						return True
			elif s == 'h':
				print "Turn Over"
				self.players[self.current_player].update_score(self.sum_roll)
				self.sum_roll = 0
				if self.check_win():
					return True
				self.current_player = self.current_player + 1
			
			else:
				print "Invalid Command"
			
			print "Roll Sum:{}".format(self.sum_roll)
			time.sleep(1)
			for i in range(0, 4):
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
			
				

	def print_scores(self):
		str_score = ''
		for i in range(0, self.num_players):
			str_score = str_score + "Player{}:{}\t".format(i, self.players[i].get_score())
		str_score = str_score + '\n'
		sys.stdout.write(str_score)
		
	def check_win(self):
		win = False
		temp_score = self.players[self.current_player].get_score() + self.sum_roll
		
		if self.timed:
			if self.proxy.check_time():
				print "Time limit reached"
				self.players[self.current_player].update_score(self.sum_roll)
				win = True
		elif (temp_score >= self.game_limit):
			print "Game limit reached"
			self.players[self.current_player].update_score(self.sum_roll)
			win = True
		
		return win
		
	def reset_params(self):
		if self.timed:
			self.proxy.reset_time()
		self.current_player = 0
		self.sum_roll = 0
		for player in self.players:
			player.reset_score()
		random.seed(0)
	
class Player:
	score = 0
	
	def update_score(self,score):
		self.score = self.score + score
	
	def get_score(self):
		return self.score
	
	def reset_score(self):
		self.score = 0
	
	def get_player_state(self):
		return self.player_state
	
	@classmethod
	def get_roll_state(self):
		pass

class Computer(Player):
	
	def __init(self):
		pass
	
	def get_roll_state(self, roll_sum):
		thresh = 25
		if (100 - self.score) < 25:
			thresh = 100 - self.score
		
		if roll_sum >= thresh:
			print 'h'
			return 'h'
		else:
			print 'r'
			return 'r'

class Human(Player):
	
	def __init(self):
		pass
	
	def get_roll_state(self, roll_sum = 0):
		s = raw_input()
		return s

class PlayerFactory:
	
	def __init__(self):
		pass
	
	def get_player(self, arg):
		player = None
		if arg == 'human':
			player = Human()
		elif arg == 'computer':
			player = Computer()
		
		return player				

	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	player1 = parser.add_argument("--player1", type=str)
	player2 = parser.add_argument("--player2", type=str)
	timed = parser.add_argument("--timed", action='store_true')

	try:
		args = parser.parse_args()
			
		pf = PlayerFactory()
			
		p1 = pf.get_player(args.player1)
		p2 = pf.get_player(args.player2)
			
		if (p1 == None) or (p2 == None):
			print "Invalid Player Arguments"
		else:
			Game(p1, p2, args.timed)
		
	except:
		
		print "Invalid Arguments Format"	
		
	
		
		
	
