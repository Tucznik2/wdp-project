import time
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TrackedArray():

    def __init__(self, arr, kind="minimal"):
        self.arr = np.copy(arr)
        self.kind = kind
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
        if self.kind == "full":
            self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])

    def __delitem__(self, key):
        self.track(key, "del")
        self.arr.__delitem__(key)

    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):
        return self.arr.__len__()

    def __str__(self):
        return self.arr.__str__()

    def __repr__(self):
        return self.arr.__repr__()

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
        self.speed_select = tk.OptionMenu(self.speed_frame, self.speed_default,"1","10","100", "200", "500", "1000", "2000", "3000")
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

    def show_graph(self, button):
        N = 30
        FPS = 60
        arr = np.round(np.linspace(0, 1000, N), 0)
        np.random.seed(0)
        np.random.shuffle(arr)

        arr = TrackedArray(arr, "full")

        np.random.seed(0)

        sorter = "Insertion"
        t0 = time.perf_counter()
        i = 1
        while i < len(arr):
            j = i
            while (j > 0) and (arr[j-1] > arr[j]):
                temp = arr[j-1]
                arr[j-1] = arr[j]
                arr[j] = temp
                j -= 1

            i += 1
        t_ex = time.perf_counter() - t0

        print(f"---------- {sorter} Sort ----------")
        print(f"Array Sorted in {t_ex * 1E3:.1f} ms | {len(arr.full_copies):.0f} "
              f"array access operations were performed")


        fig, ax = plt.subplots(figsize=(16, 8))
        container = ax.bar(np.arange(0, len(arr), 1),
                           arr.full_copies[0], align="edge", width=0.8)
        fig.suptitle(f"{sorter} sort")
        ax.set(xlabel="Index", ylabel="Value")
        ax.set_xlim([0, N])
        txt = ax.text(0.01, 0.99, "", ha="left", va="top", transform=ax.transAxes)


        def update(frame):
            txt.set_text(f"Accesses = {frame}")
            for rectangle, height in zip(container.patches, arr.full_copies[frame]):
                rectangle.set_height(height)
                rectangle.set_color("#1f77b4")

            idx, op = arr.GetActivity(frame)
            if op == "get":
                container.patches[idx].set_color("magenta")
            elif op == "set":
                container.patches[idx].set_color("red")


            return (*container,)


        if __name__ == "__main__":
            ani = FuncAnimation(fig, update, frames=range(len(arr.full_copies)),
                                blit=True, interval=1000. / FPS, repeat=False)

            plt.show()

GUI()