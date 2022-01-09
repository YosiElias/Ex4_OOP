# Oop_Ex4
This project is the final task in the course. In this assignment we get a graph, a number of agents, and pokemons. The goal of the game is to collect as much pokemons as we can in the time given to each level (0-15).

We took the graph implementation from our [prevoius assignment](https://github.com/roee-tal/EX3-OOP)



![gif](https://github.com/roee-tal/Final-project-part-2/blob/main/gif.gif)



## The algorithm
* We took inspiration from our first elevator assignment and second elevator assignment, and used the algorithms we build in our first graph assignment and second graph assignment.
* The same algorithm works on both cases of one agent and more than one, but let's separate the explanation into 2 parts:
One agent:
  1. Create an empty list that will hold the nodes that the agent has to go through
  2. Iterate over all the pokemons: if there is pokemon on some edge that connected to node that the agent is there-take this pokemon. else - find the shortest path and              distance from each one to the agent.
  3. Each time set only one pokemon to the agent(it will be the closest pokemon).

In case of more than one agent:
  * We created a dict of all the edges which saves if there is allocated pokemon on each edge, to avoid the case that 2 agents will go to the same pokemon.
  * If agent were allocated to pokemon, the fitting place in the dict became true. Only when the agent got the pokemon - the place in the dict became false - which means we       can go there once again. 
  * How do we know if the agent got the pokemon? because we have the pokemon list given from the server every time.
  * The rest is the same as one agent case.


## Download and run

First clone the project.
Next run the jar file like this: java -jar Ex4_Server_v0.0.jar __
  Instead of the underscore put a number between 0 and 15 (levels).

Last open the project in Pycharm and run the GUI file with a 3.8 python interpreter:
  Edit the configuration by changing the 'Script path' to your local directory and specify to Ex4\Client\GUI.py
