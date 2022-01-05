"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace

from Digraph import *
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

from GraphAlgo import GraphAlgo
import matplotlib.pyplot as plt

import time
import pygame_menu
# from pygame_menu.examples import create_example_window
import math
# import tkinter as tk
# from tkinter import filedialog
# from tkinter import END
# from tkinter import messagebox


#########################################################################################################
#                                      calculate function                                               #
#########################################################################################################



def arrow(start, end, d, h, color):
    dx =(end[0] - start[0])
    dy =(end[1] - start[1])
    D = (math.sqrt(dx * dx + dy * dy))
    xm =(D - d)
    xn =(xm)
    ym =(h)
    yn = -h
    sin = dy / D
    cos = dx / D
    x = xm * cos - ym * sin + start[0]
    ym = xm * sin + ym * cos + start[1]
    xm = x
    x = xn * cos - yn * sin + start[0]
    yn = xn * sin + yn * cos + start[1]
    xn = x
    points = [(end[0], end[1]), (int(xm), int(ym)), (int(xn), int(yn))]

    # pygame.draw.line(surface, color, start, end, width=3)
    pygame.draw.polygon(screen, color, points)

def edge_for_pokemon_calculator(pokemons, alg:GraphAlgo):
    """
    find the edge the pokemon on it
    *Note: for any run of this function the pokemon id is
    different, so this function run only with gating pokemons from client and "id's" theme
    :param pokemons: list of pokemons
    :return: dict of edge for any pokemon in time of this function
    """
    ans = {}
    for p in pokemons:
      x_p, y_p = p.pos.x, p.pos.y
      e:Edge
      for e in alg.get_graph()._Edges.values():
          src = e.get_src()
          n_src = alg.get_graph().getNode(e.get_src()).get_location()
          n_dest = alg.get_graph().getNode(e.get_dest()).get_location()
          if n_dest[0] == n_src[0]: # x1==x2
              if min(n_dest[1],n_src[1]) <= y_p <= max(n_dest[1] ,n_src[1]): # checking condition for `p` to be on line (between the points)
                  if (p.type > 0 and e.get_src() < e.get_dest()) or (p.type < 0 and e.get_src() > e.get_dest()):
                      ans[p.id] = e
                      # if not edge_pokemon_is_allocate[(e.get_src(), '-', e.get_dest())]:
                      #     edge_pokemon_value[(e.get_src(), '-', e.get_dest())] = (
                      #     edge_pokemon_value[(e.get_src(), '-', e.get_dest())][0] + p.value, -1)
                      break
          else:
            slope = (n_dest[1] - n_src[1]) / (n_dest[0] - n_src[0]) # calculating slope of two points of e
            # if e.get_src()==8 and e.get_dest() == 9:
            #     print(y_p - n_src[1])
            #     print(slope * (x_p - n_src[0]))
            if abs((y_p - n_src[1]) - (slope * (x_p - n_src[0]))) <= 0.00000001:
                if (p.type > 0  and e.get_src() < e.get_dest()) or (p.type < 0  and e.get_src() > e.get_dest()):
                    ans[p.id] = e
                    # if not edge_pokemon_is_allocate[(e.get_src(), '-', e.get_dest())]:
                    #     edge_pokemon_value[(e.get_src(), '-', e.get_dest())] = (edge_pokemon_value[(e.get_src(), '-', e.get_dest())][0] + p.value, -1)
                    break
    # print('\n\nedge_for_pokemon: ',ans,'\n')
    return ans

# decorate scale with the correct values
def my_scale(data, x=False, y=False):
  if x:
      return scale(data, 50, screen.get_width() - 50, min_x, max_x)
  if y:
      return scale(data, 50, screen.get_height() - 50, min_y, max_y)

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen

# def agent_alocate_calculator_update(agents:{}, agents_mission:{}, edge_for_pokemon:{} , alg:GraphAlgo, agent_ids):
#     """
#     calculat the best alocats of pokemon for any agent and update
#     there mission lists
#     :param agents: dict of agents
#     :param agent_ids: id's agents to check for
#     :param agents_mission: mission for now of agent
#     :param edge_for_pokemon: edge the pokemons on them
#     :param alg: main AlgoGraph
#     :return: updated agents_mission
#     """
#     p_e:Edge
#     for p_id, p_e in edge_for_pokemon.items():
#         src_id = p_e.get_src()
#         dest_id = p_e.get_dest()
#         # if not pokemon_is_alocated.get((src_id,'-',dest_id)):
#             # pokemon_is_alocated[(src_id, '-', dest_id)] = True  #Todo: need this?
#         mission_list:[]
#         min_short_path = []
#         min_dest = float('inf')
#         at_end = False
#         for agent_id, mission_list in agents_mission.items():
#             if agent_id in agent_to_allocate:
#                 agent = agents[agent_id]
#                 if src_id in mission_list and dest_id in mission_list:
#                     break # the pokemon on list of agent   #Todo: check that only internal loop is break
#                 elif src_id in mission_list and not dest_id in mission_list:
#                     if agent.src == dest_id:
#                         break
#                     mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                     print(mission_list.index(src_id))
#                     print(len(mission_list) - 1)
#                     if mission_list.index(dest_id) != (len(mission_list)-1):
#                         mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                     break
#
#                 elif not src_id in mission_list and dest_id in mission_list:
#                     if agent.src == src_id:
#                         break
#                     mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                     if mission_list.index(src_id) != (len(mission_list)- 1):
#                         mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                     break
#
#                 else:   # if not in list of mission
#                     temp_d, temp_path = alg.shortest_path(mission_list[-1], src_id)   #Todo: mission_list[-1] is the last one ?
#                     temp_d = temp_d * agent.speed
#                     if temp_d < min_dest:
#                         min_dest = temp_d
#                         min_short_path = temp_path
#                         min_agent = agent.id
#                     at_end = True
#
#         if at_end:
#             min_short_path.pop(0)
#             min_short_path.append(dest_id)
#             agents_mission[min_agent] = agents_mission[min_agent]+min_short_path
#     print(agents_mission)
#     return agents_mission
#

#
# def agent_alocate_calculator_update_multi(agents:{}, agents_mission:{}, edge_for_pokemon:{} , alg:GraphAlgo, agent_ids):
#     """
#     calculat the best alocats of pokemon for any agent and update
#     there mission lists
#     :param agents: dict of agents
#     :param agent_ids: id's agents to check for
#     :param agents_mission: mission for now of agent
#     :param edge_for_pokemon: edge the pokemons on them
#     :param alg: main AlgoGraph
#     :return: updated agents_mission
#     """
#     p_e:Edge
#
#     # for agent_id, mission_list in agents_mission.items():
#     #     first=2
#     #     delete = []
#     #     for m in mission_list:
#     #         if first == 0:
#     #             delete.append(mission_list.index(m))
#     #         else:
#     #             first =first-1
#     #     for i in delete:
#     #         del mission_list[delete.pop(0)]
#     # at_end = False
#
#     capital = 1
#     gridi = 1
#
#     for agent_id, mission_list in agents_mission.items():
#         if  len(mission_list) < 2: #agent_id in agent_ids
#             agent = agents[agent_id]
#             if len(edge_for_pokemon) == 0:
#                 print("***************************************")
#             min_dest = float('inf')
#             for p_id, p_e in edge_for_pokemon.items():
#                 src_id = p_e.get_src()
#                 dest_id = p_e.get_dest()
#                 mission_list: []
#                 min_short_path = []
#                 at_end = False
#
#                 if not edge_pokemon_value.get((src_id, '-', dest_id)):   #if pok not allocated
#
#                     p = next(n for n in pokemons if n.id == p_id)
#                     if src_id in mission_list and dest_id in mission_list:
#                         edge_pokemon_value[(src_id, '-', dest_id)] = True
#                         agents_target[agent_id] = (src_id, dest_id, p.value)
#                         break # the pokemon on list of agent   #Todo: check that only internal loop is break
#                     elif src_id in mission_list and not dest_id in mission_list:
#                         if agent.src == dest_id:
#                             edge_pokemon_value[(src_id, '-', dest_id)] = True
#                             agents_target[agent_id] = (src_id, dest_id,p.value)
#                             break
#                         mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                         print(mission_list.index(src_id))
#                         print(len(mission_list) - 1)
#                         if mission_list.index(dest_id) != (len(mission_list)-1):
#                             mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                         edge_pokemon_value[(src_id, '-', dest_id)] = True
#                         agents_target[agent_id] = (src_id, dest_id, p.value)
#                         break
#
#                     elif not src_id in mission_list and dest_id in mission_list:
#                         if agent.src == src_id:
#                             edge_pokemon_value[(src_id, '-', dest_id)] = True
#                             agents_target[agent_id] = (src_id, dest_id, p.value)
#                             break
#                         mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                         if mission_list.index(src_id) != (len(mission_list)- 1):
#                             mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                         edge_pokemon_value[(src_id, '-', dest_id)] = True
#                         agents_target[agent_id] = (src_id, dest_id, p.value)
#                         break
#
#                     else:   # if not in list of mission
#                         temp_d, temp_path = alg.shortest_path(mission_list[-1], src_id)   #Todo: mission_list[-1] is the last one ?
#                         # p = [p for p in pokemons if p.id==p_id]
#                         temp_d = (temp_d * (agent.value *capital)* agent.speed)/ (p.value ** gridi)
#                         if temp_d < min_dest:
#                             min_dest = temp_d
#                             min_short_path = temp_path
#                             min_short_path.append(dest_id)
#                             min_agent = agent.id
#                             min_src_id = src_id
#                             min_dest_id = dest_id
#                         at_end = True
#
#             if at_end:
#                 # src_target, dest_terget, p_tar_val = agents_target.get(agent_id)
#                 # temp_d, temp_path = alg.shortest_path(mission_list[0], src_target)
#                 # temp_d = (temp_d * agent.value * capital * agent.speed) / (p_tar_val * gridi)
#                 #
#                 # if src_target == agent.src or -1 == agent.dest or min_dest < temp_d:
#                 min_short_path.pop(0)
#                 # min_short_path.append(dest_id)
#                 edge_pokemon_value[(min_src_id, '-', min_dest_id)] = True
#                 agents_target[agent_id] = (src_id, dest_id, p.value)
#                 agents_mission[agent.id] = agents_mission[agent.id]+min_short_path
#     print(agents_mission)
#     return agents_mission
#
#
#
# def agent_alocate_calculator_update_realtime(agents:{}, agents_mission:{}, edge_for_pokemon:{} , alg:GraphAlgo, agent_ids):
#     """
#     calculat the best alocats of pokemon for any agent and update
#     there mission lists
#     :param agents: dict of agents
#     :param agent_ids: id's agents to check for
#     :param agents_mission: mission for now of agent
#     :param edge_for_pokemon: edge the pokemons on them
#     :param alg: main AlgoGraph
#     :return: updated agents_mission
#     """
#     p_e:Edge
#
#     # for agent_id, mission_list in agents_mission.items():
#     #     first=2
#     #     delete = []
#     #     for m in mission_list:
#     #         if first == 0:
#     #             delete.append(mission_list.index(m))
#     #         else:
#     #             first =first-1
#     #     for i in delete:
#     #         del mission_list[delete.pop(0)]
#     # at_end = False
#
#     capital = 5
#     gridi = 0.1
#
#     for agent_id, mission_list in agents_mission.items():
#         if agent_id in agent_ids and len(mission_list) < 2:
#             agent = agents[agent_id]
#             if len(edge_for_pokemon) == 0:
#                 print("***************************************")
#             for p_id, p_e in edge_for_pokemon.items():
#                 src_id = p_e.get_src()
#                 dest_id = p_e.get_dest()
#                 mission_list: []
#                 min_short_path = []
#                 min_dest = float('inf')
#                 at_end = False
#
#                 if not edge_pokemon_value.get((src_id, '-', dest_id)):   #if pok not allocated
#
#                     p = next(n for n in pokemons if n.id == p_id)
#                     if src_id in mission_list and dest_id in mission_list:
#                         edge_pokemon_value[(src_id, '-', dest_id)] = True
#                         agents_target[agent_id] = (src_id, dest_id, p.value)
#                         break # the pokemon on list of agent   #Todo: check that only internal loop is break
#                     elif src_id in mission_list and not dest_id in mission_list:
#                         if agent.src == dest_id:
#                             edge_pokemon_value[(src_id, '-', dest_id)] = True
#                             agents_target[agent_id] = (src_id, dest_id,p.value)
#                             break
#                         mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                         print(mission_list.index(src_id))
#                         print(len(mission_list) - 1)
#                         if mission_list.index(dest_id) != (len(mission_list)-1):
#                             mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                         edge_pokemon_value[(src_id, '-', dest_id)] = True
#                         agents_target[agent_id] = (src_id, dest_id, p.value)
#                         break
#
#                     elif not src_id in mission_list and dest_id in mission_list:
#                         if agent.src == src_id:
#                             edge_pokemon_value[(src_id, '-', dest_id)] = True
#                             agents_target[agent_id] = (src_id, dest_id, p.value)
#                             break
#                         mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                         if mission_list.index(src_id) != (len(mission_list)- 1):
#                             mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                         edge_pokemon_value[(src_id, '-', dest_id)] = True
#                         agents_target[agent_id] = (src_id, dest_id, p.value)
#                         break
#
#                     else:   # if not in list of mission
#                         temp_d, temp_path = alg.shortest_path(mission_list[0], src_id)   #Todo: mission_list[-1] is the last one ?
#                         # p = [p for p in pokemons if p.id==p_id]
#                         temp_d = (temp_d * (agent.value *capital)* agent.speed)/ (p.value ** gridi)
#                         if temp_d < min_dest:
#                             min_dest = temp_d
#                             min_short_path = temp_path
#                             min_short_path.append(dest_id)
#                             min_agent = agent.id
#                             min_src_id = src_id
#                             min_dest_id = dest_id
#                         at_end = True
#
#             if at_end:
#                 start = min_short_path.pop(0)   #pop -> mission_list[0]
#                 edge_pokemon_value[(min_src_id, '-', min_dest_id)] = True
#                 agents_target[agent_id] = (src_id, dest_id, p.value)
#                 agents_mission[agent.id] = agents_mission[agent.id][agents_mission[agent.id].index(start):]
#                 agents_mission[agent.id] = agents_mission[agent.id]+min_short_path
#     print(agents_mission)
#     return agents_mission

# def agent_alocate_calculator_update_alon(agents: {}, agents_mission: {}, edge_for_pokemon: {}, alg: GraphAlgo,
#                                          agent_ids):
#         """
#         calculat the best alocats of pokemon for any agent and update
#         there mission lists
#         :param agents: dict of agents
#         :param agent_ids: id's agents to check for
#         :param agents_mission: mission for now of agent
#         :param edge_for_pokemon: edge the pokemons on them
#         :param alg: main AlgoGraph
#         :return: updated agents_mission
#         """
#
#         p_e: Edge
#
#         for agent_id, mission_list in agents_mission.items():
#             if len(mission_list) < 2:#agent_id in agent_ids and
#                 agent = agents[agent_id]
#                 min_dest = float('inf')
#                 min_short_path = []
#                 at_end = False
#
#                 for p_id, p_e in edge_for_pokemon.items():
#                     src_id = p_e.get_src()
#                     dest_id = p_e.get_dest()
#                     mission_list: []
#                     # min_short_path = []
#                     # min_dest = float('inf')
#
#                     if edge_pokemon_value.get((src_id, '-', dest_id))[0] > 0 or edge_pokemon_value.get((src_id, '-', dest_id))[1] == agent_id or edge_pokemon_value.get((src_id, '-', dest_id))[1] == -1:  # if pok not allocated
#                         # for l in agents_mission:
#                         #     if l != agent_id:
#                         #         if agents_mission.get(l)[len(agents_mission.get(l))-1] != dest_id:
#                         print( edge_pokemon_value.get((src_id, '-', dest_id)),'  ->  ',src_id, '->', dest_id)
#                         print(agents_mission)
#
#                         if src_id in mission_list and dest_id in mission_list:
#                             edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                             edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                             break  # the pokemon on list of agent   #Todo: check that only internal loop is break
#                         elif src_id in mission_list and not dest_id in mission_list:
#                             if agent.src == dest_id:
#                                 edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                                 edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                                 break
#                             mission_list.insert(mission_list.index(src_id) + 1, dest_id)
#                             print(mission_list.index(src_id))
#                             print(len(mission_list) - 1)
#                             if mission_list.index(dest_id) != (len(mission_list) - 1):
#                                 mission_list.insert(mission_list.index(dest_id) + 1, src_id)
#                             edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                             edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                             break
#
#                         elif not src_id in mission_list and dest_id in mission_list:
#                             if agent.src == src_id:
#                                 edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                                 edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                                 break
#                             mission_list.insert(mission_list.index(dest_id) + 1, src_id)
#                             if mission_list.index(src_id) != (len(mission_list) - 1):
#                                 mission_list.insert(mission_list.index(src_id) + 1, dest_id)
#                             edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                             edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                             break
#
#                         else:  # if not in list of mission
#                             temp_d, temp_path = alg.shortest_path(mission_list[0],
#                                                                   src_id)  # Todo: mission_list[-1] is the last one ?
#                             # p = [p for p in pokemons if p.id==p_id]
#                             temp_d = (temp_d * (agent.value) * agent.speed)
#                             if temp_d < min_dest:
#                                 min_dest = temp_d
#                                 min_short_path = temp_path
#                                 min_short_path.append(dest_id)
#                                 min_agent = agent.id
#                                 min_src_id = src_id
#                                 min_dest_id = dest_id
#                             at_end = True
#
#                 if at_end:
#                     start = min_short_path.pop(0)  # pop -> mission_list[0]
#                     edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                     edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                     agents_target[agent_id] = (src_id, dest_id, p.value)
#                     agents_mission[agent.id] = agents_mission[agent.id][agents_mission[agent.id].index(start):]
#                     agents_mission[agent.id] = agents_mission[agent.id] + min_short_path
#
#
#                 #         else:  # if not in list of mission
#                 #             temp_d, temp_path = alg.shortest_path(mission_list[-1],src_id)
#                 #             # p = [p for p in pokemons if p.id==p_id]
#                 #             p = next(n for n in pokemons if n.id == p_id)
#                 #             temp_d = (temp_d * agent.value * agent.speed)/p.value
#                 #             if temp_d < min_dest:
#                 #                 min_dest = temp_d
#                 #                 min_short_path = temp_path
#                 #                 # min_short_path.clear()
#                 #                 min_short_path.append(dest_id)
#                 #                 min_agent = agent.id
#                 #                 min_src_id = src_id
#                 #                 min_dest_id = dest_id
#                 #             at_end = True
#                 #
#                 # if at_end:
#                 #     min_short_path.pop(0)
#                 #     # min_short_path.append(dest_id)
#                 #     # pokemon_is_alocated[(min_src_id, '-', min_dest_id)] = True
#                 #     edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
#                 #     edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
#                 #     agents_mission[agent.id] = agents_mission[agent.id] + min_short_path
#         # print(agents_mission)
#         return agents_mission


def agent_alocate_calculator_update_best(agents: {}, agents_mission: {}, edge_for_pokemon: {}, alg: GraphAlgo,
                                         agent_ids):
    """
    calculat the best alocats of pokemon for any agent and update
    there mission lists
    :param agents: dict of agents
    :param agent_ids: id's agents to check for
    :param agents_mission: mission for now of agent
    :param edge_for_pokemon: edge the pokemons on them
    :param alg: main AlgoGraph
    :return: updated agents_mission
    """

    p_e:Edge

    for agent_id, mission_list in agents_mission.items():
        if agent_id in agent_ids and len(mission_list) < 2:
            agent = agents[agent_id]
            min_dest = float('inf')
            min_short_path = []
            at_end = False

            for p_id, p_e in edge_for_pokemon.items():
                src_id = p_e.get_src()
                dest_id = p_e.get_dest()
                mission_list: []
                # min_short_path = []
                # min_dest = float('inf')
                # at_end = False

                if not edge_pokemon_is_allocate.get((src_id,'-',dest_id)):   #if pok not allocated
                # for l in agents_mission:
                #     if l != agent_id:
                #         if agents_mission.get(l)[len(agents_mission.get(l))-1] != dest_id:

                    if src_id in mission_list and dest_id in mission_list:
                        edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
                        break # the pokemon on list of agent   #Todo: check that only internal loop is break
                    elif src_id in mission_list and not dest_id in mission_list:
                        if agent.src == dest_id:
                            edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
                            break
                        mission_list.insert(mission_list.index(src_id)+1, dest_id)
                        print(mission_list.index(src_id))
                        print(len(mission_list) - 1)
                        if mission_list.index(dest_id) != (len(mission_list)-1):
                            mission_list.insert(mission_list.index(dest_id)+1, src_id)
                        edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
                        break

                    elif not src_id in mission_list and dest_id in mission_list:
                        if agent.src == src_id:
                            edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
                            break
                        mission_list.insert(mission_list.index(dest_id)+1, src_id)
                        if mission_list.index(src_id) != (len(mission_list)- 1):
                            mission_list.insert(mission_list.index(src_id)+1, dest_id)
                        edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
                        break

                    else:  # if not in list of mission
                        temp_d, temp_path = alg.shortest_path(mission_list[0],
                                                              src_id)  # Todo: mission_list[-1] is the last one ?
                        # p = [p for p in pokemons if p.id==p_id]
                        temp_d = (temp_d * (agent.value) * agent.speed)
                        if temp_d < min_dest:
                            min_dest = temp_d
                            min_short_path = temp_path
                            min_short_path.append(dest_id)
                            min_agent = agent.id
                            min_src_id = src_id
                            min_dest_id = dest_id
                        at_end = True

                if at_end:
                    start = min_short_path.pop(0)  # pop -> mission_list[0]
                    # edge_pokemon_value[(src_id, '-', dest_id)] = (0, agent_id)
                    edge_pokemon_is_allocate[(src_id, '-', dest_id)] = True
                    agents_target[agent_id] = (src_id, dest_id, p.value)
                    agents_mission[agent.id] = agents_mission[agent.id][agents_mission[agent.id].index(start):]
                    agents_mission[agent.id] = agents_mission[agent.id] + min_short_path



            #                     else:   # if not in list of mission
            #                         temp_d, temp_path = alg.shortest_path(mission_list[-1], src_id)   #Todo: mission_list[-1] is the last one ?
            #                         # p = [p for p in pokemons if p.id==p_id]
            #                         p = next(n for n in pokemons if n.id == p_id)
            #                         temp_d = (temp_d * agent.value * agent.speed)
            #                         if temp_d < min_dest:
            #                             min_dest = temp_d
            #                             min_short_path = temp_path
            #                             # min_short_path.clear()
            #                             min_short_path.append(dest_id)
            #                             min_agent = agent.id
            #                             min_src_id = src_id
            #                             min_dest_id = dest_id
            #                         at_end = True
            #
            # if at_end:
            #     min_short_path.pop(0)
            #     # min_short_path.append(dest_id)
            #     edge_pokemon_is_allocate[(min_src_id, '-', min_dest_id)] = True
            #     agents_mission[agent.id] = agents_mission[agent.id]+min_short_path
    print(agents_mission)
    return agents_mission
#########################################################################################################
#                                     main game play                                                    #
#########################################################################################################


# init pygame
WIDTH, HEIGHT = 1080, 720
# pygame.font.init()
# FONT=pygame.font.SysFont('comicsans',20)
# FONT_w=pygame.font.SysFont('comicsans',42)

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()
# from pygame_menu.examples import create_example_window
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
# screen = create_example_window('MY GRAPH', (WIDTH, HEIGHT))#(, depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
time_game = pygame.time.Clock()
pygame.font.init()


client = Client()
client.start_connection(HOST, PORT)

#############################################################################
#                              pygame_menu                                  #
#############################################################################

theme = pygame_menu.themes.THEME_DARK.copy()  # Create a new copy
theme.background_color = (0, 0, 0, 180)  # Enable transparency

# -------------------------------------------------------------------------
# Create menus: About
# -------------------------------------------------------------------------
about_theme = pygame_menu.themes.THEME_DARK.copy()
about_theme.widget_font = pygame_menu.font.FONT_NEVIS
about_theme.title_font = pygame_menu.font.FONT_8BIT
about_theme.title_offset = (5, -2)
about_theme.widget_offset = (0, 0.14)
#
# def exit():
#     # client.stop_connection()
#     pygame_menu.events.EXIT()


about_menu = pygame_menu.Menu(
    center_content=False,
    height=400,
    # mouse_visible=False,
    theme=about_theme,
    title='About',
    width=600
)
m = "Assignment 3: The Pokemon game\n" \
    "Authors: Roee Tal and Yossi Elias\n\n" \
    "We hope the use of this \ninterface is as intuitive and convenient \nas we tried to create it.\n\n"\
    "Note: The value on the agents\n is the amount of points they \nhave accumulated so far\n" \
    "The value on the Pokemon marks \nthe value of each"


about_menu.add.label(m, margin=(0, 0))
# about_menu.add.label('')
about_menu.add.button('Return to Menu', pygame_menu.events.BACK)

# file
file_menu = pygame_menu.Menu(
    height=400,
    onclose=pygame_menu.events.RESET,
    theme=theme,
    title='File Menu',
    width=600
)
file_menu.add.button('Return to Menu', pygame_menu.events.BACK)
file_menu.add.button('Close Menu', pygame_menu.events.CLOSE)
main_menu = pygame_menu.Menu(
    enabled=False,
    height=400,
    theme= pygame_menu.themes.THEME_BLUE,
    title='Main Menu',
    onclose=pygame_menu.events.BACK,
    width=600
)
main_menu.add.button(about_menu.get_title(), about_menu)  # Add about submenu
main_menu.add.button('STOP And Exit (Double-tap)', client.stop_connection)  # Add exit







FONT = pygame.font.SysFont('comicsans', 18, bold=True)
FONT_in = pygame.font.SysFont('comicsans', 13, bold=True)
# load the json string into SimpleNamespace Object


# init graph:
graph_json = client.get_graph()
graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

alg = GraphAlgo()

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))
    id_n = n.id
    # alg.get_graph().add_node(id_n, n.pos)


# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


for n in graph.Nodes:
    n.pos = SimpleNamespace(x= float(n.pos.x), y=float(n.pos.y))
    # n.pos = SimpleNamespace(x= my_scale(float(n.pos.x), x=True), y= my_scale(float(n.pos.y), y=True))
    id_n = n.id
    alg.get_graph().add_node(id_n, (n.pos.x, n.pos.y))
    print('\nnode_scaled: ',alg.get_graph().getNode(id_n).get_location())

for e in graph.Edges:
    src_e = e.src
    dest_e= e.dest
    w_e = e.w
    alg.get_graph().add_edge(e.src, e.dest, e.w)
print('\nedges: ',alg.get_graph()._Edges,'\n\n')



# pokemons = client.get_pokemons()
# pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
global pokemons
pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
pokemons = [p.Pokemon for p in pokemons]
p_id = 0
for p in pokemons:
    x, y, _ = p.pos.split(',')
    p.pos = SimpleNamespace(x=float(x), y=float(y))
    # p.pos = SimpleNamespace(x=my_scale(float(x), x=True), y=my_scale(float(y), y=True))
    p.id = p_id
    p_id = p_id +1

# for e in alg.get_graph()._Edges
global edge_pokemon_is_allocate
edge_pokemon_is_allocate = {}
global edge_pokemon_value
edge_pokemon_value = {}
# for e in alg.get_graph()._Edges.values():
#     edge_pokemon_value[(e.get_src(), '-', e.get_dest())] = (0, 0)
#     edge_pokemon_is_allocate[(e.get_src(), '-', e.get_dest())] = False


edge_for_pokemon  = edge_for_pokemon_calculator(pokemons, alg)
# e:Edge
for e in edge_for_pokemon.values():
    edge_pokemon_is_allocate[(e.get_src(), '-', e.get_dest())] = False



# graph_json = client.get_graph()
#
# FONT = pygame.font.SysFont('Arial', 20, bold=True)
# # load the json string into SimpleNamespace Object
#
# graph = json.loads(
#     graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
#
# for n in graph.Nodes:
#     x, y, _ = n.pos.split(',')
#     n.pos = SimpleNamespace(x=float(x), y=float(y))
#
#
#
#  # get data proportions
# min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
# min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
# max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
# max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
#
#



# # decorate scale with the correct values
#
# def my_scale(data, x=False, y=False):
#     if x:
#         return scale(data, 50, screen.get_width() - 50, min_x, max_x)
#     if y:
#         return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15

global agents_mission
agents_mission = {}
global agents_target
agents_target = {}

src_alocated = []
pokemons_is_alcated = [p for p in edge_for_pokemon.values()]
cuont_agent = 0
ag_sucses = 'true'
while ag_sucses == 'true':
    if len(pokemons_is_alcated) != 0:
        pok_alocate = pokemons_is_alcated.pop(0)
        while(pok_alocate.get_src() in src_alocated):
            pok_alocate = pokemons_is_alcated.pop()
        src_alocated.append(pok_alocate.get_src())
        start_node, end_node = pok_alocate.get_src(), pok_alocate.get_dest()
        ag_str = "{}\"id\":{}{}".format('{', start_node, '}')
    else:
        start_node = cuont_agent
        ag_str = "{}\"id\":{}{}".format('{', start_node, '}')
    ag_sucses =  client.add_agent(ag_str)
    if ag_sucses == 'true':
        agents_mission[cuont_agent] = [start_node]
        agents_target[cuont_agent] = (start_node,end_node,1)
        cuont_agent = cuont_agent + 1


# this commnad starts the server - the game is running now
client.start()
time_from_start = time.time()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    current_menu = main_menu.get_current()
    if current_menu.get_title() != 'Main Menu' or not main_menu.is_enabled():

        image = pygame.image.load(r'pocemon.jpg ')
        image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        # copying the image surface object to the display surface object at (0, 0) coordinate.
        screen.blit(image, (0, 0))

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            # if event.type == pygame.VIDEORESIZE:
                # # re-init graph, for case the size of screen change:
                # alg = GraphAlgo()
                # graph_json = client.get_graph()
                # graph = json.loads(
                #     graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
                # for n in graph.Nodes:
                #     x, y, _ = n.pos.split(',')
                #     n.pos = SimpleNamespace(x=float(x), y=float(y))
                #     n.pos = SimpleNamespace(x=my_scale(float(n.pos.x), x=True), y=my_scale(float(n.pos.y), y=True))
                #     alg.get_graph().add_node(id_n, (n.pos.x, n.pos.y))
                #     id_n = n.id
                # for e in graph.Edges:
                #     alg.get_graph().add_edge(e.src, e.dest, e.w)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and \
                        current_menu.get_title() == 'Main Menu':
                    main_menu.toggle()

        if main_menu.is_enabled():
            main_menu.mainloop(screen)
            # main_menu.draw(screen)
            # main_menu.update(pygame.event.get())

        # pygame.display.flip()
        # refresh surface
        # screen.blit(image, (0, 0))
        screen.fill(Color(0, 134, 139))



        graph_json = client.get_graph()
        graph = json.loads(
            graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        for n in graph.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))
            n.pos = SimpleNamespace(x=my_scale(float(n.pos.x), x=True), y=my_scale(float(n.pos.y), y=True))
            # alg.get_graph().add_node(id_n, (n.pos.x, n.pos.y))
            id_n = n.id
        # for e in graph.Edges:
            # alg.get_graph().add_edge(e.src, e.dest, e.w)






        pokemons = json.loads(client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        p_id = 0
        for p in pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=
                float(x), y=float(y))
            p.id = p_id
            p_id = p_id + 1
        edge_for_pokemon:{} = edge_for_pokemon_calculator(pokemons, alg)

        for p in pokemons:
            p.pos = SimpleNamespace(x=my_scale(
                float(p.pos.x), x=True), y=my_scale(float(p.pos.y), y=True))

        for e in edge_for_pokemon.values():
            edge_pokemon_value[(e.get_src(), '-', e.get_dest())] = 5
            # is_in = False
            # for agent_id, mission_list in agents_mission.items():
            #     if e.get_src() in mission_list and e.get_dest() in mission_list:
            #         is_in = True
            # if not is_in:

        agents = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents_list = [agent.Agent for agent in agents]
        agents = {}
        for a in agents_list:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=my_scale(
                float(x), x=True), y=my_scale(float(y), y=True))
            agents[a.id] = a















        # drow text
        inf = json.loads(client.get_info(),
                            object_hook=lambda d: SimpleNamespace(**d)).GameServer
        text = FONT.render("Moves: {}".format(inf.moves, (float())), True, (0, 0, 0))
        screen.blit(text, (105, 25))
        # if inf.moves != 0:
        text = FONT.render("Moves/second: {:.1f}".format(inf.moves/(time.time() - time_from_start)), True, (0, 0, 0))
        screen.blit(text, (105, 45))
        text = FONT.render("time: {:.1f}".format((time.time() - time_from_start)), True, (0, 0, 0))
        screen.blit(text, (105, 65))
        text = FONT.render("grade: {}".format(inf.grade), True, (0, 0, 0))
        screen.blit(text, (105, 85))
        esc_text = FONT_in.render("To get to the Main-Menu please press->\'esc\'", True, (0, 0, 0))
        screen.blit(esc_text, (25, 2))
        text = FONT.render("Level: {}".format(inf.game_level), True, (255, 255, 255))
        screen.blit(text, (690, 680))


        # draw edges
        for e in graph.Edges:
            # find the edge nodes
            src = next(n for n in graph.Nodes if n.id == e.src)
            dest = next(n for n in graph.Nodes if n.id == e.dest)

            # # scaled positions
            # src_x = my_scale(src.pos.x, x=True)
            # src_y = my_scale(src.pos.y, y=True)
            # dest_x = my_scale(dest.pos.x, x=True)
            # dest_y = my_scale(dest.pos.y, y=True)

            # draw the line
            # pygame.draw.line(screen, Color(61, 72, 126),
            #                  (my_scale(src.pos.x, x=True), my_scale(src.pos.y, y=True)), (my_scale(dest.pos.x,x=True), my_scale(dest.pos.y,y=True)))
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src.pos.x, src.pos.y), (dest.pos.x, dest.pos.y))
            arrow((src.pos.x, src.pos.y), (dest.pos.x, dest.pos.y), 23, 5, color=(61, 72, 126))
            # pygame.draw.line(screen, Color(61, 72, 126),
            #                  (src_x, src_y), (dest_x, dest_y))

        # draw nodes
        for n in graph.Nodes:
            x = n.pos.x  # my_scale(n.pos.x, x=True)
            y = n.pos.y  # my_scale(n.pos.y, y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  radius, Color(64, 80, 174))
            gfxdraw.aacircle(screen, int(x), int(y),
                             radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        # draw agents
        for agent in agents.values():
            pygame.draw.circle(screen, Color(122, 61, 23),
                               (int(agent.pos.x), int(agent.pos.y)), 10)
            # draw the agent id
            val_srf = FONT_in.render(str(int(agent.value)), True, Color(0, 0, 0))
            rect = val_srf.get_rect(center=((int(agent.pos.x), int(agent.pos.y))))
            screen.blit(val_srf, rect)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in pokemons:
            # edge_of_p:Edge = edge_for_pokemon.get(p.id)
            if p.type > 0:
                pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
            else:
                pygame.draw.circle(screen, Color(255, 255, 0), (int(p.pos.x), int(p.pos.y)), 10)
            # draw the pokemon value
            val_srf = FONT_in.render(str(int(p.value)), True, Color(0, 0, 0))
            rect = val_srf.get_rect(center=((int(p.pos.x), int(p.pos.y))))
            screen.blit(val_srf, rect)


        # update screen changes
        display.update()

        # refresh rate
        clock.tick(600)

        # choose next edge
        agent_to_allocate = []
        for agent in agents.values():
            if agent.dest == -1:
                agent_to_allocate.append(agent.id)
        count_of_change = 0
        if len(agent_to_allocate) > 0:
            # agent_alocate_calculator_update_multi(agents, agents_mission, edge_for_pokemon, alg, agent_to_allocate)
            agent_alocate_calculator_update_best(agents, agents_mission, edge_for_pokemon, alg, agent_to_allocate)
            for agent in agents.values():
                # if (agent.src,'-',agents_mission[agent.id][0]) in edge_pokemon_is_allocate and edge_pokemon_is_allocate[(agent.src,'-',agents_mission[agent.id][0])]:
                #     edge_pokemon_is_allocate[(agent.src, '-', agents_mission[agent.id][0])] = False
                if agent.dest == -1:
                    count_of_change = count_of_change + 1
                    # if agent.src == agents_mission[agent.id][0] and len(agents_mission[agent.id]) > 1:
                    #     agents_mission[agent.id].pop(0)
                    # next_node = agents_mission[agent.id][0]

                    if len(agents_mission[agent.id]) > 1:
                        next_node = agents_mission[agent.id].pop(0)
                    else:
                        next_node = agents_mission[agent.id][0]
                    # next_node = (agent.src - 1) % len(graph.Nodes)
                    client.choose_next_edge(
                        '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
                    # ttl = client.time_to_end()
                    # print(ttl, client.get_info())


        if count_of_change==0 and inf.moves/(time.time()-time_from_start)<10:
            client.move()
    else:
        # Background color if the menu is enabled and graph is hidden
        # screen.fill((40, 0, 40))
        screen.blit(image, (0, 0))
    # print(time.time()-time_from_start)
# game over:

































