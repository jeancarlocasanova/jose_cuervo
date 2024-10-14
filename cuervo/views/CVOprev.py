from zeep import Client
from zeep import Client, Settings
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests
from datetime import datetime, timedelta
import pyodbc
from decimal import Decimal
from requests import Session

def search_order_service():

    wsdl_url = 'http://C1.cuervo.com.mx:8001/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/zfun_ws_ordproc_pp/050/zfun_ws_ordproc_pp/zfun_ws_ordproc_pp?sap-client=050'




    # Configuración de autenticación
    username = 'cvowebservic'
    password = 'Mexico2018+'


    # Calcular el rango de fechas
    fecha_actual = datetime.now()
    fecha_inicio = (fecha_actual - timedelta(days=180)).strftime('%Y-%m-%d')
    fecha_fin = (fecha_actual + timedelta(days=180)).strftime('%Y-%m-%d')

    # Crear una sesión con autenticación
    session = Session()
    session.auth = HTTPBasicAuth(username, password)

    # Configurar el transporte con la sesión
    transport = Transport(session=session)

    # Configuración para evitar redirecciones automáticas
    settings = Settings(strict=False, xml_huge_tree=True)

    # Crear el cliente con la URL del WSDL
    client = Client(wsdl=wsdl_url, transport=transport, settings=settings)

    # Forzar el endpoint a la URL correcta
    for service in client.wsdl.services.values():
        for port in service.ports.values():
            port.binding_options['address'] = 'http://C1.cuervo.com.mx:8001/sap/bc/srt/rfc/sap/zfun_ws_ordproc_pp/050/zfun_ws_ordproc_pp/zfun_ws_ordproc_pp?sap-client=050'
            #port.binding_options['address'] = 'http://DV2.cuervo.com.mx:8000/sap/bc/srt/rfc/sap/zfun_ws_ordenes_pp/050/zfun_ws_ordenes_pp/zfun_ws_ordenes_pp?sap-client=050'


    # Parámetros de la función
    params = {
        'item': [
            {
                'SIGN': 'I',
                'OPTION':'BT',
                'LOW': fecha_inicio,
                'HIGH': fecha_fin
            }
        ]
    }

    # Llamar a la función del servicio web con los parámetros adecuados
    try:
        response = client.service.ZFUN_WS_ORDPROC_PP(
            ET_DETALLE=[],   # Tabla vacía inicialmente
            ET_ORDENES=[],   # Tabla vacía inicialmente
            IT_FECHAS=[params],  # Pasar la lista con las fechas
            I_CENTRO='1100',  # Centro
            I_FECHA=''        # Fecha opcional, dejar vacío si no se usa
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")



search_order_service()
