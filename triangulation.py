from random import shuffle
from visualization import *


class Triangulation:

    def __init__(self):
        self.triangles = set()
        self.edges_map = {}
        self.outer_triangle = None
    

    def add_triangle(self, triangle):
        self.triangles.add(triangle)

        a, b, c = triangle
        self.edges_map[(a, b)] = c
        self.edges_map[(b, c)] = a
        self.edges_map[(c, a)] = b


    def remove_triangle(self, triangle):
        self.triangles.remove(triangle)
        
        a, b, c = triangle
        del self.edges_map[(a, b)]
        del self.edges_map[(b, c)]
        del self.edges_map[(c, a)]


    def make_outer_triangle(self, points):
        '''
        dodanie do triangulacji tymczasowego duzego trójkąta, który zawiera wszystkie punkty
        '''
        max_coord = abs(max(points, key = lambda x: abs(x[0]))[0])
        max_coord = max(max_coord, abs(max(points, key = lambda x: abs(x[1]))[1]))

        self.outer_triangle = ((3*max_coord, 0), (0, 3*max_coord), (-3*max_coord, -3*max_coord))
        self.add_triangle(self.outer_triangle)

        
    def triangle_containing(self, point):
        '''
        zwraca trójkąt, w którym lezy punkt, ewentualnie lezy na brzegu
        '''

    def triangle_adjacent(self, triangle, edge):
        '''
        zwraca trójkąt przyległy do 'triangle' o wspólnej krawędzi edge
        '''

    def split_triangle(self, triangle, point):
        '''
        podział trójkąta w przypadku, gdy nowy punkt lezy wewnątrz
        '''

    def split_triangle_on_edge(self, triangle, edge, point):
        '''
        podział trójkątów, gdy nowy punkt lezy na krawędzi
        '''

    def remove_outer(self):
        '''
        usunięcię wszystkich trójkątów, które zawierają dodane na początku wierzchołki duzego trójkąta
        '''

        outer_vertices = set(self.outer_triangle)
        triangles = list(self.triangles)

        for triangle in triangles:
            if not triangle[0] in outer_vertices and not triangle[1] in outer_vertices and not triangle[2] in outer_vertices:
                continue

            self.remove_triangle(triangle)

        
    def is_illegal(self, edge):
        pass


    def legalize_edge(self, point, edge, triangle):
        pass

    
    def edge_with_point(self, point):
        pass


    def third_vertex(self, triangle, edge):
        '''
        zwraca wierzchołek trójkąta, który nie nalezy do edge
        '''

    def is_on_edge(self, point):
        pass
    

    def find_circumcircle(self, triangle):
        pass



def delaunay_triangulation(points):
    '''
    główna funkcja do triangulacji w pierwszym wariancie
    na podstawie pseudokodu z ksiązki de Berga
    '''
    triangulation = Triangulation()
    triangulation.make_outer_triangle(points)

    shuffle(points)

    for point in points:
        triangle_containing = triangulation.triangle_containing(point)

        if not triangle_containing.is_on_edge(point): # punkt wewnątrz trójkąta
            triangulation.split_triangle(triangle_containing, point)
            i, j, k = triangle_containing.get_vertices()
            triangulation.legalize_edge(point, (i, j))
            triangulation.legalize_edge(point, (j, k))
            triangulation.legalize_edge(point, (k, i))

        else: # punkt na brzegu trójkąta
            i, j = triangle_containing.edge_with_point(point)
            triangle_adjacent = triangulation.triangle_adjacent(triangle_containing, (i, j))
            l = triangulation.third_vertex((i, j))

            triangulation.split_triangle_on_edge(triangle_containing, (i,j), point)
            triangulation.split_triangle_on_edge(triangle_adjacent, (i,j), point)

            triangulation.legalize_edge(point, (i, l))
            triangulation.legalize_edge(point, (l, j))
            triangulation.legalize_edge(point, (j, k))
            triangulation.legalize_edge(point, (k, i))

    triangulation.remove_outer()
