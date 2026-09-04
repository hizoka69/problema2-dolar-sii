#JOAQUIN HERNANDEZ Y BLAS ROJAS
#responde a preguntas B1, B2 y B4
import numpy as np
from cargar_datos import cargar_serie
from errores import redondear_cifras_significativas, error_absoluto


def demo_b1():
    """Cifras significativas = mantisa corta."""
    valor = 1000.76
    aprox_3 = redondear_cifras_significativas(valor, 3)
    ea = error_absoluto(valor, aprox_3)
    return {"valor": valor, "aprox_3_cifras": float(aprox_3), "error_absoluto": float(ea)}


def ida_y_vuelta(monto, precios, dtype=np.float64):
    # Convertimos a numpy array con el dtype indicado

    precios = np.asarray(precios, dtype=dtype)
    monto_dtype = dtype(monto)

    usd = monto_dtype / precios
    monto_recuperado = usd * precios

    desviacion = monto_recuperado - monto_dtype
    return desviacion.astype(np.float64)  # se sube a float64 solo para poder imprimir/graficar comodo


def demo_b4():
    #cancelacion en float32 vs float64: 874.67 - 875.66
    a64 = np.float64(874.67)
    b64 = np.float64(875.66)
    resultado_64 = a64 - b64

    a32 = np.float32(874.67)
    b32 = np.float32(875.66)
    resultado_32 = a32 - b32

    return {
        "float64": float(resultado_64),
        "float32": float(resultado_32),
        "diferencia_entre_dtypes": float(abs(float(resultado_64) - float(resultado_32))),
    }


if __name__ == "__main__":
    print("B1 ->", demo_b1())

    anios, meses_num, nombres_mes, precios = cargar_serie()
    monto = 1_000_000.0
    dev64 = ida_y_vuelta(monto, precios, dtype=np.float64)
    dev32 = ida_y_vuelta(monto, precios, dtype=np.float32)
    print("B2 -> desviacion maxima float64:", np.max(np.abs(dev64)))
    print("B2 -> desviacion maxima float32:", np.max(np.abs(dev32)))

    print("B4 ->", demo_b4())
