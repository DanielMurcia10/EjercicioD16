# clase empleado en donde se crearan los diferentes empleados dentro de la empresa
class Empleado:

    def __init__(self, nombre: str, edad: int, salario: float, AnioIngreso: int, TiempoTrabajando: int,
                 email: str, rol: str, id: int = None, horas_por_dia: float = 8,
                 vacaciones_anuales: int = 15, bonos: float = 0.0,
                 recibe_comision: bool = False, porcentaje_comision: float = 0.0):
        # atributos publicos del empleado
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.salario = salario
        self.AnioIngreso = AnioIngreso
        self.TiempoTrabajando = TiempoTrabajando
        self.email = email
        self.rol = rol
        self.horas_por_dia = horas_por_dia
        self.vacaciones_anuales = vacaciones_anuales
        self.bonos = bonos
        self.recibe_comision = recibe_comision
        self.porcentaje_comision = porcentaje_comision

    def __str__(self):
        return (f"ID: {self.id}, Nombre: {self.nombre}, Edad: {self.edad}, Salario: {self.salario}, "
                f"AnioIngreso: {self.AnioIngreso}, TiempoTrabajando: {self.TiempoTrabajando}, "
                f"Email: {self.email}, Rol: {self.rol}")

    def __repr__(self):
        return (f"Empleado(id={self.id}, nombre={self.nombre}, edad={self.edad}, salario={self.salario}, "
                f"AnioIngreso={self.AnioIngreso}, TiempoTrabajando={self.TiempoTrabajando}, "
                f"email={self.email}, rol={self.rol})")