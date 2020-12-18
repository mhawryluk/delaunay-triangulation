from random import shuffle
from visualization import *

class Triangulation:

    def __init__(self):
        self.triangles = set()
        self.edges_map = {}
        self.outer_triangle = None
    

    def add_triangle(self, triangle):
        triangle = self.sort_triangle_vertices(triangle)
        
        self.triangles.add(triangle)

        a, b, c = triangle
        self.edges_map[(a, b)] = c
        self.edges_map[(b, c)] = a
        self.edges_map[(c, a)] = b


    def remove_triangle(self, triangle):
        triangle = self.sort_triangle_vertices(triangle)
        
        self.triangles.remove(triangle)
        
        a, b, c = triangle
        del self.edges_map[(a, b)]
        del self.edges_map[(b, c)]
        del self.edges_map[(c, a)]

    def sort_triangle_vertices(self, triangle):
        a, b, c = triangle
        
        if detSgn(a,b,c) == -1:
            a, b = b, a

        while(a[1] > min(b[1], c[1])
              or (a[1] == min(b[1], c[1]) and a[1] != b[1])):
            a, b, c = b, c, a
            
        return (a, b, c)
        


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

    def triangle_adjacent(self, edge):
        '''
        zwraca trójkąt przyległy do 'triangle' o wspólnej krawędzi edge
        zakłada, ze edge jest krawędzią skierowaną zgodną z kierunkiem trójkąta
        przeciwnym do ruchu wskazówek zegara
        '''
        return (edge[1], edge[0], self.edges_map(edge[1], edge[0]))


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
        '''
        czworokąt abcd o przekątnej edge

        TODO: poprawić, gdy wierzchołek naley do zewnętrznego trójkąta
        '''

        b, c = edge
        a = self.edges_map[edge]
        d = self.edges_map[(c, b)]

        circumcenter, radius = self.find_circumcircle((b, c, a))
        
        d_dist = self.dist(d, circumcenter)
        if d_dist >= radius:
            return False
            
        return True


    def legalize_edge(self, point, edge, triangle):
        pass

    
    def edge_with_point(self, point):
        pass


    def third_vertex(self, edge):
        '''
        zwraca wierzchołek trójkąta, który nie nalezy do edge
        '''
        return self.edges_map(edge)


    def is_on_edge(self, point):
        pass


    def dist(self, point_1, point_2):
        '''
        odległość euklidesowa punktów point_1 i point_2
        '''
        return ((point_2[0]-point_1[0])**2 + (point_2[1]-point_1[1])**2)**0.5


    def find_circumcircle(self, triangle):
        '''
        zwraca środek i promień okręgu opisanego na trójkącie triangle
        wzorki z wikipedii
        '''
        a, b, c = triangle
        
        d = 2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
        
        x = ((a[0]**2 + a[1]**2)*(b[1]-c[1]) 
            + (b[0]**2 + b[1]**2)*(c[1]-a[1])
            + (c[0]**2 + c[1]**2)*(a[1]-b[1]))/d

        y = ((a[0]**2 + a[1]**2)*(c[0]-b[0]) 
            + (b[0]**2 + b[1]**2)*(a[0]-c[0])
            + (c[0]**2 + c[1]**2)*(b[0]-a[0]))/d

        return (x, y), self.dist((x,y), a)

tolerance = 10**(-12)

def det_sgn(a, b, c):
    l1 = a[0]*b[1]
    l2 = a[1]*c[0]
    l3 = b[0]*c[1]
    r1 = b[1]*c[0]
    r2 = a[0]*c[1]
    r3 = a[1]*b[0]

    value = (l1 + l2 + l3) - (r1 + r2 + r3)

    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0

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
            triangle_adjacent = triangulation.triangle_adjacent((i, j))
            l = triangulation.third_vertex((i, j))

            triangulation.split_triangle_on_edge(triangle_containing, (i,j), point)
            triangulation.split_triangle_on_edge(triangle_adjacent, (i,j), point)

            triangulation.legalize_edge(point, (i, l))
            triangulation.legalize_edge(point, (l, j))
            triangulation.legalize_edge(point, (j, k))
            triangulation.legalize_edge(point, (k, i))

    triangulation.remove_outer()
