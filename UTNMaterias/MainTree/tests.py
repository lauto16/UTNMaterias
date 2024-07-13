def f(st):
    ingreso_child_sql_ids = []
    number = ''
    for char in st:
        if char == ',':
            ingreso_child_sql_ids.append(int(number))
            number = ''
            continue
        elif char.isdigit():
            number += char
    ingreso_child_sql_ids.append(int(number))
    return ingreso_child_sql_ids


print(f("1,2,3,4,5,6,7,8,9,101212121,"))
