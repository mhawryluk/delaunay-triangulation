import triangulation as t
import triangulation_speed as ts
from points_generator import *
from visualization import *

class Option:
    def __init__(self, value, name, function):
        self.value = value
        self.name = name
        self.function = function
    def compareTo(self, value):
        return self.value == value

    def execute(self):
        return self.function()

    def show(self):
        print(f"{self.value}) {self.name}")

class Options:
    def __init__(self, options):
        self.list = options

    def values(self):
        values = []
        for option in self.list:
            values.append(option.value)
        return values
    
    def get(self, value):
        for option in self.list:
            if option.compareTo(value):
                return option
        return None

def end():
    return None

def draw_by_hand():
    print("W otwartym oknie wprowadź punkty, a następnie zamknij je, gdy skończysz")
    plot = Plot()
    plot.draw()

    fig = plot.get_added_elements()
    if len(fig.points) > 0:
        return fig.points[0].points
    return None

def random_points():
    print("Wprowadź liczbę punktów")

    amount = int(input())
    return generate_random_points(amount, -amount/2, amount/2)

def points_on_circle():
    print("Wprowadź liczbę punktów")
    
    amount = int(input())
    return generate_points_on_circle(amount)

def points_on_rectangle():
    print("Wprowadź liczbę punktów na osisach i liczbę punktów na przekątnych")

    amount_axis, amount_diagonal  = map(int, input().split())
    return generate_points_on_axis_and_diagonals(amount_axis, amount_diagonal, amount_axis, 1.5*amount_axis)
    
def main(options):
    flag = True
    points = None
    while flag:
        print("Dostępne opcje: ")
        for option in options.list:
            option.show()
        print("Wybierz jedną z nich, a następnie wciśnij ENTER")

        chosen_value = input()
        chosen_option = options.get(chosen_value)

        if chosen_option is None:
            print("Taka opcja nie istnieje")
        else:
            points = chosen_option.execute()
            if points is None:
                flag = False
            else:
                print("Jeśli chcesz otrzymać pełną wizualizację dizałania algorytmu wpisz \"tak\" i wciścnij ENTER\n UWAGA!!! Ta opcja znacząco wpowalnia dizałanie algorytmu i jest zalecana tylko dla małych zbiorów punktów")
                extend_visuals = input()
                if extend_visuals in ["TAK", "Tak", "tak"]:
                    extend_visuals = True
                else:
                    extend_visuals = False
                    
                if extend_visuals:
                    print("Uruchamiam algorytmy z poszerzoną wizualizacją")
                    _, _, scenes1 = t.delaunay_triangulation(points)
                    _, _, scenes2 = t.delaunay_triangulation_v2(points)
                    scenes1 = [Scene(PointsCollection([points]))] + [scenes1[-1]] + scenes1[:-1]
                    scenes2 = [Scene(PointsCollection([points]))] + [scenes2[-1]] + scenes2[:-1]
                    plot1 = Plot(scenes=scenes1)
                    plot2 = Plot(scenes=scenes2)

                    plot1.draw()
                    plot2.draw()
                else:
                    print("Uruchamiam algorytmy")
                    time1, search1, insert1, init1, remove1, scenes = ts.delaunay_triangulation(points)
                    time2, search2, insert2, init2, remove2, _ = ts.delaunay_triangulation_v2(points)
                    scenes = [Scene(PointsCollection[points])] + scenes
                    plot = Plot(scenes=scenes)
                    plot.draw()
                    print("Version 1:")
                    print(f'''{n}:
                        \nv1: 
                        init: {init1}
                        search time: {search1} 
                        insert time: {sum(insert1)}
                        remove time: {remove1}
                        total time: {time1} ''')
                    print("Version 2:")
                    print(f'''v2: 
                        init: {init2}
                        search time: {search2} 
                        insert time: {sum(insert2)}
                        remove time: {remove2}
                        total time: {time2}''')

                
    


options = Options([
    Option("A", "Narysuj punkty własnoręcznie", draw_by_hand),
    Option("B", "Losowe punkty", random_points),
    Option("C", "Losowe punkty na okręgu", points_on_circle),
    Option("D", "Losowe punkty na osiach i przekątnych kwadratu", points_on_rectangle),
    Option("Z", "Zakończ", end)
    ])

main(options)
