import unicodedata
import argparse
import sqlite3


def list_to_str(lst: list) -> str:
    """
    Convert a list of integers to a string with comma-separated values.
    example: [1,2,3,4] -> '1,2,3,4'

    Args:
        lst (list): A list of integers.

    Returns:
        str: A string with the elements of the list separated by commas.
    """
    if lst == []:
        return '1'

    return ','.join(map(str, lst))


def parse_str_list(str_list: str) -> list:
    """
    Parse from str('int,int') to list(int,int)
    example: '1,2,3,4' -> [1,2,3,4]

    Args:
        str_list (str): A str with the following format -> '1,2,3,4'

    Returns:
        list: A list containing int elements separeted by commas
    """
    if not str_list:
        return [1]
    try:
        return [(int(x) + 1) for x in str_list.split('-') if x.isdigit()]
    except:
        raise Exception('ERROR EN EL PARSING DE STR A LISTA')


def parse_txt_list(filename: str) -> list:
    with open(filename, 'r') as correlativas:
        lineas = correlativas.readlines()

    cc = 2
    subjects = []
    subject = []
    appended = 0

    for i, linea in enumerate(lineas):

        if i % 4 != 0:
            cadena_normalizada = unicodedata.normalize('NFD', linea.strip())
            cadena_sin_tildes = ''.join(
                c for c in cadena_normalizada if unicodedata.category(c) != 'Mn')
            cadena_sin_guiones_espaciados = cadena_sin_tildes.replace(
                ' - ', '-')
            cadena_sin_guiones_disparejos_derecha = cadena_sin_guiones_espaciados.replace(
                ' -', '-')
            cadena_final = cadena_sin_guiones_disparejos_derecha.replace(
                ' -', '-')

            if appended in [1, 2]:
                cadena_final = parse_str_list(cadena_final)
                cadena_final = list(set(cadena_final))

            subject.append(cadena_final)
            appended += 1

        elif i != 0:
            subjects.append(subject)
            subject = []
            cc += 1
            appended = 0

    if subject:
        subjects.append(subject)

    return subjects


def insertar_datos(database, table, subjects_list):
    contador = 2
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        try:
            for subject in subjects_list:
                print(database, table, subject)
                instruccion = str(f'INSERT INTO {
                                  table} (id, name, approval_fathers, approval_children, regular_fathers, regular_children, year) VALUES (?, ?, ?, ?, ?, ?, ?)')
                cursor.execute(instruccion, (contador, subject[0], list_to_str(
                    subject[2]), '', list_to_str(subject[1]), '', 0))
                conn.commit()
                contador += 1
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Procesa un archivo de correlativas.")
    parser.add_argument('-f', '--file', type=str, required=True,
                        help="El archivo de correlativas a procesar")
    parser.add_argument('-d', '--database', type=str,
                        required=True, help="La base de datos a modificar")
    parser.add_argument('-t', '--table', type=str, required=True,
                        help="La tabla de la base de datos a modificar")

    args = parser.parse_args()
    subjects_list = parse_txt_list(args.file)

    insertar_datos(args.database, args.table, subjects_list)


if __name__ == '__main__':
    main()
