import interfaz  # se llama al archivo interfaz.py para mandar a llamar el menu creado
import funciones  # se llama al archivo funciones.py para poder hacer uso de todas las funciones

def Ejecutar_sistema():

    funciones.cargar_empleado()

    while True:

        interfaz.mostrar_menu()#se llama la funcion que esta en interfaz.py para mostrar el menu

        opcion = input("\n Seleccione la opcion que desea realizar: ")

        if opcion == "1":
            datos = interfaz.pedir_datos_nuevo_empleado()
            empleado = funciones.agregar_empleado(datos)
            print(f"\nEmpleado agregado correctamente con ID {empleado.id}.\n")

        elif opcion == "2":
            print("\t == Buscar empleado por ID ==\n")
            id_buscado = interfaz.buscar_empleado_por_id()
            empleado = funciones.obtener_empleado_por_id(id_buscado)
            if empleado is None:
                print(f"\nNo se encontro ningun empleado con ID {id_buscado}.\n")
            else:
                interfaz.mostrar_empleado_encontrado(empleado)

        elif opcion == "3":
            print("\t == Editar empleado por ID ==\n")
            id_buscado = interfaz._pedir_entero("\nIngrese el ID del empleado a editar: ")
            empleado = funciones.obtener_empleado_por_id(id_buscado)
            if empleado is None:
                print(f"\nNo se encontro ningun empleado con ID: {id_buscado}.\n")
            else:
                while True:
                    cambio = interfaz.pedir_cambio_empleado(empleado)
                    if cambio is None:
                        break
                    if cambio == "invalido":
                        continue
                    campo, valor = cambio
                    funciones.editar_empleado_por_id(empleado, campo, valor)
                    print("\nCambio guardado correctamente.\n")
                
        elif opcion == "4":
            print("\t == Eliminar empleado por ID==\n")
            id_buscado = interfaz.pedir_id_a_eliminar()
            empleado = funciones.obtener_empleado_por_id(id_buscado)
            if empleado is None:
                print(f"\nNo se encontro ningun empleado con ID {id_buscado}.\n")
            else:
                confirmar = interfaz.confirmar_eliminacion(empleado)
                if confirmar:
                    funciones.eliminar_empleado_por_id(empleado)
                    print("\nEmpleado eliminado correctamente.\n")
                else:
                    print("\nEliminacion cancelada.\n")

        elif opcion == "5":
            print("\t == Mostrar empleado por departamento == \n")
            if not funciones.lista_empleados:
                print("\nNo hay empleados registrados todavia.\n")
            else:
                rol_buscado = interfaz.buscar_empleado_por_departamento()
                encontrado = funciones.mostrar_empleados_por_departamento(rol_buscado)
                if not encontrado:
                    print(f"\nNo hay empleados registrados en: '{rol_buscado}'.\n")
                else:
                    print(f"\n-- Empleados en '{rol_buscado}' --")
                    for empleado in encontrado:
                        print(empleado)

        elif opcion == "6":
            print("\t == Mostrar informacion detallada de un empleado == \n")
            id_buscado = interfaz.mostrar_informacion_detallada_por_id()
            empleado = funciones.obtener_empleado_por_id(id_buscado)

            if empleado is None:
                print(f"\nNo se encontro ningun empleado con ID {id_buscado}.\n")
            else:
                salario_neto = funciones.calcular_salario_neto(empleado)
                monto_comision = funciones.calcular_comision(empleado)
                interfaz.mostrar_info_empleado(empleado, salario_neto, monto_comision)

        elif opcion == "7":
            print("Hasta luego...")
            break

        else:
            print("Opcion invalida, intentalo nuevamente")


Ejecutar_sistema()