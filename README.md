# EjercicioD16 – Sistema de Gestión de Empleados

Sistema para registrar y administrar los empleados de una empresa, hecho en Python.
Se puede usar de dos formas que comparten la misma lógica y los mismos datos:

- **Consola** (`main.py`): menú en la terminal.
- **Web** (`web.py`): interfaz en el navegador, hecha solo con la librería estándar de Python (no hay que instalar nada).

## Requisitos

- Python 3.9 o superior.
- No necesita librerías externas ni `pip install`.

## Cómo correr el servidor web

1. Abre una terminal y entra a la carpeta del proyecto:

   ```bash
   cd ED-16
   ```

2. Inicia el servidor:

   ```bash
   python3 web.py
   ```

   Verás este mensaje:

   ```
   Sistema de gestion de empleados en http://localhost:8000  (Ctrl+C para detener)
   ```

3. Abre el navegador en **http://localhost:8000**.

4. Para detener el servidor, presiona `Ctrl + C` en la terminal.

Si el puerto 8000 está ocupado, puedes indicar otro:

```bash
python3 web.py 8080
```

> El servidor solo escucha en `127.0.0.1`, así que únicamente se puede abrir desde tu propia computadora.

### Qué se ve en la web

| Página | Dirección | Qué hace |
|---|---|---|
| Lista de empleados | `/` | Tabla con todos los empleados, buscador por ID y filtro por departamento/rol |
| Agregar empleado | `/nuevo` | Formulario para registrar un empleado nuevo |
| Ficha del empleado | `/empleado?id=1` | Datos generales y desglose del salario (descuentos, bonos, comisión y salario neto) |
| Editar empleado | `/editar?id=1` | Formulario con los datos actuales para modificarlos |
| Eliminar empleado | `/eliminar?id=1` | Pide confirmación antes de borrar |

Los formularios validan los datos: si falta un campo o un número no es válido, se marca en rojo con un mensaje.
El diseño se adapta a pantallas pequeñas y cambia a modo oscuro si el sistema lo tiene activado.

## Cómo correr la versión de consola

```bash
cd ED-16
python3 main.py
```

Menú disponible:

```
1. Agregar empleado
2. Buscar empleado por ID
3. Editar empleado por ID
4. Eliminar empleado por ID
5. Mostrar empleado por departamento
6. Mostrar informacion detallada de un empleado
7. Salir
```

## Estructura del código

```
ED-16/
├── employee.py       # Clase Empleado con sus atributos
├── funciones.py      # Lógica: agregar, buscar, editar, eliminar, guardar/cargar JSON y cálculos de salario
├── interfaz.py       # Menú y pedido de datos por consola (con validaciones)
├── main.py           # Punto de entrada de la versión de consola
├── web.py            # Servidor web: rutas, validación de formularios y respuestas
├── plantillas.py     # Funciones que arman el HTML de cada página
├── static/
│   └── estilos.css   # Estilos de la interfaz web
└── empleados.json    # Datos guardados de los empleados
```

### Cómo se conectan las partes

- **`employee.py`** define la clase `Empleado` (nombre, edad, salario, año de ingreso, email, rol, horas por día, vacaciones, bonos y comisión).
- **`funciones.py`** es el núcleo: mantiene la lista de empleados en memoria, asigna los ID automáticamente y guarda cada cambio en `empleados.json`. Al iniciar, carga los empleados que ya existen en ese archivo.
- **`main.py` + `interfaz.py`** forman la versión de consola: `interfaz.py` muestra el menú y pide los datos, y `main.py` llama a las funciones de `funciones.py`.
- **`web.py` + `plantillas.py`** forman la versión web: `web.py` recibe las peticiones del navegador (`GET` para ver páginas y `POST` para guardar cambios) y usa las mismas funciones de `funciones.py`; `plantillas.py` genera el HTML.

### Cálculo del salario neto

```
salario neto = salario - descuentos (10%) + bonos + comisión
```

- **Descuentos:** 10% del salario (ISSS, AFP, etc.).
- **Comisión:** solo si el empleado recibe comisión; es un porcentaje del salario.

Ejemplo: salario $900, bonos $3 y comisión del 10% → 900 − 90 + 3 + 90 = **$903.00**

### Seguridad

- Todo el texto que escribe el usuario se escapa antes de mostrarse en la página, para evitar que se inyecte HTML o JavaScript.
- Después de guardar un formulario, el servidor redirige a otra página, así al recargar no se envía el formulario dos veces.
- Un candado (`threading.Lock`) evita que dos peticiones modifiquen la lista al mismo tiempo.

## Nota

La consola y la web usan el mismo archivo `empleados.json`, pero cada una lo lee solo al iniciar.
Es mejor no usar las dos a la vez: si lo haces, reinicia la otra para ver los cambios y no sobrescribirlos.
