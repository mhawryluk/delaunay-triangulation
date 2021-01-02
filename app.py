import triangulation as t
import triangulation_speed as ts
from points_generator import *
from visualization import *
import sys
from matplotlib.animation import FuncAnimation

class Option:
    def __init__(self, value, name, function):
        self.value = value.upper()
        self.name = name
        self.function = function

    def compare_to(self, value):
        return self.value == value.upper()

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
            if option.compare_to(value):
                return option
        return None

class AnimationSet:
    def __init__(self, scenes = [Scene()], points = [], lines = []):
        self.scenes = scenes

        if points or lines:
            self.scenes[0].points = points
            self.scenes[0].lines = lines
            self.compressScenes()

    def compressScenes(self):
        self.scenes = list(dict.fromkeys(self.scenes))

def end():
    return None

def draw_by_hand():
    print("W otwartym oknie wprowadź punkty, a następnie zamknij je, gdy skończysz")
    plot = Plot()
    plot.draw()

    fig = plot.get_added_elements()
    if len(fig.points) > 0:
        return fig.points[0].points
    return []

def random_points():
    print("Wprowadź liczbę punktów")

    amount = int(input())
    return generate_random_points(amount, -amount/2, amount/2)

def points_on_circle():
    print("Wprowadź liczbę punktów\nzalecany zakres [3, 5000]")
    
    amount = int(input())
    return generate_points_on_circle(amount)

def points_on_rectangle():
    print("Wprowadź liczbę punktów na osiach i liczbę punktów na przekątnych (w jednej linijce po spacji)\nzalecany zakres [0, 1000]")

    amount_axis, amount_diagonal  = map(int, input().split())
    return generate_points_on_axis_and_diagonals(amount_axis, amount_diagonal, amount_axis+1, 1.5*amount_axis+1)

def many_rectangles():
    print("Wprowadź liczbę kwadratów do wygenerowania")

    amount = int(input())
    return generate_multiple_rectangles(amount, amount/2, 2)
    
def main(options):
    flag = True
    points = None
    sys.setrecursionlimit(10000)
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

            elif len(points) == 0:
                print("\nNie wprowadzono punktów.\n")
                continue

            elif len(points) < 3:
                print("\nLiczba punktów powinna wynosić co najmniej 3.\n")
                continue

            else:
                print("\nJeśli chcesz zobaczyć animację wizualizacji działania algorytmu krok po kroku wpisz \"tak\" i wciśnij ENTER...\n(UWAGA! Ta opcja znacząco spowalnia działanie algorytmu i jest zalecana tylko dla małych zbiorów punktów)\n\ndla otrzymania czasów i końcowej wizualizacji wpisz cokolwiek innego.\n")
                extend_visuals = input()
                if extend_visuals in ["TAK", "Tak", "tak"]:
                    extend_visuals = True
                else:
                    extend_visuals = False
                    
                if extend_visuals:
                    print("Uruchamiam algorytmy z poszerzoną wizualizacją")

                    try:
                        _, scenes2 = t.delaunay_triangulation_v2(points)
                        _, scenes1 = t.delaunay_triangulation(points)
                    except:
                        print("an error occured")
                        continue

                    delay = 1.2

                    anim = AnimationSet(scenes = scenes1 + [scenes1[-1]]*12 + scenes2 + [scenes2[-1]]*12)
                    fig = plt.figure()
                    ax = plt.axes(autoscale_on = True)

                    def animate(index):
                        ax.clear()

                        for collection in (anim.scenes[index].points):
                            if len(collection.points) > 0:
                                ax.scatter(*zip(*(np.array(collection.points))), **collection.kwargs)
                        
                        for collection in (anim.scenes[index].lines):
                            ax.add_collection(collection.get_collection())

                        ax.autoscale(True)
                        plt.draw()
                        return None

                    animate(0)
                    animation = FuncAnimation(fig, animate, repeat = True, frames = np.arange(0, len(anim.scenes)), interval = delay)
                    plt.show()

                else:
                    print("Uruchamiam algorytmy")

                    try:
                        time1, search1, insert1, init1, remove1, scenes1 = ts.delaunay_triangulation(points)
                        time2, search2, insert2, init2, remove2, scenes2 = ts.delaunay_triangulation_v2(points)
                    except:
                        print("an error occured")
                        continue

                    scenes = [Scene([PointsCollection([(0,0)], color='white')]), Scene([PointsCollection(points)])] + scenes1 + scenes2
                    plot = Plot(scenes=scenes)
                    plot.draw()
                    print(f'''Liczba punktów: {len(points)}:
                        \nWersja 1: 
    Czas inicjalizacji: {init1}
    Czas wyszukiwania: {search1} 
    Czas wstawiania: {insert1}
    Czas usuwania: {remove1}
    Łączny czas: {time1} ''')
                    print(f'''Wersja 2: 
    Czas inicjalizacji: {init2}
    Czas wyszukiwania: {search2} 
    Czas wstawiania: {insert2}
    Czas usuwania: {remove2}
    Łączny czas: {time2}
    
    ''')

                

options = Options([
    Option("A", "Losowe punkty", random_points),
    Option("B", "Losowe punkty na okręgu", points_on_circle),
    Option("C", "Losowe punkty na osiach i przekątnych kwadratu", points_on_rectangle),
    Option("D", "Symetryczne kwadraty o środku w punkcie (0,0)", many_rectangles),
    Option("M", "Wprowadź punkty za pomocą myszki", draw_by_hand),
    Option("Z", "Zakończ", end)
    ])

main(options)

