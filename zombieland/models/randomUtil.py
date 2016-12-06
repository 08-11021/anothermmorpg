from random import uniform

#recibe como argumento un diccionario de datos {'elemento':probabilidad}
def arbitrary(elements):
    total = 0
    ranges = {}
    #se actualizan los rangos y se invierten las tuplas (clave, valor)
    for index in elements:
        ranges[total + elements[index]] = index
        total = total + elements[index]

    chosenValue = uniform(0.0,total)
    for index in ranges:
        if chosenValue<=index:
            chosenElement = ranges[index]
    return chosenElement