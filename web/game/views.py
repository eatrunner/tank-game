from django.shortcuts import render
import sys, os
sys.path.append(sys.path[0] + '/../game/')
# for tests
sys.path.append(sys.path[0] + '/../../game/')

from GameObserver import GameObserver
from GameThread import GameThread



# import models
import thread

		
# Create your views here.
class Controller(GameObserver):
	"""docstring for Controller"""
	tanks_ = []
	bullets_ = []
	game_threads_=[]
	maps_ = []

	def __init__(self):
		super(Controller, self).__init__()
		GameObserver.__init__(self)

	def updateTankPosition(self, id, pos, dir):
		for i in xrange(len(self.tanks)):
			if self.tanks_[i]['id'] == id:
				self.tanks[_i]['pos'] = pos
				self.tanks_[i]['dir'] = dir
				return 1
		return 0

	def updateBulletPosition(self, id, pos, dir):
		for i in xrange(len(self.bullets)):
			if self.bullets_[i]['id'] == id:
				self.bullets_[i]['pos'] = pos
				self.bullets_[i]['dir'] = dir
				return 1
		return 0



	def addTank(self, id, pos, dir):
		self.tanks_.append({'id':id, 'pos':pos, 'dir':dir})
	
	def removeTank(self, id):
		for i in xrange(len(self.tanks)):
			if self.tanks_[i]['id']==id:
				return self.tanks_.pop(i)		
		return None

	def addBullet(self, id, pos , dir):
		self.bullets_.append({'id':id, 'pos':pos, 'dir':dir})

	def removeBullet(self,id):
		for i in xrange(len(self.bullets)):
			if self.bullets_[i]['id']==id:
				return self.bullets_.pop(i)		
		return None

	"""game handling functions"""

	def creategame(self, params):
		if self.game_threads_ == []:
			self.game_threads_.append(GameThread(1,13))
			self.game_threads_[len(self.game_threads_)-1].addObserver(self)
			self.maps_.append(self.game_threads_[len(self.game_threads_)-1].getMap())
			return {
				"error":""
			}
		else:
			return {
				"error":"game_is_created"
			}

	def startgame(self):
		if self.game_threads_ == []:
			return {
				"error":"none games created"
			}
			
		if not self.game_threads_[0].is_alive():
			self.game_threads_[len(self.game_threads_)-1].start()
			return {
				"mapsize": self.game_threads_[0].getMapSize(),
				"error":""
			}
		else:
			return {
				"error":"game_is_running"
			}


	def stopgame(self,params):
		if self.game_threads_ == []:
			return {
				"error":"no_running_game"

			}
		else:
			self.game_threads_[0].kill()
			self.game_threads_.pop(0)
			self.maps_.pop(0)
			return {
				"error": ""
			}

	def pausegame(self, params):
		if self.game_threads_ == []:
			return {
				"error":"no_running_game"

			}
		else:
			self.game_threads_[0].pause()
			return {
				"error": ""
			}

	def resumegame(self,params):
		return {
			"error":"function not ready"
		}

	def getavalmaps(self,params):
		return {
			"error":"function not ready"
		}


	def getmap(self,params):
		"""map table of content"""
		if self.maps_ == []:
			return {
				'error':'no_maps'
			}
		else:
			try:
				tmp = self.game_threads_[0].getMap()
				return {
				'map':tmp,
				'error':""
			}
			except IndexError:
				return {
					"error":"IndexError"
				}
			
		
	def gettanks(self,params):
		"""player tank position"""
		if self.tanks_ == []:
			return {
				'error':'no_tanks'
			}
		else:
			return {
				"tanks": self.tanks_,
				"error":""
			}

	def getbullets(self,params):
		"""bullet position with given id"""
		if self.bullets_ == []:
			return {
				'error':'no_bullets'
			}
		else:
			return {
				'bullets':self.bullets_,
				'error':""
				}

	def moveplayer(self,params):
		if self.game_threads_ == []:
			return {
				'error':'no_game_threads'
			}
		else:
			try:
				self.game_threads_[params['game_id']].movePlayer(params['id'], params['dir'])
				return {
				"error": ""
				}
			except IndexError:
				return {
					"error":"IndexError"
				}
			

	def playershoot(self,params):
		if self.game_threads_ == []:
			return {
				'error':'no_game_threads'
			}
		else:
			try:
				self.game_threads_[params['game_id']].shoot(params['id'])
				return {
					"error": ""
				}
			except IndexError:
				return{
					"error":"IndexError"
				}

				

def getscores():
	"""array of best scores"""
	scores_array = Scores.objects.ordered_by("position")
	return scores_array.values_list()

def getscore(params):
	"""score with given position"""
	if params['pos']<1:
		return {"error":"wrong pos"}

	scores_array = Scores.objects.filter(position=params['pos'])
	return scores_array.values_list();