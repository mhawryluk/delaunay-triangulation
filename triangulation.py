from random import shuffle

class Triangulation:

    def __init__(self):
        self.triangles = set()
        self.edges_map = {}
    
    def add_triangle(self, triangle):
        pass

    def make_outer_triangle(self, points):
        '''
        dodanie do triangulacji tymczasowego duzego trójkąta, który zawiera wszystkie punkty
        '''
        
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
        podział trójkąta w przypadku, gdy nowy punk lezy wewnątrz
        '''

    def split_triangle_on_edge(self, triangle, edge, point):
        '''
        podział trójkątów, gdy nowy punkt lezy na krawędzi
        '''

    def remove_outer(self):
        '''
        usunięcię wszystkich trójkątów, które zawierają dodane na początku wierzchołki duzego trójkąta
        '''
        
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
