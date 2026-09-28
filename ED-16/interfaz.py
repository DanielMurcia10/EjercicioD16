def mostrar_menu(): #funcion que contiene el menu del programa 

    print("\t ====================================")
    print("\t  SISTEMA DE GESTION DE EMPLEADOS  ")
    print("\t ====================================")

    print("1. Agregar empleado \n")
    print("2. Buscar empleado por ID \n")
    print("3. Editar empleado por ID \n")
    print("4. Eliminar empleado por ID \n" )
    print("5. Mostrar empleado por departamento \n")
    print("6. Mostrar informacion detallada de un empleado \n")
    print("7. Salir... ")

def _pedir_texto(mensaje): #funcion que valida el texto ingresado por el usuario 
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este dato no puede estar vacio. Intentalo de nuevo.")

def _pedir_entero(mensaje): #funcion que valida el numero ingresado por el usuario
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print("Debes ingresar un numero entero valido.")

def _pedir_decimal(mensaje): #funcion que valida el numero decimal ingresado por el usuario
    while True:
        valor = input(mensaje).strip()
        try:
            return float(valor)
        except ValueError:
            print("Debes ingresar un numero valido (usa punto para decimales).")

def _pedir_si_no(mensaje): # funcion que valida la respuesta del usuario
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("s", "si"):
            return True
        if valor in ("n", "no"):
            return False
        print("Responde 's' para si o 'n' para no.")

def pedir_datos_nuevo_empleado():
    print("\n-- Ingresa los datos del nuevo empleado --\n")
    
    nombre = _pedir_texto("Nombre completo: ")
    edad = _pedir_entero("Edad: ")
    salario = _pedir_decimal("Salario: ")
    AnioIngreso = _pedir_entero("Anio de ingreso a la empresa: ")
    TiempoTrabajando = _pedir_entero("Tiempo trabajando en la empresa (anios): ")
    email = _pedir_texto("Email: ")
    rol = _pedir_texto("Rol / departamento: ")
    horas_por_dia = _pedir_decimal("Horas trabajadas al dia: ")
    vacaciones_anuales = _pedir_entero("Dias de vacaciones anuales: ")
    bonos = _pedir_decimal("Monto de bonos: ")
    recibe_comision = _pedir_si_no("Recibe comision? (s/n): ")
    
    porcentaje_comision = 0.0
    if recibe_comision:
        porcentaje_comision = _pedir_decimal("Porcentaje de comision (ej. 5 = 5%): ")

    return {
        "nombre": nombre,
        "edad": edad,
        "salario": salario,
        "AnioIngreso": AnioIngreso,
        "TiempoTrabajando": TiempoTrabajando,
        "email": email,
        "rol": rol,
        "horas_por_dia": horas_por_dia,
        "vacaciones_anuales": vacaciones_anuales,
        "bonos": bonos,
        "recibe_comision": recibe_comision, 
        "porcentaje_comision": porcentaje_comision
    }


def pedir_cambio_empleado(empleado):
    print("\n-- Editando empleado --")
    print(empleado)
    print("\nQue campo deseas editar?")
    print("1. Nombre")
    print("2. Edad")
    print("3. Salario")
    print("4. Rol / departamento")
    print("5. Email")
    print("6. Horas por dia")
    print("7. Vacaciones anuales")
    print("8. Bonos")
    print("9. Comision")
    print("0. Terminar edicion")
    
    opcion = input("Opcion: ").strip()

    # devuelve (campo, valor) para que funciones.editar_empleado_por_id aplique el cambio,
    # None para terminar la edicion o "invalido" si la opcion no existe
    if opcion == "1":
        return "nombre", _pedir_texto("Nuevo nombre: ")
    elif opcion == "2":
        return "edad", _pedir_entero("Nueva edad: ")
    elif opcion == "3":
        return "salario", _pedir_decimal("Nuevo salario: ")
    elif opcion == "4":
        return "rol", _pedir_texto("Nuevo rol / departamento: ")
    elif opcion == "5":
        return "email", _pedir_texto("Nuevo email: ")
    elif opcion == "6":
        return "horas_por_dia", _pedir_decimal("Nuevas horas por dia: ")
    elif opcion == "7":
        return "vacaciones_anuales", _pedir_entero("Nuevos dias de vacaciones anuales: ")
    elif opcion == "8":
        return "bonos", _pedir_decimal("Nuevo monto de bonos: ")
    elif opcion == "9":
        recibe_comision = _pedir_si_no("Recibe comision? (s/n): ")
        porcentaje_comision = 0.0
        if recibe_comision:
            porcentaje_comision = _pedir_decimal("Nuevo porcentaje de comision: ")
        return "comision", (recibe_comision, porcentaje_comision)
    elif opcion == "0":
        print("\nEdicion finalizada.\n")
        return None
    else:
        print("Opcion invalida, intentalo de nuevo.")
        return "invalido"


def pedir_id_a_eliminar():
    return _pedir_entero("\nIngrese el ID del empleado a eliminar: ")

def confirmar_eliminacion(empleado):
    print("\n-- Empleado a eliminar --")
    print(empleado)
    return _pedir_si_no("\nSeguro desea eliminarlo? (s/n): ")

def buscar_empleado_por_departamento():
    return _pedir_texto("\nIngrese el departamento / rol a consultar: ")

def mostrar_informacion_detallada_por_id():
    return _pedir_entero("\nIngresa el ID del empleado a consultar: ")

def mostrar_info_empleado(empleado, salario_neto, monto_comision):
    print("\n============ INFORMACION DETALLADA ============")
    print(f"ID: {empleado.id}")
    print(f"Nombre: {empleado.nombre}")
    print(f"Rol / departamento: {empleado.rol}")
    print(f"Edad: {empleado.edad}")
    print(f"Anio de ingreso: {empleado.AnioIngreso}")
    print(f"Tiempo trabajando: {empleado.TiempoTrabajando} anios")
    print(f"Horas trabajadas al dia: {empleado.horas_por_dia}")
    print(f"Vacaciones anuales: {empleado.vacaciones_anuales} dias")
    print(f"Salario base: ${empleado.salario:.2f}")
    print(f"Bonos: ${empleado.bonos:.2f}")
    print(f"Recibe comision: {'Si' if empleado.recibe_comision else 'No'}")
    if empleado.recibe_comision:
        print(f"Monto de comision: ${monto_comision:.2f}")
    print(f"Salario neto (despues de descuentos): ${salario_neto:.2f}")
    print("=================================================\n")

def buscar_empleado_por_id():
    return _pedir_entero("\nIngresa el ID del empleado a buscar: ")

def mostrar_empleado_encontrado(empleado):
    print("\n-- Empleado encontrado --")
    print(empleado)