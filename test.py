a = [[1232, 455], [75, 456]]
mi = 0
ma = a[0][0]
for i, k in enumerate(a):
    if k[0] > ma:
        mi = i
        ma = k[0]
print(mi, ma    )


# print(max(range(len(a)), key=a.__getitem__))
# print(max([k[0] for k in a], key=lambda i: i[]))
# print(max([k[1][0] for k in enumerate(a)], key=.__getitem__))
# print(max(enumerate(a), key=lambda x: x[1]))
# print(max([print(k) for k in enumerate(a)]))
# print(sum([k[1] for k in a]))