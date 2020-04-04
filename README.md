# Genetic Algorithm Grid World Path Search #

This set of Files attempts to finds the best path S[tart] to E[end] cells within a Grid World using Genetic Algorithms. 

![picture alt](https://github.com/JulesVerny/GeneticGridWorldRoute/blob/master/GridSearchResult.PNG "Grid World Path Search")

### General Method ###
A population ThePopulationList of Path Genomes (Path and Fitness) is created in line 233.  

The Algorithm then goes through the main Iteraiton loop at line 237. 

This initial populaiton uses a Path Generating function (GeneratePath see line 51) which generates a random walk path from teh starting Cell. (Avoiding Holes, and self crossing or repeating nodes not being permissable.) 

The population list is sorted, according the fitness function (CalculateFitness). This function is calculated as the Sum of the Path legth + 5 x the remaining manhatten distance to the End Cell. In this way there is a significant penalty in the path in not reaching the End Cell. The Genetic Algorithm is then to minimise this Fitness value.

The GA algorithm selects and reuses the top 3 perfoming Paths (Genomes) by copying these into the next population and then useing these as parents off offsprings.  See line 248

The two main GA offpsring methods are:
* ReturnCrossChildren  see line 179. This takes two parents, identifies a common path node within both parent paths, and cross exchanges the paths after the common path node
* GenerateChildPath see line 91:  This mutates an exisitg path, by simply selecting a Node within the path, and generating a new extension path from that Node 

The new Population copies across the top three performing Genome paths

The Top three Paths are Crossed using ReturnCrossChildren to generate three more pairs of Chilren see line 258

Another three Children are Mutated from the Top three using GenerateChildPath  see line 270

The remaining population is filled with new Generated paths, using the GeneratePath, see line 278   

The New Populaton si copied overinto the main poopulation, for the next Iteraiton and sort.  


### Conclusions ###
The algorithm does seem to work, and it converges pretty quickly within 20 Iterations, to a reasonably optimal paths. A pretty step initial convergence.

However up to 250 Iterations can be required to flesh out final wrinkles for absolute optimal paths. So its fairly long slow convergence for absolute perfomance. 
  
![picture alt](https://github.com/JulesVerny/GeneticGridWorldRoute/blob/master/FinalConsole.PNG "Final Iterations")

### Useage ###

The Search is started using:
  * python GAGridWorld.py

The following files are required to run the UAV Simulation
* GAGridWorld.py     : The main method, including managing population of Path Genomes, Lopping through up to 200 iterations, whilst choosing best three, cross mutating the best, and mutatation extension of others
* DisplayGrid.py     : This displays the Grid and the Best Route, usiong Pygame
* RouteGenome.py  	: An Entity class to simply represent each Genome consiting of a RoutePath, and its asociated Fitness

### Main Python Package Dependencies: ###
pygame,
