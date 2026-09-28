# interfaz web del sistema de gestion de empleados, hecha solo con la libreria estandar de Python
# se ejecuta con: python3 web.py   y se abre en el navegador: http://localhost:8000
import math
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import funciones  # la misma logica que usa la version de consola (main.py)
import plantillas  # funciones que arman el HTML de cada pagina

CARPETA = os.path.dirname(os.path.abspath(__file__))
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# campos del formulario: (nombre del atributo, etiqueta, tipo de dato)
CAMPOS_NUEVO = [
    ("nombre", "Nombre completo", "texto"),
    ("edad", "Edad", "entero"),
    ("salario", "Salario", "decimal"),
    ("AnioIngreso", "Anio de ingreso a la empresa", "entero"),
    ("TiempoTrabajando", "Tiempo trabajando en la empresa (anios)", "entero"),
    ("email", "Email", "texto"),
    ("rol", "Rol / departamento", "texto"),
    ("horas_por_dia", "Horas trabajadas al dia", "decimal"),
    ("vacaciones_anuales", "Dias de vacaciones anuales", "entero"),
    ("bonos", "Monto de bonos", "decimal"),
]

# al editar se usan los mismos campos que en el menu de consola (sin anio de ingreso ni tiempo trabajando)
CAMPOS_EDITAR = [c for c in CAMPOS_NUEVO if c[0] not in ("AnioIngreso", "TiempoTrabajando")]

# mensajes fijos que se muestran despues de una accion (nunca se muestra texto tal cual de la url)
MENSAJES = {
    "creado": "Empleado agregado correctamente.",
    "editado": "Cambios guardados correctamente.",
    "sin_cambios": "No se hizo ningun cambio.",
    "eliminado": "Empleado eliminado correctamente.",
}

candado = threading.Lock()  # evita que dos peticiones modifiquen la lista al mismo tiempo


def _valor(datos, clave): #devuelve el primer valor de un parametro o "" si no viene
    return datos.get(clave, [""])[0].strip()


# valida el formulario con las mismas reglas que las funciones _pedir_* de interfaz.py
def validar_formulario(form, campos):
    datos = {}
    errores = {}
    valores = {}  # lo que escribio el usuario, para volver a mostrarlo si hay errores

    for campo, etiqueta, tipo in campos:
        valor = _valor(form, campo)
        valores[campo] = valor

        if tipo == "texto":
            if valor:
                datos[campo] = valor
            else:
                errores[campo] = "Este dato no puede estar vacio."
        elif tipo == "entero":
            if valor.isdigit():
                datos[campo] = int(valor)
            else:
                errores[campo] = "Debes ingresar un numero entero valido."
        elif tipo == "decimal":
            numero = _a_decimal(valor)
            if numero is None:
                errores[campo] = "Debes ingresar un numero valido (usa punto para decimales)."
            else:
                datos[campo] = numero

    recibe_comision = _valor(form, "recibe_comision") == "si"
    valores["recibe_comision"] = recibe_comision
    valores["porcentaje_comision"] = _valor(form, "porcentaje_comision")
    datos["recibe_comision"] = recibe_comision
    datos["porcentaje_comision"] = 0.0
    if recibe_comision:
        numero = _a_decimal(valores["porcentaje_comision"])
        if numero is None:
            errores["porcentaje_comision"] = "Debes ingresar un porcentaje valido (ej. 5 = 5%)."
        else:
            datos["porcentaje_comision"] = numero

    return datos, errores, valores


def _a_decimal(valor):
    try:
        numero = float(valor)
    except ValueError:
        return None
    return numero if math.isfinite(numero) else None


def _numero_a_texto(numero): #muestra 400.0 como "400" y 7.5 como "7.5" en los formularios
    return str(int(numero)) if float(numero).is_integer() else str(numero)


def _valores_de_empleado(empleado): #valores actuales del empleado para llenar el formulario de edicion
    valores = {campo: _numero_a_texto(getattr(empleado, campo)) if tipo == "decimal" else str(getattr(empleado, campo))
               for campo, etiqueta, tipo in CAMPOS_EDITAR}
    valores["recibe_comision"] = empleado.recibe_comision
    valores["porcentaje_comision"] = _numero_a_texto(empleado.porcentaje_comision) if empleado.recibe_comision else ""
    return valores


class Manejador(BaseHTTPRequestHandler):

    # ---------- respuestas ----------
    def _enviar(self, contenido, estado=200, tipo="text/html; charset=utf-8"):
        cuerpo = contenido.encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _pagina(self, titulo, contenido, estado=200, mensaje=None, tipo_mensaje="exito"):
        self._enviar(plantillas.pagina(titulo, contenido, mensaje, tipo_mensaje), estado)

    def _redirigir(self, destino):
        # 303 hace que el navegador pida la nueva pagina con GET, asi recargar no reenvia el formulario
        self.send_response(303)
        self.send_header("Location", destino)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _no_encontrado(self, texto="La pagina que buscas no existe."):
        self._pagina("No encontrado", plantillas.no_encontrado(texto), estado=404)

    def _empleado_de_url(self, parametros):
        # devuelve (id escrito, empleado); el empleado es None si el ID no es valido o no existe
        id_texto = _valor(parametros, "id")
        if not id_texto.isdigit():
            return id_texto, None
        return id_texto, funciones.obtener_empleado_por_id(int(id_texto))

    def _empleado_no_encontrado(self, id_texto):
        self._no_encontrado(f"No se encontro ningun empleado con ID {id_texto}.")

    # ---------- GET ----------
    def do_GET(self):
        url = urlparse(self.path)
        parametros = parse_qs(url.query)
        ruta = url.path

        if ruta == "/":
            self.inicio(parametros)
        elif ruta == "/nuevo":
            self._pagina("Agregar empleado", plantillas.formulario(CAMPOS_NUEVO, {}, {}, "/nuevo", "Guardar empleado", "/"))
        elif ruta == "/empleado":
            self.ver_empleado(parametros)
        elif ruta == "/editar":
            id_texto, empleado = self._empleado_de_url(parametros)
            if empleado is None:
                return self._empleado_no_encontrado(id_texto)
            self._formulario_editar(empleado, _valores_de_empleado(empleado), {})
        elif ruta == "/eliminar":
            id_texto, empleado = self._empleado_de_url(parametros)
            if empleado is None:
                return self._empleado_no_encontrado(id_texto)
            self._pagina("Eliminar empleado", plantillas.confirmar_eliminacion(empleado))
        elif ruta == "/static/estilos.css":
            with open(os.path.join(CARPETA, "static", "estilos.css"), encoding="utf-8") as archivo:
                self._enviar(archivo.read(), tipo="text/css; charset=utf-8")
        else:
            self._no_encontrado()

    # opciones 2 y 5 del menu: buscar por ID y mostrar por departamento
    def inicio(self, parametros):
        if "id" in parametros:
            return self._redirigir(plantillas.url_empleado(_valor(parametros, "id")))

        rol_buscado = _valor(parametros, "rol")
        if rol_buscado:
            empleados = funciones.mostrar_empleados_por_departamento(rol_buscado)
        else:
            empleados = funciones.lista_empleados

        mensaje = MENSAJES.get(_valor(parametros, "msg"))
        self._pagina("Empleados", plantillas.lista_empleados(empleados, rol_buscado), mensaje=mensaje)

    # opcion 6 del menu: informacion detallada
    def ver_empleado(self, parametros):
        id_texto, empleado = self._empleado_de_url(parametros)
        if empleado is None:
            return self._empleado_no_encontrado(id_texto)

        contenido = plantillas.ficha_empleado(
            empleado,
            funciones.calcular_descuentos(empleado),
            funciones.calcular_comision(empleado),
            funciones.calcular_salario_neto(empleado),
        )
        mensaje = MENSAJES.get(_valor(parametros, "msg"))
        self._pagina(empleado.nombre, contenido, mensaje=mensaje)

    def _formulario_editar(self, empleado, valores, errores):
        contenido = plantillas.formulario(CAMPOS_EDITAR, valores, errores, f"/editar?id={empleado.id}",
                                          "Guardar cambios", f"/empleado?id={empleado.id}")
        self._pagina(f"Editar: {empleado.nombre}", contenido)

    # ---------- POST ----------
    def do_POST(self):
        url = urlparse(self.path)
        parametros = parse_qs(url.query)
        largo = int(self.headers.get("Content-Length") or 0)
        form = parse_qs(self.rfile.read(largo).decode("utf-8"), keep_blank_values=True)

        with candado:
            if url.path == "/nuevo":
                self.agregar(form)
            elif url.path == "/editar":
                self.editar(parametros, form)
            elif url.path == "/eliminar":
                self.eliminar(parametros)
            else:
                self._no_encontrado()

    # opcion 1 del menu: agregar empleado
    def agregar(self, form):
        datos, errores, valores = validar_formulario(form, CAMPOS_NUEVO)
        if errores:
            contenido = plantillas.formulario(CAMPOS_NUEVO, valores, errores, "/nuevo", "Guardar empleado", "/")
            return self._pagina("Agregar empleado", contenido)

        empleado = funciones.agregar_empleado(datos)
        self._redirigir(f"/empleado?id={empleado.id}&msg=creado")

    # opcion 3 del menu: editar empleado, solo se aplican los campos que cambiaron
    def editar(self, parametros, form):
        id_texto, empleado = self._empleado_de_url(parametros)
        if empleado is None:
            return self._empleado_no_encontrado(id_texto)

        datos, errores, valores = validar_formulario(form, CAMPOS_EDITAR)
        if errores:
            return self._formulario_editar(empleado, valores, errores)

        hubo_cambios = False
        for campo, etiqueta, tipo in CAMPOS_EDITAR:
            if getattr(empleado, campo) != datos[campo]:
                funciones.editar_empleado_por_id(empleado, campo, datos[campo])
                hubo_cambios = True

        comision = (datos["recibe_comision"], datos["porcentaje_comision"])
        if (empleado.recibe_comision, empleado.porcentaje_comision) != comision:
            funciones.editar_empleado_por_id(empleado, "comision", comision)
            hubo_cambios = True

        self._redirigir(f"/empleado?id={empleado.id}&msg={'editado' if hubo_cambios else 'sin_cambios'}")

    # opcion 4 del menu: eliminar empleado
    def eliminar(self, parametros):
        id_texto, empleado = self._empleado_de_url(parametros)
        if empleado is None:
            return self._empleado_no_encontrado(id_texto)

        funciones.eliminar_empleado_por_id(empleado)
        self._redirigir("/?msg=eliminado")


def iniciar_servidor():
    funciones.cargar_empleado()
    servidor = ThreadingHTTPServer(("127.0.0.1", PUERTO), Manejador)
    print(f"Sistema de gestion de empleados en http://localhost:{PUERTO}  (Ctrl+C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nHasta luego...")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()
