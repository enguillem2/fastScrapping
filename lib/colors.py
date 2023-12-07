blue="\33[1;36m" #clear blue
azul="\33[1;36m" #clear blue
gris="\33[0;37m"
verde="\33[1;32m"
rojo="\33[1;31m"
amarillo="\33[1;33m"

def cursor_arriba(n=1):
    print(f'\33[{n}A',end='')

def borrar_linea():
    print("\33[k")
