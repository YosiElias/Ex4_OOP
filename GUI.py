
#############################################################################
#
# pygame function to display
# the graph and algorithm
#
#############################################################################

__all__ = ['main']

import json
from types import SimpleNamespace

import networkx as nx
import pygame
import pygame_menu
from pygame import RESIZABLE, gfxdraw, display
from pygame.locals import Color
from pygame_menu.examples import create_example_window
import GraphAlgo_1
# from src.DiGraph import DiGraph
# from src.Node import Node
import math
import tkinter as tk
from tkinter import filedialog
from tkinter import END
from tkinter import messagebox
import ctypes

import datetime
from random import randrange
from typing import List, Tuple, Optional

from GraphAlgo_1 import GraphAlgo, Node

clock = pygame.time.Clock()
pygame.font.init()




FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object




COLOR_BACKGROUND = [128, 0, 128]
FPS = 60

user32 = ctypes.windll.user32
# W_SIZE,H_SIZE  = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size

surface: Optional['pygame.Surface'] = None
timer: Optional[List[float]] = None

pygame.font.init()
FONT=pygame.font.SysFont('comicsans',20)
FONT_w=pygame.font.SysFont('comicsans',42)

def mainmenu_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    surface.fill((40, 0, 40))



def resert_color()->None:
    """
    reset color of all edges
    :return: None
    """
    for e in algo.get_graph()._Edges.values():
        e.set_color((255,52,179))



class TestCallClassMethod(object):
    """
    Class call method.
    """


# def update():
#     pokemons = json.loads(client.get_pokemons(),
#                           object_hook=lambda d: SimpleNamespace(**d)).Pokemons
#     pokemons = [p.Pokemon for p in pokemons]
#     for p in pokemons:
#         x, y, _ = p.pos.split(',')
#         p.pos = SimpleNamespace(x=my_scale(
#             float(x), x=True), y=my_scale(float(y), y=True))
#     agents = json.loads(client.get_agents(),
#                         object_hook=lambda d: SimpleNamespace(**d)).Agents
#     agents = [agent.Agent for agent in agents]
#     for a in agents:
#         x, y, _ = a.pos.split(',')
#         a.pos = SimpleNamespace(x=my_scale(
#             float(x), x=True), y=my_scale(float(y), y=True))


def update_data():
    pokemons = json.loads(algo._client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    algo.pokemons = [p.Pokemon for p in pokemons]
    for p in algo.pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(algo._client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    algo.agents = [agent.Agent for agent in agents]
    for a in  algo.agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))


def main(test: bool = False, alg:GraphAlgo_1=None) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    :return: None
    """

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    # # Write help message on console
    # for m in HELP:
    #     print(m)

    # Create window
    global surface
    global func_resulte
    global algo
    algo = GraphAlgo()
    surface = create_example_window('MY GRAPH', (W_SIZE, H_SIZE), flags=RESIZABLE)#, depth=32

    if algo != None:
        # scale all point:
        min_max()

    frame = 0

    # -------------------------------------------------------------------------
    # Create menus: File
    # -------------------------------------------------------------------------

    theme = pygame_menu.themes.THEME_DARK.copy()  # Create a new copy
    theme.background_color = (0, 0, 0, 180)  # Enable transparency

    # file
    file_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=theme,
        title='File Menu',
        width=600
    )

    # Add widgets
    # file_menu.add.button('Load New Graph', Load_graph)
    # file_menu.add.button('Save Graph', save_graph)

    # Adds a selector (element that can handle functions)
    # file_menu.add.selector(
    #     title='Change color ',
    #     items=[('Random', (-1, -1, -1)),  # Values of selector, call to change_color_bg
    #            ('Default', (128, 0, 128)),
    #            ('Black', (0, 0, 0)),
    #            ('Blue', (12, 12, 200))],
    #     default=1,  # Optional parameter that sets default item of selector
    #     onchange=change_color_bg,  # Action when changing element with left/right
    #     onreturn=change_color_bg,  # Action when pressing return on an element
    #     # All the following kwargs are passed to change_color_bg function
    #     write_on_console=True
    # )
    # file_menu.add.button('Update game object', TestCallClassMethod().update_game_settings)
    file_menu.add.button('Return to Menu', pygame_menu.events.BACK)
    file_menu.add.button('Close Menu', pygame_menu.events.CLOSE)

    # -------------------------------------------------------------------------
    # Create menus: Function
    # -------------------------------------------------------------------------
    function_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=theme,
        width=600,
        title='Function Menu',
    )
    # Add widgets
    # function_menu.add.button('Short Path', short_path)
    # function_menu.add.button('Center', center)
    # function_menu.add.button('TSP', tsp)
    function_menu.add.button('Return to Menu', pygame_menu.events.BACK)


    # -------------------------------------------------------------------------
    # Create menus: Edit
    # -------------------------------------------------------------------------
    edit_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=theme,
        width=600,
        title='Edit Menu',
    )
    # Add widgets
    # edit_menu.add.button('Add Node', add_n)
    # edit_menu.add.button('Add Edge', add_e)
    # edit_menu.add.button('Remove Node', remove_n)
    # edit_menu.add.button('Remove Edge', remove_e)
    edit_menu.add.button('Return to Menu', pygame_menu.events.BACK)


    # -------------------------------------------------------------------------
    # Create menus: About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DARK.copy()
    about_theme.widget_font = pygame_menu.font.FONT_NEVIS
    about_theme.title_font = pygame_menu.font.FONT_8BIT
    about_theme.title_offset = (5, -2)
    about_theme.widget_offset = (0, 0.14)

    about_menu = pygame_menu.Menu(
        center_content=False,
        height=400,
        # mouse_visible=False,
        theme=about_theme,
        title='About',
        width=600
    )
    m= "Assignment 3: Graphs\n" \
       "Authors: Roee Tal and Yossi Elias\n\n" \
      "We have created this interface\n in order to make the operation of the\n functions more accessible\n\n" \
       "We hope the use of this \ninterface is as intuitive and convenient \nas we tried to create it."

    about_menu.add.label(m, margin=(0, 0))
    # about_menu.add.label('')
    about_menu.add.button('Return to Menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu = pygame_menu.Menu(
        enabled=False,
        height=400,
        theme=pygame_menu.themes.THEME_DARK,
        title='Main Menu',
        width=600
    )

    main_menu.add.button(file_menu.get_title(), file_menu)  # Add submenu
    main_menu.add.button(function_menu.get_title(), function_menu)  # Add func submenu
    main_menu.add.button(edit_menu.get_title(), edit_menu)  # Add edit submenu
    main_menu.add.button(about_menu.get_title(), about_menu)  # Add about submenu
    main_menu.add.button('Exit', pygame_menu.events.EXIT)  # Add exit function

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    algo.play_server()

    while True:
        frame += 1

        # Title is evaluated at current level as the title of the base pointer
        # object (main_menu) can change if user opens submenus
        current_menu = main_menu.get_current()
        if current_menu.get_title() != 'Main Menu' or not main_menu.is_enabled():
            if algo != None:
                # Draw
                update_data()
                draw()
        else:
            # Background color if the menu is enabled and graph is hidden
            surface.fill((40, 0, 40))

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and \
                        current_menu.get_title() == 'Main Menu':
                    main_menu.toggle()

        if main_menu.is_enabled():
            main_menu.draw(surface)
            main_menu.update(events)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test and frame == 2:
            break


def draw():#algo:GraphAlgo=None,
    surface.fill((0,134,139))
    radius = 15
    esc_text = FONT.render("To get to the Main-Menu please press->\'esc\'", True, (0, 0, 0))
    surface.blit(esc_text, (50, 45))
    while algo._client.is_running() == 'true':
        # draw nodes
        for n in algo.get_graph().getN().values():
            x = my_scale(n.get_location()[0], x=True)
            y = my_scale(n.get_location()[1], y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(surface, int(x), int(y),
                                  radius, pygame.Color(64, 80, 174))
            gfxdraw.aacircle(surface, int(x), int(y),
                             radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.get_id()), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            surface.blit(id_srf, rect)

        # draw edges
        for e in algo.get_graph()._Edges.values():
            # find the edge nodes
            src: Node = algo.get_graph().getNode(e.get_src())
            dest: Node = algo.get_graph().getNode(e.get_dest())

            # scaled positions
            src_x = my_scale(src.get_location()[0], x=True)
            src_y = my_scale(src.get_location()[1], y=True)
            dest_x = my_scale(dest.get_location()[0], x=True)
            dest_y = my_scale(dest.get_location()[1], y=True)

            # draw the line
            pygame.draw.line(surface, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))

            # display.update()
        # draw agents
        for agent in algo.agents:
            pygame.draw.circle(surface, Color(122, 61, 23),
                               (int(agent.pos.x), int(agent.pos.y)), 10)
        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in algo.pokemons:
            pygame.draw.circle(surface, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
        # update screen changes
        display.update()

            # refresh rate
        clock.tick(60)

        # choose next edge
        for agent in algo.agents:
            if agent.dest == -1:
                next_node = (agent.src - 1) % len(algo.get_graph()._Nodes)
                algo._client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = algo._client.time_to_end()
                print(ttl, algo._client.get_info())

        algo._client.move()
        # game over:
        # for src in algo.get_graph().getN().values():
        #     # src = algo.get_graph().getNode(src_id)
        #     x=my_scale(src.get_location()[0],x=True)
        #     y = my_scale(src.get_location()[1], y=True)
        #     pygame.draw.circle(surface, src.get_color(),(x,y),radius=7)
        #     src_text = FONT.render(str(src.get_id()), True, src.get_color())
        #     surface.blit(src_text, (x,y))
        #     # node_screens.append(NodeScreen(pygame.Rect((x,y),(20,20)),src.get_id()))
        #
        #     for dest in algo.get_graph().all_out_edges_of_node(src.get_id()):
        #         dest=algo.get_graph().getNode(dest)
        #         his_x=my_scale(dest.get_location()[0],x=True)
        #         his_y = my_scale(dest.get_location()[1], y=True)
        #         e = algo.get_graph().getEdge(src.get_id(), dest.get_id())
        #         # if (src.get_id(),dest.get_id()) in result:
        #         #     arrow((x,y), (his_x,his_y), 17, 7, color=(0,250,0))
        #         # else:
        #         arrow((x, y), (his_x, his_y), 17, 7, color=e.get_color())
        #         e_other = algo.get_graph().getEdge(dest.get_id(), src.get_id())
        #         if e_other != None and e_other.get_color() == (127, 255, 0):
        #             pygame.draw.line(surface, e_other.get_color(), start_pos=(x,y),end_pos=(his_x,his_y),width=3)
        #         else:
        #             pygame.draw.line(surface, e.get_color(), start_pos=(x,y),end_pos=(his_x,his_y),width=3)

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen
min_x=min_y=max_x=max_y=0
def min_max():
    global min_x, min_y, max_x, max_y
    min_x = min(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[0]).get_location()[0]
    min_y = min(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[1]).get_location()[1]
    max_x = max(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[0]).get_location()[0]
    max_y = max(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[1]).get_location()[1]
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, surface.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, surface.get_height() - 50, min_y, max_y)

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
    pygame.draw.polygon(surface, color, points)

if __name__ == '__main__':
    main()