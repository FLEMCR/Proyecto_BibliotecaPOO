
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
            print("5. Regresar")

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
                print("Regresando al menu principal")
            else:
                print("Opcion incorrecta")

        elif opcion == 2:
            print("\n===== MENU ADMINISTRADOR =====")
            print("1. Registrar libro")
            print("2. Ver libros")
            print("3. Eliminar libro")
            print("4. Regresar")

            opcion2 = int(input("Seleccione una opcion: "))

            if opcion2 == 1:
                print("Registrando libro...")
            elif opcion2 == 2:
                print("Mostrando libros...")
            elif opcion2 == 3:
                print("Eliminando libro...")
            elif opcion2 == 4:
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
