UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 1

# GUÍA DE LABORATORIO

## INFORMACIÓN BÁSICA

ASIGNATURA:

ANÁLISIS Y DISEÑO DE ALGORITMOS

TÍTULO DE LA
PRÁCTICA:
NÚMERO DE
PRÁCTICA:
TIPO DE
PRÁCTICA:

Métodos Heurísticos: Heurísticas Constructivas y de Búsqueda Local

9

AÑO LECTIVO:

2026-B

NRO.
SEMESTRE:

IV (cuarto)

INDIVIDUAL  X
GRUPAL

MÁXIMO DE ESTUDIANTES

FECHA INICIO:

12/11/2026

FECHA FIN:

16/11/2026

DURACIÓN:  2 horas

RECURSOS A UTILIZAR:
•  Un computador.
•  Material del curso.
•  Bibliografía del curso

DOCENTE(s):

Mg Roxana Evelyn Limache Calatayud

OBJETIVOS:

### OBJETIVOS/TEMAS Y COMPETENCIAS

•  Diferenciar entre métodos aproximados y métodos heurísticos.
•  Implementar una heurística constructiva (Nearest Neighbor) para el TSP.
•  Implementar una heurística de búsqueda local (2-opt) para mejorar una solución existente.
•  Comparar el desempeño de fuerza bruta, Monte Carlo, heurística constructiva y su combinación con

búsqueda local.

TEMAS:

•  Métodos aproximados y métodos heurísticos.
•  Heurísticas constructivas.
•  Heurísticas de búsqueda local.
•  Comparación de estrategias para el TSP.

COMPETENCIAS  C.a  Capacidad de análisis de problemas computacionales.

C.b  Diseño de soluciones algorítmicas eficientes.
C.c  Validación y verificación de algoritmos.
C.d  Comunicación técnica y redacción formal.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 2

## CONTENIDO DE LA GUÍA

- [I. Marco conceptual](#i-marco-conceptual)
    - [De «exacto» a «al azar»](#1-de-exacto-a-al-azar-cuatro-formas-de-resolver-el-tsp)
    - [Nearest Neighbor](#2-heurística-constructiva-nearest-neighbor-vecino-más-cercano)
    - [Búsqueda local 2-opt](#3-búsqueda-local-2-opt-deshacer-cruces-y-saltos-malos)
    - [Combinar construcción y búsqueda local](#4-combinar-construcción-y-búsqueda-local)
    - [Resumen](#5-resumen)
- [II. Ejercicio resuelto por el docente](#ii-ejercicioproblema-resuelto-por-el-docente)
- [III. Ejercicios propuestos](#iii-ejerciciosproblemas-propuestos)
- [IV. Cuestionario](#iv-cuestionario)
- [V. Referencias y bibliografía](#v-referencias-y-bibliografía-recomendadas)
- [Criterios de evaluación](#criterios-de-evaluación)

## I. MARCO CONCEPTUAL

En  el  Laboratorio  8  vimos  que,  para  el  TSP,  probar  todas  las  rutas  (fuerza  bruta)  solo  sirve  con  pocas
ciudades,  y  que  probar  rutas  al  azar  (Monte  Carlo)  no  garantiza  nada.  En  este  laboratorio  veremos
métodos intermedios que usan «sentido común» sobre el problema: Nearest Neighbor para construir una
ruta  y  2-opt  para  mejorarla.  Todos  los  ejemplos  usan  el  mismo  TSP  de  5  ciudades  del  Laboratorio  8  (la
misma tabla de distancias), cuyo óptimo ya conocemos: la ruta 0-1-3-4-2-0 con costo 70.

### 1. De «exacto» a «al azar»: cuatro formas de resolver el TSP

Un método aproximado promete, con una demostración matemática, que su respuesta nunca será peor
que cierto número de veces el óptimo. Un método heurístico no promete nada formal, pero en la práctica
suele dar rutas muy buenas y muy rápido. Es como un GPS que garantiza «llegarás en máximo 30 minutos»
(aproximado) frente al consejo de un taxista que dice «por aquí suele ser más rápido» (heurístico).

Figura 1. Las cuatro formas de resolver el TSP, ordenadas de más garantía y más lento a menos garantía y más rápido.

Tabla 1. Método aproximado frente a método heurístico.

Aspecto

Método aproximado

Método heurístico

¿Qué promete?

Una garantía demostrada: «nunca peor que k veces
el óptimo»

Ninguna garantía formal

¿Cómo se sabe que sirve?  Con una demostración matemática
¿En qué se basa?

Un algoritmo con una cota demostrada

Probándolo con experimentos
Una regla de sentido común sobre el problema

Ejemplos en el TSP

Algoritmo basado en el árbol de expansión mínima
(hasta 2 veces el óptimo)

Nearest Neighbor, 2-opt

### 2. Heurística constructiva: Nearest Neighbor (vecino más cercano)

Una heurística constructiva arma la solución paso a paso, eligiendo en cada paso lo que parece mejor en
ese momento. Nearest Neighbor (NN) funciona así:

•  Empezar en la ciudad de origen (la ciudad 0).
•  Ir siempre a la ciudad no visitada más cercana a la ciudad actual.
•  Repetir hasta visitar todas y, al final, regresar al origen.

La Tabla 2 muestra los pasos con las 5 ciudades del Laboratorio 8, y la Figura 2 los dibuja. En cada paso se
compara solo con las ciudades que faltan por visitar.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 3

Tabla 2. Nearest Neighbor paso a paso desde la ciudad 0 (ruta 0-1-3-4-2-0, costo 70).

Paso
1

2

3
4

5 (cierre)

Ciudad actual
0

1

3
4

2

Candidatos (distancia)

1 (10), 2 (15), 3 (20), 4 (25)

2 (35), 3 (25), 4 (30)

2 (30), 4 (15)
2 (5)

solo queda volver al origen: 0 (15)

Elige
1

3

4
2

0

Tramo
10

Acumulado
10

25

15
5

15

35

50
55

70

Figura 2. Nearest Neighbor construye la ruta paso a paso (cada número sobre una arista es su distancia). Termina con costo 70.

¡Nearest  Neighbor  encontró  el  óptimo!  Pero  cuidado:  fue  suerte  de  la  ciudad  de  partida.  NN  siempre
empieza donde se le diga, y la Tabla 3 muestra qué pasa si se empieza en cada una de las 5 ciudades.

Tabla 3. Nearest Neighbor según la ciudad de inicio (las 5 rutas de NN).

Ciudad de inicio
0
1
2
3
4

Ruta que arma NN
0-1-3-4-2-0
1-0-2-4-3-1
2-4-3-0-1-2
3-4-2-0-1-3
4-2-0-1-3-4

Costo
70
70
85
70
70

Frente al óptimo (70)
Óptimo
Óptimo
21 % peor
Óptimo
Óptimo

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 4

Figura 3. Con 5 ciudades, NN acierta el óptimo en 4 de 5 inicios; solo empezando en la ciudad 2 queda en 85.

Ventaja:  es  muy  rápida,  porque  una  sola  pasada  basta  (unos  n²  cálculos).  Debilidad:  cada  decisión  es
«golosa» y nunca se corrige. Empezando en la ciudad 2, NN va a 4 (5), luego a 3 (15), luego a 0 (20) y a 1
(10), y al final debe cerrar con el tramo 1 a 2, que cuesta 35, el más caro de todo el mapa. Resultado: 85.
Esa ruta es justo la que mejorará 2-opt.

### 3. Búsqueda local: 2-opt (deshacer cruces y saltos malos)

Una heurística de búsqueda local no construye: parte de una ruta que ya está completa y la mejora con
pequeños cambios. En 2-opt el cambio es: elegir un tramo de la ruta e invertirlo (recorrerlo al revés). Si el
costo  baja,  se  acepta  el  cambio;  si  no,  se  descarta.  La  Figura  4  muestra  el  ejemplo:  partimos  de  la  ruta
mala de NN, 0-1-2-4-3-0 (costo 85), e invertimos el tramo de las posiciones 2 a 4 (ciudades 2-4-3 pasan a 3-
4-2). Aclaración: esta es la misma ruta mala de la Figura 3 (NN empezando en la ciudad 2: 2-4-3-0-1-2).
Una  ruta  del  TSP  es  un  ciclo  y  puede  escribirse  empezando  en  cualquier  ciudad;  la  escribimos  desde  la
ciudad  0  porque  el  programa  de  2-opt  siempre  deja  la  ciudad  0  como  primera  posición.  Las  aristas  y  el
costo (85) son exactamente los mismos.

Figura 4. Idea de 2-opt (la ruta de la izquierda es la de NN con inicio en la ciudad 2, escrita desde la 0): al invertir el tramo 2-4-3 se
quitan las aristas rojas de la izquierda (1-2 y 3-0, que suman 55) y entran las de la derecha (1-3 y 2-0, que suman 40). El costo baja
de 85 a 70.

2-opt  repite  esto:  prueba  invertir  cada  tramo  posible,  se  queda  con  la  inversión  si  el  costo  baja,  y  se
detiene cuando ninguna inversión mejora. La Tabla 4 muestra los primeros intentos del programa.

Tabla 4. Traza de 2-opt sobre la ruta inicial 0-1-2-4-3-0 (costo 85).

Intento
1

Se invierte (posiciones)
1 a 2

Ruta que resulta
0-2-1-4-3-0

2
3
4
5

1 a 3
1 a 4
2 a 3
2 a 4

0-4-2-1-3-0
0-3-4-2-1-0
0-1-4-2-3-0
0-1-3-4-2-0

6 a 12

todas las demás

(ya no hay mejora)

Costo
115

110
85
95
70

≥ 70

¿Mejora?
No

No
No (empata)
No
Sí: se acepta

No: 2-opt se detiene

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 5

Cuando  2-opt  se  detiene,  la  ruta  es  un  óptimo  local:  es  la  mejor  entre  todas  sus  «vecinas»  (las  que  se
obtienen  invirtiendo  un  tramo).  Esto  no  garantiza  que  sea  el  óptimo  global;  aquí  sí  lo  fue  (70),  pero  en
problemas más grandes 2-opt puede quedarse atascado en una ruta buena que no es la mejor.

### 4. Combinar construcción y búsqueda local

Lo más efectivo es usar ambas: Nearest Neighbor entrega rápido un buen punto de partida y 2-opt lo pule.
La Figura 5 compara con Monte Carlo, que en cada prueba elige una de las 12 rutas al azar: con 20 pruebas
solo tiene 82 % de probabilidad de haber visto el óptimo, mientras que NN lo obtiene en una sola pasada
(si el inicio es bueno) y 2-opt corrige cuando no.

Figura 5. Probabilidad de que Monte Carlo haya probado la ruta óptima según el número de pruebas (1-(11/12)^k). NN + 2-opt no
depende de la suerte.

Tabla 5. Comparación de las cuatro estrategias en el TSP de 5 ciudades.

Estrategia

Rutas revisadas

Costo obtenido

¿Llega al óptimo (70)?

Fuerza bruta
Monte Carlo, 5 pruebas
Monte Carlo, 20 pruebas
Nearest Neighbor

NN + 2-opt

Las 12
5 al azar
20 al azar
1 construida

1 + mejoras

70
84.4 (promedio)
72.9 (promedio)
70 (inicio 0) o 85 (inicio 2)

Siempre
35 % de las veces
82 % de las veces
Depende de la ciudad de inicio

70 (desde 85, un solo movimiento)  Sí en este caso, sin garantía general

Con solo 5 ciudades todos los métodos se ven parecidos, porque hay apenas 12 rutas. La diferencia real
aparece  cuando  crece  el  problema.  En  el  Laboratorio  10  usaremos  un  TSP  de  12  ciudades:  allí  Nearest
Neighbor da 84.73 (17.3 % peor que el óptimo, 72.21) y NN + 2-opt baja a 81.14 (12.4 % peor). La Figura 6
lo muestra: las heurísticas se acercan al óptimo, pero no lo garantizan, y eso motiva las metaheurísticas del
siguiente laboratorio.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 6

Figura 6. Con 12 ciudades (instancia del Laboratorio 10) las heurísticas dejan de coincidir con el óptimo.

### 5. Resumen

Idea

Qué recordar

Tabla 6. Las cinco ideas clave del laboratorio.

Aproximado vs. heurístico

El aproximado tiene garantía demostrada de calidad; el heurístico no, pero suele ser bueno y
rápido.

Nearest Neighbor

2-opt

Combinar

Sin garantías

Construye una ruta yendo siempre a la ciudad más cercana. Rápida, pero depende de la ciudad de
inicio y nunca se corrige.
Invierte tramos de una ruta completa mientras el costo baje. Termina en un óptimo local.

NN da el punto de partida y 2-opt lo mejora: mejor resultado que cada uno por separado.

En el TSP de 5 ciudades llegamos al óptimo (70); con 12 ciudades ya no. Por eso existen las
metaheurísticas.

## II. EJERCICIO/PROBLEMA RESUELTO POR EL DOCENTE

Problema: el TSP de 5 ciudades del Laboratorio 8 (la misma matriz de distancias). Construir una ruta con
Nearest Neighbor y mejorarla con 2-opt, comparando ambos resultados contra el óptimo conocido (70).

### Heurística constructiva: Nearest Neighbor
#include <iostream>

#include <vector>

using namespace std;

const int N = 5;

int dist[N][N] = {

    { 0, 10, 15, 20, 25},

    {10,  0, 35, 25, 30},

    {15, 35,  0, 30,  5},

    {20, 25, 30,  0, 15},

    {25, 30,  5, 15,  0}

};

int main() {

    int inicio = 0;

    vector<bool> visitado(N, false);

    vector<int> ruta = { inicio };

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 7

    visitado[inicio] = true;

    for (int paso = 1; paso < N; paso++) {

        int actual = ruta.back();

        int masCercano = -1;

        int mejorDist = 1000000;

        for (int c = 0; c < N; c++) {

            if (!visitado[c] && dist[actual][c] < mejorDist) {

                mejorDist = dist[actual][c];

                masCercano = c;

            }

        }

        ruta.push_back(masCercano);

        visitado[masCercano] = true;

    }

    int costo = 0;

    for (int i = 0; i + 1 < N; i++) costo += dist[ruta[i]][ruta[i + 1]];

    costo += dist[ruta.back()][ruta[0]];

    cout << "Ruta (Nearest Neighbor): ";

    for (int c : ruta) cout << c << " -> ";

    cout << ruta[0] << endl;

    cout << "Costo total: " << costo << endl;

    return 0;

}
Salida del programa:
Ruta (Nearest Neighbor): 0 -> 1 -> 3 -> 4 -> 2 -> 0

Costo total: 70

### Búsqueda local: 2-opt (a partir de la ruta que arma NN al empezar en la ciudad 2)
#include <iostream>

#include <vector>

#include <algorithm>

using namespace std;

const int N = 5;

int dist[N][N] = {

    { 0, 10, 15, 20, 25},

    {10,  0, 35, 25, 30},

    {15, 35,  0, 30,  5},

    {20, 25, 30,  0, 15},

    {25, 30,  5, 15,  0}

};

int costoRuta(const vector<int>& ruta) {

    int c = 0;

    for (int i = 0; i + 1 < N; i++) c += dist[ruta[i]][ruta[i + 1]];

    c += dist[ruta[N - 1]][ruta[0]];

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 8

    return c;

}

int main() {

    // Ruta inicial: la que arma Nearest Neighbor al empezar en la ciudad 2

    vector<int> ruta = { 0, 1, 2, 4, 3 };

    cout << "Ruta inicial: ";

    for (int c : ruta) cout << c << " -> ";

    cout << ruta[0] << "  (costo " << costoRuta(ruta) << ")" << endl;

    bool mejora = true;

    while (mejora) {

        mejora = false;

        for (int i = 1; i < N - 1; i++) {

            for (int j = i + 1; j < N; j++) {

                vector<int> nueva = ruta;

                reverse(nueva.begin() + i, nueva.begin() + j + 1);

                if (costoRuta(nueva) < costoRuta(ruta)) {

                    ruta = nueva;

                    mejora = true;

                }

            }

        }

    }

    cout << "Ruta (2-opt): ";

    for (int c : ruta) cout << c << " -> ";

    cout << ruta[0] << endl;

    cout << "Costo total: " << costoRuta(ruta) << endl;

    return 0;

}

Salida del programa:
Ruta inicial: 0 -> 1 -> 2 -> 4 -> 3 -> 0  (costo 85)

Ruta (2-opt): 0 -> 1 -> 3 -> 4 -> 2 -> 0

Costo total: 70

Nearest Neighbor construye la ruta 0-1-3-4-2-0 con costo 70 cuando empieza en la ciudad 0 (Tabla 2 y Figura
2), pero empezando en la ciudad 2 obtiene 85 (Tabla 3). 2-opt toma esa ruta de 85 y la mejora en un solo
movimiento: invierte el tramo de las posiciones 2 a 4 y llega a 0-1-3-4-2-0 con costo 70 (Tabla 4 y Figura 4).

## III. EJERCICIOS/PROBLEMAS PROPUESTOS

Nota:  en  cada  ejercicio,  además  del  código  y  su  ejecución,  incluyan  una  breve  explicación  de  qué  hace  el
código  y  cómo  está  implementada  la  solución  (qué  estructuras  de  datos  usaron,  cómo  adaptaron  el
algoritmo  al  problema,  qué  decisiones  tomaron).  No  se  aceptará  únicamente  el  código  copiado  sin
explicación: la calificación considera qué tan bien pueden justificar y explicar su implementación, no solo si
el programa compila y corre correctamente.

Ejercicio 1:

Implementa  Nearest  Neighbor  para  un  TSP  de  15  ciudades  generadas  aleatoriamente,  y  ejecútalo

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 9

partiendo de cada una de las 15 ciudades como origen. ¿El resultado cambia según el punto de partida?

Ejercicio 2:

Aplica 2-opt sobre las 15 soluciones del ejercicio anterior. ¿El mejor resultado final sigue dependiendo de
la ciudad de origen usada por Nearest Neighbor?

Ejercicio 3:

Implementa otra heurística constructiva: la heurística del "vecino más barato" (cheapest insertion), que en
cada paso inserta la ciudad no visitada que menos aumenta el costo total, en cualquier posición de la ruta.
Compárala contra Nearest Neighbor.

Ejercicio 4:

Mide  el  tiempo  de  ejecución  de  Nearest  Neighbor  +  2-opt  para  instancias  de  20,  50  y  100  ciudades,  y
compáralo  contra  el  tiempo  que  tomaría  fuerza  bruta  para  esos  mismos  tamaños  (estimado,  sin
ejecutarlo).

Ejercicio 5:

Aplica Nearest Neighbor + 2-opt a un caso real: una lista de direcciones o puntos de interés de tu ciudad
(puedes usar coordenadas aproximadas), y calcula la ruta de reparto o visita más corta posible.

## IV. CUESTIONARIO

1. ¿Cuál es la diferencia entre un método aproximado y un método heurístico?

2.  ¿Por  qué  Nearest  Neighbor  puede  terminar  con  un  salto  muy  costoso  al  final  de  la  ruta?  Usa  como
ejemplo el inicio en la ciudad 2 de la Tabla 3.

3. ¿Qué significa que 2-opt encuentre un "óptimo local"? ¿Por qué no garantiza el óptimo global?

4. ¿Por qué combinar una heurística constructiva con una de búsqueda local suele dar mejores resultados
que usar cualquiera de las dos por separado?

5.  Comparando  la  Figura  5  (y  la  Tabla  5)  de  este  laboratorio  con  lo  visto  en  el  Laboratorio  8,  ¿por  qué
Nearest Neighbor + 2-opt es preferible a Monte Carlo incluso con un presupuesto de cómputo similar?

## V. REFERENCIAS Y BIBLIOGRAFÍA RECOMENDADAS

•  Cormen, T. et al. Introduction to Algorithms (MIT Press, 2022).
•  Sedgewick, R. & Wayne, K. Algorithms (Addison-Wesley, 2011).
•  Brassard, G. & Bratley, P. Fundamentals of Algorithmics (Prentice Hall, 1996).

TÉCNICAS:
Resolución de ejercicios
prácticos
Redacción escrita
## CRITERIOS DE EVALUACIÓN
Criterio  de
evaluación/
Niveles  de
Expectativa
Informe

1 = Insatisfactorio

El  informe  es  difícil
de leer y no cuenta
con  la  información
pedida (0)

Cantidad de
Información

Uno  o  más  de  los
temas  no  han  sido
tratados (0)

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 10

### TÉCNICAS E INSTRUMENTOS DE EVALUACIÓN

INSTRUMENTOS:
Rubrica

2 = En proceso

3 = Satisfactorio

4 = Sobresaliente

parte

informe

incluye
de

la
la
solicitada,
cuesta

El
mayor
información
pero
comprenderlo (2)
Todos los temas han sido
la
tratados,  pero  solo
las
mayor  parte  de
sido
preguntas
contestadas,
como
mínimo  con  una  frase
cada una (2)

han

El informe incluye
información
la
solicitada  y  es
comprensible (4)

Todos  los  temas
han  sido  tratados
las
y
todas
han
preguntas
sido  contestadas,
aunque  de  forma
breve,  con  una  o
dos  frases  cada
una (3)
La
información
está
claramente
con
relacionada
el  tema  principal
(3)

toda

El
está
informe
claramente  detallado  e
incluye
la
información  solicitada
(8)
los  temas  han
Todos
sido  tratados  y  todas
las  preguntas  han  sido
contestadas  con  tres  o
más frases cada una (6)

La
información  está
claramente  relacionada
con  el  tema  principal  y
presenta
otros
ejemplos (6)

Calidad  de
información

La
información
tiene  poco  que  ver
tema
el
con
principal (0)

La
está
información
relacionada  con  el  tema
principal (2)

