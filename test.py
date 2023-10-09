from pymodbus.client import ModbusTcpClient as ModbusClient
import pyodbc
import time

server = 'MES-AUTOMATION\SQLEXPRESS'
database = 'Cuervo'
username = 'cuervo'
password = 'Hola123456.'
driver = '{ODBC Driver 17 for SQL Server}'

# Crear la cadena de conexión
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Variable de bandera para verificar si es la primera vez
first_time = True


def insert_into_database(value):
    global first_time  # Declarar que estamos utilizando la variable global

    if value is not None:
        url = f'Mensaje recibido: {value}'

        if first_time:
            # Si es la primera vez, realiza una inserción
            cursor.execute("INSERT INTO cuervo_test (url) VALUES (?)", (url,))
            print(f"Valor {value} insertado en la base de datos")
            first_time = False  # Cambia la bandera a False para futuras actualizaciones
        else:
            # Si no es la primera vez, realiza una actualización
            cursor.execute("UPDATE cuervo_test SET url = ? WHERE id = (SELECT MAX(id) FROM cuervo_test)", (url,))
            print(f"Valor {value} actualizado en la base de datos")

        conn.commit()


while True:
    try:
        client = ModbusClient('192.168.10.1')
        client.connect()
        # First digital input address
        address = 1
        # It will send '11111111' to the output
        print(client.read_holding_registers(address, 1, 1).registers[0])
        longitud = int(client.read_holding_registers(address, 1, 1).registers[0])
        print(client.read_holding_registers(100, longitud, 1).registers)
        var = client.read_holding_registers(100, longitud, 1).registers
        cadena = ''
        for char in var:
            char1 = bytearray(char.to_bytes(2, 'big'))
            cadena += str(chr(char1[1])) + str(chr(char1[0]))
        insert_into_database(cadena)
        first_time = False
    except Exception as e:
        print('Error: ' + str(e))

    # Agrega un retraso de 2 segundos
    time.sleep(2)
