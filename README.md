# OOP_Ex4 - the pokemon game
![gif](https://github.com/roee-tal/Final-project-part-2/blob/main/gif.gif)

This project is the final task in the course. In this assignment we get a graph, a number of agents, and pokemons.

The goal of the game is to collect as much pokemons as we can in the time given to each level (0-15).

We took the graph implementation from our [prevoius assignment](https://github.com/roee-tal/EX3-OOP)



**Visit the [wiki](https://github.com/YosiElias/Ex4_OOP/wiki) for more information** 




## Table of contents
* [Design the project](#Design-the-project)
* [The main algorithm](#The-main-algorithm)
* [Download and run](#Download-and-run)
* [Results](#Results)
* [UML](#UML)

## Design the project
* We built our solution in the structure of MVC, we used the classes we wrote in the previous task for the purpose of using the ShortPath algorithm.
In the MAIN_ALGO class we collect the data from the client and arrange it in such a way that the functions from the previous task can work with it.
In addition from there we pass commands to the next steps in the game and update over time the GUI what to display on the screen.
* In addition, out of this class runs in the GraphAlgo class the calculation of the fastest way for the next step in the game in the most optimal way.

* It should be noted that according to the structure we created there is no direct connection between the GUI and the client and also between the GraphAlgo class and the client since the MAIN_ALGO class is responsible for the connection between them and thus it serves as a Controller, which connects the Model and the View.

* In choosing the next step of the agents we took as many considerations as possible in order to make as good a decision as possible, among them - agent speed, Pokemon value, weighted distance, agent value and more.

![This is an image](https://github.com/YosiElias/Ex4_OOP/blob/master/imgs/im6.png)

## The main algorithm
* Our idea was to allocate only one pokemon each iteration. We thought if we sort all the pokenoms in some way, the agent will miss closer pokemons, because pokemons always added. We saw the difference between those 2 attitudes in thee results. This way we got much better results.
* We took inspiration from our first elevator assignment and second elevator assignment, and used the algorithms we build in our first graph assignment and second graph assignment.
* The same algorithm works on both cases of one agent and more than one, but let's separate the explanation into 2 parts:

One agent:
  1. Create an empty list that will hold the nodes that the agent has to go through
  2. Iterate over all the pokemons: if there is pokemon on some edge that connected to node that the agent is there-take this pokemon. else - find the shortest path(using shortest path function in the graph task) and              distance from each one to the agent.
  3. Each time set only one pokemon to the agent(it will be the closest pokemon).
  4. We keep the moves to be less than 10 per second.

In case of more than one agent:
  * We created a dict of all the edges which saves if there is allocated pokemon on each edge, to avoid the case that 2 agents will go to the same pokemon.
  * If agent were allocated to pokemon, the fitting place in the dict became true. Only when the agent got the pokemon - the place in the dict became false - which means we       can go there once again. 
  * How do we know if the agent got the pokemon? because we have the pokemon list given from the server every time.
  * The rest is the same as one agent case.


## Download and run

* First clone the project.
* Next go to cmd were the project's folder is, and run the jar file like this: java -jar Ex4_Server_v0.0.jar __
  Instead of the underscore put a number between 0 and 15 (levels).

* Last open the project in Pycharm and run the **MVC_GUI file**.
* To stop the run press double esc.

**Please visit our wiki page for a short view of how the GUI looks like and how it works**
  
  
## Results

![This is an image](https://github.com/YosiElias/Ex4_OOP/blob/master/imgs/res.png)


## UML
![This is an image](https://github.com/YosiElias/Ex4_OOP/blob/master/imgs/im5.png)
