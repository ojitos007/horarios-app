def obtener_prioridad(tipo):
    if tipo == "sindicalizado":
        return 3
    elif tipo == "contrato":
        return 2
    else:
        return 1
