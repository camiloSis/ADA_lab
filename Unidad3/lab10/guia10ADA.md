# GUÍA DE LABORATORIO

## INFORMACIÓN BÁSICA

| Campo | Información |
|---|---|
| Universidad | Universidad Nacional de San Agustín |
| Facultad | Facultad de Ingeniería de Producción y Servicios |
| Escuela | Escuela Profesional de Ingeniería de Sistemas |
| Asignatura | Análisis y Diseño de Algoritmos |
| Título de la práctica | Metaheurísticas Iterativas: Búsqueda Local Iterada (ILS) y Algoritmo Iterativo Goloso (IG) |
| Número de práctica | 10 |
| Año lectivo | 2026-B |
| Semestre | IV (cuarto) |
| Tipo de práctica | Individual (X) / Grupal |
| Fecha de inicio | 19/11/2026 |
| Fecha de fin | 23/11/2026 |
| Duración | 2 horas |
| Docente | Mg. Roxana Evelyn Limache Calatayud |

### Recursos

- Un computador.
- Material del curso.
- Bibliografía del curso.

### Objetivos

- Comprender por qué una búsqueda local se atrapa en óptimos locales y cómo las metaheurísticas escapan de ellos.
- Implementar la Búsqueda Local Iterada (ILS) con perturbación *double-bridge* para el TSP.
- Implementar el Algoritmo Iterativo Goloso (IG) con destrucción y reconstrucción golosa.
- Comparar ILS e IG frente a Nearest Neighbor y NN + 2-opt en calidad de la solución y tiempo.

### Temas

- Metaheurísticas: intensificación y diversificación.
- Búsqueda Local Iterada (ILS).
- Algoritmo Iterativo Goloso (IG).
- Comparación de metaheurísticas de trayectoria para el TSP.

### Competencias

- C.a. Capacidad de análisis de problemas computacionales.
- C.b. Diseño de soluciones algorítmicas eficientes.
- C.c. Validación y verificación de algoritmos.
- C.d. Comunicación técnica y redacción formal.

## CONTENIDO DE LA GUÍA

- [I. Marco conceptual](#i-marco-conceptual)
- [II. Ejercicio resuelto por el docente](#ii-ejercicio-resuelto-por-el-docente)
- [III. Ejercicios/Problemas propuestos](#iii-ejerciciosproblemas-propuestos)
- [IV. Cuestionario](#iv-cuestionario)
- [V. Referencias y bibliografía recomendadas](#v-referencias-y-bibliografía-recomendadas)
- [Técnicas e instrumentos de evaluación](#técnicas-e-instrumentos-de-evaluación)
- [Criterios de evaluación](#criterios-de-evaluación)

## I. MARCO CONCEPTUAL

En el Laboratorio 9, Nearest Neighbor armó una ruta rápida y 2-opt la mejoró hasta que ya no pudo más. Pero «ya no pudo más» no significa «llegó a la mejor ruta». En este laboratorio veremos dos metaheurísticas que ayudan a salir de ese atasco: ILS (Búsqueda Local Iterada) e IG (Algoritmo Iterativo Goloso). Todos los ejemplos usan el mismo TSP de 12 ciudades, cuyo óptimo exacto es 72.21.

### 1. El problema: quedarse atascado en un óptimo local

Si una búsqueda local llega a una ruta en la que ninguna modificación pequeña mejora el costo, se encuentra en un óptimo local. El problema es que puede existir otro óptimo local mejor en otra parte del paisaje de soluciones. 2-opt no puede salir de ese valle por sí solo porque rechaza cualquier ruta peor durante la mejora local.

La metaheurística intenta decidir cuándo es útil escapar temporalmente de un óptimo local, qué tan lejos perturbar la solución y cuándo aceptar la nueva solución.

### 2. Metaheurísticas: intensificación y diversificación

Las metaheurísticas combinan dos mecanismos:

- **Intensificación:** explora intensamente alrededor de buenas soluciones para refinarlas.
- **Diversificación:** cambia suficientemente la búsqueda para explorar regiones distintas del espacio de soluciones y evitar repetir siempre el mismo valle.

En ILS, la búsqueda local y la perturbación mantienen el equilibrio entre ambos mecanismos. En IG, la reconstrucción golosa produce intensificación y la destrucción aleatoria aporta diversificación.

### 3. ILS: perturbar y volver a mejorar

Iterated Local Search repite un ciclo sencillo sobre la solución actual:

1. **Perturbar:** cambiar la ruta de forma fuerte y aleatoria para «salir del valle».
2. **Mejorar:** aplicar 2-opt a la ruta perturbada hasta llegar a un nuevo óptimo local.
3. **Aceptar o descartar:** si la nueva ruta es mejor que la actual, reemplazarla; en este ejercicio se usa un criterio de aceptación estricto.

La perturbación utilizada es *double-bridge*: se corta la ruta en cuatro puntos y se reordenen cuatro segmentos. Esta operación modifica varias aristas a la vez y permite que la búsqueda salga de una región del paisaje de soluciones.

### 4. IG: destruir y reconstruir con criterio goloso

Iterated Greedy usa la misma idea general de salir y volver a bajar, pero cambia las herramientas:

1. **Destruir:** eliminar una parte de la ruta actual.
2. **Reconstruir:** insertar las ciudades eliminadas una por una en la posición que produzca el menor aumento de costo.
3. **Localizar:** el proceso puede continuar con la eliminación y reconstrucción repetidas.
4. **Aceptar o descartar:** conservar la nueva solución únicamente si mejora el costo actual.

IG evita resolver el problema completo desde cero: conserva partes buenas de la ruta, destruye algunas ciudades y reconstruye una solución nueva con decisiones locales.

### 5. ILS frente a IG

Los dos métodos mantienen la misma estructura general —salir del valle, volver a mejorar y aceptar si mejora—, pero cambian la forma de generar nuevas soluciones:

| Aspecto | ILS | IG |
|---|---|---|
| Diversificación | Perturbación *double-bridge* | Destrucción de ciudades y reconstrucción |
| Intensificación | 2-opt sobre la ruta perturbada | Inserción golosa y, si se aplica, búsqueda local |
| Estado conservado | Solución actual y mejor solución encontrada | Solución actual y mejor solución encontrada |
| Ventaja principal | Perturbación fuerte y sencilla | Reutiliza estructura buena de la ruta actual |
| Riesgo principal | Perturbación demasiado débil o demasiado fuerte | Destrucción excesiva o reconstrucción poco diversa |

## II. EJERCICIO RESUELTO POR EL DOCENTE

El ejercicio resuelto muestra la comparación de ILS y IG sobre el mismo TSP de 12 ciudades. ILS comienza con Nearest Neighbor y 2-opt, perturba la ruta con *double-bridge* y vuelve a mejorarla con 2-opt. IG destruye ciudades de la ruta y las vuelve a insertar en la posición que menos aumenta el costo.

Al ejecutar los algoritmos, se registran el costo inicial, los resultados de cada iteración y la mejor ruta encontrada. El código completo de ambos métodos y sus salidas se conserva en el [texto fuente extraído](#texto-fuente-extraído) al final de esta guía.

### Resultados de referencia

- Óptimo exacto del TSP: 72.21.
- La solución inicial NN + 2-opt cuesta 81.14.
- Una ejecución de ILS puede mejorar a 74.32 en la iteración 1 y a 72.21 en la iteración 2.
- La comparación considera calidad de la solución y costo de ejecución.

## III. EJERCICIOS/PROBLEMAS PROPUESTOS

> Nota: en cada ejercicio, además del código y su ejecución, incluyan una breve explicación de qué hace el código y cómo está implementada la solución (qué estructuras de datos usaron, cómo adaptaron el algoritmo al problema y qué decisiones tomaron). No se aceptará únicamente el código copiado sin explicación: la calificación considera qué tan bien pueden justificar y explicar su implementación, no solo si el programa compila y corre correctamente.

### Ejercicio 1

Ejecuta el ILS del ejercicio resuelto con 10 semillas distintas (por ejemplo 1 a 10) y registra para cada una el costo final y la iteración en que se encontró. ¿En cuántas semillas se llega al óptimo 72.21? ¿Qué te dice eso sobre la confiabilidad de un algoritmo aleatorio?

### Ejercicio 2

Modifica el IG para probar d = 1, 2, 3, 5 y 8 ciudades destruidas. Para cada valor, ejecútalo con 10 semillas y reporta el costo promedio. ¿Qué pasa con d muy pequeño? ¿Y con d muy grande? Relaciona tus resultados con los conceptos de intensificación y diversificación.

### Ejercicio 3

Cambia el criterio de aceptación del ILS: además de aceptar soluciones mejores, acepta una solución peor con probabilidad 5%. Compara el resultado con el criterio «solo si mejora» usando varias semillas. ¿Ayuda aceptar soluciones peores a escapar de los valles? Guarda siempre la mejor solución encontrada, aunque la actual empeore.

### Ejercicio 4

Genera un TSP aleatorio de 50 ciudades (con semilla fija) y compara cuatro métodos: Nearest Neighbor, NN + 2-opt, ILS e IG con 500 iteraciones cada uno. Reporta costo y tiempo de ejecución en una tabla. ¿Cuánto mejora cada metaheurística respecto a NN + 2-opt y a qué costo de tiempo?

### Ejercicio 5

Aplica la metaheurística que mejor te funcionó a un caso real: el recorrido de entrega por 15 a 20 puntos de tu ciudad (o capitales del Perú) con coordenadas reales o aproximadas. Muestra la ruta final y compárala con la ruta que obtendrías con solo Nearest Neighbor. Justifica por qué elegiste ILS o IG.

## IV. CUESTIONARIO

1. ¿Qué es un óptimo local? ¿Por qué 2-opt, por sí solo, no puede salir de él aunque exista una ruta mejor?
2. ¿Qué diferencia hay entre intensificación y diversificación? Indica qué componente de ILS y qué componente de IG se encargan de cada una.
3. En ILS y en IG la solución nueva solo se acepta si mejora la actual. ¿Qué ventaja y qué riesgo tiene este criterio de aceptación?
4. ¿Qué pasaría en ILS si la perturbación fuera demasiado débil? ¿Y si fuera tan fuerte que cambiara casi toda la ruta? Explica con el paisaje de soluciones de la Figura 1.
5. Según la Figura 7, ILS baja más rápido por iteración que IG. ¿Significa eso que ILS es siempre mejor? Considera el costo de cada iteración en ambos algoritmos.

## V. REFERENCIAS Y BIBLIOGRAFÍA RECOMENDADAS

- Lourenço, H., Martin, O. y Stützle, T. «Iterated Local Search». En *Handbook of Metaheuristics*, Springer, 2003.
- Ruiz, R. y Stützle, T. «A simple and effective iterated greedy algorithm for the permutation flowshop scheduling problem». *European Journal of Operational Research*, 2007.
- Talbi, E.-G. *Metaheuristics: From Design to Implementation*. Wiley, 2009.
- Cormen, T. et al. *Introduction to Algorithms*. MIT Press, 2022.

## TÉCNICAS E INSTRUMENTOS DE EVALUACIÓN

**Técnicas:**

- Resolución de ejercicios prácticos.
- Redacción escrita.

**Instrumentos:**

- Rúbrica.

## CRITERIOS DE EVALUACIÓN

| Criterio | Insatisfactorio (1) | En proceso (2) | Satisfactorio (3) | Sobresaliente (4) |
|---|---|---|---|---|
| Informe | El informe es difícil de leer y no cuenta con la información pedida (0 puntos) | El informe incluye la mayor parte de la información solicitada, pero cuesta comprenderlo (2 puntos) | El informe incluye la información solicitada y es comprensible (4 puntos) | El informe está claramente detallado e incluye toda la información solicitada (8 puntos) |
| Cantidad de información | Uno o más temas no han sido tratados (0 puntos) | Todos los temas han sido tratados, pero solo la mayor parte de las preguntas han sido contestadas, como mínimo con una frase cada una (2 puntos) | Todos los temas han sido tratados y todas las preguntas han sido contestadas, aunque de forma breve, con una o dos frases cada una (3 puntos) | Todos los temas han sido tratados y todas las preguntas han sido contestadas con tres o más frases cada una (6 puntos) |
| Calidad de información | La información tiene poco que ver con el tema principal (0 puntos) | La información está relacionada con el tema principal (2 puntos) | La información está claramente relacionada con el tema principal (3 puntos) | La información está claramente relacionada con el tema principal y presenta otros ejemplos (6 puntos) |