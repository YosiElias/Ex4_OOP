from types import SimpleNamespace
from MVC_Algo import MainAlgo
from Digraph import *
from pygame import gfxdraw
import pygame
from pygame import *
from GraphAlgo import GraphAlgo
import time
import pygame_menu
import math



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
#
# def edge_for_pokemon_calculator(pokemons, alg:GraphAlgo):
#     """
#     find the edge the pokemon on it
#     *Note: for any run of this function the pokemon id is
#     different, so this function run only with gating pokemons from client and "id's" theme
#     :param pokemons: list of pokemons
#     :return: dict of edge for any pokemon in time of this function
#     """
#     ans = {}
#     for p in pokemons:
#       x_p, y_p = p.pos.x, p.pos.y
#       e:Edge
#       for e in alg.get_graph()._Edges.values():
#           src = e.get_src()
#           n_src = alg.get_graph().getNode(e.get_src()).get_location()
#           n_dest = alg.get_graph().getNode(e.get_dest()).get_location()
#           if n_dest[0] == n_src[0]: # x1==x2
#               if min(n_dest[1],n_src[1]) <= y_p <= max(n_dest[1] ,n_src[1]): # checking condition for `p` to be on line (between the points)
#                   if (p.type > 0 and e.get_src() < e.get_dest()) or (p.type < 0 and e.get_src() > e.get_dest()):
#                       ans[p.id] = e
#                       break
#           else:
#             slope = (n_dest[1] - n_src[1]) / (n_dest[0] - n_src[0]) # calculating slope of two points of e
#             # if e.get_src()==8 and e.get_dest() == 9:
#             #     print(y_p - n_src[1])
#             #     print(slope * (x_p - n_src[0]))
#             if abs((y_p - n_src[1]) - (slope * (x_p - n_src[0]))) <= 0.00000001:
#                 if (p.type > 0  and e.get_src() < e.get_dest()) or (p.type < 0  and e.get_src() > e.get_dest()):
#                     ans[p.id] = e
#                     break
#     # print('\n\nedge_for_pokemon: ',ans,'\n')
#     return ans

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
#     #     for m in mission_list:
#     #         if first == 0:
#     #             del mission_list[mission_list.index(m)]
#     #         else:
#     #             first =first-1
#
#     for agent_id, mission_list in agents_mission.items():
#         if agent_id in agent_ids and len(mission_list) < 2:
#             agent = agents[agent_id]
#             min_dest = float('inf')
#             min_short_path = []
#             at_end = False
#
#             for p_id, p_e in edge_for_pokemon.items():
#                 src_id = p_e.get_src()
#                 dest_id = p_e.get_dest()
#                 mission_list: []
#                 at_end = False
#                 not_allocate = True
#
#                 if not pokemon_is_alocated.get((src_id,'-',dest_id)):   #if pok not allocated
#
#                     for agent_id_in, mission_list_in in agents_mission.items():
#                         if agent_id_in != agent_id and src_id in mission_list_in and dest_id in mission_list_in and mission_list_in.index(src_id) == mission_list_in.index(dest_id)-1:
#                             not_allocate = False
#                             break
#
#                     if  not_allocate and src_id in mission_list and dest_id in mission_list:
#                         pokemon_is_alocated[(src_id, '-', dest_id)] = True
#                         break # the pokemon on list of agent   #Todo: check that only internal loop is break
#                     elif not_allocate and src_id in mission_list and not dest_id in mission_list:
#                         if agent.src == dest_id:
#                             pokemon_is_alocated[(src_id, '-', dest_id)] = True
#                             break
#                         mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                         print(mission_list.index(src_id))
#                         print(len(mission_list) - 1)
#                         if mission_list.index(dest_id) != (len(mission_list)-1):
#                             mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                         pokemon_is_alocated[(src_id, '-', dest_id)] = True
#                         break
#
#                     elif not_allocate and not src_id in mission_list and dest_id in mission_list:
#                         if agent.src == src_id:
#                             pokemon_is_alocated[(src_id, '-', dest_id)] = True
#                             break
#                         mission_list.insert(mission_list.index(dest_id)+1, src_id)
#                         if mission_list.index(src_id) != (len(mission_list)- 1):
#                             mission_list.insert(mission_list.index(src_id)+1, dest_id)
#                         pokemon_is_alocated[(src_id, '-', dest_id)] = True
#                         break
#
#                     elif not_allocate:  # if not in list of mission
#                         temp_d, temp_path = alg.shortest_path(mission_list[0], src_id)   #Todo: mission_list[-1] is the last one ?
#                         # p = [p for p in pokemons if p.id==p_id]
#                         temp_d = (temp_d * (agent.value)* agent.speed)
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
#                 pokemon_is_alocated[(min_src_id, '-', min_dest_id)] = True
#                 # agents_target[agent_id] = (src_id, dest_id, p.value)
#                 agents_mission[agent.id] = agents_mission[agent.id][agents_mission[agent.id].index(start):]
#                 agents_mission[agent.id] = agents_mission[agent.id]+min_short_path
#
#             #         else:   # if not in list of mission
#             #             temp_d, temp_path = alg.shortest_path(mission_list[-1], src_id)   #Todo: mission_list[-1] is the last one ?
#             #             # p = [p for p in pokemons if p.id==p_id]
#             #             p = next(n for n in pokemons if n.id == p_id)
#             #             temp_d = (temp_d * agent.value * agent.speed)/p.value
#             #             if temp_d < min_dest:
#             #                 min_dest = temp_d
#             #                 min_short_path = temp_path
#             #                 min_short_path.append(dest_id)
#             #                 min_agent = agent.id
#             #                 min_src_id = src_id
#             #                 min_dest_id = dest_id
#             #             at_end = True
#             #
#             # if at_end:
#             #     min_short_path.pop(0)
#             #     # min_short_path.append(dest_id)
#             #     pokemon_is_alocated[(min_src_id, '-', min_dest_id)] = True
#             #     agents_mission[agent.id] = agents_mission[agent.id]+min_short_path
#     print(agents_mission)
#     return agents_mission
#
#

#########################################################################################################
#                                     main game play                                                    #
#########################################################################################################


# init pygame
WIDTH, HEIGHT = 1080, 720
# pygame.font.init()
# FONT=pygame.font.SysFont('comicsans',20)
# FONT_w=pygame.font.SysFont('comicsans',42)


pygame.init()
# from pygame_menu.examples import create_example_window
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
# screen = create_example_window('MY GRAPH', (WIDTH, HEIGHT))#(, depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
time_game = pygame.time.Clock()
pygame.font.init()


global main_algo
main_algo = MainAlgo()

min_x = main_algo._min_x
min_y = main_algo._min_y
max_x = main_algo._max_x
max_y = main_algo._max_y

# init graph to draw:
graph = main_algo.get_graph_to_draw()
# scale nodes
for n in graph.Nodes:
    n.pos.x = my_scale(n.pos.x, x=True)
    n.pos.y = my_scale(n.pos.y, y=True)



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
main_menu.add.button('STOP And Exit (Double-tap)', main_algo._client.stop_connection)  # Add exit





FONT = pygame.font.SysFont('comicsans', 18, bold=True)
FONT_in = pygame.font.SysFont('comicsans', 13, bold=True)


radius = 15

# this commnad starts the server - the game is running now
main_algo.start_game()
time_from_start = time.time()

try:
    while main_algo.is_running():
        current_menu = main_menu.get_current()
        if current_menu.get_title() != 'Main Menu' or not main_menu.is_enabled():

            # image = pygame.image.load(r'pocemon.jpg ')
            # image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
            # copying the image surface object to the display surface object at (0, 0) coordinate.
            # screen.blit(image, (0, 0))
            pokemons = main_algo.get_update_pocemon()
            p_id = 0
            for p in pokemons:
                p.pos = SimpleNamespace(x=my_scale(
                    float(p.pos.x), x=True), y=my_scale(float(p.pos.y), y=True))
                p.id = p_id
                p_id = p_id + 1
            agents:{} = main_algo.get_update_agent()
            for a in agents.values():
                a.pos = SimpleNamespace(x=my_scale(
                    float(a.pos.x), x=True), y=my_scale(float(a.pos.y), y=True))

            # check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.VIDEORESIZE:
                    # re-init graph, for case the size of screen change:
                    graph = main_algo.get_graph_to_draw()
                    # scale nodes
                    for n in graph.Nodes:
                        n.pos.x = my_scale(n.pos.x, x=True)
                        n.pos.y = my_scale(n.pos.y, y=True)
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
            screen.fill(Color(0,134,139))

            # drow text
            inf = main_algo.get_inf()
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

            # init graph to draw:
            # graph = main_algo.get_graph_to_draw()
            # # scale nodes
            # for n in graph.Nodes:
            #     n.pos.x = my_scale(n.pos.x, x=True)
            #     n.pos.y = my_scale(n.pos.y, y=True)

            # draw edges
            for e in graph.Edges:
                # find the edge nodes
                src = next(n for n in graph.Nodes if n.id == e.src)
                dest = next(n for n in graph.Nodes if n.id == e.dest)

                # draw the line
                pygame.draw.line(screen, Color(61, 72, 126),
                                 (src.pos.x, src.pos.y), (dest.pos.x, dest.pos.y))
                arrow((src.pos.x, src.pos.y), (dest.pos.x, dest.pos.y), 23, 5, color=(61, 72, 126))


            # draw nodes
            for n in graph.Nodes:
                x = n.pos.x
                y = n.pos.y

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
                val_srf = FONT_in.render((str(int(agent.id))), True, Color(0, 0, 0))
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

            main_algo.nex_step()

        else:
            # Background color if the menu is enabled and graph is hidden
            # screen.fill((40, 0, 40))
            screen.blit(image, (0, 0))
        # print(time.time()-time_from_start)
except AttributeError:
    if (main_algo.is_running()):
        print("ERROR: game not over")
except ConnectionResetError:
    if (main_algo.is_running()):
        print("ERROR: game not over")
except OSError:
    if (main_algo.is_running()):
        print("ERROR: game not over")
# game over:
































