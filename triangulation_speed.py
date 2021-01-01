from random import shuffle
from math import inf
from visualization import *
from points_generator import *
from time import time

TOLERANCE = 1e-8
scenes = []

class Triangulation:

    def __init__(self, algorithm=0):
        self.triangles = set()
        self.edges_map = {}
        self.outer_triangle = None
        self.central_triangle = None
        self.central_point = None
        self.time = 0
        self.search_time = 0
        self.insert_times = []

        if algorithm == 1:
            self.scale = 1000
        else:
            self.scale = 1

    def get_lines(self):
        return list(self.edges_map.keys())


    def centroid_of_triangle(self, triangle):
        (ax, ay), (bx, by), (cx, cy) = triangle
        return ((ax+bx+cx)/3 , (ay+by+cy)/3)
    

    def add_triangle(self, triangle):
        triangle = self.sort_triangle_vertices(triangle)
        
        self.triangles.add(triangle)
        
        a, b, c = triangle
        self.edges_map[(a, b)] = c
        self.edges_map[(b, c)] = a
        self.edges_map[(c, a)] = b


    def remove_triangle(self, triangle):
        '''
        funkcja wyliczająca śtrodek ciężkości trójkąta
        '''
        triangle = self.sort_triangle_vertices(triangle)
        
        self.triangles.remove(triangle)
        
        a, b, c = triangle
        # if (a,b) in self.edges_map:
        del self.edges_map[(a, b)]
        
        # if (b, c) in self.edges_map:
        del self.edges_map[(b, c)]
        
        # if (c,a) in self.edges_map:
        del self.edges_map[(c, a)]


    def sort_triangle_vertices(self, triangle):
        '''
        sortowanie wierzchołków trójkąta ccw
        '''
        a, b, c = triangle
        
        if det_sgn(a,b,c) == -1:
            a, b = b, a

        while(a[1] > min(b[1], c[1])
              or (a[1] == min(b[1], c[1]) and a[1] != b[1])):
            a, b, c = b, c, a
            
        return (a, b, c)


    def make_outer_triangle(self, points):
        '''
        dodanie do triangulacji tymczasowego duzego trójkąta, który zawiera wszystkie punkty
        dodanie trójkąta środkowego i punktu środkowego (pomagającego w jego aktualicacji)
        '''
        max_coord = abs(max(points, key=lambda x: abs(x[0]))[0])
        max_coord = max(max_coord, abs(max(points, key = lambda x: abs(x[1]))[1]))

        self.outer_triangle = ((4*max_coord, 0), (0, 4*max_coord), (-4*max_coord, -4*max_coord))
        self.outer_triangle = self.sort_triangle_vertices(self.outer_triangle)
        self.add_triangle(self.outer_triangle)

        self.central_triangle = self.outer_triangle
        self.central_point = self.centroid_of_triangle(self.outer_triangle)


    def remove_outer(self):
        '''
        usunięcię wszystkich trójkątów, które zawierają dodane na początku wierzchołki duzego trójkąta
        '''

        outer_vertices = set(self.outer_triangle)

        triangles = list(self.triangles)
        for triangle in triangles:
            if triangle[0] in outer_vertices or triangle[1] in outer_vertices or triangle[2] in outer_vertices:
                self.remove_triangle(triangle)


    def triangle_containing(self, point):

        start = time()
        '''
        zwraca trójkąt, w którym lezy punkt, ewentualnie lezy na brzegu
        '''
        current = self.central_triangle

        i = 0

        while True:
            i += 1

            if (i > len(self.triangles)):
                print(i)
                scenes.append(Scene(points=[PointsCollection([point], color='red')],
                lines=[LinesCollection(self.get_lines(), color='blue'),
                LinesCollection(self.edges(current), color='yellow')]))
            
            if (i >= len(self.triangles) + 100):
                return

            a, b, c = current

            if det_sgn(a, b, point) == -1:
                current = self.triangle_adjacent((a,b))
            elif det_sgn(b, c, point) == -1:
                current = self.triangle_adjacent((b,c))
            elif det_sgn(c, a, point) == -1:
                current = self.triangle_adjacent((c,a))
            else:
                end = time()
                self.search_time += (end-start)
                return current


    def triangle_adjacent(self, edge):
        '''
        zwraca trójkąt przyległy do 'triangle' o wspólnej krawędzi edge
        zakłada, ze edge jest krawędzią skierowaną zgodną z kierunkiem trójkąta
        przeciwnym do ruchu wskazówek zegara
        '''
        if (edge[1], edge[0]) in self.edges_map:
            return self.sort_triangle_vertices((edge[1], edge[0], self.edges_map[(edge[1], edge[0])]))
        
        return None


    def all_triangles_adjacent(self, triangle):
        triangles = []
        a, b, c = triangle

        triangle_adjacent = self.triangle_adjacent((a,b))
        if triangle_adjacent:
            triangles.append(triangle_adjacent)

        triangle_adjacent = self.triangle_adjacent((b,c))
        if triangle_adjacent:
            triangles.append(triangle_adjacent)

        triangle_adjacent = self.triangle_adjacent((c,a))
        if triangle_adjacent:
            triangles.append(triangle_adjacent)
        
        return triangles


    def is_triangle_central(self, triangle):
        '''
        sprawdzenie, czy trójkąt jest trójkątem centralnym
        '''
        return self.sort_triangle_vertices(triangle) == self.central_triangle


    def update_central_triangle(self, triangle_list):
        '''
        update centralnego trójkąta
        '''
        for triangle in triangle_list:
            a, b, c = self.sort_triangle_vertices(triangle)
            if det_sgn(a, b, self.central_point) != -1 and det_sgn(b, c, self.central_point) != -1 and det_sgn(c, a, self.central_point) != -1:
                self.central_triangle = (a,b,c)


    def edges(self, triangle):  
        a, b, c = triangle
        return [(a,b), (b,c), (c,a)]


    def split_triangle(self, triangle, point):
        '''
        podział trójkąta w przypadku, gdy nowy punkt lezy wewnątrz
        '''
        start = time()
        triangle1 = point, triangle[0], triangle[1]
        triangle2 = point, triangle[1], triangle[2]
        triangle3 = point, triangle[0], triangle[2]


        if self.is_triangle_central(triangle):
            self.update_central_triangle([triangle1, triangle2, triangle3])
            
        self.remove_triangle(triangle)
        
        self.add_triangle(triangle1)
        self.add_triangle(triangle2)
        self.add_triangle(triangle3)

        self.legalize_edge(point, (triangle[0], triangle[1]))
        self.legalize_edge(point, (triangle[1], triangle[2]))
        self.legalize_edge(point, (triangle[2], triangle[0]))

        end = time()
        self.insert_times.append(end-start)


    def split_triangle_on_edge(self, edge, point):
        '''
        podział trójkątów, gdy nowy punkt lezy na krawędzi
        '''

        start = time()

        ver1, ver2 = edge

        if not edge in self.edges_map:
            ver1, ver2 = ver2, ver1

        edge1 = ver1, ver2
        edge2 = ver2, ver1
        third_vertex_1 = self.third_vertex(edge1)
        third_vertex_2 = self.third_vertex(edge2)
    
        oldTriangle1 = ver1, ver2, third_vertex_1
        oldTriangle2 = ver1, ver2, third_vertex_2
        
        triangle1 = point, ver1, third_vertex_1
        triangle2 = point, ver1, third_vertex_2
        triangle3 = point, ver2, third_vertex_1
        triangle4 = point, ver2, third_vertex_2

        if self.is_triangle_central(oldTriangle1) or self.is_triangle_central(oldTriangle2):
            self.update_central_triangle([triangle1, triangle2, triangle3, triangle4])

        self.remove_triangle(oldTriangle1)
        self.remove_triangle(oldTriangle2)

        self.add_triangle(triangle1)
        self.add_triangle(triangle2)
        self.add_triangle(triangle3)
        self.add_triangle(triangle4)

        self.legalize_edge(point, (ver1, third_vertex_1))
        self.legalize_edge(point, (ver1, third_vertex_2))
        self.legalize_edge(point, (ver2, third_vertex_1))
        self.legalize_edge(point, (ver2, third_vertex_2))

        end = time()
        self.insert_times.append(end-start)


    def intersect(self, l1b, l1e, l2b, l2e):
        return det_sgn(l1b, l1e, l2b) * det_sgn(l1b, l1e, l2e) == -1 and det_sgn(l2b, l2e, l1b) * det_sgn(l2b, l2e, l1e) == -1 


    def is_illegal(self, edge):
        '''
        czworokąt abcd o przekątnej edge
        '''
        b, c = edge
        if not (c, b) in self.edges_map: return False

        a = self.edges_map[edge]
        d = self.edges_map[(c, b)]

        if not self.intersect(a, d, b, c):
            return False

        outer_vertices = set(self.outer_triangle)

        if (a in outer_vertices or b in outer_vertices or c in outer_vertices or d in outer_vertices):
            return self.is_illegal_outer(edge)
        
        return self.is_within_circumcircle_det((a,b,c), d)
        

    def is_illegal_outer(self, edge):
        b, c = edge
        
        a = self.edges_map[edge]
        d = self.edges_map[(c, b)]

        def outer_triangle_index(x):
            v1 = max(self.outer_triangle, key=lambda x: x[0])
            v2 = max(self.outer_triangle, key=lambda x: x[1])
            v3 = min(self.outer_triangle, key=lambda x: x[0])

            if x == v1: return -1
            if x == v2: return -2
            if x == v3: return -3
            return 0

        indices = list(map(outer_triangle_index, [a, b, c, d]))
        is_outer = list(map(lambda x: x<0, indices))

        if is_outer[1] and is_outer[2]:
            return False

        if is_outer == [False, True, False, False] or is_outer == [False, False, True, False]:
            return True

        if is_outer == [True, False, False, False] or is_outer == [False, False, False, True]:
            return False
        
        negative_index_a_d = min(indices[0], indices[3])
        negative_index_b_c = min(indices[1], indices[2])

        return negative_index_b_c > negative_index_a_d


    def legalize_edge(self, point, edge):
        if not edge in self.edges_map:
            return  

        illegal = self.is_illegal(edge)

        if illegal:
            a, b = edge
            if(self.third_vertex(edge) != point):
                a, b = b, a
            c = self.third_vertex((b,a)) 

            if self.is_triangle_central((a,b,point)) or  self.is_triangle_central((a,b,c)):
                self.update_central_triangle([(a, point, c), (b, point, c)])

            self.remove_triangle((a,b,point))
            self.remove_triangle((a,b,c))
            
            self.add_triangle((a, point, c))
            self.add_triangle((b, point, c))

            self.legalize_edge(point, (a, c))
            self.legalize_edge(point, (b, c))

    
    def edge_with_point(self, point, triangle):
        a, b, c = triangle
        
        if det_sgn(a, b, point) == 0:
            return (a, b)
        if det_sgn(b, c, point) == 0:
            return (b, c)
        if det_sgn(c, a, point) == 0:
            return (c, a)
        return None


    def third_vertex(self, edge):
        '''
        zwraca wierzchołek trójkąta, który nie nalezy do edge
        '''
        return self.edges_map[edge]


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

        return (x, y), dist((x,y), a)


    def is_within_circumcircle(self, triangle, point):

        circumcenter, radius = self.find_circumcircle(triangle)
        dist_to_center = dist(point, circumcenter)

        return dist_to_center <= radius - TOLERANCE

    
    def is_within_circumcircle_det(self, triangle, point):

        a, b, c = self.sort_triangle_vertices(triangle)
        d = point

        if a in self.outer_triangle:
            a = (a[0]*self.scale, a[1]*self.scale)

        if b in self.outer_triangle:
            b = (b[0]*self.scale, b[1]*self.scale)

        if c in self.outer_triangle:
            c = (c[0]*self.scale, c[1]*self.scale)

        if d in self.outer_triangle:
            d = (d[0]*self.scale, d[1]*self.scale)


        matrix = [[a[0], a[1], a[0]**2 + a[1]**2, 1],
                            [b[0], b[1], b[0]**2 + b[1]**2, 1],
                            [c[0], c[1], c[0]**2 + c[1]**2, 1],
                            [d[0], d[1], d[0]**2 + d[1]**2, 1]]

        return determinant_recursive(matrix) > -TOLERANCE
    

    def is_within_triangle(self, triangle, point):
        a, b, c, = self.sort_triangle_vertices(triangle)
        return det_sgn(a, b, point) != -1 and det_sgn(b, c, point) != -1 and det_sgn(c, a, point) != -1 


    def remove_and_connect(self, triangles_to_remove, point_to_add):
        points = set()

        for triangle in triangles_to_remove:
            points.add(triangle[0])
            points.add(triangle[1])
            points.add(triangle[2])
            self.remove_triangle(triangle)
        
        points = list(points)
        sort_points(points, point_to_add, 0, len(points)-1)
        triangles_added = []
        edges_added = []

        for i in range(len(points)):
            triangles_added.append((point_to_add, points[i], points[i-1]))
            self.add_triangle((point_to_add, points[i], points[i-1]))
        
        if self.central_triangle in triangles_to_remove:
            self.update_central_triangle(triangles_added)
    

    def remove_and_connect_2(self, triangles_to_remove, point_to_add):
        outer_edges = []

        triangles_to_remove = list(map(lambda x: self.sort_triangle_vertices(x), triangles_to_remove))

        for triangle in triangles_to_remove:
            for edge in self.edges(triangle):
                a, b = edge
                if not (b, a) in self.edges_map:
                    outer_edges.append(edge)
                elif not self.triangle_adjacent((a,b)) in triangles_to_remove:
                    outer_edges.append(edge)

        for triangle in triangles_to_remove:
            self.remove_triangle(triangle)
        
        triangles_added = []

        for edge in outer_edges:
            triangles_added.append(self.sort_triangle_vertices((point_to_add, edge[0], edge[1])))
            self.add_triangle((point_to_add, edge[0], edge[1]))

        
        if self.central_triangle in triangles_to_remove:
            self.update_central_triangle(triangles_added)


def det_sgn(a, b, c):
    l1 = a[0]*b[1]
    l2 = a[1]*c[0]
    l3 = b[0]*c[1]
    r1 = b[1]*c[0]
    r2 = a[0]*c[1]
    r3 = a[1]*b[0]

    value = (l1 + l2 + l3) - (r1 + r2 + r3)

    if value > TOLERANCE:
        return 1
    if value < -TOLERANCE:
        return -1
    return 0


def dist(point_1, point_2):
    '''
    odległość euklidesowa punktów point_1 i point_2
    do kwadratu
    '''
    return (point_2[0]-point_1[0])**2 + (point_2[1]-point_1[1])**2

def copy_array(A):
    return [x[:] for x in A]


def determinant_recursive(A, total=0):
    indices = list(range(len(A)))
     
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val
 
    for fc in indices:
        As = copy_array(A)
        As = As[1:]
        height = len(As)
 
        for i in range(height): 
            As[i] = As[i][0:fc] + As[i][fc+1:] 
 
        sign = (-1) ** (fc % 2)
        sub_det = determinant_recursive(As)
        total += sign * A[0][fc] * sub_det 
 
    return total


def sort_points(t, p0, a, b):  
    '''
    t -> tablica do posortowania (modyfikuje przekazaną tablicę)
    p0 -> punkt względem którego sortujemy
    a, b -> liczby naturalne określające przedział aktualnie sortowany
    '''
    
    pivot = t[b]
    i = a

    for j in range(a, b):
        if det_sgn(p0, t[j], pivot) == 1:
            t[i], t[j] = t[j], t[i]
            i += 1

    t[b], t[i] = t[i], t[b]
    if i > a: sort_points(t, p0, a, i-1)
    if i < b: sort_points(t, p0, i+1, b)


def delaunay_triangulation(points):
    '''
    główna funkcja do triangulacji w pierwszym wariancie
    na podstawie pseudokodu z ksiązki de Berga
    '''

    start = time()

    init_start = time()
    triangulation = Triangulation(0)
    triangulation.make_outer_triangle(points)
    init_end = time()

    # shuffle(points)

    for point in points:
        print(points.index(point), '/', len(points))
        triangle_containing = triangulation.triangle_containing(point)
        edge = triangulation.edge_with_point(point, triangle_containing)

        if edge is None: # punkt wewnątrz trójkąta
            triangulation.split_triangle(triangle_containing, point)
            i, j, k = triangle_containing


        else: # punkt na brzegu trójkąta
            i, j = edge
            triangle_adjacent = triangulation.triangle_adjacent((i, j))
            l = triangulation.third_vertex((i, j))

            triangulation.split_triangle_on_edge((i,j), point)

    remove_start = time()
    triangulation.remove_outer()
    remove_end = time()

    end = time()
    return end - start, triangulation.search_time, triangulation.insert_times, init_end - init_start, remove_end - remove_start, [ Scene([LinesCollection(self.get_lines(), color='darkblue')]) ]


def delaunay_triangulation_v2(points): # Bowyer–Watson
    '''
    główna funkcja do triangulacji w drugim wariancie
    na podstawie wykładu
    '''

    main_start = time()

    init_start = time()
    triangulation = Triangulation(1)
    triangulation.make_outer_triangle(points)
    init_end = time()

    # shuffle(points)

    for point in points:
        triangle_containing = triangulation.triangle_containing(point)

        start = time()
        stack = []
        triangles_to_remove = [triangle_containing]
        triangles_adjacent = triangulation.all_triangles_adjacent(triangle_containing)
        stack += triangles_adjacent
        triangles_visited = [triangle_containing]


        while len(stack) > 0:
            current_triangle = stack.pop()
            triangles_visited.append(current_triangle)
            if triangulation.is_within_circumcircle_det(current_triangle, point):
                triangles_to_remove.append(current_triangle)
                triangles_adjacent = triangulation.all_triangles_adjacent(current_triangle)
                for triangle in triangles_adjacent:
                    if triangle not in triangles_visited and triangle not in stack:
                        stack.append(triangle)
    
        triangulation.remove_and_connect_2(triangles_to_remove, point)
        end = time()
        triangulation.insert_times.append(end-start)
    
    remove_start = time()
    triangulation.remove_outer()
    remove_end = time()

    main_end = time()
    return main_end-main_start, triangulation.search_time, triangulation.insert_times, init_end - init_start, remove_end - remove_start, [ Scene([LinesCollection(self.get_lines(), color='lightblue')]) ]



if __name__ == '__main__':
    # N = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    N = [10000, 50000]

    for n in N:
        points = generate_points_on_circle(n)

        try:
            time1, search1, insert1, init1, remove1 = delaunay_triangulation(points)
            print(f'''{n}:
                    \nv1: 
                    init: {init1}
                    search time: {search1} 
                    insert time: {sum(insert1)}
                    remove time: {remove1}
                    total time: {time1} ''')
            
            if len(scenes) > 0:
                plot1 = Plot(scenes=scenes)
                plot1.draw()
        except:
            pass
        scenes = []

        try:
            time2, search2, insert2, init2, remove2 = delaunay_triangulation_v2(points)
            print(f'''v2: 
                    init: {init2}
                    search time: {search2} 
                    insert time: {sum(insert2)}
                    remove time: {remove2}
                    total time: {time2}''')
        except:
            pass
        
        if len(scenes) > 0:
            plot2 = Plot(scenes=scenes)
            plot2.draw()


        # print(f'''{n}:
        #             \nv1: 
        #             init: {init1}
        #             search time: {search1} 
        #             insert time: {sum(insert1)}
        #             remove time: {remove1}
        #             total time: {time1} 
        #             \nv2: 
        #             init: {init2}
        #             search time: {search2} 
        #             insert time: {sum(insert2)}
        #             remove time: {remove2}
        #             total time: {time2}''')
        
