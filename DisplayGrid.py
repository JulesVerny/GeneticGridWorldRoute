#
#  A Display Grid  Class 
# ============================================================================================
import pygame 
import math
# ===========================================================================================================
#size of our window
SCREENWIDTH = 600
SCREENHEIGHT = 600
FPS = 20	#  Experiment Performance Seems rather sensitive to Computer performance 

GRIDSIZE = 10
CELLWIDTH = 50
GRIDDISPLAYBIAS = 50

#RGB colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (140,140,140)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
# =====================================================================
# Create the Main PyGame Environment
pygame.init()
FPSCLOCK = pygame.time.Clock()
TheScreen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('GA GridWorld Search')
	
MainGameFont = pygame.font.SysFont("calibri",20)
LegItemFont = pygame.font.SysFont("calibri",16)
# =====================================================
#game class
class GridDisplay:
	def __init__(self, TheStartCell, TheEndCell,TheHoles):
		self.DisplayedRoute = []
		self.StartCell = TheStartCell
		self.EndCell = TheEndCell
		self.Holes = TheHoles
	# =====================================================================================
	def SetDisplayedRoute(self, ARoute):
		self.DisplayedRoute.clear()
		for ARouteLeg in ARoute:
			self.DisplayedRoute.append(ARouteLeg) 

	# =======================================================================
    #  Main Display Update
	def UpdateDisplay(self,):
	
		Quit = False	
		# ====================================
		#  Process Keyboard Entry
		KeyPressed = pygame.key.get_pressed()
		if (KeyPressed[pygame.K_ESCAPE]):
			print("Esc pressed")
			Quit = True  			
		pygame.event.pump() # process event queue
		# ===================================
		TheScreen.fill(BLACK)
				
		# Draw N+1 Vertical Lines
		LineLength = GRIDSIZE * CELLWIDTH
		for vindex in range (0,GRIDSIZE+1):
			pygame.draw.line(TheScreen, LIGHTGREY, (GRIDDISPLAYBIAS+vindex*CELLWIDTH,GRIDDISPLAYBIAS),(GRIDDISPLAYBIAS+vindex*CELLWIDTH,GRIDDISPLAYBIAS+LineLength))
			IndexDisplay = MainGameFont.render(str(vindex), True,WHITE)
			TheScreen.blit(IndexDisplay,(GRIDDISPLAYBIAS+15+vindex*CELLWIDTH,15))
			TheScreen.blit(IndexDisplay,(GRIDDISPLAYBIAS+15+vindex*CELLWIDTH,60+LineLength))
		
		# Now Draw the Horizontal Lines
		for hindex in range (0,GRIDSIZE+1):
			pygame.draw.line(TheScreen, LIGHTGREY, (GRIDDISPLAYBIAS,50+hindex*CELLWIDTH),(GRIDDISPLAYBIAS+LineLength,GRIDDISPLAYBIAS+hindex*CELLWIDTH))
			IndexDisplay = MainGameFont.render(str(hindex), True,WHITE)
			TheScreen.blit(IndexDisplay,(15,GRIDDISPLAYBIAS+15+hindex*CELLWIDTH))
			TheScreen.blit(IndexDisplay,(60+LineLength,GRIDDISPLAYBIAS+15+hindex*CELLWIDTH))
				
	
		# Display the Start Cell
		(XStartCell,YStartCell) = self.StartCell
		XLabelPos = GRIDDISPLAYBIAS+XStartCell*CELLWIDTH + 10
		YLabelPos = GRIDDISPLAYBIAS+YStartCell*CELLWIDTH + 20
		StartLabelDisplay = MainGameFont.render(" S " , True,RED)
		TheScreen.blit(StartLabelDisplay,(XLabelPos,YLabelPos))
	
		# Display the End Cell
		(XEndCell,YEndCell) = self.EndCell
		XLabelPos = GRIDDISPLAYBIAS+XEndCell*CELLWIDTH + 10
		YLabelPos = GRIDDISPLAYBIAS+YEndCell*CELLWIDTH + 20
		EndLabelDisplay = MainGameFont.render(" E " , True,RED)
		TheScreen.blit(EndLabelDisplay,(XLabelPos,YLabelPos))
	
		# Now Display The Holes
		for (HoleX,HoleY) in self.Holes:
			HoleRect = pygame.Rect(GRIDDISPLAYBIAS+HoleX*CELLWIDTH, GRIDDISPLAYBIAS+HoleY*CELLWIDTH, CELLWIDTH, CELLWIDTH)
			pygame.draw.rect(TheScreen, RED, HoleRect)
		
		# Now Display the Proposed Route
		Rleg = 0
		for RouteCell in self.DisplayedRoute:
			RouteLegX,RouteLegY = RouteCell
			#RouteCellRect = pygame.Rect(GRIDDISPLAYBIAS+RouteLegX*CELLWIDTH + 20, GRIDDISPLAYBIAS+RouteLegY*CELLWIDTH +20, 10, 10)
			#pygame.draw.rect(TheScreen, GREEN, RouteCellRect)
			LegLable = LegItemFont.render(str(Rleg), True,GREEN)
			TheScreen.blit(LegLable,(GRIDDISPLAYBIAS+RouteLegX*CELLWIDTH + 20,GRIDDISPLAYBIAS+RouteLegY*CELLWIDTH +20))
			Rleg = Rleg+1
	
		#Now update the PyGame Display
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
		return Quit
	# =========================================================================
	def Closedown(self,):
		pygame.quit()
	
	# ==========================================================================================