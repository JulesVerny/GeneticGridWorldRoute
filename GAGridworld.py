#
#  Experimentong with Genetic Lagorithm for  Brute Force GridWorld Route Ploicy S=G Cell Search
# 
#  requires pygame, numpy,
# ==========================================================================================
import numpy as np 
import random 
import pygame 
from random import randint
import DisplayGrid
import RouteGenome
from copy import deepcopy
# =======================================================================
# Grid World and GA Parameters
GRIDSIZE = 10
NUMBERITERATIONS = 500
POPULATIONSIZE = 20

# =======================================================================
# Create the Grid
StartCell = (0,1)  # (3,6)
EndCell = (9,8)	
Holes = [(1,1),(4,2),(5,2),(4,4),(4,6),(4,7),(3,8),(4,5),(1,5),(6,7),(7,9),(2,7),(7,3),(9,3),(8,5)] 

PolicyLength = GRIDSIZE*GRIDSIZE-len(Holes)
# ========================================================================


# ============================================================================
def ReturnCellId(coord):
	(x,y) = coord
	return x+ GRIDSIZE*y
	
def ConvertCellIdXY(Id):
	yIndex= int(Id/ GRIDSIZE)
	xIndex = Id % GRIDSIZE
	return (xIndex,yIndex) 

# =========================================================================	
def CheckProposedCellAllowed(ProposedCell,CurrentRoute):
	Allowed = True
	(XProp,YProp) = ProposedCell
	if((XProp<0) or (YProp<0) or (XProp>= GRIDSIZE) or (YProp>= GRIDSIZE)):
		Allowed = False
	if(ProposedCell in Holes):
		Allowed = False
	if(ProposedCell == StartCell):
		Allowed = False
	if(ProposedCell in CurrentRoute):
		Allowed = False
	return Allowed
# ==========================================================================
# Generte a Path Assume starting 
def GeneratePath(StartId):
	ProposedPath = []
	
	(CurrentCellX, CurrentCellY) = ConvertCellIdXY(StartId)
	PathAttempts = 0
	Complete = False
	while ((not Complete) and (PathAttempts < GRIDSIZE*4)):
		RandomDirectionInt = randint(0,100)
		(NextCellX,NextCellY) = (CurrentCellX, CurrentCellY)
		if(RandomDirectionInt<=25):
			NextCellX = CurrentCellX -1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ProposedPath)):
				ProposedPath.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)
		if((RandomDirectionInt>25) and (RandomDirectionInt<=50)):
			NextCellY = CurrentCellY -1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ProposedPath)):
				ProposedPath.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)
		if((RandomDirectionInt>50) and (RandomDirectionInt<=75)):
			NextCellX = CurrentCellX +1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ProposedPath)):
				ProposedPath.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)
		if(RandomDirectionInt>75):
			NextCellY = CurrentCellY +1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ProposedPath)):
				ProposedPath.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)

		PathAttempts = PathAttempts +1
		if((NextCellX,NextCellY) ==  EndCell):
			Complete = True

	return ProposedPath, Complete
# ==========================================================================
# Random Extend Route
def GenerateChildPath(ParentRoute):
	ChildRoute = []
	# Choose a Random Node to Mutate From
	SplittingNode = random.choice(ParentRoute)
	
	# Copy First Part of Parent into Child  - Note we DO want to copy the Endindex into the Child
	EndIndex = ParentRoute.index(SplittingNode)	
	for NodeIndex in range(0,EndIndex+1):
		ChildRoute.append(ParentRoute[NodeIndex])
	
	# Now Generate and append Forward Path 
	(CurrentCellX, CurrentCellY) = SplittingNode
	PathAttempts = 0
	Complete = False
	while ((not Complete) and (PathAttempts < GRIDSIZE*4)):
		RandomDirectionInt = randint(0,100)
		(NextCellX,NextCellY) = (CurrentCellX, CurrentCellY)
		if(RandomDirectionInt<=25):
			NextCellX = CurrentCellX -1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ChildRoute)):
				ChildRoute.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)
		if((RandomDirectionInt>25) and (RandomDirectionInt<=50)):
			NextCellY = CurrentCellY -1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ChildRoute)):
				ChildRoute.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)
		if((RandomDirectionInt>50) and (RandomDirectionInt<=75)):
			NextCellX = CurrentCellX +1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ChildRoute)):
				ChildRoute.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)
		if(RandomDirectionInt>75):
			NextCellY = CurrentCellY +1
			if(CheckProposedCellAllowed((NextCellX,NextCellY),ChildRoute)):
				ChildRoute.append((NextCellX,NextCellY))
				(CurrentCellX, CurrentCellY) = (NextCellX,NextCellY)

		PathAttempts = PathAttempts +1
		if((NextCellX,NextCellY) ==  EndCell):
			Complete = True

	return ChildRoute, Complete
# ==========================================================================
def CalculateFitness(ARoute):
	Fitness = 0.0 			# GRIDSIZE*GRIDSIZE/2.0

	# Route Distance
	for RouteLeg in ARoute:
		Fitness = Fitness + 1.0

	# Get the Final Cell
	(LastCellX, LastCellY) = ARoute[-1]
	(EndCellX,EndCellY) = EndCell
	AdditionalDistance = 5*(abs(EndCellX-LastCellX) + abs(EndCellY-LastCellY))   # 5 x Manhatten distance

	Fitness = Fitness + AdditionalDistance
	
	return Fitness
# ==========================================================================
# Define Sort function, simply by Fitness
def SortFitness(GItem):
	return GItem.Fitness
	
# =====================================================================
# Return a List of Common Nodes, so can be used for supporting Cross Mutations	
def ReturnCommonNodes(RouteA,RouteB):
	CommonNodes = [Node for Node in RouteA if Node in RouteB]
	return CommonNodes
# ====================================================================
# A function to identify a Splitting Node, which is common to Two Routes	
# Use Random Choice to Pick a random element from a list
def ReturnSplittingNode(RouteA,RouteB):
	FoundSplit = False
	RtnNode = (-1,-1)
	# Find  List of all Common Nodes
	CommonNodes = [Node for Node in RouteA if Node in RouteB]
	if(len(CommonNodes)<1):
		RtnNode = (-1,-1)
	if(len(CommonNodes)==1):
		RtnNode = CommonNodes[0]
		FoundSplit = True
	if(len(CommonNodes)>1):
		RtnNode = random.choice(CommonNodes)
		FoundSplit = True
		
	return FoundSplit,RtnNode
# =======================================================
def ReturnCrossChildren(RouteA,RouteB):
	ChildX = []
	ChildY = []

	# Find a Common Splitting Node between two parents
	SuccessCommon,SplittingNode = ReturnSplittingNode(RouteA,RouteB)
	if(SuccessCommon):
		# Find the Indexes of the Splitting Node in original parents
		IndexA = RouteA.index(SplittingNode)
		IndexB = RouteB.index(SplittingNode)
		# Copy First Part of Route A into Child X
		for NodeIndex in range(0,IndexA):
			ChildX.append(RouteA[NodeIndex])
		# Copy First Part of Route B into Child Y
		for NodeIndex in range(0,IndexB):
			ChildY.append(RouteB[NodeIndex])			
		# Copy Second Part of Route A into Child Y			
		for NodeIndex in range(IndexA,len(RouteA)):
			ChildY.append(RouteA[NodeIndex])		
		# Copy Second Part of Route B into Child X			
		for NodeIndex in range(IndexB,len(RouteB)):
			ChildX.append(RouteB[NodeIndex])		

	else:
		# No Common Split - so copy Route A into Child X and Route B into Child Y
		for ANode in RouteA:
			ChildX.append(ANode)
		for BNode in RouteB:
			ChildY.append(BNode)			

	return ChildX,ChildY
# ========================================================
def ReturnFitnessGenome(APath):
	TheFitness = CalculateFitness(APath)
	TheRouteGenome = RouteGenome.Genome(APath,TheFitness)
	return TheRouteGenome
# ========================================================
# Main GA Search Method 
def RunGASearch():
	IterationCount = 0
	ScenarioQuit = False

	StartCellId = ReturnCellId(StartCell)
	
	# Create the Display
	TheDisplay = DisplayGrid.GridDisplay(StartCell,EndCell,Holes)
	TheDisplay.UpdateDisplay()
	
	ThePopulationList = []
	
	# =============================================
	# Generate an Initial Population
	for PopI in range (0,POPULATIONSIZE):
		APath,Completed = GeneratePath(StartCellId)
		ThePopulationList.append(ReturnFitnessGenome(APath))
	
    # =================================================================
	#Main Search Loop 
	while ((IterationCount< NUMBERITERATIONS) and (not ScenarioQuit)):    
		IterationCount = IterationCount+1
				
		# Sort the Population List  - using key against SortFitness function - Do Want Sorted ascendeing so Lowest Fitness at Top of Populaiton List  
		TheSortedPoplist = sorted(ThePopulationList,key=SortFitness)
	
		TheBestPath = TheSortedPoplist[0].Path
		print("[ ",IterationCount, " ]  Best Fitness (low is Good) : ",TheSortedPoplist[0].Fitness)
		
		# Now Start Slections and Creating new Population 
		NewPopulation = []
		# Copy the Best 3 Across
		NewPopulation.append(deepcopy(TheSortedPoplist[0]))
		NewPopulation.append(deepcopy(TheSortedPoplist[1]))
		NewPopulation.append(deepcopy(TheSortedPoplist[2]))
	
		# Create Children from the Top 3
		ParentRouteA = TheSortedPoplist[0].Path
		ParentRouteB = TheSortedPoplist[1].Path
		ParentRouteC = TheSortedPoplist[2].Path
		
		ChildA, ChildB = ReturnCrossChildren(ParentRouteA,ParentRouteB)
		NewPopulation.append(ReturnFitnessGenome(ChildA))
		NewPopulation.append(ReturnFitnessGenome(ChildB))
		ChildC, ChildD = ReturnCrossChildren(ParentRouteB,ParentRouteA)
		NewPopulation.append(ReturnFitnessGenome(ChildC))
		NewPopulation.append(ReturnFitnessGenome(ChildD))
		ChildE, ChildF = ReturnCrossChildren(ParentRouteA,ParentRouteC)
		NewPopulation.append(ReturnFitnessGenome(ChildE))
		NewPopulation.append(ReturnFitnessGenome(ChildF))
		
		# Now Mutate Extend the first Three
		
		GenChildP,Completed = GenerateChildPath(ParentRouteA)
		NewPopulation.append(ReturnFitnessGenome(GenChildP))
		GenChildQ,Completed = GenerateChildPath(ParentRouteB)
		NewPopulation.append(ReturnFitnessGenome(GenChildQ))
		GenChildR,Completed = GenerateChildPath(ParentRouteC)
		NewPopulation.append(ReturnFitnessGenome(GenChildR))
		
		# And now for the remainder [12..POPULATIONSIZE]  Create completely new 
		for NewPathIndex in range(len(NewPopulation),POPULATIONSIZE):
			APath,Completed = GeneratePath(StartCellId)
			NewPopulation.append(ReturnFitnessGenome(APath))
		
		# We can now copy across the population
		ThePopulationList = deepcopy(NewPopulation)
		
	# =============================================================
	print("================================")
	print(" Search Complete: Best Fitness Result : ",TheSortedPoplist[0].Fitness)
	
	# Display the Best Result on the Grid
	TheDisplay.SetDisplayedRoute(TheSortedPoplist[0].Path)
	TheDisplay.UpdateDisplay()
		
	print(" Now Press ENTER to Exit")
	dog = input()
	
	TheDisplay.Closedown() 	# Close Down Display
	# =======================================================================
def main():
    #  Main method to perform
	print("Creating the Grid Pat Search Problem: ")
	
	RunGASearch()
	
	print()
	# =======================================================================
if __name__ == "__main__":
    main()
