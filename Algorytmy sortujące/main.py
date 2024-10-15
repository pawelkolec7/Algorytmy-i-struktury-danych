import random
import time
import threading
import sys
import copy

def GeneratorKlawiaurta(n):
    tablica = []
    for i in range(n):
        a = int(input())
        tablica.append(a)
    return tablica

def GeneratorLosowy(n, max_wartosc):
    tablica = [random.randint(1, max_wartosc) for i in range(n)]
    return tablica

def GeneratorRosnacy(n, max_wartosc):
    tablica = [random.randint(1, max_wartosc) for i in range(n)]
    tablica.sort()
    return tablica

def GeneratorMalejacy(n, max_wartosc):
    tablica = [random.randint(1, max_wartosc) for i in range(n)]
    tablica.sort(reverse=True)
    return tablica

def GeneratorA(n, max_wartosc):
    polowa = (n + 1) // 2
    pierwsza_polowa = [2*i+1 for i in range(polowa)]
    druga_polowa = [max_wartosc-2*i for i in range(n-polowa)]
    return pierwsza_polowa + druga_polowa

def GeneratorV(n, max_wartosc):
    polowa = (n + 1) // 2
    pierwsza_polowa = [2*i+1 for i in range(polowa)]
    druga_polowa = [max_wartosc-2*i for i in range(n-polowa)]
    return druga_polowa + pierwsza_polowa

def InsertionSort(tablica):
    operacje = 0
    for i in range(1, len(tablica)):
        klucz = tablica[i]
        j = i - 1
        while j >= 0 and klucz > tablica[j]:
            operacje += 1
            tablica[j + 1] = tablica[j]
            operacje += 1
            j -= 1
            operacje += 1
        tablica[j+1] = klucz
        operacje += 1
    return tablica, operacje

def SelectionSort(tablica):
    i = 0
    operacje = 0
    while i < len(tablica) - 1:
        maxIndex = i
        j = i + 1
        while j < len(tablica):
            if tablica[maxIndex] < tablica[j]:
                maxIndex = j
            j += 1
            operacje += 1
        if tablica[i] != tablica[maxIndex]:
            tablica[i], tablica[maxIndex] = tablica[maxIndex], tablica[i]
            operacje += 1
        i += 1
    return tablica, operacje

def BubbleSort(tablica):
    operacje = 0
    i = 0
    while i < len(tablica) - 1:
        j = 0
        while j < len(tablica) - 1:
            if tablica[j] < tablica[j + 1]:
                tablica[j], tablica[j + 1] = tablica[j + 1], tablica[j]
                operacje += 1
            operacje += 1
            j += 1
        i += 1
    return tablica, operacje

def ShellSort(tablica):
    N = len(tablica)
    operacje = 0
    k = 1
    while (3**k - 1) // 2 <= N // 3:
        odstep = (3**k - 1) // 2
        for i in range(odstep, N):
            j = i
            while j >= odstep and tablica[j - odstep] < tablica[j]:
                tablica[j], tablica[j - odstep] = tablica[j - odstep], tablica[j]
                j -= odstep
                operacje += 1
            operacje += 1
        k += 1
    return tablica, operacje

def ShellSortReczny(tablica):
    N = len(tablica)
    operacje = 0
    k = 1
    while (3**k - 1) // 2 <= N // 3:
        odstep = (3**k - 1) // 2
        for i in range(odstep, N):
            print("Wartość przyrostu w", i, "iteracji:", odstep)
            j = i
            while j >= odstep and tablica[j - odstep] < tablica[j]:
                tablica[j], tablica[j - odstep] = tablica[j - odstep], tablica[j]
                j -= odstep
                operacje += 1
            operacje += 1
        k += 1
    return tablica, operacje

def PodzielTablice(tablica, poczatek, koniec, operacje):
    piwot = tablica[koniec]
    czy_wiekszy = poczatek
    czy_mniejszy = koniec - 1
    while True:
        while czy_wiekszy <= czy_mniejszy and tablica[czy_wiekszy] >= piwot:
            operacje += 1
            czy_wiekszy += 1
        while czy_wiekszy <= czy_mniejszy and tablica[czy_mniejszy] <= piwot:
            operacje += 1
            czy_mniejszy -= 1
        if czy_wiekszy <= czy_mniejszy:
            tablica[czy_mniejszy], tablica[czy_wiekszy] = tablica[czy_wiekszy], tablica[czy_mniejszy]
            operacje += 1
        else:
            break
    tablica[koniec], tablica[czy_wiekszy] = tablica[czy_wiekszy], tablica[koniec]
    operacje += 1
    return czy_wiekszy, operacje

def QuickSort(tablica, poczatek, koniec):
    operacje = 0
    if poczatek < koniec:
        piwot, operacje = PodzielTablice(tablica, poczatek, koniec, operacje)
        operacje += 1
        tablica, operacje1 = QuickSort(tablica, poczatek, piwot - 1)
        operacje += operacje1
        tablica, operacje2 = QuickSort(tablica, piwot + 1, koniec)
        operacje += operacje2
    return tablica, operacje

def PodzielTabliceReczny(tablica, poczatek, koniec, operacje):
    piwot = tablica[koniec]
    print("Wartość piwota: ", piwot)
    czy_wiekszy = poczatek
    czy_mniejszy = koniec - 1
    while True:
        while czy_wiekszy <= czy_mniejszy and tablica[czy_wiekszy] >= piwot:
            operacje += 1
            czy_wiekszy += 1
        while czy_wiekszy <= czy_mniejszy and tablica[czy_mniejszy] <= piwot:
            operacje += 1
            czy_mniejszy -= 1
        if czy_wiekszy <= czy_mniejszy:
            tablica[czy_mniejszy], tablica[czy_wiekszy] = tablica[czy_wiekszy], tablica[czy_mniejszy]
            operacje += 1
        else:
            break
    tablica[koniec], tablica[czy_wiekszy] = tablica[czy_wiekszy], tablica[koniec]
    operacje += 1
    return czy_wiekszy, operacje

def QuickSortReczny(tablica, poczatek, koniec):
    operacje = 0
    if poczatek < koniec:
        piwot, operacje = PodzielTabliceReczny(tablica, poczatek, koniec, operacje)
        operacje += 1
        tablica, operacje1 = QuickSortReczny(tablica, poczatek, piwot - 1)
        operacje += operacje1
        tablica, operacje2 = QuickSortReczny(tablica, piwot + 1, koniec)
        operacje += operacje2
    return tablica, operacje

def MergeSort(tablica):
    porownania = 0
    if len(tablica) > 1:
        srodek = len(tablica) // 2
        L = tablica[:srodek]
        R = tablica[srodek:]
        MergeSort(L)
        MergeSort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            porownania += 1
            if L[i] > R [j]:
                tablica[k] = L[i]
                i += 1
            else:
                tablica[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            tablica[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            tablica[k] = R[j]
            j += 1
            k += 1
    return tablica, porownania

def MergeSortReczny(tablica):
    porownania = 0
    scalenia = 0
    if len(tablica) > 1:
        srodek = len(tablica) // 2
        L = tablica[:srodek]
        R = tablica[srodek:]
        L, porownania_L, scalenia_L = MergeSortReczny(L)
        R, porownania_R, scalenia_R = MergeSortReczny(R)
        porownania += porownania_L + porownania_R
        scalenia += scalenia_L + scalenia_R
        i = j = k = 0
        while i < len(L) and j < len(R):
            porownania += 1
            if L[i] > R[j]:
                tablica[k] = L[i]
                i += 1
            else:
                tablica[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            tablica[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            tablica[k] = R[j]
            j += 1
            k += 1
        scalenia += 1
    return tablica, porownania, scalenia

def heapify(tablica, n, i, operacje):
    najmniejszy = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and tablica[l] < tablica[najmniejszy]:
        operacje += 1
        najmniejszy = l
    if r < n and tablica[r] < tablica[najmniejszy]:
        operacje += 1
        najmniejszy = r
    if najmniejszy != i:
        tablica[i], tablica[najmniejszy] = tablica[najmniejszy], tablica[i]
        operacje += 1
        operacje = heapify(tablica, n, najmniejszy, operacje)
    return operacje

def HeapSort(tablica):
    n = len(tablica)
    operacje = 0
    for i in range(n // 2 - 1, -1, -1):
        operacje = heapify(tablica, n, i, operacje)
    for i in range(n - 1, 0, -1):
        tablica[0], tablica[i] = tablica[i], tablica[0]
        operacje += 1
        operacje = heapify(tablica, i, 0, operacje)
    return tablica, operacje


def test_sort_InsertionSort(arr):
    start_time = time.time()
    tablica, licznik = InsertionSort(arr)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def test_sort_SelectionSort(arr):
    start_time = time.time()
    tablica, licznik = SelectionSort(arr)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def test_sort_BubbleSort(arr):
    start_time = time.time()
    tablica, licznik = BubbleSort(arr)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def test_sort_ShellSort(arr):
    start_time = time.time()
    tablica, licznik = ShellSort(arr)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def test_sort_MergeSort(arr):
    start_time = time.time()
    tablica, licznik = MergeSort(arr)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def test_sort_HeapSort(arr):
    start_time = time.time()
    tablica, licznik = HeapSort(arr)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def test_sort_QuickSort(arr):
    start_time = time.time()
    tablica, licznik = QuickSort(arr, 0, len(arr) - 1)
    end_time = time.time()
    czas = end_time - start_time
    return czas, licznik

def main():
    print("Witaj w programie!", "Wybierz tryb:")
    print("Tryb wpisywania ręcznego. Wybierz 1.")
    print("Tryb automatycznych testów. Wybierz 2.")
    choice = input("Wybierz tryb (wpisz 1 lub 2): ")


    if choice == "1":
        print("Wybrałeś tryb 1. Wykonuję kod dla trybu 1...")
        n = int(input("Ile libcz chcesz wpisać?"))
        tablica_do_sortu = []
        for i in range(n):
            a = int(input("Wpisz liczbę: "))
            tablica_do_sortu.append(a)

        print("Ciąg wejściowy:", copy.deepcopy(tablica_do_sortu))
        print("InsertionSort")
        posortowana_tablica, operacje = InsertionSort(copy.deepcopy(tablica_do_sortu))
        czas, licznik  = test_sort_InsertionSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ciąg wyjściowy po InsertionSort:",posortowana_tablica)

        print("BubbleSort")
        posortowana_tablica, operacje = BubbleSort(copy.deepcopy(tablica_do_sortu))
        czas, licznik  = test_sort_BubbleSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ciąg wyjściowy po BubbleSort:",posortowana_tablica)

        print("SelectionSort")
        posortowana_tablica, operacje = SelectionSort(copy.deepcopy(tablica_do_sortu))
        czas, licznik  = test_sort_SelectionSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ciąg wyjściowy po SelectionSort:",posortowana_tablica)

        print("ShellSort")
        posortowana_tablica, operacje = ShellSortReczny(copy.deepcopy(tablica_do_sortu))
        czas, licznik = test_sort_ShellSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ciąg wyjściowy po ShellSort:",posortowana_tablica)

        print("MergeSort")
        posortowana_tablica, operacje, sacelnia = MergeSortReczny(copy.deepcopy(tablica_do_sortu))
        czas, licznik = test_sort_MergeSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ilość scaleń podzbiorów: ",sacelnia)
        print("Ciąg wyjściowy po MergeSort:",posortowana_tablica)

        print("HeapSort")
        posortowana_tablica, operacje = HeapSort(copy.deepcopy(tablica_do_sortu))
        czas, licznik = test_sort_HeapSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ciąg wyjściowy po HeapSort:",posortowana_tablica)

        print("QuickSort")
        posortowana_tablica, operacje = QuickSortReczny(copy.deepcopy(tablica_do_sortu), 0, len(copy.deepcopy(tablica_do_sortu)) - 1)
        czas, licznik = test_sort_QuickSort(copy.deepcopy(tablica_do_sortu))
        print("Czas sortowania: ", czas, "s")
        print("Ilość operacji: ",operacje)
        print("Ciąg wyjściowy po QuickSort:",posortowana_tablica)
    elif choice == "2":
        print("Wybrałeś tryb 2. Wykonuję kod dla trybu 2...")
        ns = [100, 500, 1000, 2500, 5000, 10000, 20000, 30000, 40000, 50000]
        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_BubbleSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_BubbleSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_BubbleSort(malejaco)
                A_czas, A_licznik = test_sort_BubbleSort(A)
                V_czas, V_licznik = test_sort_BubbleSort(V)

                with open("Wyniki BubbleSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")
                with open("Wyniki BubbleSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")
        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_SelectionSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_SelectionSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_SelectionSort(malejaco)
                A_czas, A_licznik = test_sort_SelectionSort(A)
                V_czas, V_licznik = test_sort_SelectionSort(V)

                with open("Wyniki SelectionSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")
                with open("Wyniki SelectionSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")
        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_InsertionSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_InsertionSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_InsertionSort(malejaco)
                A_czas, A_licznik = test_sort_InsertionSort(A)
                V_czas, V_licznik = test_sort_InsertionSort(V)

                with open("Wyniki InsertionSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")
                with open("Wyniki InsertionSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")

        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_ShellSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_ShellSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_ShellSort(malejaco)
                A_czas, A_licznik = test_sort_ShellSort(A)
                V_czas, V_licznik = test_sort_ShellSort(V)

                with open("Wyniki ShellSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")

                with open("Wyniki ShellSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")

        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_MergeSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_MergeSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_MergeSort(malejaco)
                A_czas, A_licznik = test_sort_MergeSort(A)
                V_czas, V_licznik = test_sort_MergeSort(V)

                with open("Wyniki MergeSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")

                with open("Wyniki MergeSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")

        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_HeapSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_HeapSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_HeapSort(malejaco)
                A_czas, A_licznik = test_sort_HeapSort(A)
                V_czas, V_licznik = test_sort_HeapSort(V)

                with open("Wyniki HeapSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")

                with open("Wyniki HeapSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")

        for n in ns:
            for i in range(10):
                losowo = GeneratorLosowy(n, 10 * n)
                rosnaco = GeneratorRosnacy(n, 10 * n)
                malejaco = GeneratorMalejacy(n, 10 * n)
                A = GeneratorA(n, 10 * n)
                V = GeneratorV(n, 10 * n)

                losowo_czas, losowo_licznik = test_sort_QuickSort(losowo)
                rosnaco_czas, rosnaco_licznik = test_sort_QuickSort(rosnaco)
                malejaco_czas, malejaco_licznik = test_sort_QuickSort(malejaco)
                A_czas, A_licznik = test_sort_QuickSort(A)
                V_czas, V_licznik = test_sort_QuickSort(V)

                with open("Wyniki QuickSort - czas.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_czas:.6f}\n")
                    file.write(f"M {rosnaco_czas:.6f}\n")
                    file.write(f"R {malejaco_czas:.6f}\n")
                    file.write(f"A {A_czas:.6f}\n")
                    file.write(f"V {V_czas:.6f}\n")
                    file.write("\n")

                with open("Wyniki QuickSort - liczba.txt", "a") as file:
                    file.write(f"n = {n}\n")
                    file.write(f"L {losowo_licznik:.6f}\n")
                    file.write(f"M {rosnaco_licznik:.6f}\n")
                    file.write(f"R {malejaco_licznik:.6f}\n")
                    file.write(f"A {A_licznik:.6f}\n")
                    file.write(f"V {V_licznik:.6f}\n")
                    file.write("\n")

threading.stack_size(67108864)
sys.setrecursionlimit(2**20)
thread = threading.Thread(target=main)
thread.start()




