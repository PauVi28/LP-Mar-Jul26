def imprimir_tablero(tablero):
    print("\n")
    print(f" {tablero[0]} | {tablero[1]} | {tablero[2]} ")
    print("---+---+---")
    print(f" {tablero[3]} | {tablero[4]} | {tablero[5]} ")
    print("---+---+---")
    print(f" {tablero[6]} | {tablero[7]} | {tablero[8]} ")
    print("\n")


def verificar_ganador(tablero):
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != " ":
            return tablero[a]

    if " " not in tablero:
        return "Empate"

    return None