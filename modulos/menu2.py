
misiones = []

while True:
    print("\n===== SISTEMA DE BIBLIOTECA =====")
    print("1. Ingresar como estudiante")
    print("2. Ingresar como administrador")
    print("3. Salir")

    try:
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            print("\n===== MENU ESTUDIANTE =====")
            print("1. Ver libros")
            print("2. Buscar libro")
            print("3. Prestar libro")
            print("4. Devolver libro")
            print("5. Ver misiones de lectura")
            print("6. Regresar")

            opcion2 = int(input("Seleccione una opcion: "))

            if opcion2 == 1:
                print("Mostrando libros...")
            elif opcion2 == 2:
                print("Buscando libro...")
            elif opcion2 == 3:
                print("Prestamo de libro...")
            elif opcion2 == 4:
                print("Devolucion de libro...")

            elif opcion2 == 5:
                print("\n===== MISIONES DE LECTURA =====")

                if len(misiones) == 0:
                    print("Todavia no hay misiones disponibles")
                else:
                    for i in range(len(misiones)):
                        print("\nMision", i + 1)
                        print("Nombre:", misiones[i]["nombre"])
                        print("Pregunta:", misiones[i]["pregunta"])

                        for j in range(3):
                            print(str(j + 1) + ".",
                                  misiones[i]["opciones"][j])

                    if len(misiones) > 0:
                        numero = int(input(
                            "\nSeleccione una mision para responder: "
                        ))

                        if numero >= 1 and numero <= len(misiones):
                            respuesta = input(
                                "Ingrese su respuesta (1, 2 o 3): "
                            )

                            if respuesta == misiones[numero - 1]["correcta"]:
                                print("¡Respuesta correcta!")
                                print("Mision completada")
                            else:
                                print("Respuesta incorrecta")

                        else:
                            print("Mision incorrecta")

            elif opcion2 == 6:
                print("Regresando al menu principal")
            else:
                print("Opcion incorrecta")

        elif opcion == 2:
            print("\n===== MENU ADMINISTRADOR =====")
            print("1. Registrar libro")
            print("2. Ver libros")
            print("3. Eliminar libro")
            print("4. Crear mision de lectura")
            print("5. Ver misiones")
            print("6. Regresar")

            opcion2 = int(input("Seleccione una opcion: "))

            if opcion2 == 1:
                print("Registrando libro...")
            elif opcion2 == 2:
                print("Mostrando libros...")
            elif opcion2 == 3:
                print("Eliminando libro...")

            elif opcion2 == 4:
                print("\n===== CREAR MISION =====")

                nombre = input("Nombre de la mision: ")
                pregunta = input("Escriba la pregunta: ")

                opciones = []

                for i in range(3):
                    respuesta = input(
                        "Escriba la opcion " + str(i + 1) + ": "
                    )
                    opciones.append(respuesta)

                correcta = input(
                    "Numero de la respuesta correcta (1, 2 o 3): "
                )

                if correcta == "1" or correcta == "2" or correcta == "3":
                    mision = {
                        "nombre": nombre,
                        "pregunta": pregunta,
                        "opciones": opciones,
                        "correcta": correcta
                    }

                    misiones.append(mision)

                    print("Mision creada correctamente")
                else:
                    print("Respuesta correcta no valida")

            elif opcion2 == 5:
                print("\n===== LISTA DE MISIONES =====")

                if len(misiones) == 0:
                    print("No hay misiones registradas")
                else:
                    for i in range(len(misiones)):
                        print("\nMision", i + 1)
                        print("Nombre:", misiones[i]["nombre"])
                        print("Pregunta:", misiones[i]["pregunta"])

                        for j in range(3):
                            print(str(j + 1) + ".",
                                  misiones[i]["opciones"][j])

            elif opcion2 == 6:
                print("Regresando al menu principal")
            else:
                print("Opcion incorrecta")

        elif opcion == 3:
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion incorrecta")

    except ValueError:
        print("Debe ingresar un numero")
