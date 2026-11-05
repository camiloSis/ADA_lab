# Guía de laboratorio

## Información institucional

- **Universidad:** Universidad Nacional de San Agustín
- **Facultad:** Facultad de Ingeniería de Producción y Servicios
- **Escuela profesional:** Escuela Profesional de Ingeniería de Sistemas
- **Formato:** Guía de Práctica de Laboratorio / Talleres / Centros de Simulación
- **Código:** GUIA-PRLD-001
- **Fecha de aprobación:** 2022/03/01

## Información básica

| Campo | Detalle |
|---|---|
| **Asignatura** | Análisis y Diseño de Algoritmos |
| **Título de la práctica** | Programación Dinámica: Mochila 0/1 y Mochila Ilimitada |
| **Número de práctica** | 7 |
| **Año lectivo** | 2026-B |
| **Semestre** | IV (cuarto) |
| **Tipo de práctica** | Individual (X); grupal |
| **Máximo de estudiantes** | No especificado |
| **Fecha de inicio** | 29/10/2026 |
| **Fecha de fin** | 02/11/2026 |
| **Duración** | 2 horas |
| **Docente** | Mg. Roxana Evelyn Limache Calatayud |

### Recursos

- Un computador.
- Material del curso.
- Bibliografía del curso.

### Objetivos

- Comprender el problema de la mochila y sus variantes.
- Implementar la solución de Mochila 0/1 mediante programación dinámica.
- Implementar la solución de Mochila Ilimitada mediante programación dinámica.
- Aplicar la técnica SRTBOT y analizar la complejidad de ambas variantes.

### Temas

- El problema de la mochila.
- Mochila 0/1.
- Mochila Ilimitada.
- Comparación y complejidad.

### Competencias

- **C.a:** Capacidad de análisis de problemas computacionales.
- **C.b:** Diseño de soluciones algorítmicas eficientes.
- **C.c:** Validación y verificación de algoritmos.
- **C.d:** Comunicación técnica y redacción formal.

## I. Marco conceptual

### 1. El problema de la mochila (*Knapsack Problem*)

Dado un conjunto de objetos, cada uno con un peso y un valor, y una mochila con capacidad máxima limitada, se busca elegir qué objetos llevar para maximizar el valor total sin exceder la capacidad disponible. Es uno de los problemas de optimización combinatoria más estudiados y aparece en situaciones reales, como decidir qué comprar con un presupuesto fijo, qué carga llevar en un camión con capacidad limitada, qué proyectos financiar con un capital de inversión limitado o cómo cortar materiales minimizando el desperdicio.

Existen dos variantes principales, que se diferencian en si un objeto se puede llevar más de una vez o no.

El ejemplo que se usa en toda la guía contiene tres objetos, cada uno con su peso y valor, y una mochila de capacidad 4 (la capacidad se mide en peso). El objeto 1 tiene la mejor relación valor/peso: 2.00, es decir, 2 unidades de valor por cada unidad de peso. Esto será clave al comparar las dos variantes.

> **Figura 1.** Objetos del ejemplo (peso, valor) y mochila de capacidad 4.

### 2. Mochila 0/1

En esta variante, cada objeto se puede llevar como máximo **una vez**: se toma completo o no se toma, sin fracciones ni repeticiones. De ahí el nombre «0/1»: 0 si no se lleva y 1 si se lleva.

#### Aplicación de SRTBOT

- **S (subproblemas):** `dp[i][w]` es el valor máximo alcanzable usando solo los primeros `i` objetos, con capacidad disponible `w`.
- **R (recurrencia):**

  ```text
  Si peso[i] <= w:
      dp[i][w] = max(dp[i - 1][w],
                     valor[i] + dp[i - 1][w - peso[i]])
  En caso contrario:
      dp[i][w] = dp[i - 1][w]
  ```

- **T (orden topológico):** se recorren los objetos `i` de 1 a `n` y, para cada uno, todas las capacidades `w` de 0 a `W`.
- **B (casos base):** `dp[0][w] = 0` para toda capacidad `w` (sin objetos, el valor es 0); `dp[i][0] = 0` para todo `i` (con capacidad 0, no cabe nada).
- **O (problema original):** la respuesta buscada es `dp[n][W]`.
- **T (tiempo):** `O(n × W)`.

La Figura 2 resume los seis pasos de SRTBOT con los objetos del ejemplo. La Figura 3 muestra la tabla `dp` completa: las filas son los objetos disponibles (la fila `i` significa que se pueden usar los objetos 1 a `i`), las columnas son la capacidad `w` y cada celda `dp[i][w]` contiene el **valor** máximo posible.

Para calcular cada celda se decide si **no** llevar el objeto `i` (se copia la celda de arriba) o **sí** llevarlo (se suma su valor a la celda de la fila anterior con capacidad `w − peso[i]`); se conserva el mayor resultado. Para saber qué objetos se llevaron, se recorre la tabla desde `dp[3][4]` hacia arriba: si `dp[i][w]` es distinto de `dp[i-1][w]`, se llevó el objeto `i`.

> **Figura 2.** SRTBOT aplicado a la Mochila 0/1 con el ejemplo de la guía.
>
> **Figura 3.** Mochila 0/1: tabla `dp` completa, cálculo de `dp[3][4]` y reconstrucción (objetos 1 y 3).

### 3. Mochila Ilimitada

En esta variante, cada objeto se puede llevar tantas veces como se quiera, siempre que la capacidad lo permita.

#### Aplicación de SRTBOT

- **S (subproblemas):** `dp[w]` es el valor máximo alcanzable con capacidad disponible `w`.
- **R (recurrencia):** `dp[w]` es el máximo, entre todos los objetos `i` cuyo peso no supera `w`, de `valor[i] + dp[w - peso[i]]`.
- **T (orden topológico):** basta recorrer las capacidades `w` de 0 a `W` una sola vez, sin una dimensión adicional por objeto, porque cada objeto puede reutilizarse.
- **B (caso base):** `dp[0] = 0`.
- **O (problema original):** la respuesta buscada es `dp[W]`.
- **T (tiempo):** `O(n × W)`.

La Figura 4 aplica SRTBOT a la Mochila Ilimitada y la Figura 5 muestra el cálculo de `dp[4]`. La diferencia clave con la Mochila 0/1 es que, al llevar un objeto, se consulta `dp[w − peso]` en el **mismo arreglo**, que ya puede incluir ese mismo objeto. Por eso un objeto se puede repetir y no hace falta una fila por objeto. Para reconstruir la solución, se sigue desde `dp[4]` la decisión ganadora de cada celda.

> **Figura 4.** SRTBOT aplicado a la Mochila Ilimitada con el ejemplo de la guía.
>
> **Figura 5.** Mochila Ilimitada: arreglo `dp[w]`, cálculo de `dp[4]` y reconstrucción (objeto 1 × 4).

La Figura 6 compara ambas soluciones sobre el mismo conjunto de tres objetos con capacidad 4: en Mochila 0/1, la mejor combinación son los objetos 1 y 3 (valor 6); en Mochila Ilimitada, conviene repetir cuatro veces el objeto 1, con el mejor valor/peso (valor 8).

> **Figura 6.** Mochila 0/1 (valor 6) frente a Mochila Ilimitada (valor 8) con capacidad 4.

### 4. Comparación entre ambas variantes

| Criterio | Mochila 0/1 | Mochila Ilimitada |
|---|---|---|
| Repetición de objetos | No permitida | Permitida (ilimitada) |
| Estructura de la tabla | Bidimensional `dp[i][w]` | Unidimensional `dp[w]` |
| Complejidad | `O(n × W)` | `O(n × W)` |
| Ejemplo de aplicación | Selección de proyectos únicos | Corte de barras, cambio de monedas |

A medida que crece la capacidad, la diferencia entre ambas soluciones se hace más evidente. La Figura 7 muestra que la Mochila 0/1 se detiene en 9 (cuando ya llevó los tres objetos, uno solo de cada uno), mientras que la Mochila Ilimitada sigue creciendo porque siempre puede repetir el objeto con la mejor relación valor/peso.

> **Figura 7.** Valor óptimo según capacidad: Mochila 0/1 frente a Mochila Ilimitada.

## II. Ejercicio/problema resuelto por el docente

**Problema:** dados los objetos `{(peso 1, valor 2), (peso 2, valor 3), (peso 3, valor 4)}` y una mochila de capacidad 4, calcular el valor máximo alcanzable con Mochila 0/1 y con Mochila Ilimitada.

### Mochila 0/1

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> peso  = { 1, 2, 3 };
    vector<int> valor = { 2, 3, 4 };
    int n = peso.size();
    int W = 4;

    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0)); // B: casos base en 0

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            dp[i][w] = dp[i - 1][w]; // no se lleva el objeto i
            if (peso[i - 1] <= w) {
                // R: relación de recurrencia
                dp[i][w] = max(dp[i][w], valor[i - 1] + dp[i - 1][w - peso[i - 1]]);
            }
        }
    }

    cout << "Valor maximo (0/1): " << dp[n][W] << endl;

    // Reconstruir los objetos elegidos
    cout << "Objetos elegidos: ";
    int w = W;
    for (int i = n; i >= 1; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            cout << i << " ";
            w -= peso[i - 1];
        }
    }
    cout << endl;

    return 0;
}
```

### Mochila Ilimitada

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> peso  = { 1, 2, 3 };
    vector<int> valor = { 2, 3, 4 };
    int n = peso.size();
    int W = 4;

    vector<int> dp(W + 1, 0); // B: dp[0] = 0

    for (int w = 1; w <= W; w++) {
        for (int i = 0; i < n; i++) {
            if (peso[i] <= w) {
                // R: se permite reutilizar el objeto i
                dp[w] = max(dp[w], valor[i] + dp[w - peso[i]]);
            }
        }
    }

    cout << "Valor maximo (ilimitada): " << dp[W] << endl;

    return 0;
}
```

### Comparación de resultados

| Criterio | Mochila 0/1 | Mochila Ilimitada |
|---|---:|---:|
| Objetos usados | Objeto 1 + Objeto 3 | Objeto 1 × 4 |
| Peso total | 1 + 3 = 4 | 1 × 4 = 4 |
| Valor total | 2 + 4 = 6 | 2 × 4 = 8 |

Con la misma capacidad, la Mochila Ilimitada logra un valor mayor (8 frente a 6) porque puede repetir el objeto con mejor relación valor/peso (2.0) tantas veces como quepa, algo que la Mochila 0/1 no permite.

## III. Ejercicios/problemas propuestos

En cada ejercicio, además del código y su ejecución, incluyan una breve explicación de qué hace el código y cómo está implementada la solución: qué estructuras de datos usaron, cómo adaptaron el algoritmo al problema y qué decisiones tomaron. No se aceptará únicamente el código copiado sin explicación. La calificación considera qué tan bien pueden justificar y explicar su implementación, no solo si el programa compila y corre correctamente.

### Ejercicio 1

Implementa Mochila 0/1 para un conjunto de al menos 8 objetos ingresados por el usuario e imprime tanto el valor máximo como la lista de objetos elegidos.

### Ejercicio 2

Implementa Mochila Ilimitada para el clásico «problema del cambio de monedas»: dado un conjunto de denominaciones y un monto objetivo, encuentra la combinación que usa la menor cantidad de monedas.

### Ejercicio 3

Modifica la solución de Mochila 0/1 para que, además del valor máximo, muestre la tabla `dp` completa (todas las filas y columnas) y explique cómo se reconstruyó la solución.

### Ejercicio 4

Compara el uso de memoria de Mochila 0/1 (tabla 2D) contra una versión optimizada que use solo un arreglo 1D recorrido de derecha a izquierda. Explica por qué ese recorrido evita reutilizar el mismo objeto más de una vez.

### Ejercicio 5

Aplica Mochila 0/1 a un caso real: dado un presupuesto fijo y una lista de posibles compras (con costo y beneficio estimado), determina la combinación que maximiza el beneficio sin exceder el presupuesto.

## IV. Cuestionario

1. ¿Por qué Mochila 0/1 necesita una tabla bidimensional, mientras que Mochila Ilimitada se resuelve con un arreglo unidimensional?
2. En Mochila 0/1, ¿qué representa exactamente el valor `dp[i][w]`?
3. ¿Por qué en el ejemplo resuelto Mochila Ilimitada obtiene un valor mayor que Mochila 0/1 con la misma capacidad?
4. ¿Cómo se podría adaptar Mochila 0/1 para permitir llevar cada objeto hasta un número limitado de veces (por ejemplo, máximo 3 unidades de cada uno)?
5. ¿Qué papel cumple el paso B (casos base) de SRTBOT en ambas variantes de la mochila?

## V. Referencias y bibliografía recomendadas

- Cormen, T. et al. *Introduction to Algorithms*. MIT Press, 2022.
- Sedgewick, R. y Wayne, K. *Algorithms*. Addison-Wesley, 2011.
- Brassard, G. y Bratley, P. *Fundamentals of Algorithmics*. Prentice Hall, 1996.

## Técnicas e instrumentos de evaluación

**Instrumento:** rúbrica.

La conversión del documento dejó desordenadas algunas celdas de la rúbrica. Se organizan aquí los descriptores legibles y sus puntajes, sin completar información que no aparece en el texto fuente:

- **2 — En proceso:** el informe incluye parte de la información solicitada, pero cuesta comprenderlo. Todos los temas han sido tratados, pero la mayor parte de las preguntas han sido contestadas, como mínimo, con una frase cada una.
- **3 — Satisfactorio:** todos los temas han sido tratados y todas las preguntas han sido contestadas, aunque de forma breve, con una o dos frases cada una. La información está claramente relacionada con el tema principal.
- **4 — Sobresaliente:** el informe incluye la información solicitada y es comprensible.
