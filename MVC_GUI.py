from types import SimpleNamespace
from MVC_Controller import MainAlgo
from pygame import gfxdraw
import pygame
from pygame import *
import time
import pygame_menu
import math

"""
In this task we used pattern MVC (Model-View-Controller), we did it in order to maintain the code order and correct implementation of the problem.
This is the main executable file, i.e. the part responsible for the 'View'.

From here you can run the program so that it will run the relevant algorithms 
and display the data in a convenient visual way on the screen.
This part has no direct communication with the client but only with the 'Controller'.

Authors: Roee Tal and Yossi Elias
"""

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


#########################################################################################################
#                                     main game play                                                    #
#########################################################################################################


# init pygame
WIDTH, HEIGHT = 1080, 720


pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
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
#                             reset pygame_menu                             #
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


about_menu = pygame_menu.Menu(
    center_content=False,
    height=400,
    # mouse_visible=False,
    theme=about_theme,
    title='About',
    width=600
)
m = "Assignment 3: The Pokemon game :)\n" \
    "Authors: Roee Tal and Yossi Elias\n\n" \
    "We hope the use of this \ninterface is as intuitive and convenient \nas we tried to create it.\n\n"\
    "Note: The number on the agents\n is there id's\n" \
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
# -------------------------------------------------------------------------
# End of main menu
# -------------------------------------------------------------------------




# -------------------------------------------------------------------------
# Start of the game
# -------------------------------------------------------------------------

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
            # draw pokemons
            for p in pokemons:
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
            screen.blit(image, (0, 0))
    else:
        main_algo._client.stop_connection()
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
































