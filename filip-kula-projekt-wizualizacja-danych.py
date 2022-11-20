# importowanie potrzebnych bibliotek
import tkinter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import tkinter as tk


# funkcja sortowania bombelkowego
def bubble_sort(lst):
    for i in range(len(lst)):
        for j in range(0, len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
            yield lst


# funckja sortowania przez wybieranie
def selection_sort(lst):
    for i in range(len(lst) - 1):
        minimum = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[minimum]:
                minimum = j
            yield lst
        if i != minimum:
            pom = lst[i]
            lst[i] = lst[minimum]
            lst[minimum] = pom
            yield lst


# funkcja sortowania przez wstawianie
def insertion_sort(lst):
    for i in range(1, len(lst)):
        selected = lst[i]
        y = i - 1
        while y >= 0 and selected < lst[y]:
            lst[y + 1] = lst[y]
            y -= 1
        lst[y + 1] = selected
        yield lst


# definicja klasy
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

    # funkcja sprawdza, który guzik został wciśnięty, a nastepnie generuje wykres i ustawia odpowiedni tytuł
    def show_graph(self, button):
        amount = int(self.size_entry.get())
        lst = np.random.randint(0, 100, amount)
        # otwieranie i wprowadzanie danych do posorotwania do pliku
        result_file = open('wyniki.txt', 'a')
        result_file.write('Dane do posortowania:\n')
        for x in lst:
            result_file.write(str(x) + " ")

        result_file.write('\n')

        if button == "insert":
            anim_data = insertion_sort(lst)
            title = 'Sortowanie przez wstawianie'
        elif button == "bubble":
            anim_data = bubble_sort(lst)
            title = 'Sortowanie bombelkowe'
        elif button == "select":
            anim_data = selection_sort(lst)
            title = 'Sortowanie przez wybieranie'
        else:
            return
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.set_title(title)
        bar_rect = ax.bar(range(len(lst)), lst, align='edge')

        ax.set_xlim(0, len(lst))
        ax.set_ylim(0, int(1.07 * max(lst)))

        text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

        iteration = [0]

        # funkcja odpowiadająca za odświeżanie wykresu i zliczanie ilości operacji
        def update_fig(lst, rects, iteration):
            for rect, val in zip(rects, lst):
                rect.set_height(val)
            iteration[0] += 1
            text.set_text("Ilość operacji: {}".format(iteration[0]))

        anim = FuncAnimation(fig, func=update_fig, fargs=(bar_rect, iteration), frames=anim_data,
                             repeat=False,
                             interval=self.speed_default.get())
        plt.show()


        # wprowadzanie posortowanych danych do pliku, a nastepnie jego zamknięcie
        result_file.write('Dane posortowane:\n')
        for x in lst:
            result_file.write(str(x) + " ")

        result_file.write('\n')
        result_file.close()

# instacja klasy
GUI()
