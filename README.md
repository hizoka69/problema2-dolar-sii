La ganancia que se evapora

Análisis de cancelación y propagación de error usando los datos del dólar observado del SII (2022–2025).

¿Qué hace este repositorio?

Este código toma los datos mensuales del dólar entre enero 2022 y diciembre 2025 y simula cómo los guardaría un computador usando una mantisa corta, es decir, con pocas cifras significativas. Calculamos el error inicial que esto genera y vemos cómo se arrastra o propaga al hacer los cálculos típicos de compra y venta de divisas. El objetivo es establecer un criterio matemático para saber si una variación en el precio es real, o si es puro ruido provocado por el redondeo (efecto de cancelación).

Estructura

problema2-dolar-sii/
├── README.md                  <- Este archivo
├── INFORME.md                 <- Documento de entrega con las conclusiones
├── requirements.txt           <- Dependencias (numpy, matplotlib)
├── data/
│   └── dolar_observado_sii_2022_2025.csv
├── src/
│   ├── cargar_datos.py        <- Lee el CSV usando np.genfromtxt
│   ├── errores.py             <- Cálculos de error absoluto, relativo y propagado
│   ├── anualidad.py           <- Cálculos de la variación año a año (pregunta A4)
│   ├── punto_flotante.py      <- Análisis en float32/float64 e ida y vuelta (B1, B2, B4)
│   └── generar_resultados.py  <- Script principal que saca los 5 gráficos y la tabla CSV
└── graficos/                  <- Carpeta de salida para los PNG y evaluacion_errores.csv

Cómo correrlo

pip install -r requirements.txt
cd src
python3 generar_resultados.py

Esto va a generar los 5 gráficos obligatorios y el archivo graficos/evaluacion_errores.csv, el cual contiene la tabla con el error absoluto, relativo y propagado para cada mes, las variaciones mensuales y las variaciones de enero a diciembre de cada año.


Parámetros y normas del cálculo

Cifras significativas: Representamos los precios con 2 cifras significativas.

Capital de trabajo: Operamos con un monto base de 1.000.000 CLP.

Reglas de propagación:Para multiplicaciones y divisiones, sumamos los errores relativos en porcentaje.Para sumas y restas, sumamos los errores absolutos en pesos.

El criterio de signo confiable: establece que un cambio en el precio solo se considera seguro si, al sumarle y restarle su margen de error absoluto, el rango resultante no cruza por el número cero.  Si este margen de error incluye al cero, la incertidumbre es demasiado grande, por lo que resulta imposible confirmar si el valor del dólar realmente aumentó o disminuyó. Cuando esto ocurre, significa que estamos ante un caso de cancelación matemática.  

Resultados y conclusión

Ver [`INFORME.md`](./INFORME.md) para el detalle de cada pregunta (A1-A5,
B1-B4) y la conclusión final sobre cuándo conviene comprar y vender dólares.