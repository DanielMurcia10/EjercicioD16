# funciones que arman el HTML de cada pagina de la interfaz web
# todo dato que viene de un empleado o del usuario pasa por escape() para evitar inyeccion de HTML
from html import escape
from urllib.parse import quote


def pagina(titulo, contenido, mensaje=None, tipo_mensaje="exito"): #estructura comun de todas las paginas
    aviso = ""
    if mensaje:
        aviso = f'<div class="aviso aviso-{tipo_mensaje}">{escape(mensaje)}</div>'

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)} - Gestion de Empleados</title>
  <link rel="stylesheet" href="/static/estilos.css">
</head>
<body>
  <header class="barra">
    <a class="marca" href="/">Gestion de Empleados</a>
    <nav>
      <a href="/">Empleados</a>
      <a class="boton" href="/nuevo">+ Agregar empleado</a>
    </nav>
  </header>
  <main>
    {aviso}
    <h1>{escape(titulo)}</h1>
    {contenido}
  </main>
</body>
</html>"""


def dinero(valor):
    return f"${valor:,.2f}"


# pagina principal: buscador por ID, filtro por departamento y tabla de empleados
def lista_empleados(empleados, rol_buscado=""):
    buscadores = f"""
    <div class="buscadores">
      <form method="get" action="/" class="buscador">
        <label for="id">Buscar por ID</label>
        <div class="fila">
          <input type="number" id="id" name="id" min="1" step="1" required>
          <button type="submit">Buscar</button>
        </div>
      </form>
      <form method="get" action="/" class="buscador">
        <label for="rol">Filtrar por departamento / rol</label>
        <div class="fila">
          <input type="text" id="rol" name="rol" value="{escape(rol_buscado)}" required>
          <button type="submit">Filtrar</button>
          {'<a class="boton secundario" href="/">Ver todos</a>' if rol_buscado else ''}
        </div>
      </form>
    </div>"""

    if not empleados:
        if rol_buscado:
            vacio = f"No hay empleados registrados en: '{escape(rol_buscado)}'."
        else:
            vacio = "No hay empleados registrados todavia."
        return buscadores + f'<p class="vacio">{vacio}</p>'

    filas = ""
    for e in empleados:
        filas += f"""
        <tr>
          <td>{e.id}</td>
          <td><a href="/empleado?id={e.id}">{escape(e.nombre)}</a></td>
          <td>{escape(e.rol)}</td>
          <td>{escape(e.email)}</td>
          <td class="numero">{dinero(e.salario)}</td>
          <td class="acciones">
            <a href="/empleado?id={e.id}">Ver</a>
            <a href="/editar?id={e.id}">Editar</a>
            <a class="peligro" href="/eliminar?id={e.id}">Eliminar</a>
          </td>
        </tr>"""

    titulo_tabla = f"Empleados en '{escape(rol_buscado)}'" if rol_buscado else "Todos los empleados"
    return buscadores + f"""
    <h2>{titulo_tabla} ({len(empleados)})</h2>
    <div class="tabla-contenedor">
      <table>
        <thead>
          <tr><th>ID</th><th>Nombre</th><th>Rol</th><th>Email</th><th class="numero">Salario</th><th>Acciones</th></tr>
        </thead>
        <tbody>{filas}
        </tbody>
      </table>
    </div>"""


def _campo(campo, etiqueta, tipo, valores, errores): #genera un campo del formulario con su error si lo hay
    valor = escape(valores.get(campo, ""))
    if tipo == "entero":
        entrada = f'<input type="number" id="{campo}" name="{campo}" value="{valor}" min="0" step="1" required>'
    elif tipo == "decimal":
        entrada = f'<input type="number" id="{campo}" name="{campo}" value="{valor}" min="0" step="any" required>'
    elif campo == "email":
        entrada = f'<input type="email" id="{campo}" name="{campo}" value="{valor}" required>'
    else:
        entrada = f'<input type="text" id="{campo}" name="{campo}" value="{valor}" required>'

    error = f'<p class="error">{escape(errores[campo])}</p>' if campo in errores else ""
    return f"""
      <div class="campo{' con-error' if error else ''}">
        <label for="{campo}">{escape(etiqueta)}</label>
        {entrada}
        {error}
      </div>"""


# formulario para agregar o editar un empleado
def formulario(campos, valores, errores, accion, texto_boton, url_cancelar):
    contenido = "".join(_campo(c, etiqueta, tipo, valores, errores) for c, etiqueta, tipo in campos)

    marcado = "checked" if valores.get("recibe_comision") else ""
    porcentaje = escape(valores.get("porcentaje_comision", ""))
    error_porcentaje = ""
    if "porcentaje_comision" in errores:
        error_porcentaje = f'<p class="error">{escape(errores["porcentaje_comision"])}</p>'

    resumen = ""
    if errores:
        resumen = '<div class="aviso aviso-error">Revisa los campos marcados en rojo.</div>'

    return f"""
    {resumen}
    <form method="post" action="{escape(accion)}" class="formulario">
      <div class="rejilla">{contenido}
      </div>
      <fieldset class="comision">
        <legend>Comision</legend>
        <label class="casilla">
          <input type="checkbox" id="recibe_comision" name="recibe_comision" value="si" {marcado}>
          Recibe comision
        </label>
        <div class="campo campo-porcentaje{' con-error' if error_porcentaje else ''}">
          <label for="porcentaje_comision">Porcentaje de comision (ej. 5 = 5%)</label>
          <input type="number" id="porcentaje_comision" name="porcentaje_comision" value="{porcentaje}" min="0" step="any">
          {error_porcentaje}
        </div>
      </fieldset>
      <div class="botones">
        <button type="submit">{escape(texto_boton)}</button>
        <a class="boton secundario" href="{escape(url_cancelar)}">Cancelar</a>
      </div>
    </form>"""


# ficha con la informacion detallada del empleado (opcion 6 del menu de consola)
def ficha_empleado(empleado, descuentos, monto_comision, salario_neto):
    comision = "Si" if empleado.recibe_comision else "No"
    if empleado.recibe_comision:
        comision += f" ({empleado.porcentaje_comision:g}%)"

    return f"""
    <div class="ficha">
      <section>
        <h2>Datos generales</h2>
        <dl>
          <dt>ID</dt><dd>{empleado.id}</dd>
          <dt>Nombre</dt><dd>{escape(empleado.nombre)}</dd>
          <dt>Rol / departamento</dt><dd>{escape(empleado.rol)}</dd>
          <dt>Email</dt><dd>{escape(empleado.email)}</dd>
          <dt>Edad</dt><dd>{empleado.edad}</dd>
          <dt>Anio de ingreso</dt><dd>{empleado.AnioIngreso}</dd>
          <dt>Tiempo trabajando</dt><dd>{empleado.TiempoTrabajando} anios</dd>
          <dt>Horas trabajadas al dia</dt><dd>{empleado.horas_por_dia:g}</dd>
          <dt>Vacaciones anuales</dt><dd>{empleado.vacaciones_anuales} dias</dd>
        </dl>
      </section>
      <section>
        <h2>Salario</h2>
        <dl class="montos">
          <dt>Salario base</dt><dd>{dinero(empleado.salario)}</dd>
          <dt>Descuentos (ISSS, AFP, etc.)</dt><dd>- {dinero(descuentos)}</dd>
          <dt>Bonos</dt><dd>+ {dinero(empleado.bonos)}</dd>
          <dt>Recibe comision</dt><dd>{comision}</dd>
          {f'<dt>Monto de comision</dt><dd>+ {dinero(monto_comision)}</dd>' if empleado.recibe_comision else ''}
          <dt class="total">Salario neto</dt><dd class="total">{dinero(salario_neto)}</dd>
        </dl>
      </section>
    </div>
    <div class="botones">
      <a class="boton" href="/editar?id={empleado.id}">Editar</a>
      <a class="boton peligro" href="/eliminar?id={empleado.id}">Eliminar</a>
      <a class="boton secundario" href="/">Volver a la lista</a>
    </div>"""


# confirmacion antes de eliminar (opcion 4 del menu de consola)
def confirmar_eliminacion(empleado):
    return f"""
    <div class="tarjeta">
      <p><strong>{escape(empleado.nombre)}</strong> (ID {empleado.id}) - {escape(empleado.rol)} - {escape(empleado.email)}</p>
      <p>Seguro desea eliminarlo? Esta accion no se puede deshacer.</p>
      <form method="post" action="/eliminar?id={empleado.id}" class="botones">
        <button type="submit" class="peligro">Si, eliminar</button>
        <a class="boton secundario" href="/empleado?id={empleado.id}">Cancelar</a>
      </form>
    </div>"""


def no_encontrado(texto):
    return f"""
    <p class="vacio">{escape(texto)}</p>
    <div class="botones"><a class="boton secundario" href="/">Volver a la lista</a></div>"""


def url_empleado(id_texto): #arma la url de la ficha escapando lo que haya escrito el usuario
    return "/empleado?id=" + quote(id_texto)
