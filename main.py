from random import randint


class Product:
    wood = 0
    metal = 0
    glass = 0
    cost = 0
    work = 0

    def __init__(self):
        self.wood = randint(5, 10)
        self.metal = randint(3, 8)
        self.glass = randint(1, 4)
        self.cost = randint(1, 100)
        self.work = False
        self.fitness = self.wood*0.5 + self.metal*0.2 + self.glass*0.15

    def set(self, wood, metal, glass, cost, work=False):
        self.wood = int(wood)
        self.metal = int(metal)
        self.glass = int(glass)
        self.cost = int(cost)
        self.work = bool(work)
        self.fitness = self.wood*0.5 + self.metal*0.2 + self.glass*0.1


if __name__ == "__main__":
    # random.seed("34567")
    read = input("Read? y/n")
    if read.lower() == "y":
        f = []
        with open("input.txt", "r") as file:
            products = file.readlines()
            for product in products:
                f.append(Product.set(Product, wood=product[product.find("W") + 1:product.find(";;")],
                                     metal=product[product.find("M") + 1:product.find("$$")],
                                     glass=product[product.find("G") + 1:product.find("%%")],
                                     cost=product[product.find("C") + 1::].rstrip()))
    else:
        f = [Product() for p in range(400)]
        with open("output.txt", "w", encoding="UTF-8") as file:
            for i, p in enumerate(f):
                file.write(
                    f"Product {i}\n Метал: {p.metal}, Стекло: {p.glass}, Дерево: {p.wood}, Стоимость: {p.cost} \n")
        with open("input.txt", "w", encoding="UTF-8") as file:
            for i, p in enumerate(f):
                file.write(f"{i}:M{p.metal}$$G{p.glass}%%W{p.wood};;C{p.cost}\n")
    print(f)
