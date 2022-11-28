# zaimportowane biblioteki
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# funkcje algorytmów sortowania
def selection_sort(lst):
    for i in range(len(lst) - 1):
        minimum = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[minimum]:
                minimum = j
        if i != minimum:
            pom = lst[i]
            lst[i] = lst[minimum]
            lst[minimum] = pom


def bubble_sort(lst):
    for i in range(len(lst)):
        for j in range(0, len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]


def insertion_sort(lst):
    for i in range(1, len(lst)):
        selected = lst[i]
        y = i - 1
        while y >= 0 and selected < lst[y]:
            lst[y + 1] = lst[y]
            y -= 1
        lst[y + 1] = selected


# definicja klasy, która pozwala nam śledzić operacje jakie zostały wykonane na naszej liście
class TrackedArray:

    def __init__(self, arr):
        self.arr = np.copy(arr)
        self.reset()

    def reset(self):
        self.indices = []
        self.values = []
        self.access_type = []
        self.full_copies = []

    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return self.indices[idx], self.access_type[idx]

    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):
        return self.arr.__len__()


class GUI:
    # konstruktor tworzący interfejs graficzny
    def __init__(self):
        # bazowe okno
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("Wizualizacja Algorytmów Sortowania")

        # kontener na dane wejsciowe
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.columnconfigure(0, weight=1)
        self.entry_frame.columnconfigure(1, weight=1)

        # kontener ilosci liczb
        self.size_frame = tk.Frame(self.entry_frame)
        self.size_frame.columnconfigure(0, weight=1)
        self.size_frame.columnconfigure(1, weight=1)
        self.size_label = tk.Label(self.size_frame, text="Wprowadź ilość liczb do sortowania:", font=('Arial', 16))
        self.size_entry = tk.Entry(self.size_frame)
        self.size_label.grid(row=0, column=0, sticky=tk.W + tk.E, padx=10)
        self.size_entry.grid(row=0, column=1, sticky=tk.W + tk.E)

        # kontener predkosci sortowania
        self.speed_frame = tk.Frame(self.entry_frame)
        self.speed_frame.columnconfigure(0, weight=1)
        self.speed_frame.columnconfigure(1, weight=1)
        self.speed_label = tk.Label(self.speed_frame, text="Wybierz prędkość sortowania:", font=('Arial', 16))
        self.speed_default = tk.StringVar(self.speed_frame)
        self.speed_default.set("1000")
        self.speed_select = tk.OptionMenu(self.speed_frame, self.speed_default, "1", "10", "100", "200", "500", "1000",
                                          "2000", "3000")
        self.speed_label.grid(row=0, column=0, sticky=tk.W + tk.E, padx=10)
        self.speed_select.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.size_frame.grid(row=0, column=0, sticky=tk.W + tk.E, padx=10)
        self.speed_frame.grid(row=0, column=1, sticky=tk.W + tk.E, padx=10)
        self.entry_frame.place(relx=0.5, y=20, anchor=tk.CENTER)

        # kontener przyciskow
        self.buttonframe = tk.Frame(self.root)

        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)

        self.bubble_button = tk.Button(self.buttonframe, text="Sortowanie Bąbelkowe", font=('Arial', 16),
                                       command=lambda t="bubble": self.show_graph(t))
        self.bubble_button.grid(row=0, column=0, sticky=tk.W + tk.E, padx=10)

        self.insertion_button = tk.Button(self.buttonframe, text="Sortowanie przez wstawianie", font=('Arial', 16),
                                          command=lambda t="insert": self.show_graph(t))
        self.insertion_button.grid(row=0, column=1, sticky=tk.W + tk.E, padx=10)

        self.selection_button = tk.Button(self.buttonframe, text="Sortowanie przez wybieranie", font=('Arial', 16),
                                          command=lambda t="select": self.show_graph(t))
        self.selection_button.grid(row=0, column=2, sticky=tk.W + tk.E, padx=10)

        self.buttonframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.root.mainloop()

    # funkcja sprawdza, który guzik został wciśnięty, a nastepnie generuje wykres i ustawia odpowiedni tytuł
    def show_graph(self, button):
        fps = 60
        lst = np.random.randint(1, 100, int(self.size_entry.get()))
        np.random.seed(0)
        np.random.shuffle(lst)
        lst = TrackedArray(lst)
        np.random.seed(0)

        # zapis do pliku danych do posortowania
        result_file = open('wyniki.txt', 'a')
        result_file.write('Dane do posortowania:\n')
        for x in lst.arr:
            result_file.write(str(x) + " ")

        result_file.write('\n')

        # wybór algorytmu sortowania
        if button == "bubble":
            title = "Bubble"
            bubble_sort(lst)
        elif button == "insert":
            title = "Insertion"
            insertion_sort(lst)
        elif button == "select":
            title = "Selection"
            selection_sort(lst)

        fig, ax = plt.subplots(figsize=(16, 8))
        bar_rect = ax.bar(np.arange(0, len(lst), 1),
                          lst.full_copies[0], align="edge", width=0.8)
        fig.suptitle(f"{title} sort")
        ax.set(xlabel="Index", ylabel="Wartość")
        ax.set_xlim([0, int(self.size_entry.get())])
        txt = ax.text(0.01, 0.99, "", ha="left", va="top", transform=ax.transAxes)

        # odświeżanie wykresu
        def update(frame):
            txt.set_text(f"Operacje = {frame}")
            for rectangle, height in zip(bar_rect.patches, lst.full_copies[frame]):
                rectangle.set_height(height)
                rectangle.set_color("#1f77b4")

            idx, op = lst.GetActivity(frame)
            if op == "get":
                bar_rect.patches[idx].set_color("green")
            elif op == "set":
                bar_rect.patches[idx].set_color("red")

            return txt, *bar_rect

        # animacja wykresu
        anim = FuncAnimation(fig, update, frames=range(len(lst.full_copies)),
                            blit=True, interval=int(self.speed_default.get()) / fps, repeat=False)

        plt.show()

        # zapis do pliku
        result_file.write('Dane posortowane:\n')
        for x in lst.arr:
            result_file.write(str(x) + " ")

        result_file.write('\n')
        result_file.close()


# instacja klasy
GUI()
