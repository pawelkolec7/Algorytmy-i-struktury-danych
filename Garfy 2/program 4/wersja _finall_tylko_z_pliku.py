import networkx as nx
import matplotlib.pyplot as plt

#Czytanie garfu z pliku
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

def adjacency_matrix_from_edges(edges, n):
    adjacency_matrix = [[0] * n for _ in range(n)]
    for edge in edges:
        # W tym przypadku dla garfu nieskierowanego, więc jak istnieje krawędź, nie ważne w którą stronę dajemy 1.
        adjacency_matrix[edge[0]][edge[1]] = 1
        adjacency_matrix[edge[1]][edge[0]] = 1
    return adjacency_matrix

def lista_nastepnikow_from_krawedzie(krawedzie, n):
    #Generuje listę następników na podstawie listy krawędzi grafu
    lista_nastepnikow = [[] for _ in range(n)]
    for edge in krawedzie:
    #Pod indexami tablicy kryją się numer wierzchołła z którego wychodzi krawędź, a wartości to wierzchołki do któych wchodzi łuk.
        lista_nastepnikow[edge[0]].append(edge[1])
    return lista_nastepnikow

########################################################################################################################

#Z listy następników
def HamiltonianCycleL(graph):
    n = len(graph) #liczba wierzchołków grafu
    O = [False] * n  #tablica, w której zaznaczamy odwiedzone wierzchołki
    Path = []  #lista zawierająca konstruowany cykl Hamiltona
    start = 0  #startowy wierzchołek
    visited = 0  #licznik odwiedzonych wierzchołków
    k = 0  #indeks następnego elementu w ścieżce

    def HamiltonianL(v):
        nonlocal visited, k #zmienne zadnieżdżone w fukcji głównej

        O[v] = True #wierzchołek odwiedzony
        visited += 1

        Path.append(v)

        if visited == n and start in graph[v]:
            return True #czy odwiedzone wszystkie oraz czy isteje połacznenie z początkiem

        for i in graph[v]:
            if not O[i]: #jeśli nie sprawdzamy wszystkie inne sąsiedznie wierzchołki, które nie zostały odwiedzone
                if HamiltonianL(i):
                    return True

        O[v] = False #jeśli się okarze, że z żadnego sąsiada nie można jechać dalej cofamy się robiąc go jako nieoznaczony
        visited -= 1 #oraz zmiejszamy liczbę odwiedoznych wierzchołków
        Path.pop() #oraz usuawamy wierzchołęk ze scieżki, bo się cofneliśmy o jeden
        return False

    def HcycleL():
        nonlocal O, Path, visited, k

        for i in range(n):
            O[i] = False #na początku wszytskie nieodwiedzoe

        Path.append(start) #dodajemy startowy wierzchołek
        visited = 1

        for i in graph[start]: #przechodzimy przez wszystkie sąsiednie wierzchołki i wywołujemy funkcję szukania po sąsiadach
            if HamiltonianL(i): #jak ona nie wyjdzie, cofa się i wtedy zaczynam szukac po innych sąsiadach, jak nie wyjdzie to powtrót itd
                return Path  #jak ta wyżej da true to daj scieżkę jako cykl Hamiltona

        Path.pop() #jak nic nie wróci true to brak cyklu
        return "Brak cyklu Hamiltona"

    return HcycleL()

#Z macierzy sąsiedztwa
def HamiltonianCycleM(graph):
    n = len(graph) #liczba wierzchołków w grafie
    path = [0] * n  # tablica zawierająca konstruowany cykl Hamiltona
    visited = [False] * n  # tablica, w której zaznaczamy odwiedzone wierzchołki, na początku wszystkie na false

    def HamiltonianM(v, pos): #funkcja sprawdza czy można zależć cykl hamiltona zaczynajć do v n apozycji pos w scieżce
        visited[v] = True #odwiedzony
        path[pos] = v #dodanie wierzchołka do scieżki

        if pos == n - 1:  #sprawdzenie, czy znaleziono cykl Hamiltona, to zanczy dojechano do końca
            if graph[v][path[0]] == 1:  #sprawdzenie, czy istnieje krawędź między ostatnim wierzchołkiem a początkowym
                return True
            else:
                visited[v] = False #jesli nie oznaczmy go jako nieodwiedzony
                return False

        for i in range(n): #przechodzimy przez wszystkie wierzchołki i sprawdzamy czy isteje krawędź między v oraz i
            if graph[v][i] == 1 and not visited[i]:  #oraz czy i nie był już odwiedzony przypadkiem
                if HamiltonianM(i, pos + 1): #jesli wszytko jest spełnione szukamy dalej, no i zapismey potem ten wierzchołek na pos + 1
                    return True #znaleziono cykl Hamiltona

        visited[v] = False #jesli nie uda się nic stworzyć, musimy oznczyć go jako false i szukamy zaczynając od innego
        return False #jeśli się nie uda zwracamy false

    if HamiltonianM(0, 0): #wywołujemy funkcje od unkty (0,0)
        return path #jeśli istenje zwróci scieżkę
    else:
        return "Brak cyklu Hamiltona"

########################################################################################################################

def znajdz_cykl_eulera(lista_nastepnikow):
    def dfs(v, cykl): #przeszukiwanie w głąb DFS od wiezrchołka v
        while lista_nastepnikow[v]: #dopóki isteją sasiedzi
            u = lista_nastepnikow[v].pop(0) #usuwamy pierwszego sąsida i przechodimy rekurencyjnie dfs
            dfs(u, cykl)
        cykl.append(v) #dodajemy v do cyklu do sprawdzenia

    cykl = []
    start = None
    for v in range(len(lista_nastepnikow)): #przechodzimy przez wszystkie wierzchołki
        if len(lista_nastepnikow[v]) > 0: #jeśli każdy ma minimum jedego sąsiada, czyli brak pustych, przypisujemy do start v i przerywamy
            start = v
            break

    if start is None: #jeśli nie znaleziono stratu, czyli wszytskie wierzchołki mają pustą listę następników, nie istnieje cykl Eulera.
        return None

    dfs(start, cykl) #rozpoczynamy przeszukiwanie w głąb od wierzchołka startowego.

    if sum(len(neighbors) for neighbors in lista_nastepnikow) > 0:
        return None #czy istnieją jeszcze krawędzie na listach następników wierzchołków. Jeśli tak, oznacza to, że graf nie jest spójny i nie istnieje cykl Eulera

    return cykl[::-1][:-1] #zmiana

def znajdz_cykl_eulera1(macierz_sasiedztwa):
    n = len(macierz_sasiedztwa) #ilość wierzchołków
    cykl = []

    def dfs(v):
        nonlocal cykl

        for u in range(n): #przechodzimy przez wszystkie wierzchołki grafu
            if macierz_sasiedztwa[v][u] > 0: #jesli istnieje krawędź oraz przez nią przeszliśmy zminejsz wartość w macierzy o 1, by zazanczyć, że już tędy szliśmy
                macierz_sasiedztwa[v][u] -= 1
                macierz_sasiedztwa[u][v] -= 1
                dfs(u) #rekurencyjne wywołanie

        cykl.append(v) #dodajemy v do cyklu, ponieważ przeszliśmy przez wszystkie jego sąsiednie krawędzie.

    dfs(0) #rozpoczynamy od wierzchołka 0

    if sum(sum(row) for row in macierz_sasiedztwa) > 0: #sprawdzamy, czy nie zostały jakieś nieodwiedzone.
        return None #Jeśli suma jest większa niż 0, oznacza to, że graf nie jest spójny i nie istnieje cykl Eulera.
    else:
        return cykl[::-1]


########################################################################################################################

def wyswietl_cykl(cykl):
    G = nx.DiGraph()
    n = len(cykl)
    for i in range(n - 1):
        G.add_edge(cykl[i], cykl[i + 1]) #dodawanie krawędzi między obecnym, a kolejnym wierzchołkiem
    G.add_edge(cykl[-1], cykl[0]) #dodanie ostatniej krawędzi
    pos = nx.circular_layout(G) #wierzchołki po okręgu
    nx.draw_networkx_nodes(G, pos, node_color='lightblue') #rysowanie wierzchołków
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10) #rysowanie łuków jako strzałek
    nx.draw_networkx_labels(G, pos, font_color='black') #rysowanie etykiet wierzchołków
    plt.axis('off') #bez osi
    plt.show()

########################################################################################################################

def main():
    program_on = True
    while program_on:
        print("***************************************")
        print("Wczytaj graf z pliku:")
        print("1) Graf skierowany z cyklem Hamiltona")
        print("2) Graf nieskierowany z cyklem Hamiltona")
        print("3) Graf skierowany z cyklem Eulera")
        print("4) Graf nieskierowany z cyklem Eulera")
        print("0) wyjdź z programu")
        choice = int(input("Wybierz opcję: "))
        match (choice):
            case 1:
                edges, n = read_graph_from_file('HamiltonS.txt')
                lista_nastepnikow = lista_nastepnikow_from_krawedzie(edges, n)
                print("Lista następników: ",lista_nastepnikow)
                print("Czy chcesz go wyświetlić?")
                print("1) TAK")
                print("2) Nie")
                print()
                pokaz = int(input("Wybierz opcję: "))
                if pokaz == 1:
                    G = nx.DiGraph() #pusty graf
                    for i, neighbors in enumerate(lista_nastepnikow):
                        G.add_edges_from((i, v) for v in neighbors) #dodanie wierzchołków
                    pos = nx.circular_layout(G) #po okręgu
                    node_colors = 'lightblue'
                    edge_colors = 'gray'
                    nx.draw_networkx_nodes(G, pos, node_color=node_colors) #rusuj wiezrchołki
                    nx.draw_networkx_labels(G, pos) #rysuj etykiety
                    nx.draw_networkx_edges(G, pos, arrowstyle='->', edge_color=edge_colors) #rysuj krawędzie
                    plt.axis('off')
                    plt.show()
                print("Sprawdź czy ma cykl:")
                cykl_hamiltona = HamiltonianCycleL(lista_nastepnikow)
                if cykl_hamiltona:
                    print("Tak, ma cykl Hamiltona :",cykl_hamiltona )
                    print("Czy chcesz go wyświetlić?")
                    print("1) TAK")
                    print("2) Nie")
                    print()
                    pokaz = int(input("Wybierz opcję: "))
                    if pokaz == 1:
                        wyswietl_cykl(cykl_hamiltona)
                else:
                    print("Nie znaleziono cyklu")
            case 2:
                edges, n = read_graph_from_file('HamiltonN.txt')
                macierz = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
]
                print("Macierz sąsiedztwa: ")
                print(macierz)
                print("Czy chcesz go wyświetlić?")
                print("1) TAK")
                print("2) Nie")
                print()
                pokaz = int(input("Wybierz opcję: "))
                if pokaz == 1:
                    G = nx.Graph() #pusty graf
                    n = len(macierz)
                    G.add_nodes_from(range(n))
                    for i in range(n):
                        for j in range(i + 1, n):
                            if macierz[i][j] == 1:
                                G.add_edge(i, j) #dodanie wierzchołków
                    nx.draw_circular(G, with_labels=True, node_color='lightblue', edge_color='gray') #rysowanie po okręgu z cechami
                    plt.show()
                print("Sprawdź czy graf skierowany ma cykl Hamiltona w reprezentacji macierz sąsiedztwa")
                cykl_hamiltona = HamiltonianCycleM(macierz)
                if cykl_hamiltona:
                    print("Tak, ma cykl Hamiltona :", cykl_hamiltona)
                    print("Czy chcesz go wyświetlić?")
                    print("1) TAK")
                    print("2) Nie")
                    print()
                    pokaz = int(input("Wybierz opcję: "))
                    if pokaz == 1:
                        wyswietl_cykl(cykl_hamiltona)
                else:
                    print("Nie znaleziono cyklu")
            case 3:
                lista_nastepnikow = [[1,3],[0,4],[4,3],[2,0],[1,2]]
                print("Lista następników: ", lista_nastepnikow)
                print("Czy chcesz go wyświetlić?")
                print("1) TAK")
                print("2) Nie")
                print()
                pokaz = int(input("Wybierz opcję: "))
                if pokaz == 1:
                    G = nx.DiGraph()
                    for i, neighbors in enumerate(lista_nastepnikow):
                        G.add_edges_from((i, v) for v in neighbors)
                    pos = nx.circular_layout(G)
                    node_colors = 'lightblue'
                    edge_colors = 'gray'
                    nx.draw_networkx_nodes(G, pos, node_color=node_colors)
                    nx.draw_networkx_labels(G, pos)
                    nx.draw_networkx_edges(G, pos, arrowstyle='->', edge_color=edge_colors)
                    plt.axis('off')
                    plt.show()
                print("Sprawdź czy ma cykl:")
                cykl_eulera = znajdz_cykl_eulera(lista_nastepnikow)
                if cykl_eulera:
                    print("Tak, ma cykl Euelra :", cykl_eulera)
                    print("Czy chcesz go wyświetlić?")
                    print("1) TAK")
                    print("2) Nie")
                    print()
                    pokaz = int(input("Wybierz opcję: "))
                    if pokaz == 1:
                        wyswietl_cykl(cykl_eulera)
                else:
                    print("Nie znaleziono cyklu")
            case 4:
                edges, n = read_graph_from_file('EulerN.txt')
                macierz = adjacency_matrix_from_edges(edges, n)
                print("Macierz sąsiedztwa: ")
                for wiersz in macierz:
                    print(wiersz)
                print("Czy chcesz go wyświetlić?")
                print("1) TAK")
                print("2) Nie")
                print()
                pokaz = int(input("Wybierz opcję: "))
                if pokaz == 1:
                    # Tworzenie grafu
                    G = nx.Graph()
                    n = len(macierz)
                    G.add_nodes_from(range(n))
                    for i in range(n):
                        for j in range(i + 1, n):
                            if macierz[i][j] == 1:
                                G.add_edge(i, j)
                    nx.draw_circular(G, with_labels=True, node_color='lightblue', edge_color='gray')
                    plt.show()
                print("Sprawdź czy graf skierowany ma cykl Eulera w reprezentacji macierz sąsiedztwa")
                cykl_eulera = znajdz_cykl_eulera1(macierz)
                if cykl_eulera:
                    print("Tak, ma cykl Euelra :", cykl_eulera)
                    print("Czy chcesz go wyświetlić?")
                    print("1) TAK")
                    print("2) Nie")
                    print()
                    pokaz = int(input("Wybierz opcję: "))
                    if pokaz == 1:
                        wyswietl_cykl(cykl_eulera)
                else:
                    print("Nie znaleziono cyklu")
            case 0:
                program_on = False

if __name__ == '__main__':
    main()