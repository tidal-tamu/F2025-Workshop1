import random
import sys
import Q_Learning as ql
import pygame
from pygame.locals import *
import matplotlib.pyplot as plt


SW = 280
SH = 511

BASEY = SH *0.8
pygame.font.init()
WINDOW = pygame.display.set_mode((SW,SH))
Font = pygame.font.SysFont("comicsans",30)

# Assets
IMAGES = {}
BIRD = 'imgs/bird1.png'
BG = 'imgs/bg.png'
PIPE = 'imgs/pipe.png'


def static():
	birdxpos = int(SW/5)
	birdypos = int((SH - IMAGES['bird'].get_height())/2)
	basex = 0
	while (True):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
				return
			else :
				WINDOW.blit(IMAGES['background'],(0,0))
				WINDOW.blit(IMAGES['bird'],(birdxpos,birdypos))
				WINDOW.blit(IMAGES['base'],(basex,BASEY))
				pygame.display.update()

def game_start(generation,x,y):
	score = 0
	birdxpos = int(SW/5)
	birdypos = int(SH/2)
	basex1 = 0
	basex2 = SW

	bgx1=0
	bgx2 = IMAGES['background'].get_width()

	newPipe1 = get_new_pipe()
	newPipe2 = get_new_pipe()

	up_pipes = [
	{'x':SW +200,'y': newPipe1[0]['y']},
	{'x':SW +500 ,'y': newPipe2[0]['y']}
	]

	bttm_pipes = [
	{'x':SW+200,'y':newPipe1[1]['y']},
	{'x':SW +500 ,'y': newPipe2[1]['y']}
	]

	pipeVelx = -4

	birdyvel = -9
	birdymaxvel = 10
	birdyvelmin = -8
	birdyacc = 1

	playerFlapAccv = -8
	playerFlapped =False
	
	while(True):
		
		x_prev,y_prev = ql.bird_relative_to_pipe(birdxpos,birdypos,bttm_pipes)
		jump = False
		if ql.ai_on:
			jump = ql.ai_play(x_prev,y_prev)


		for event in pygame.event.get():
			if event.type == QUIT:
				plt.scatter(x,y)
				plt.xlabel("Number of Trials")
				plt.ylabel("Score")
				plt.title("Flappy Bird AI")
				plt.show()
				pygame.quit()
				sys.exit()
			if not ql.ai_on and event.type == KEYDOWN and (event.key == K_SPACE):
				jump = True
				

		if jump:
			if birdypos>0:
				birdyvel = playerFlapAccv
				playerFlapped = True

		
		playerMidPos= birdxpos + IMAGES['bird'].get_width()/2
		for pipe in up_pipes:
			pipeMidPos = pipe ['x'] +IMAGES['pipe'][0].get_width()/2
			if pipeMidPos <= playerMidPos < pipeMidPos +4 :

				x_new,y_new = ql.bird_relative_to_pipe(birdxpos,birdypos,bttm_pipes)
				ql.ai_passed_pipe(x_prev, y_prev, jump, x_new, y_new)
				
				score += 1
		



		if birdyvel < birdymaxvel and not playerFlapped:
			birdyvel += birdyacc


		if playerFlapped:
			playerFlapped = False

		playerHeight = IMAGES['bird'].get_height()

		birdypos = birdypos + min (birdyvel, BASEY - birdypos -playerHeight)

		for upperPipe,lowerPipe in zip(up_pipes,bttm_pipes):
			upperPipe['x'] += pipeVelx
			lowerPipe['x'] += pipeVelx

		if (0<up_pipes[0]['x']<5):
			newPipe = get_new_pipe()
			up_pipes.append(newPipe[0])
			bttm_pipes.append(newPipe[1])

		if(up_pipes[0]['x'] < -IMAGES['pipe'][0].get_width() ):
			up_pipes.pop(0)
			bttm_pipes.pop(0)
		basex1-=4
		basex2-=4
		if(basex1 <= -IMAGES['base'].get_width()):
			basex1 = basex2
			basex2 = basex1 + IMAGES['base'].get_width()

		bgx1-=2
		bgx2-=2
		if(bgx1 <= -IMAGES['background'].get_width()):
			bgx1 = bgx2
			bgx2 = bgx1 + IMAGES['background'].get_width()
		
		# Collision Detection

		birdCrashed = Collision(birdxpos,birdypos,up_pipes,bttm_pipes)
		x_new,y_new = ql.bird_relative_to_pipe(birdxpos,birdypos,bttm_pipes)
		
		if birdCrashed:
			ql.ai_crashed(x_prev, y_prev, jump, x_new, y_new)
			# ql.decay_epsilon() # decay epsilon after each episode

			return score
		else:
			ql.ai_didnt_crash(x_prev, y_prev, jump, x_new, y_new)

		WINDOW.blit(IMAGES['background'],(bgx1,0))
		WINDOW.blit(IMAGES['background'],(bgx2,0))
		for upperPipe,lowerPipe in zip(up_pipes,bttm_pipes):
			WINDOW.blit(IMAGES['pipe'][0],(upperPipe['x'],upperPipe['y']))
			WINDOW.blit(IMAGES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
		WINDOW.blit(IMAGES['base'],(basex1,BASEY))
		WINDOW.blit(IMAGES['base'],(basex2,BASEY))
		text1 = Font.render("Score: "+ str(score),1,(255,255,255))
		text2 = Font.render("Trial: "+ str(generation),1,(255,255,255))
		WINDOW.blit(text1,(SW - text1.get_width() - 5, 0))
		WINDOW.blit(text2,(0, 0))
		WINDOW.blit(IMAGES['bird'],(birdxpos,birdypos))

		pygame.display.update()
		FPSCLOCK.tick(45)

def Collision(birdxpos,birdypos,up_pipes,bttm_pipes):
	if (birdypos >= BASEY - IMAGES['bird'].get_height() or birdypos < 0):
		return True
	for pipe in up_pipes:
		pipeHeight = IMAGES['pipe'][0].get_height()
		if(birdypos < pipeHeight + pipe['y'] and abs(birdxpos - pipe['x']) < IMAGES['pipe'][0].get_width()):
			return True

	for pipe in bttm_pipes:
		if (birdypos + IMAGES['bird'].get_height() > pipe['y'] and abs(birdxpos - pipe['x']) < IMAGES['pipe'][0].get_width()):
			return True
	return False


def get_new_pipe():

	pipeHeight = IMAGES['pipe'][1].get_height()
	gap = int(SH/4)
	y2 = int(gap + random.randrange(0,int(SH - IMAGES['base'].get_height() - 1.2*gap)))
	pipex = int(SW+300 )
	y1 = int(pipeHeight -y2 +gap)

	pipe = [
	{'x':pipex,'y':-y1},
	{'x':pipex,'y':y2}
	]
	return pipe




if __name__=="__main__":

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	pygame.display.set_caption("Flappy Bird AI")

	IMAGES['base'] = pygame.image.load('imgs/base.png').convert_alpha()
	IMAGES['pipe'] = ( pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180) , pygame.image.load(PIPE).convert_alpha())
	IMAGES['background']= pygame.image.load(BG).convert()
	IMAGES['bird'] = pygame.image.load(BIRD).convert_alpha()
	generation = 1
	static()
	x=[]
	y=[]
	while(True):
		score = game_start(generation,x,y)
		if (score==-1):
			break
		x.append(generation)
		y.append(score)
		generation+=1
	
		
	print(generation)


