import random
import matplotlib.pyplot as plt
from cycler import cycler

# константы задачи
ONE_MAX_LENGTH = 13    # длина особи

# константы генетического алгоритма
POPULATION_SIZE = 400   # количество генов в популяции
P_CROSSOVER = 0.9       # вероятность скрещивания
P_MUTATION = 0.32        # вероятность мутации индивидуума
MAX_GENERATIONS = 50    # максимальное количество поколений

mu = ''
while "y" != mu != "n":
    mu = input("Использоавть мутации? Y/N").lower()

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
costs = []
sumcosts = []
#формирование набора генов
n = 400
m = 4  #колличество параметров
z = 0
x = 0
s=[]
while z < n:
    s.append([random.randint(0, 100), random.randint(5,10),random.randint(3,8),random.randint(1,4)])
    z +=1



#конструктор, приспособленость в начале 0
class FitnessMax():
    def __init__(self):
        self.values = [0]

#конструктор
class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()

#вычисляем приспособленость отдельной особи (вычисление фитнес функции)
def oneMaxFitness(individual):
    return sum(map(lambda x: int(x[0]), individual))
    # return sum(individual),
#создаем список отдельных индивидумов
def individualCreator():
    return Individual([s[random.randint(0, POPULATION_SIZE-1)] for i in range(ONE_MAX_LENGTH)])

# def individualCreator2():
#     return Individual([random.randint(0,100)  for i in range(ONE_MAX_LENGTH)])
#формирование популяции (список)
def populationCreator(n = 0):
    return list([individualCreator() for i in range(n)])
# def populationCreator2(n = 0):
#     return list([individualCreator2() for i in range(n)])

population = populationCreator(n=POPULATION_SIZE)
# population2 = populationCreator2(n=POPULATION_SIZE)
# счетчик числа поколений
generationCounter = 0
#вычисляем приспособленость каждой оотдельной особи
fitnessValues = list(map(oneMaxFitness, population))

for individual, fitnessValue in zip(population, fitnessValues):
    individual.fitness.values = fitnessValue

maxFitnessValues = [] #максимальная приспособленость в популяии
meanFitnessValues = [] #средняя приспособленость всех особей в популяции

# клонируем индивидумов
def clone(value):
    ind = Individual(value[:])
    ind.fitness.values[0] = value.fitness.values
    return ind

#отбор индивидумов  (отбираем 3 особей с различными индексами, и отбираем среди них особь с максимальной приспособленостью )
def selTournament(population, p_len):
    offspring = [] #список отобраных особей
    for n in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(0, p_len-1), random.randint(0, p_len-1), random.randint(0, p_len-1)

        offspring.append(max([population[i1], population[i2], population[i3]], key=lambda ind: ind.fitness.values))

    return offspring

#одноточечный кроссинговер
def cxOnePoint(child1, child2):
    s = random.randint(2, len(child1)-3)  #выбираем точку разреза
    child1[s:], child2[s:] = child2[s:], child1[s:] #заменяем части хромосом

#мутация перестановки
def mutFlipBit(mutant, indpb=0.01):
    for indx in range(len(mutant)):
        if random.random() < indpb:
            k = random.randint(0,10)
            n = 10 -k
            S1 = mutant[k]
            mutant[k] = mutant[n]
            mutant[n] = S1

#состоит из значений приспособленности осбоей популяции
fitnessValues = [individual.fitness.values for individual in population]

#цикл пока либо не найдем лучшее решение либопройдем 50 поколений
while max(fitnessValues) < 1300 and generationCounter < MAX_GENERATIONS:
    generationCounter += 1 #число поколений

    summ = 0
#штрафы
    for i in range(len(fitnessValues)):
        summ += s[i][1]
        if summ >200:
            fitnessValues[i] = fitnessValues[i] - 250
    offspring = selTournament(population, len(population)) #отбираем лучших особей
    offspring = list(map(clone, offspring)) #клонируем для избежания повторений

#скрещиваем чётную и нечетную особи
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            cxOnePoint(child1, child2) #получаем потомков

#мутация
    if mu == "y":
        for mutant in offspring:
           if random.random() < P_MUTATION: #вероятность мутации индивидума
               mutFlipBit(mutant, indpb=1.0/ONE_MAX_LENGTH) #вероятность мутации отдельных генов

    freshFitnessValues = list(map(oneMaxFitness, offspring))
    for individual, fitnessValue in zip(offspring, freshFitnessValues):
        individual.fitness.values = fitnessValue
#обновляем список
    population[:] = offspring
#обновляем список
    fitnessValues = [ind.fitness.values for ind in population]

    maxFitness = max(fitnessValues)
    # costInd = max(range(len(fitnessValues)), key=fitnessValues.__getitem__)
    # print(fitnessValues[cost])
    meanFitness = sum(fitnessValues) / len(population)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
#вывод на экран статистики по каждому поколению
    print(f"Поколение {generationCounter}: Макс приспособ. = {maxFitness}, Средняя приспособ.= {meanFitness}")

    best_index = fitnessValues.index(max(fitnessValues)) #индекс лучшего индивидума
    costs.append(population[best_index].copy())
    sumcosts.append(population[best_index].copy())
    print("Лучший индивидуум = ", *population[best_index], "\n") #хромосома лучшего индивидума

sumcosts = []
for i in range(len(costs)):
    # sumcosts.append(costs[i][1])
    sumcosts.append([sum(map(lambda x: int(x[1]), costs[i])), sum(map(lambda x: int(x[2]), costs[i])),sum(map(lambda x: int(x[3]), costs[i]))])
#строим график


fig1, ax1 = plt.subplots(figsize=(10, 5))
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax1.plot(maxFitnessValues, color='red', label="Лучший индивид популяции")
ax1.plot(meanFitnessValues, color='green', label="Среднее значение")
ax1.legend()
cy = cycler('color', ['brown', 'grey', 'blue'])
ax2.set_prop_cycle(cy)
ax2.plot(sumcosts, label=['дерево', 'металл', 'стекло'])
ax2.legend()
fig1.supxlabel('Поколение')
fig1.supylabel('Макс/средняя приспособленность')
fig1.suptitle('Зависимость максимальной и средней приспособленности от поколения')
plt.show()
