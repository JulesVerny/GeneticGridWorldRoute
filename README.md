# Genetic Algorithm Grid World Path Search #

This set of Files attempts to finds the best path S[tart] to E[end] cells within a Grid World using Genetic Algorithms. 


![picture alt](https://github.com/JulesVerny/GeneticGridWorldRoute/blob/master/GridSearchResult.PNG "Grid World Path Search")

### General Method ###
An initial population, ThePopulationList of Path Genomes (Path and Fitness) is created in line 233, based upon a POPULATIONSIZE
This initial population uses a Path Generating function (GeneratePath see line 51) which generates a random walk path from the starting Cell S. The random path avoids the list of Hole cells, and avoids crossing itself by checks of cels lready in its path.
The Algorithm then goes through the main Iteration loop at line 237. 

The population list is sorted, according the fitness function (CalculateFitness). This function is calculated as the Sum of the Path length + 5 x the remaining Manhatten distance to the End Cell E. In this way there is a significant penalty in the path in not reaching the End Cell. The Genetic Algorithm objective is then to Minimise this Fitness value.

The GA algorithm selects and reuses the top 3 perfoming Paths (Genomes) by copying these into the next population and then using these as parents off offsprings.  See line 248
The two main GA offpsring methods are:
* ReturnCrossChildren  see line 179. This takes two parents, identifies a random common path node within both parent paths, and cross exchanges the paths after this common path node to return two child paths
* GenerateChildPath see line 91:  This mutates an existing path, by simply selecting a random Node within the path, and generating a new extension path from that Node 

The new Population copies across the top three performing Genome paths
The Top Three Paths are Crossed using ReturnCrossChildren to generate Three more pairs of Children see line 258
Another Three Children are Mutated from the Top three using GenerateChildPath  see line 270
The remaining population is filled with new Generated paths, using the GeneratePath, see line 278   

The New Population is copied over into the main population, for the next Iteraiton and sort.  

### Conclusions ###
The algorithm does seem to work, and it converges pretty quickly within 20 Iterations, to a reasonably optimal paths. A pretty steep initial convergence performance.

However up to 250 Iterations may be required to flesh out final wrinkles for absolute optimal paths. So absolute perfomance is reliant upon some long term slower convergence over a significant number of iterations.

  
![picture alt](https://github.com/JulesVerny/GeneticGridWorldRoute/blob/master/FinalConsole.PNG "Final Iterations")

### Useage ###
The Search is started using:
  * python GAGridWorld.py

The following files are required to run the UAV Simulation
* GAGridWorld.py     : The main script, including managing population of Path Genomes, Looping through up to ITERATIONCOUNT. It chooses the best three paths, cross mutating the best, and mutate extending others
* DisplayGrid.py     : This script displays the Grid and the Best Route, using Pygame
* RouteGenome.py  	: An Entity class to simply represent each Genome consisting of a Route Path and its associated Fitness score

### Main Python Package Dependencies: ###
pygame
