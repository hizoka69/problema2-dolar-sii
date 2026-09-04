#JOAQUIN HERNANDEZ Y BLAS ROJAS
#este codigo se encarga de recibir los datos proporcionados por los otros archivos (cargar_datos, errores, anualidad y punto_flotante)
#con esto se contesta las preguntas A1-A5 y B1-B4, ademas genera graficos y el csv con los errores calculados.
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cargar_datos import cargar_serie, etiquetas_periodo
from errores import (
    resumen_representacion, evaluar_operacion_compra_venta, evaluar_variacion,
)
from anualidad import variacion_anual
from punto_flotante import ida_y_vuelta, demo_b1, demo_b4

CIFRAS = 2
DIR_GRAFICOS = os.path.join(os.path.dirname(__file__), "..", "graficos")
MONTO = 1_000_000.0

os.makedirs(DIR_GRAFICOS, exist_ok=True)


def grafico_1_serie(anios, etiquetas, precios):
    plt.figure(figsize=(13, 5))
    plt.plot(etiquetas, precios, color="#1f6feb", linewidth=1.6)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel("CLP por USD")
    plt.title("Dolar observado SII Promedio Mensual (2022-2025)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "1_serie_mensual.png")
    plt.savefig(ruta, dpi=140)
    plt.close()
    return ruta


def grafico_2_variacion_mensual(etiquetas, precios):
    delta = np.diff(precios)
    r_ini = resumen_representacion(precios[:-1], CIFRAS)
    r_fin = resumen_representacion(precios[1:], CIFRAS)
    ea_delta = r_ini["error_absoluto"] + r_fin["error_absoluto"]

    colores = np.where(np.abs(delta) <= ea_delta, "#7a0808", "#41c541")

    plt.figure(figsize=(13, 5))
    plt.bar(etiquetas[1:], delta, color=colores)
    plt.errorbar(etiquetas[1:], delta, yerr=ea_delta, fmt="none",
                 ecolor="black", elinewidth=0.8, capsize=2)
    plt.axhline(0, color="grey", linewidth=0.8)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel("Variación mes a mes (CLP)")
    plt.title("Variación mes a mes — rojo: |Variacion| ≤ error propagado (cancelación)")
    plt.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "2_variacion_mensual.png")
    plt.savefig(ruta, dpi=140)
    plt.close()
    n_cancelados = int(np.sum(np.abs(delta) <= ea_delta))
    return ruta, n_cancelados, len(delta)


def grafico_3_error_representacion(etiquetas, precios):
    r = resumen_representacion(precios, CIFRAS)
    plt.figure(figsize=(13, 5))
    plt.bar(etiquetas, r["error_relativo_pct"], color="#452c5c")
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel("Error relativo (%)")
    plt.title("Error de representación mensual")
    plt.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "3_error_representacion.png")
    plt.savefig(ruta, dpi=140)
    plt.close()
    return ruta, r


def grafico_4_rentabilidad(etiquetas, precios, i_min):
    rentabilidades, errores = [], []
    for j in range(i_min + 1, len(precios)):
        r = evaluar_operacion_compra_venta(MONTO, precios[i_min], precios[j], cifras=CIFRAS)
        rentabilidades.append(r["rentabilidad_pct"])
        errores.append(r["ea_rentabilidad_pct"] if np.isfinite(r["ea_rentabilidad_pct"]) else 0.0)

    etiquetas_post = etiquetas[i_min + 1:]
    plt.figure(figsize=(13, 5))
    plt.bar(etiquetas_post, rentabilidades, color="#31708d")
    plt.errorbar(etiquetas_post, rentabilidades, yerr=errores, fmt="none",
                 ecolor="black", elinewidth=0.8, capsize=2)
    plt.axhline(0, color="grey", linewidth=0.8)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel("Rentabilidad (%)")
    plt.title(f"Rentabilidad de comprar en el mínimo ({etiquetas[i_min]}) y vender en cada mes posterior")
    plt.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "4_rentabilidad_desde_minimo.png")
    plt.savefig(ruta, dpi=140)
    plt.close()
    return ruta


def grafico_5_deriva_flotante(etiquetas, precios):
    dev64 = ida_y_vuelta(MONTO, precios, dtype=np.float64)
    dev32 = ida_y_vuelta(MONTO, precios, dtype=np.float32)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
    ax1.plot(etiquetas, dev64, marker="o", markersize=3, color="#17becf")
    ax1.set_title("Deriva ida y vuelta (pesos→USD→pesos) — float64")
    ax1.set_ylabel("Desviación (CLP)")
    ax1.grid(alpha=0.3)

    ax2.plot(etiquetas, dev32, marker="o", markersize=3, color="#e377c2")
    ax2.set_title("Deriva ida y vuelta (pesos→USD→pesos) — float32")
    ax2.set_ylabel("Desviación (CLP)")
    ax2.set_xticklabels(etiquetas, rotation=90, fontsize=7)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "5_deriva_punto_flotante.png")
    plt.savefig(ruta, dpi=140)
    plt.close()
    return ruta, float(np.max(np.abs(dev64))), float(np.max(np.abs(dev32)))


def _formatear_celda(x):
    #convierte celda de tabla a texto para csv, truncando a 2 nros decimales.
    #tambien los bool y strings se dejan tal cual, solo se manipula nros.
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, float, np.floating, np.integer)):
        if not np.isfinite(x):
            return "inf"
        return f"{float(x):.2f}"
    return str(x)


def resultado_a3():
    #respuesta a pregunta A3
    return evaluar_variacion(875.66, 874.67, cifras=CIFRAS)


def generar_tabla_evaluacion(anios, meses_num, etiquetas, precios):
    #generador de grafico y evaluciones
    filas = []

    # A3 (cancelacion Dic-22 vs Dic-23), con la norma de 2 cifras del proyecto
    r_a3 = resultado_a3()
    filas.append([
        "cancelacion_a3", "Dic-22", "Dic-23",
        r_a3["delta_real"], r_a3["delta_aprox"],
        r_a3["ea_delta"], r_a3["er_delta_pct"], r_a3["signo_confiable"],
    ])

    # Representacion mensual
    r = resumen_representacion(precios, CIFRAS)
    for i in range(len(precios)):
        filas.append([
            "representacion_mensual", etiquetas[i], "", precios[i], r["aproximado"][i],
            r["error_absoluto"][i], r["error_relativo_pct"][i], "",
        ])

    # Variacion mes a mes (misma norma de 2 cifras significativas que el grafico 2)
    for i in range(1, len(precios)):
        r_var = evaluar_variacion(precios[i - 1], precios[i], cifras=CIFRAS)
        filas.append([
            "variacion_mes_a_mes", etiquetas[i - 1], etiquetas[i],
            r_var["delta_real"], r_var["delta_aprox"],
            r_var["ea_delta"], r_var["er_delta_pct"], r_var["signo_confiable"],
        ])

    # Variacion anual
    for r_anio in variacion_anual(anios, meses_num, precios):
        filas.append([
            "variacion_anual", f"Ene-{str(r_anio['anio'])[2:]}", f"Dic-{str(r_anio['anio'])[2:]}",
            r_anio["delta_real"], r_anio["delta_aprox"],
            r_anio["ea_delta"], r_anio["er_delta_pct"], r_anio["signo_confiable"],
        ])

    ruta = os.path.join(DIR_GRAFICOS, "evaluacion_errores.csv")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("tipo,periodo_inicial,periodo_final,valor_real,valor_aprox,error_absoluto,error_relativo_pct,signo_confiable\n")
        for fila in filas:
            f.write(",".join(_formatear_celda(x) for x in fila) + "\n")
    return ruta


def main():
    anios, meses_num, nombres_mes, precios = cargar_serie()
    etiquetas = etiquetas_periodo(anios, meses_num)

    ruta1 = grafico_1_serie(anios, etiquetas, precios)
    ruta2, n_cancel, n_total = grafico_2_variacion_mensual(etiquetas, precios)
    ruta3, r3 = grafico_3_error_representacion(etiquetas, precios)
    i_min = int(np.argmin(precios))
    ruta4 = grafico_4_rentabilidad(etiquetas, precios, i_min)
    ruta5, max_dev64, max_dev32 = grafico_5_deriva_flotante(etiquetas, precios)
    ruta_tabla = generar_tabla_evaluacion(anios, meses_num, etiquetas, precios)

    print("Gráficos generados:")
    for r in (ruta1, ruta2, ruta3, ruta4, ruta5):
        print(" -", r)
    print("Tabla de evaluación:", ruta_tabla)
    print()
    print(f"Meses con cancelación (|ΔP| ≤ error propagado): {n_cancel} de {n_total}")
    print(f"Mes con mayor error relativo de representación: "
          f"{etiquetas[int(np.argmax(r3['error_relativo_pct']))]} "
          f"({np.max(r3['error_relativo_pct']):.3f}%)")
    print(f"Deriva máxima ida y vuelta float64: {max_dev64:.3e} CLP")
    print(f"Deriva máxima ida y vuelta float32: {max_dev32:.4f} CLP")
    print("B1:", demo_b1())
    print("B4:", demo_b4())
    print()
    r_a3 = resultado_a3()
    print(f"A3 (2 cifras) -> ΔP = {r_a3['delta_aprox']:.1f} ± {r_a3['ea_delta']:.2f} CLP "
          f"(Er = {r_a3['er_delta_pct']:.1f}%), signo confiable: {r_a3['signo_confiable']}")


if __name__ == "__main__":
    main()
