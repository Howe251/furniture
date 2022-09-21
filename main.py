from random import randint, random
from matplotlib import pyplot as plt
import copy

"""Для  изготовления  мебели  используется  три  вида  ресурсов:  
дерево, металл, стекло. Запасы сырья: дерево –200 ед.; 
металл –80 ед.; стекло –60 ед.
 Сгенерировать 400 предметов мебели со случайной стоимостью от 1 до 100 у.е. и 
 состоящими из следующих материалов: дерево в интервале [5;10] ед.,  
 металл –[3;8]  ед., стекло –[1;4]  ед.  
 Требуется  получить  наибольший доход от изготовления продукции."""

population = 30
loopSize = 50
mutationRate = 0.2
itemsSize = 400


class Limitations:
    limits = [200, 80, 60] # Ограничения: Дерево металл стекло
    minCosts = [5, 3, 1]  # Минимальная стоимость: дерево, металл, стекло
    maxCosts = [10, 8, 4]  # Максимальная стоимость: дерево, металл, стекло
    # SYMBOLS = [k for k in locals().keys() if not k.startswith('_')]


class Product(Limitations):
    # wood = 0
    # metal = 0
    # glass = 0
    prcosts = [0,0,0]
    cost = 0
    work = False

    def __init__(self):
        self.prcosts[0] = randint(self.minCosts[0], self.maxCosts[0])
        self.prcosts[1] = randint(self.minCosts[1], self.maxCosts[1])
        self.prcosts[2] = randint(self.minCosts[2], self.maxCosts[2])
        self.cost = randint(1, 100)
        # self.fitness = self.wood*0.5 + self.metal*0.2 + self.glass*0.15

    def set(self, wood, metal, glass, cost, work=False):
        self.prcosts[0] = int(wood)
        self.prcosts[1] = int(metal)
        self.prcosts[2] = int(glass)
        self.cost = int(cost)
        self.work = bool(work)
        # self.fitness = self.wood*0.5 + self.metal*0.2 + self.glass*0.15
        return self

    def __str__(self):
        return self.work


def weight(s, c):
    weight = int(s[0]/c[0])
    for i in range(len(s)):
        if int(s[i]/c[i]) <= weight:
            weight = int(s[i]/c[i])
    return weight


# individ = {
#     'fitnes': 0,
#     'use': []
#     }


class Individ(Limitations):
    fitness = 0
    use = []

    def setWork(self, weight, products):
        self.use.clear()
        self.fitness = 0
        for i in range(len(products)):
            k = randint(0, len(products))
            if k < weight:
                products[i].work = True
                self.use.append(products[i])
                self.fitness += products[i].cost
            else:
                self.use.append(products[i])
        return self

    def checkWorth(self): #individ, stocks):
        individCost = [0, 0, 0]
        fit = 0
        k = 0
        for i in self.use:
            if i.work:
                k += 1
        print(k)
        for k, person in enumerate(self.use):
            if person.work:
                for i in range(len(self.limits)):
                    individCost[i] += person.prcosts[i]
                    if individCost[i] > self.limits[i]:
                        self.fitness = -1
                        return False
                fit += person.cost
        return True


def mutation(product):
    if random() <= mutationRate:
        product.wood = randint(5, 10)
        # Остальные рандомные мутации...


def write(i, p):
    return f"Product №{i}\n Метал: {p.prcosts[0]}, Стекло: {p.prcosts[1]}, Дерево: {p.prcosts[2]}, Стоимость: {p.cost}"


if __name__ == "__main__":
    # random.seed("34567")
    read = input("Read? y/n")
    while "y" != read != "n":
        read = input("Read? y/n")
    if read.lower() == "y":
        f = []
        with open("input.txt", "r") as file:
            products = file.readlines()
            for product in products:
                f.append(Product.set(Product(), wood=product[product.find("W") + 1:product.find(";;")],
                                     metal=product[product.find("M") + 1:product.find("$$")],
                                     glass=product[product.find("G") + 1:product.find("%%")],
                                     cost=product[product.find("C") + 1::].rstrip()))
    else:
        f = [Product() for p in range(itemsSize)]
        if input("Save in file? y/n").lower() == "y":
            with open("output.txt", "w", encoding="UTF-8") as file:
                for i, p in enumerate(f):
                    file.write(write(i, p)+"\n")
            with open("input.txt", "w", encoding="UTF-8") as file:
                for i, p in enumerate(f):
                    file.write(f"{i}:M{p.metal}$$G{p.glass}%%W{p.wood};;C{p.cost}\n")
    # sor = sorted(f, key=lambda fitness: fitness.fitness)
    # Вывод отсортированной генерации в консоль
    for i, p in enumerate(f):
        print(write(i, p))
    # Рандомно выбираем индивидов которых будем использовать (Создание популяции)
    weightmin = weight(Limitations.limits, Limitations.minCosts)
    weightmax = weight(Limitations.limits, Limitations.maxCosts)
    pop = []
    while len(pop) < population:
        Ind = Individ().setWork(randint(weightmax, weightmin), copy.deepcopy(f))
        if Ind.checkWorth():
            pop.append(Ind)


    # while i < len(f):  #  сортировка по убыванию фитнесс функции
    #     # print(f"f {f[i].fitness} sor {sor[i].fitness}")
    #     print(f"m{sor[i].metal} w{sor[i].wood} g{sor[i].glass}  f{sor[i].fitness}")
    #     i += 1
    # for i in range(len(sor)):
    #     sor[i] = sor[i].fitness
    for i in range(loopSize):  # тут цикл отбора и мутаций
        pass
    plt.rc('axes', unicode_minus=False)
    fig, ax = plt.subplots(figsize=(5, 3))
    # plt.plot(sor, label="Fitness")
    plt.show()
    plt.close()


#  TODO Написать функцию отбора и скрещивания Функции построения графиков
