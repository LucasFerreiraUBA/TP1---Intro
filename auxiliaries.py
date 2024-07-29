from models import Employee
from datetime import datetime

def get_register_type(check_timestamp: datetime, employee: Employee):
    '''
    Dado una hora de fichaje, y un employee devuelve si es una entrada y la diferencia en segundos
    '''
    delta_check_in, delta_check_out = difference_time(employee, check_timestamp)
    is_check_in = abs(delta_check_in) < abs(delta_check_out)
    deviation_seconds = delta_check_in if is_check_in else delta_check_out

    return is_check_in, deviation_seconds

def replace_attr(current, new):
    '''
    Devuelve el valor nuevo solo si no esta vacio.
    '''
    if not new is None:
        return new
    else:
        return current

def deviation(employee: Employee, check_timestamp: datetime, is_check_in: bool):
    '''
    Retorna la diferencia de tiempo entre el fichaje y el horario de entrada/salida.
    '''
    delta_check_in, delta_check_out = difference_time(employee, check_timestamp)

    return delta_check_in if is_check_in else delta_check_out

def difference_time(employee: Employee, check_timestamp: datetime):
    '''
    Calcula las diferencia de tiempo entre el fichaje y los horarios de entrada/salida
    '''
    right_check_in_datetime = datetime.combine(check_timestamp.date(), employee.check_in_time)
    right_check_out_datetime = datetime.combine(check_timestamp.date(), employee.check_out_time)

    delta_check_in = check_timestamp.timestamp() - right_check_in_datetime.timestamp()
    delta_check_out = check_timestamp.timestamp() - right_check_out_datetime.timestamp()

    return delta_check_in, delta_check_out