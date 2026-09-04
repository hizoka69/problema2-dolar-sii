#JOAQUIN HERNANDEZ Y BLAS ROJAS
#funciones de error vectorizadas con numpy, redondeamos 2 cifras significativas para todo, como pide el enunciado.

import numpy as np


def redondear_cifras_significativas(valor, cifras=2):
    #convertimos a numpy array para poder usar log10 y floor de manera vectorizada
    valor = np.asarray(valor, dtype=np.float64)
    # Evita log(0)
    valor_seguro = np.where(valor == 0, 1, valor)
    exponente = np.floor(np.log10(np.abs(valor_seguro)))
    factor = 10.0 ** (cifras - 1 - exponente)
    redondeado = np.round(valor * factor) / factor
    return np.where(valor == 0, 0.0, redondeado)


def error_absoluto(valor_real, valor_aproximado):
    #Ea = | valor_verdadero - valor_aproximado |
    return np.abs(np.asarray(valor_real, dtype=np.float64) - np.asarray(valor_aproximado, dtype=np.float64))


def error_relativo(valor_real, ea):
    #Er (%) = (Ea / valor_verdadero) * 100
    valor_real = np.asarray(valor_real, dtype=np.float64)
    ea = np.asarray(ea, dtype=np.float64)
    return (ea / np.abs(valor_real)) * 100.0


def propagar_relativo_multiplicacion_division(er_a, er_b):
    #En multiplicacion o division, los errores relativos (%) se SUMAN.
    return np.asarray(er_a, dtype=np.float64) + np.asarray(er_b, dtype=np.float64)


def propagar_absoluto_suma_resta(ea_a, ea_b):
    #En suma o resta, los errores absolutos se SUMAN.
    return np.asarray(ea_a, dtype=np.float64) + np.asarray(ea_b, dtype=np.float64)


def relativo_a_absoluto(er_porcentual, valor):
    #Convierte un error relativo (%) de vuelta a un error absoluto, dado el valor.
    return (np.asarray(er_porcentual, dtype=np.float64) / 100.0) * np.abs(np.asarray(valor, dtype=np.float64))


def resumen_representacion(precios, cifras=2):
    # Convertimos a numpy array para poder usar log10 y floor de manera vectorizada
    aprox = redondear_cifras_significativas(precios, cifras)
    ea = error_absoluto(precios, aprox)
    er = error_relativo(precios, ea)
    return {
        "real": np.asarray(precios, dtype=np.float64),
        "aproximado": aprox,
        "error_absoluto": ea,
        "error_relativo_pct": er,
    }


def evaluar_operacion_compra_venta(monto, p_compra_real, p_venta_real, cifras=2):
    #flujo de pregunta A2, paso a paso, con redondeo y propagacion de error.
    # 1) Representacion con pocas cifras significativas
    p_compra_aprox = float(redondear_cifras_significativas(p_compra_real, cifras))
    p_venta_aprox = float(redondear_cifras_significativas(p_venta_real, cifras))

    ea_compra = float(error_absoluto(p_compra_real, p_compra_aprox))
    ea_venta = float(error_absoluto(p_venta_real, p_venta_aprox))

    er_compra = float(error_relativo(p_compra_real, ea_compra))
    er_venta = float(error_relativo(p_venta_real, ea_venta))

    # 2) USD = Monto / P_compra  (Monto se asume exacto, error relativo 0)
    usd = monto / p_compra_aprox
    er_usd = propagar_relativo_multiplicacion_division(0.0, er_compra)

    # 3) pesos_final = USD * P_venta
    pesos_final = usd * p_venta_aprox
    er_pesos_final = propagar_relativo_multiplicacion_division(er_usd, er_venta)
    ea_pesos_final = relativo_a_absoluto(er_pesos_final, pesos_final)

    # 4) Ganancia = pesos_final - Monto  (Monto exacto -> ea = 0)
    ganancia = pesos_final - monto
    ea_ganancia = propagar_absoluto_suma_resta(ea_pesos_final, 0.0)
    er_ganancia = error_relativo(ganancia, ea_ganancia) if ganancia != 0 else np.inf

    # 5) Rentabilidad = Ganancia / Monto * 100 (Monto exacto -> error relativo = er_ganancia)
    rentabilidad = (ganancia / monto) * 100.0
    er_rentabilidad = er_ganancia
    ea_rentabilidad = relativo_a_absoluto(er_rentabilidad, rentabilidad) if np.isfinite(er_rentabilidad) else np.inf

    return {
        "p_compra_real": p_compra_real, "p_compra_aprox": p_compra_aprox,
        "p_venta_real": p_venta_real, "p_venta_aprox": p_venta_aprox,
        "er_compra_pct": er_compra, "er_venta_pct": er_venta,
        "usd": usd, "pesos_final": pesos_final,
        "ea_pesos_final": ea_pesos_final, "er_pesos_final_pct": er_pesos_final,
        "ganancia": ganancia, "ea_ganancia": ea_ganancia, "er_ganancia_pct": er_ganancia,
        "rentabilidad_pct": rentabilidad, "ea_rentabilidad_pct": ea_rentabilidad,
    }


def evaluar_variacion(p_inicial_real, p_final_real, cifras=2):
    #redondeamos los precios a pocas cifras significativas
    p_inicial_aprox = float(redondear_cifras_significativas(p_inicial_real, cifras))
    p_final_aprox = float(redondear_cifras_significativas(p_final_real, cifras))

    ea_inicial = float(error_absoluto(p_inicial_real, p_inicial_aprox))
    ea_final = float(error_absoluto(p_final_real, p_final_aprox))

    delta_real = p_final_real - p_inicial_real
    delta_aprox = p_final_aprox - p_inicial_aprox
    ea_delta = propagar_absoluto_suma_resta(ea_inicial, ea_final)
    er_delta = error_relativo(delta_aprox, ea_delta) if delta_aprox != 0 else np.inf

    # ¿El intervalo [delta - ea, delta + ea] cambia de signo?
    limite_inf = delta_aprox - ea_delta
    limite_sup = delta_aprox + ea_delta
    signo_confiable = (limite_inf > 0) or (limite_sup < 0)

    return {
        "p_inicial_real": p_inicial_real, "p_inicial_aprox": p_inicial_aprox, "ea_inicial": ea_inicial,
        "p_final_real": p_final_real, "p_final_aprox": p_final_aprox, "ea_final": ea_final,
        "delta_real": delta_real, "delta_aprox": delta_aprox,
        "ea_delta": ea_delta, "er_delta_pct": er_delta,
        "intervalo": (limite_inf, limite_sup), "signo_confiable": signo_confiable,
    }


if __name__ == "__main__":
    # Sanity check con el ejemplo del enunciado
    print("963.44 a 2 cifras ->", redondear_cifras_significativas(963.44, 2))   # 960
    print("1000.76 a 3 cifras ->", redondear_cifras_significativas(1000.76, 3))  # 1000
