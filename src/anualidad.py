#JOAQUIN HERNANDEZ Y BLAS ROJAS
#calculamos para cada año la variacion de diciembre a enero con su respectivo error propagado, se ordena de años mas confiables a menos confiables.
#se responde pregunta A4.

import numpy as np
from cargar_datos import cargar_serie
from errores import evaluar_variacion

CIFRAS_SIGNIFICATIVAS = 2  # norma general de la seccion 4 del enunciado


def variacion_anual(anios, meses_num, precios, cifras=CIFRAS_SIGNIFICATIVAS):
    # obtenemos los años unicos y ordenados
    anios_unicos = sorted(set(anios.tolist()))
    resultados = []

    for anio in anios_unicos:
        mask = anios == anio
        precios_anio = precios[mask]
        meses_anio = meses_num[mask]

        precio_enero = float(precios_anio[meses_anio == 1][0])
        precio_diciembre = float(precios_anio[meses_anio == 12][0])

        r = evaluar_variacion(precio_enero, precio_diciembre, cifras=cifras)
        r["anio"] = anio
        resultados.append(r)

    resultados.sort(key=lambda r: r["er_delta_pct"])
    return resultados


if __name__ == "__main__":
    anios, meses_num, nombres_mes, precios = cargar_serie()
    resultados = variacion_anual(anios, meses_num, precios)

    print(f"{'Año':<6}{'Ene->Dic (aprox)':<20}{'Δ±Ea':<20}{'Er %':<10}{'Confiable'}")
    for r in resultados:
        delta_str = f"{r['delta_aprox']:.1f} ± {r['ea_delta']:.2f}"
        print(f"{r['anio']:<6}{r['p_inicial_aprox']:.0f}->{r['p_final_aprox']:.0f}{'':<6}"
              f"{delta_str:<20}{r['er_delta_pct']:<10.1f}{r['signo_confiable']}")
