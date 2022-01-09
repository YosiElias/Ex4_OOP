from unittest import TestCase
from MVC_Algo_GraphAlgo import GraphAlgo
from MVC_Model import MainAlgo

"""
Here we performed tests for our main calculation functions.
We performed the tests for data reception and proper work with the client manually, 
since the client does not support the possibility of performing automatic tests on data reception from it.

We have seen it right that these tests test within them many 
additional auxiliary functions since they are aided by them due to their centrality

Authors: Roee Tal and Yossi Elias

"""

class TestMainAlgo(TestCase):
    def test_edge_for_pokemon_calculator(self):
        p1 = pocemon_for_test({
                        "value":5.0,
                        "type":1,
                        "pos":(35,32)
                    }, 0)
        p2 = pocemon_for_test({
            "value": 5.0,
            "type": 1,
            "pos": (32, 55)
        }, 1)
        self.pokemons = []
        self.pokemons.append(p1)
        self.pokemons.append(p2)
        # print(pokemons.pop().pos)
        self.g = GraphAlgo()
        self.g.get_graph().add_node(0, (30, 32))
        self.g.get_graph().add_node(1, (35, 32))
        self.g.get_graph().add_node(2, (35, 40))
        self.g.get_graph().add_edge(0, 1, 2.5)
        self.g.get_graph().add_edge(1, 0, 2.5)
        self.g.get_graph().add_edge(1, 2, 5)
        self.g.get_graph().add_edge(2, 1, 5)
        self.main_algo = MainAlgo(test=True, g=self.g)
        self.edges_for_po = self.main_algo.edge_for_pokemon_calculator(self.pokemons, self.g)
        self.assertEqual(2.5, self.edges_for_po.get(0).get_weight()) # p1 on edge '0'
        self.assertFalse(len(self.edges_for_po) == 2) # p2 not on edge

    def test_agent_alocate_calculator_update_multi(self):
        self.test_edge_for_pokemon_calculator()
        a0 = agent_for_test({
                        "id":0,
                        "value":0.0,
                        "src":0,
                        "dest":1,
                        "speed":1.0,
                        "pos":(35,32)
                    })
        a1 = agent_for_test({
            "id": 1,
            "value": 0.0,
            "src": 0,
            "dest": 1,
            "speed": 1.0,
            "pos": (35, 40)
        })
        self.agents = {}
        self.agents_mission = {}
        self.agents_mission[1] = [2]
        self.agents_mission[0] = [1]
        self.agents[0] = a0
        self.agents[1] = a1
        self.main_algo._pokemons = self.pokemons
        self.main_algo._alg = self.g
        self.edges_for_po = self.main_algo.agent_alocate_calculator_update_multi(self.agents, self.agents_mission, self.edges_for_po, self.g, [0,1])
        self.assertEqual(self.edges_for_po.get(1), [2, 1, 0, 1])
        self.assertEqual(self.edges_for_po.get(0), [1])








class pocemon_for_test:
    def __init__(self, dict, id):
        self.id = id
        self.value = dict.get('value')
        self.type = dict.get('type')
        self.pos = pos_for_test(dict.get('pos'))
class pos_for_test:
    def __init__(self, p:tuple):
        self.x = p[0]
        self.y = p[1]
class agent_for_test:
    def __init__(self, dict:{}):
        self.id =  dict.get("id")
        self.value = dict.get('value')
        self.src = dict.get("src")
        self.dest = dict.get("dest")
        self.speed = dict.get("speed")
        self.pos  = pos_for_test(dict.get("pos"))