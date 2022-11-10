"""To jest szablon do stworzenia rozwiazania"""

import time, numpy as np
from typing import List
import sortowania, wykresy, uklad
import gauss, gaussjordan, cholesky, banachiewicz
import iteracjaprosta, iteracjaseidela

class Zadanie:
    def __init__(self, n = 300, M = 6, N = 26):
        """Konstruktor okreslajacy parametry eksperymentu"""
        self.n = n                          # maksymalny rozmiar macierzy
        self.M = M                          # liczba pomiarow
        self.N = N                          # liczba rozmiarow
        self.rozmiary = []                  # lista rozmiarow ukladow
        self.czasy: List[List] = [[], []]   # lista czasow rozwiazywania
        
    def mierz_czas(self, metoda, k):
        czas = 0.0
        ukl = uklad.Uklad(k)
        for _ in range(self.M):
            if (metoda == 1):
                ukl.losuj_uklad_symetryczny_dodatnio_okreslony()
                m1 = banachiewicz.Banachiewicz(ukl)
                stoper = time.time()
                m1.rozklad()
                m1.rozwiaz_trojkatny_dolny()
                m1.rozwiaz_trojkatny_gorny()
                czas = time.time() - stoper
            elif (metoda == 2):
                ukl.losuj_uklad()
                m2 = gauss.Gauss(ukl)
                stoper = time.time()
                m2.eliminacja()
                m2.rozwiaz_trojkatny()
                czas = time.time() - stoper
        return czas/self.M
    
    def badaj_zlozonosc(self, metoda, opis):
        # okreslamy krok zmiany rozmiaru ukladu
        krok = self.n / self.N
        self.rozmiary = []
        self.czasy[metoda-1] = []
        for i in range(self.N):
            self.rozmiary.append(int((i+1)*krok))   
            self.czasy[metoda-1].append(
                self.mierz_czas(metoda, self.rozmiary[i])
            )
            print(self.rozmiary[i], self.czasy[metoda-1][i])
        wykres = wykresy.Wykresy(self.n)
        wykres.badaj_zlozonosc(
            rozmiary = self.rozmiary,
            czasy = self.czasy[metoda-1],
            nazwa = opis
        )
    
    def porownaj_metody(self, nazwa_metody1, nazwa_metody2):
        krok = self.n / self.N
        for i in range(self.N):
            k = int((i+1)*krok)
            self.rozmiary.append(k)
            t1 = self.mierz_czas(1, k)
            t2 = self.mierz_czas(2, k)
            self.czasy[0].append(t1)
            self.czasy[1].append(t2)
            print(f"{k} \t {t1:10.8f} \t {t2:10.8f}")
        wykres = wykresy.Wykresy(self.n)
        wykres.porownaj_algorytmy(
            self.rozmiary,
            self.czasy,
            nazwa_metody1,
            nazwa_metody2
        )