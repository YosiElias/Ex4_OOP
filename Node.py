# from random import random
# import random
#
#
# class Node:
#
#     def __init__(self, id, pos:tuple=None):
#         self._color = (245,255,250)
#         self._key = id
#         self._tag = -1
#         self._info = float('inf')
#         self._visited = False
#         self._maxDist = 1.7976931348623157E308
#         if pos == None:
#             self.set_location_random()
#         else:
#             if len(pos)==2:
#                 pos_new = float(pos[0]), float(pos[1])
#             if len(pos)==3:
#                 pos_new = float(pos[0]), float(pos[1]), float(pos[2])
#             self._location=pos_new
#         self._edges_out = 0
#         self._edges_in = 0
#
#     def __repr__(self):
#         return '{}: |edges_out| {} |edges in| {}'.format(self._key, self._edges_out, self._edges_in)
#
#     def get_out(self):
#         return self._edges_out
#
#     def set_out(self, n:int=0):
#         self._edges_out = self._edges_out +n
#
#     def get_in(self):
#         return self._edges_in
#
#     def set_in(self, n:int=0):
#         self._edges_in = self._edges_in + n
#
#     def get_id(self):
#         return self._key
#
#     def get_tag(self):
#         return self._tag
#
#     def get_info(self):
#         return self._info
#
#     def set_info(self,s):
#         self._info = s
#
#     def set_tag(self,s):
#         self._tag = s
#
#     def get_visit(self):
#         return self._visited
#
#     def set_visit(self, b:bool):
#         self._visited = b
#
#     def get_maxDist(self):
#         return self._maxDist
#
#     def set_maxDist(self, n):
#         self._maxDist = n
#
#     def get_color(self):
#         return self._color
#
#     def set_color(self, color: tuple):
#         self._color = color
#
#     def get_location(self) -> tuple:
#         return self._location
#
#     def set_location_random(self):
#         (x, y) = random.uniform(0, 100), random.uniform(0, 100)
#         self._location = (x, y)
#
