import random
global n

def choice():
    print("W jaki sposób chcesz wygenerować graf?")
    print("1) Wygeneruj automatycznie spójny skierowany graf acykliczny o n wierzchołkach")
    print("2) Wczytaj graf z pliku")
    wybor = int(input())
    match(wybor):
        case 1:
            print("Podaj ilość wierzchołków n: ")
            n = int(input())
            return tworzenie_grafu(n)
        case 2:
            edges, n1 = read_graph_from_file('graf_z_cyklem.txt')
            adjacency_matrix(edges, n1)
            return edges, n1

def read_graph_from_file(file_name):
    with open(file_name, 'r') as file:
        # Wczytanie liczby wierzchołków i krawędzi
        n, m = map(int, file.readline().split())
        # Inicjalizacja listy krawędzi
        edges = []
        # Wczytanie krawędzi z pliku
        for line in file:
            u, v = map(int, line.split())
            edges.append((u, v))
        # Zwrócenie listy krawędzi oraz liczby wierzchołków
        return edges, n

def adjacency_matrix(edges, n):
    global matrix
    # Inicjalizacja macierzy zerami
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    # Dodanie krawędzi do macierzy
    for u, v in edges:
        adj_matrix[u][v] = 1
    matrix = adj_matrix

def tworzenie_grafu(n):
    global matrix
    macierz_sasiedztwa = [[0] * n for _ in range(n)]
# Liczba krawędzi pomożnona przez współczynnik nasycenia 0.5
    liczba_krawedzi = int((n * (n - 1) / 2) * 0.5)
#Tworzenie macierzy górnotrójkątnej dla grafu skierowanego
    for i in range(n):
        for j in range(i + 1, n):
            macierz_sasiedztwa[i][j] = 1
# Losowo usuń z macierzy gónotrójkątnej krawędzie, żeby spełnić warunek nasycenia
    krawedzie_to_remove = int((n * (n - 1) / 2 - liczba_krawedzi))
    for _ in range(krawedzie_to_remove):
        while True:
#Robimy n-1 oraz n-2, aby pary wylosowanych indeksów były różne, graf nie będzie składał się z izolowanych wierzchołków
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            if macierz_sasiedztwa[i][j] == 1:
                macierz_sasiedztwa[i][j] = 0
                break
    matrix = macierz_sasiedztwa
#Przekształcenie na listę krawędzi w celu sprawdzenia poprawności wygenerowanego grafu
    krawedzie = []
    for i in range(n):
        for j in range(n):
            if macierz_sasiedztwa[i][j] == 1:
                krawedzie.append((i, j))
#Srawdzenie, czy nie ma wierzchołków pustych
    for i in range(n):
        tester = 0
        for j in range(len(krawedzie)):
#Srawdzenie, czy którykolwiek z wierzchołków krawędzi jest jest połączony z innym wierzchołkiem w grafie, przez daną krawędz
#Jeśli nie, to mamy wierzchołek pusty, a więc trzeba stworzyć graf jeszcze raz, aby był acykliczny, bez wierzchołków pustych
            if i in krawedzie[j]:
                tester = 1
                break
        if tester == 0:
            krawedzie, n = tworzenie_grafu(n)
    return krawedzie, n

def macierz_sasiedztwa_from_krawedzie(krawedzie, n):
#Generuje macierz sąsiedztwa na podstawie listy krawędzi grafu skierowanego
    macierz_sasiedztwa = [[0] * n for _ in range(n)]
    for edge in krawedzie:
#Łuk traktowany jest jako krawędż zaczynająca sie 0 oraz kończąca 1, a następnie dodawana do macierzy sąsiedztwa
        macierz_sasiedztwa[edge[0]][edge[1]] = 1
    return macierz_sasiedztwa

def lista_nastepnikow_from_krawedzie(krawedzie, n):
#Generuje listę następników na podstawie listy krawędzi grafu
    lista_nastepnikow = [[] for _ in range(n)]
    for edge in krawedzie:
#Pod indexem krawędzi wchodzącej, kryje się wartość edge[1], czyli index krawędzi wychodzącej
        lista_nastepnikow[edge[0]].append(edge[1])
    return lista_nastepnikow

########################################################################################################################

#0 - nieodwiedzony, 1 - odwiedzony, 2 - do wypisania
def Tarjana_macierz(v,visited, uporzadkowana_lista):
    visited[v] = 1
    for i in range(len(matrix[v])):
#Testowanie czy nie ma cyklu, jest wtedy gdy mimo iż został już odwiedzony, nie ma go jeszcze na liście uporządkowanej
        if matrix[v][i] == 1 and i not in uporzadkowana_lista and visited[i]==1:
            print("Istnieje cykl")
            return "Istnieje cykl"
        elif matrix[v][i] == 1 and visited[i] == 0:
#Jeśli istnieje połącznie, czyli 1, ale jeszcze nie został odwiedzony, rekurencyjnie wywołuje tę funkcję
            Tarjana_macierz(i, visited, uporzadkowana_lista)
#Jak tak dojedziemy do końca, dodajemy ten wierzchołek do uporządkowanej listy i oznaczamy jako 2, czyli dodany do listy
    uporzadkowana_lista.append(v)
    visited[v] = 2

def Tarjana_dla_nastepnikow(v, lista_nastepnikow, odwiedzone, uporzadkowana_lista_2):
    odwiedzone[v] = 1
    for sasiad in lista_nastepnikow[v]:
#Cykl jeśli sąsiad został już odwiedzony, ale nie został jeszcze dodany do uporzadkowanej listy
        if odwiedzone[sasiad] == 1 and sasiad not in uporzadkowana_lista_2:
            print("Istnieje cykl")
            return "Istnieje cykl"
        elif odwiedzone[sasiad] == 0:
#Gdy sąsiad nie był jeszcze odwiedzony, wywołujmemy rekurencyjnie funkcję
            Tarjana_dla_nastepnikow(sasiad, lista_nastepnikow, odwiedzone, uporzadkowana_lista_2)
# Jak tak dojedziemy do końca, dodajemy ten wierzchołek do uporządkowanej listy i oznaczamy jako 2, czyli dodany do listy
    uporzadkowana_lista_2.append(v)
    odwiedzone[v] = 2

def Khan_macierz(arr):
#Oblicznie stopnia każdego wierzchołka
    stopien = [0] * len(arr)
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[j][i] != 0:
#Jeśli coś wchodzi to zwiększamy o 1
                stopien[i] += 1
#Najpierw wierzchołki o stopniu 0
    stos = []
    for i in range(len(stopien)):
        if stopien[i] == 0:
            stos.append(i)

    uporzadkowana_lista = []
    while stos:
#Pobieramy popem ze stosu i dodajemy do listy uporządkowanej (od razu dobra kolejność)
        node = stos.pop(0)
        uporzadkowana_lista.append(node)
#Zmniejsza stopień wierzchołków, do których prowadzą krawędzie z pobranego wierzchołka
        for i in range(len(arr)):
            if arr[node][i] != 0:
                stopien[i] -= 1
#Jeśli stopień któregoś z wierzchołków spadnie do 0, dodaje do kolejki
                if stopien[i] == 0:
                    stos.append(i)

    if len(uporzadkowana_lista) != len(arr):
        print("Istnieje cykl")
        return "Istnieje cykl"

    return uporzadkowana_lista

def Khan_nastepnikow(nastepny):
# Stopień każdego wierzchołka grafu, liczbę krawędzi wchodzących do wierzchołka
    stopien = [0] * len(nastepny)
    for i in range(len(nastepny)):
        for j in range(len(nastepny[i])):
            stopien[nastepny[i][j]] += 1
#Najpierw wierzchołki o stopniu 0
    stos = []
    for i in range(len(stopien)):
        if stopien[i] == 0:
            stos.append(i)
#Pobieramy popem ze stosu i dodajemy do listy uporządkowanej (od razu dobra kolejność)
    uporzadkowana_lista = []
    while stos:
        node = stos.pop(0)
        uporzadkowana_lista.append(node)
#Dopóki stos nie jest pusty, zdejmujemy ze stosu wierzchołek node, zmniejszamy stopien o 1, dodajemy na stos, jeśli stopień wynosi 0
        for i in range(len(nastepny[node])):
            stopien[nastepny[node][i]] -= 1
            if stopien[nastepny[node][i]] == 0:
                stos.append(nastepny[node][i])
#Jeśli stopień któregoś z wierzchołków spadnie do 0, dodaje do kolejki
    if len(uporzadkowana_lista) != len(nastepny):
        print("Istnieje cykl")
        return "Istnieje cykl"

    return uporzadkowana_lista

def menu():
    program_on = True

    graf, n = choice()
    print('Zbiór krawędzi, po wygenerowaniu: ', graf)

    ListaNastepnikow = lista_nastepnikow_from_krawedzie(graf, n)
    MacierzSasiedztwa = macierz_sasiedztwa_from_krawedzie(graf, n)

    program_on = True
    while program_on:
        print("1) Wyświetl macierz sąsiedztwa")
        print("2) Wyświetl listę następników")

        print("3) Sortowanie topologiczne Tarjana dla macierzy sąsiedztwa")
        print("4) Sortowanie topologiczne Tarjana dla listy następników")

        print("5) Sortowanie topologiczne Khana dla macierzy sąsiedztwa")
        print("6) Sortowanie topologiczne Khana dla listy następników")

        print("0) wyjdź z programu")
        user_choice = int(input())
        print("-------------------")
        match user_choice:
            case 1:
                print("Macierz sąsiedztwa:")
                for wiersz in MacierzSasiedztwa:
                    print(wiersz)
            case 2:
                print("Lista następników:")
                for i, sasiady in enumerate(ListaNastepnikow):
                    print(f"Wierzchołek {i}: {sasiady}")
                print(ListaNastepnikow)
            case 3:
                visited = [0] * n
                uporzadkowana_lista = []
                k = 0
                while k < n:
                    if visited[k] == 0:
                        Tarjana_macierz(k, visited, uporzadkowana_lista)
                    k += 1
                wynik = uporzadkowana_lista[::-1]
                print("Sortowanie topologiczne Tarjana dla macierzy sąsiedztwa", wynik)
            case 4:
                visited2 = [0] * n
                uporzadkowana_lista2 = []
                for i in range(n):
                    if visited2[i] == 0:
                        Tarjana_dla_nastepnikow(i, ListaNastepnikow, visited2, uporzadkowana_lista2)
                wynik = uporzadkowana_lista2[::-1]
                print("Sortowanie topologiczne Tarjana dla listy następników", wynik)
            case 5:
                print("Sortowanie topologiczne Khana dla macierzy sąsiedztwa", Khan_macierz(matrix))
            case 6:
                print("Sortowanie topologiczne Khana dla listy następników", Khan_nastepnikow(ListaNastepnikow))
            case 0:
                program_on = False

if __name__ == "__main__":
    menu()