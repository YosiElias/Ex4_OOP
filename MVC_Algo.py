from types import SimpleNamespace
from Digraph import *
from client import Client
import json
import pygame
from pygame import *
from GraphAlgo import GraphAlgo
import time



#########################################################################################################
#                                     main game algo                                                    #
#########################################################################################################


# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
clock = pygame.time.Clock()
time_game = pygame.time.Clock()


class MainAlgo:
    def __init__(self):
        self._client = Client()
        self._client.start_connection(HOST, PORT)
        self._draw = False
        # init graph:
        graph_json = self._client.get_graph()

        # load the json string into SimpleNamespace Object
        self._graph = json.loads(
            graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

        self._alg = GraphAlgo()

        for n in self._graph.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))

        # get data proportions
        self._min_x = min(list(self._graph.Nodes), key=lambda n: n.pos.x).pos.x
        self._min_y = min(list(self._graph.Nodes), key=lambda n: n.pos.y).pos.y
        self._max_x = max(list(self._graph.Nodes), key=lambda n: n.pos.x).pos.x
        self._max_y = max(list(self._graph.Nodes), key=lambda n: n.pos.y).pos.y

        for n in self._graph.Nodes:
            n.pos = SimpleNamespace(x=float(n.pos.x), y=float(n.pos.y))
            id_n = n.id
            self._alg.get_graph().add_node(id_n, (n.pos.x, n.pos.y))
            print('\nnode_scaled: ', self._alg.get_graph().getNode(id_n).get_location())

        for e in self._graph.Edges:
            self._alg.get_graph().add_edge(e.src, e.dest, e.w)
        print('\nedges: ', self._alg.get_graph()._Edges, '\n\n')

        self._pokemons = json.loads(self._client.get_pokemons(),
                                    object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        self._pokemons = [p.Pokemon for p in self._pokemons]
        p_id = 0
        for p in self._pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=float(x), y=float(y))
            p.id = p_id
            p_id = p_id + 1

        self._edge_for_pokemon = edge_for_pokemon_calculator(self._pokemons, self._alg)
        self._pokemon_is_alocated = {}
        e: Edge
        for e in self._edge_for_pokemon.values():
            self._pokemon_is_alocated[(e.get_src(), '-', e.get_dest())] = False

        self._agents_mission = {}

        pokemons_is_alcated = [p for p in self._edge_for_pokemon.values()]
        cuont_agent = 0
        ag_sucses = 'true'
        while ag_sucses == 'true':
            if len(pokemons_is_alcated) != 0:
                start_node = pokemons_is_alcated.pop().get_src()
                ag_str = "{}\"id\":{}{}".format('{', start_node, '}')
            else:
                start_node = cuont_agent
                ag_str = "{}\"id\":{}{}".format('{', start_node, '}')
            ag_sucses = self._client.add_agent(ag_str)
            if ag_sucses == 'true':
                self._agents_mission[cuont_agent] = [start_node]
                cuont_agent = cuont_agent + 1
        self._inf = json.loads(self._client.get_info(),
                               object_hook=lambda d: SimpleNamespace(**d)).GameServer

    def start_game(self):
        self._draw = True
        self._client.start()
        self._time_from_start = time.time()

    def get_inf(self):
        self._inf = json.loads(self._client.get_info(),
                         object_hook=lambda d: SimpleNamespace(**d)).GameServer
        return self._inf

    def get_update_pocemon(self):
        self._pokemons = json.loads(self._client.get_pokemons(),
                                    object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        self._pokemons = [p.Pokemon for p in self._pokemons]
        p_id = 0
        for p in self._pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=float(x), y=float(y))
            p.id = p_id
            p_id = p_id + 1
        self._edge_for_pokemon = edge_for_pokemon_calculator(self._pokemons, self._alg)
        self._pokemon_is_alocated = {}
        e: Edge
        for e in self._edge_for_pokemon.values():
            self._pokemon_is_alocated[(e.get_src(), '-', e.get_dest())] = False
        return self._pokemons


    def get_update_agent(self):
        self._agents = json.loads(self._client.get_agents(),
                                  object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents_list = [agent.Agent for agent in self._agents]
        self._agents = {}
        for a in agents_list:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=float(x), y=float(y))
            self._agents[a.id] = a
        return self._agents

    def nex_step(self):
        agent_to_allocate = []
        for agent in self._agents.values():
            if agent.dest == -1:
                agent_to_allocate.append(agent.id)
        count_of_change = 0
        if len(agent_to_allocate) > 0:
            agent_alocate_calculator_update_multi(self._agents, self._agents_mission, self._edge_for_pokemon, self._alg,
                                                  agent_to_allocate, self)
            for agent in self._agents.values():
                if agent.dest == -1:
                    count_of_change = count_of_change + 1
                    if agent.src == self._agents_mission[agent.id][0] and len(self._agents_mission[agent.id]) > 1:
                        self._agents_mission[agent.id].pop(0)
                    next_node = self._agents_mission[agent.id][0]
                    # if len(agents_mission[agent.id]) > 1:
                    #     next_node = agents_mission[agent.id].pop(0)
                    # else:
                    #     next_node = agents_mission[agent.id][0]
                    self._client.choose_next_edge(
                        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = self._client.time_to_end()
                    print(ttl, self._client.get_info())

        if self._inf.moves / (time.time() - self._time_from_start) < 10:  # count_of_change==0 and
            self._client.move()

    def is_running(self):
        if self._client.is_running() == 'true':
            self._draw = True
            return True
        else:
            return False

    def get_graph_to_draw(self):
        """
         # load the json string into SimpleNamespace Object
        :return: SimpleNamespace Object of graph
        """
        graph_json = self._client.get_graph()
        self._graph = json.loads(
            graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        for n in self._graph.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))
        return self._graph
































#########################################################################################################
#                                      calculate function                                               #
#########################################################################################################


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
                      break
          else:
            slope = (n_dest[1] - n_src[1]) / (n_dest[0] - n_src[0]) # calculating slope of two points of e
            # if e.get_src()==8 and e.get_dest() == 9:
            #     print(y_p - n_src[1])
            #     print(slope * (x_p - n_src[0]))
            if abs((y_p - n_src[1]) - (slope * (x_p - n_src[0]))) <= 0.00000001:
                if (p.type > 0  and e.get_src() < e.get_dest()) or (p.type < 0  and e.get_src() > e.get_dest()):
                    ans[p.id] = e
                    break
    # print('\n\nedge_for_pokemon: ',ans,'\n')
    return ans


#
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



def agent_alocate_calculator_update_multi(agents:{}, agents_mission:{}, edge_for_pokemon:{} , alg:GraphAlgo, agent_ids, main_algo:MainAlgo):
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

    # for agent_id, mission_list in agents_mission.items():
    #     first=2
    #     for m in mission_list:
    #         if first == 0:
    #             del mission_list[mission_list.index(m)]
    #         else:
    #             first =first-1

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
                at_end = False
                not_allocate = True

                if not main_algo._pokemon_is_alocated.get((src_id,'-',dest_id)):   #if pok not allocated

                    for agent_id_in, mission_list_in in agents_mission.items():
                        if agent_id_in != agent_id and src_id in mission_list_in and dest_id in mission_list_in and mission_list_in.index(src_id) == mission_list_in.index(dest_id)-1:
                            not_allocate = False
                            break

                    if  not_allocate and src_id in mission_list and dest_id in mission_list:
                        main_algo._pokemon_is_alocated[(src_id, '-', dest_id)] = True
                        break # the pokemon on list of agent   #Todo: check that only internal loop is break
                    elif not_allocate and src_id in mission_list and not dest_id in mission_list:
                        if agent.src == dest_id:
                            main_algo._pokemon_is_alocated[(src_id, '-', dest_id)] = True
                            break
                        mission_list.insert(mission_list.index(src_id)+1, dest_id)
                        print(mission_list.index(src_id))
                        print(len(mission_list) - 1)
                        if mission_list.index(dest_id) != (len(mission_list)-1):
                            mission_list.insert(mission_list.index(dest_id)+1, src_id)
                        main_algo._pokemon_is_alocated[(src_id, '-', dest_id)] = True
                        break

                    elif not_allocate and not src_id in mission_list and dest_id in mission_list:
                        if agent.src == src_id:
                            main_algo._pokemon_is_alocated[(src_id, '-', dest_id)] = True
                            break
                        mission_list.insert(mission_list.index(dest_id)+1, src_id)
                        if mission_list.index(src_id) != (len(mission_list)- 1):
                            mission_list.insert(mission_list.index(src_id)+1, dest_id)
                        main_algo._pokemon_is_alocated[(src_id, '-', dest_id)] = True
                        break

                    elif not_allocate:  # if not in list of mission
                        temp_d, temp_path = alg.shortest_path(mission_list[0], src_id)   #Todo: mission_list[-1] is the last one ?
                        # p = [p for p in pokemons if p.id==p_id]
                        temp_d = (temp_d * (agent.value)* agent.speed)
                        if temp_d < min_dest:
                            min_dest = temp_d
                            min_short_path = temp_path
                            min_short_path.append(dest_id)
                            min_agent = agent.id
                            min_src_id = src_id
                            min_dest_id = dest_id
                        at_end = True

            if at_end:
                start = min_short_path.pop(0)   #pop -> mission_list[0]
                main_algo._pokemon_is_alocated[(min_src_id, '-', min_dest_id)] = True
                # agents_target[agent_id] = (src_id, dest_id, p.value)
                agents_mission[agent.id] = agents_mission[agent.id][agents_mission[agent.id].index(start):]
                agents_mission[agent.id] = agents_mission[agent.id]+min_short_path

            #         else:   # if not in list of mission
            #             temp_d, temp_path = alg.shortest_path(mission_list[-1], src_id)   #Todo: mission_list[-1] is the last one ?
            #             # p = [p for p in pokemons if p.id==p_id]
            #             p = next(n for n in pokemons if n.id == p_id)
            #             temp_d = (temp_d * agent.value * agent.speed)/p.value
            #             if temp_d < min_dest:
            #                 min_dest = temp_d
            #                 min_short_path = temp_path
            #                 min_short_path.append(dest_id)
            #                 min_agent = agent.id
            #                 min_src_id = src_id
            #                 min_dest_id = dest_id
            #             at_end = True
            #
            # if at_end:
            #     min_short_path.pop(0)
            #     # min_short_path.append(dest_id)
            #     main_algo._pokemon_is_alocated[(min_src_id, '-', min_dest_id)] = True
            #     agents_mission[agent.id] = agents_mission[agent.id]+min_short_path
    print(agents_mission)
    return agents_mission























