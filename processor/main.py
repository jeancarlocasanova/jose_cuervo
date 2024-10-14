import datetime
import os
import django
from django.core.wsgi import get_wsgi_application
from django.conf import settings
import jose_cuervo.settings
from django.core.wsgi import get_wsgi_application
from datetime import datetime
import csv
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jose_cuervo.settings")
application = get_wsgi_application()
django.setup()

from cuervo.models import zip_file_child, zip_file_parent, init_label, label, log_files


def main_processor():
    while True:
        try:
            # Usar las rutas especificadas
            destination_dir = r'E:\ministration_files\zip-files'
            csv_destination_dir = r'E:\ministration_files\csv-files'

            for csv_filename in os.listdir(csv_destination_dir):
                if not csv_filename.endswith('.csv'):
                    continue  # Saltar archivos que no sean CSV

                # Obtener la fecha actual
                fecha_actual = datetime.now()

                # Sumar nueve meses a la fecha actual
                anno = fecha_actual.year + (fecha_actual.month + 9) // 12
                mes = (fecha_actual.month + 9) % 12
                if mes == 0:
                    mes = 12
                dia = min(fecha_actual.day, [31,
                                             29 if anno % 4 == 0 and (anno % 100 != 0 or anno % 400 == 0) else 28,
                                             31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1])

                fecha_nueve_meses_despues = datetime(anno, mes, dia)

                zip_file_obj = zip_file_child.objects.filter(
                    file_name=csv_filename,
                    seen=False,
                    processed_date=None
                ).order_by('-update_date').first()
                if zip_file_obj:
                    brand = zip_file_obj.brand_name
                    ministrationNumber = zip_file_obj.ministration_number
                    csv_file_path = os.path.join(csv_destination_dir, csv_filename)
                    # Columnas a excluir (ID y Registro en este caso)
                    columns_to_exclude = ['ID', 'REGISTRO']

                    folios = []
                    textos = []

                    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        headers = next(csv_reader)
                        exclude_indices = [headers.index(column) for column in columns_to_exclude if column in headers]

                        for row in csv_reader:
                            filtered_row = [value for index, value in enumerate(row) if index not in exclude_indices]
                            folios.extend(filtered_row[::2])  # Obtén los folios (columnas pares)
                            textos.extend(filtered_row[1::2])  # Obtén los textos (columnas impares)

                        # Verifica si hay contenido repetido en los textos
                        duplicates = []
                        seen = set()
                        for i, texto in enumerate(textos):
                            if texto in seen:
                                duplicates.append(i)
                            else:
                                seen.add(texto)

                        folios_filtrado = [valor for valor in folios if not valor.isdigit()]
                        if (textos != []) and folios_filtrado != [] and not duplicates:
                            data_exists = label.objects.filter(uniqueid__in=textos, url__in=folios_filtrado)
                            folios_filtrado = [valor for valor in folios_filtrado if valor.strip()]
                            if not data_exists:
                                if len(folios_filtrado) == len(textos):
                                    for index, x in enumerate(folios_filtrado):
                                        init_label.objects.create(
                                            uniqueid=folios_filtrado[index],
                                            url=textos[index],
                                            file_name=str(csv_file.name),
                                            brand=brand,
                                            ministrationNumber=ministrationNumber,
                                            expiration=fecha_nueve_meses_despues
                                        ).save()

                    # Actualizar la fecha de procesamiento y eliminar el archivo
                    zip_file_obj.processed_date = fecha_actual
                    zip_file_obj.save()
                    os.remove(csv_file_path)

                    # Actualizar el zip_file_parent asociado
                    parent_obj = zip_file_obj.parent
                    if parent_obj:
                        parent_obj.num_processed_files = zip_file_child.objects.filter(parent=parent_obj,
                                                                                       processed_date__isnull=False).count()
                        parent_obj.save()

                    log_files.objects.create(
                        comment='Se ha procesado con exito un archivo',
                        file_name=zip_file_obj.file_name,
                        FK_zip_child=zip_file_obj
                    )
                print('Se ha procesado con exito un archivo')
                time.sleep(10)
        except Exception as e:
            print(f"Error {str(e)}")


main_processor()
