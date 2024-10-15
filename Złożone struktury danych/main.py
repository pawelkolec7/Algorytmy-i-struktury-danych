import math
import random
import time
import threading
import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.root = None
        self.parent = None
        self.height = 1

    def __str__(self):
        return str(self.value)

#In-order lewo korzen prawo
def in_order(node):
    if node is not None:
        in_order(node.left)
        print(node.value)
        in_order(node.right)


#In-order lewo korzen prawo
def in_order_test(tab, node):
    if node is not None:
        in_order_test(tab, node.left)
        tab.append(node.value)
        in_order_test(tab, node.right)

#Pre-order korzeń lewo prawo
def pre_order(node):
    if node is not None:
        print(node.value)
        pre_order(node.left)
        pre_order(node.right)

#Post-order klucz lewo prawo korzeń

def pre_order_z_klucza(node, key):
    if node is None:
        return
    elif node.value == key:
        print(node.value)
        pre_order(node.left)
        pre_order(node.right)
    elif node.value < key:
        pre_order_z_klucza(node.right, key)
    else:
        pre_order_z_klucza(node.left, key)

#Zwracam wysokość drzewa.
def height(node):
    if node is None:
        return 0
    else:
        return node.height

#Sprawdzam za pomocą in-order drzewo i wypisuje wartości węzłów.
def search(node):
    if node is None:
        print("Drzewo jest puste")
        return
    else:
        if node.left is not None:
            search(node.left)
        print(node.value)
        if node.right is not None:
            search(node.right)

#Minimalny element max lewo
def min_element(node):
    if node.left is not None:
        min_element(node.left)
    else:
        print(node.value)

#Maksymalny element max prawo
def max_element(node):
    if node.right is not None:
        max_element(node.right)
    else:
        print(node.value)

# Wstawia wartość do drzewa BST
def insert_bst(root, key):
    # Jak drzewo jest puste nowy element staje sie rootem
    if root is None:
        return Node(key)
    else:
        # Jeśli key jest równa wartości korzenia, to funkcja kończy działanie i zwraca korzeń bez wprowadzania zmian.
        if root.value == key:
            return root
        # Jeśli wartość key jest mniejsza niż wartość korzenia, to funkcja wstawia key do lewego poddrzewa korzenia.
        elif root.value < key:
            root.right = insert_bst(root.right, key)
        # Jak nie to w prawo.
        else:
            root.left = insert_bst(root.left, key)
        return root

# Oblicza balans drzewa oblicza różnicę wysokości między lewym a prawym poddrzewem
# Jeśli wartość jest większa niż 1 lub mniejsza niż -1, drzewo uważa się za niezrównoważone i wymaga przebalansowania.

def balance(node):
    if node is None:
        return 0
    else:
        return height(node.left) - height(node.right)



# Rotacja w prawo
# Nowym korzeniem poddrzewa staje się lewe dziecko, a poprzedni korzeń staje się prawym dzieckiem nowego korzenia.

def rotate_right(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    node.height = max(height(node.left), height(node.right)) + 1
    new_root.height = max(height(new_root.left), height(new_root.right)) + 1
    return new_root

# Rotacja w lewo
def rotate_left(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    node.height = max(height(node.left), height(node.right)) + 1
    new_root.height = max(height(new_root.left), height(new_root.right)) + 1
    return new_root

# Wstawia wartość do drzewa AVL
def insert_avl(node, key):
    if node is None:
        return Node(key)
    elif key < node.value:
        node.left = insert_avl(node.left, key)
    else:
        node.right = insert_avl(node.right, key)

    node.height = max(height(node.left), height(node.right)) + 1

    balance_factor = balance(node)
    # minejsze 1 rotacja w prawo
    if balance_factor > 1 and key < node.left.value:
        return rotate_right(node)
    # wieksze 1 rotacja w lewo
    if balance_factor < -1 and key > node.right.value:
        return rotate_left(node)
    # wiekszy 1 i wklejana wartość wieksza o lewy syn - rotacja lewo
    if balance_factor > 1 and key > node.left.value:
        node.left = rotate_left(node.left)
        return rotate_right(node)
    # minejszy 1 i wklejana wartość wieksza o lewy syn - rotacja lewo
    if balance_factor < -1 and key < node.right.value:
        node.right = rotate_right(node.right)
        return rotate_left(node)

    return node

#Tablica na BST
def sorted_array_to_bst(arr):
    if not arr:
        return None

    mid = len(arr) // 2
    root = Node(arr[mid])

    for i in range(mid):
        insert_bst(root, arr[i])

    for i in range(mid + 1, len(arr)):
        insert_bst(root, arr[i])

    return root

#Tablica na AVL
def sorted_array_to_avl(arr):
    if not arr:
        return None

    mid = len(arr) // 2
    root = Node(arr[mid])

    for i in range(mid):
        root = insert_avl(root, arr[i])

    for i in range(mid + 1, len(arr)):
        root = insert_avl(root, arr[i])

    return root

#Usuwanie węzła
def delete_node(root, key):
    if root is None:
        return root
    if key < root.value:
        root.left = delete_node(root.left, key)
    elif key > root.value:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp
        temp = znajdz_wezel(root)
        root.value = temp.value
        root.right = delete_node(root.right, temp.value)
    return root

#Usuwanie węzła z post order lewo prawo
def delete_post_order(root):
    if root is not None:
        delete_post_order(root.left)
        delete_post_order(root.right)
        print("Usuwany element:", root.value)
        root.value = None
    root = None
    return root

# Znajduje węzeł o najmniejszym kluczu większym niż node
def znajdz_wezel(node):
    current = node.right
    while current.left is not None:
        current = current.left
    return current

# Tworzy winorośl
def winorosl(root):
    count = 0
    tmp = root.right
    while tmp:
        if tmp.left:
            oldTmp = tmp
            tmp = tmp.left
            oldTmp.left = tmp.right
            tmp.right = oldTmp
            root.right = tmp
        else:
            count += 1
            root = tmp
            tmp = tmp.right
    return count

# Zmienia winorośl z powrotem na drzewo
def z_powrotem_drzewo(root, m):
    tmp = root.right
    for i in range(m):
        oldTmp = tmp
        tmp = tmp.right
        root.right = tmp
        oldTmp.right = tmp.left
        tmp.left = oldTmp
        root = tmp
        tmp = tmp.right

# Balansuje drzewo, najpierw przekształcając je w winorośl, a następnie kompresuje
def balancer(root):
    grand = Node(0)
    grand.right = root
    count = winorosl(grand)
    h = int(math.log2(count + 1))
    m = pow(2, h) - 1
    z_powrotem_drzewo(grand, count - m)
    for m in [m // 2 ** i for i in range(1, h + 1)]:
        z_powrotem_drzewo(grand, m)
    return grand.right

def GeneratorMalejacy(num_elements):
    sequence = []
    current_number = num_elements * 10
    for i in range(num_elements):
        sequence.append(current_number)
        current_number -= 10
    return sequence

def test_tworzenie_bst(tablica):
    start_time = time.time()
    root = sorted_array_to_bst(tablica)
    end_time = time.time()
    czas = end_time - start_time
    return czas


def test_tworzenie_avl(tablica):
    start_time = time.time()
    root = sorted_array_to_avl(tablica)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_min_bst(tablica):
    root = sorted_array_to_bst(tablica)
    start_time = time.time()
    min_element(root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_min_avl(tablica):
    root = sorted_array_to_avl(tablica)
    start_time = time.time()
    min_element(root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_in_order_bst_bez_printa(tablica):
    tab1 = []
    root = sorted_array_to_bst(tablica)
    start_time = time.time()
    in_order_test(tab1, root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_in_order_avl_bez_printa(tablica):
    tab2 = []
    root = sorted_array_to_avl(tablica)
    start_time = time.time()
    in_order_test(tab2, root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_in_order_avl_z_printem(tablica):
    root = sorted_array_to_avl(tablica)
    start_time = time.time()
    in_order(root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_in_order_bst_z_printem(tablica):
    root = sorted_array_to_bst(tablica)
    start_time = time.time()
    in_order(root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_balancer_bst(tablica):
    root = sorted_array_to_bst(tablica)
    start_time = time.time()
    root = balancer(root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def test_balancer_avl(tablica):
    root = sorted_array_to_avl(tablica)
    start_time = time.time()
    root = balancer(root)
    end_time = time.time()
    czas = end_time - start_time
    return czas

def main():
    global n
    n = int(input("Podaj liczbe elementow tablicy: "))
    tablica = []

    while True:
        print("Wybierz dane wejsciowe")
        print("-----------------------")
        print("0. Automat")
        print("1. Podane przez uzytkownika")
        print("2. Losowe")
        print("3. Rosnące")
        print("4. Zakoncz program")

        choice = int(input("Wybor: "))

        if choice == 0:
            print("Wybrałeś tryb 0. Wykonuję kod dla trybu 0...")
            ns = [1000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
            for n in ns:
                for i in range(2):
                    malejaco = GeneratorMalejacy(n)

                    tworzenie_bst = test_tworzenie_bst(malejaco)
                    tworzenie_avl = test_tworzenie_avl(malejaco)

                    with open("Wyniki BST - tworzenie drzewa.txt", "a") as file:
                        file.write(f"{n} {tworzenie_bst:.6f}\n")
                        file.write("\n")
                    with open("Wyniki AVL - tworzenie drzewa.txt", "a") as file:
                        file.write(f"{n} {tworzenie_avl:.6f}\n")
                        file.write("\n")
            for n in ns:
                for i in range(2):
                    malejaco = GeneratorMalejacy(n)

                    min_bst = test_min_bst(malejaco)
                    min_avl = test_min_avl(malejaco)

                    with open("Wyniki BST - minimum.txt", "a") as file:
                        file.write(f"{n} {min_bst:.6f}\n")
                        file.write("\n")
                    with open("Wyniki AVL - minimum.txt", "a") as file:
                        file.write(f"{n} {min_avl:.6f}\n")
                        file.write("\n")
            for n in ns:
                for i in range(2):
                    malejaco = GeneratorMalejacy(n)

                    in_order_bst1 = test_in_order_bst_bez_printa(malejaco)
                    in_order_avl1 = test_in_order_avl_bez_printa(malejaco)

                    with open("Wyniki BST - in-order bez printa.txt", "a") as file:
                        file.write(f"{n} {in_order_bst1:.6f}\n")
                        file.write("\n")
                    with open("Wyniki AVL - in-order bez printa.txt", "a") as file:
                        file.write(f"{n} {in_order_avl1:.6f}\n")
                        file.write("\n")
            for n in ns:
                for i in range(2):
                    malejaco = GeneratorMalejacy(n)

                    in_order_bst2 = test_in_order_bst_z_printem(malejaco)
                    in_order_avl2 = test_in_order_avl_z_printem(malejaco)

                    with open("Wyniki BST - in-order z printem.txt", "a") as file:
                        file.write(f"{n} {in_order_bst2:.6f}\n")
                        file.write("\n")
                    with open("Wyniki AVL - in-order z printem.txt", "a") as file:
                        file.write(f"{n} {in_order_avl2:.6f}\n")
                        file.write("\n")
            for n in ns:
                for i in range(2):
                    malejaco = GeneratorMalejacy(n)

                    balancer_bst = test_balancer_bst(malejaco)
                    balancer_avl = test_balancer_avl(malejaco)

                    with open("Wyniki BST - balancer.txt", "a") as file:
                        file.write(f"{n} {balancer_bst:.6f}\n")
                        file.write("\n")
                    with open("Wyniki AVL - balancer.txt", "a") as file:
                        file.write(f"{n} {balancer_avl:.6f}\n")
                        file.write("\n")


        elif choice == 1:
            # uzytkownik podaje
            for i in range(n):
                for i in range(0, n):
                    print("Podaj", i + 1, "element do ciągu:")
                    number_to_add = int(input())
                    tablica.append(number_to_add)

        elif choice == 2:
            for i in range(0, n):
                number_to_add = random.randint(0, 100)
                if number_to_add in tablica:
                    number_to_add = random.randint(0, 2000)
                tablica.append(number_to_add)
            tablica.sort()

        elif choice == 3:
            for i in range(0, n):
                tablica.append(i)

        elif choice == 4:
            break

        print("Jakie drzewo chcesz stworzyc?")
        print("1. AVL")
        print("2. BST")

        ch2 = int(input("Wybor: "))

        if ch2 == 1:
            root = sorted_array_to_bst(tablica)
            #search(root)
        elif ch2 == 2:
            root = sorted_array_to_avl(tablica)
            #search(root)
        else:
            print("Wpisano bledna wartosc. Program uruchomi sie od nowa")

        proc = 1

        while proc == 1:
            print("Jaka procedure chcesz wykonac na drzewie?:")
            print("-----------------------")
            print("1.Wyszukanie w drzewie elementu o najmniejszej wartosci")
            print("2.Wyszukanie w drzewie elementu o najwiekszej wartosci")
            print("3.Usuniecie elementu drzewa o wartosci klucza podanej przez uzytkownika")
            print("4.Wypisanie wszystkich elementow drzewa w porzadku in-order oraz pre-order")
            print("5.Usuniecie calego drzewa element po elemencie metoda post-order")
            print("6.Rownowazenie drzewa przez rotacje")
            print("7.Wyjdz")
            choice2 = int(input())

            if choice2 == 1:
                min_element(root)
                print("Najmniejsza wartosc")
                print()
                print("-------------------")
            elif choice2 == 2:
                max_element(root)
                print("Najwieksza wartosc")
                print()
                print("-------------------")
            elif choice2 == 3:
                print("Podaj element który chcesz usunąć z drzewa: ")
                el_to_delete = int(input())
                root = delete_node(root, el_to_delete)
                print("Drzewo po usunięciu")
                search(root)
                print("-------------------")
            elif choice2 == 4:
                print()
                print("Elementy wypisane in-order:")
                in_order(root)
                print()
                print("Elementy wypisane pre-order:")
                pre_order(root)
                print()
                print("-------------------")
            elif choice2 == 5:
                print("Usuwanie drzewa metodą post-order")
                root = delete_post_order(root)
                search(root)
                print("-------------------")
            elif choice2 == 6:
                print("Równoważenie drzewa")
                root = balancer(root)
                search(root)
                print("-------------------")
            elif choice2 == 7:
                proc = 0
            else:
                print("Wpisano bledna wartosc.")
                continue


threading.stack_size(67108864)
sys.setrecursionlimit(2**20)
thread = threading.Thread(target=main)
thread.start()