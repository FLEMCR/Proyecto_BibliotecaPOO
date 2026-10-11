from datetime import date

from dateutil.relativedelta import relativedelta

partes = str(date.today()).split("-")
print(partes)


if int(partes[1]) < 12:
    modificado_mes = str(int(partes[1]) + 1)
else:
    modificado_mes = str(1)


unir = "-".join([partes[0], modificado_mes, partes[2]])
# El join solo permite unir listas
print([partes[0], modificado_mes, partes[2]])
print(unir)

# PENSABA USAR ESTO DE ARRIBA AL CALCULAR VENCIMIENTO DE LAS MEMBRESIAS PERO LUEGO PENSE Q PODRIAMOS TENER EL PROBLEMA DE LOS MESES CON FINAL IRREGULAR (28, 29, 30, 31), ENTONCES ENCONTRE UNA SOLUCION USANDO RELATIVEDELA.


# Lo siguiente son formas de usar date
print(date(2026, 10, 11))
print(date.fromisoformat("2026-10-11"))
print(date.today())

# Entre formatos date se puede comparar
print(date.fromisoformat("2026-10-11") > date(2026, 10, 11))
print(date.fromisoformat("2026-10-11") < date(2026, 10, 11))
print(date.fromisoformat("2026-10-11") == date(2026, 10, 11))


# En timedelta solo se puede usar hasta dias pero con relativedelta se puede usar meses y años. Pero para sacar su diferencia en vez de usar operadores se hace de la siguiente forma.
a = date.fromisoformat("2027-01-05")
b = date.fromisoformat("2026-10-11")

r = relativedelta(a, b)  # para sacar la diferencia se construye con las DOS fechas
print(r)  # relativedelta(months=+2, days=+25)
print(r.years, r.months, r.days)  # 0 2 25
