UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 1

# Guía de laboratorio

## Información básica

ASIGNATURA:

ANÁLISIS Y DISEÑO DE ALGORITMOS

TÍTULO DE LA
PRÁCTICA:
NÚMERO DE
PRÁCTICA:
TIPO DE
PRÁCTICA:

Métodos Heurísticos: Problemas NP y Búsqueda Aleatoria (Monte Carlo)

8

AÑO LECTIVO:

2026-B

NRO.
SEMESTRE:

IV (cuarto)

INDIVIDUAL  X
GRUPAL

MÁXIMO DE ESTUDIANTES

FECHA INICIO:

05/11/2026

FECHA FIN:

09/11/2026

DURACIÓN:  2 horas

RECURSOS A UTILIZAR:
•  Un computador.
•  Material del curso.
•  Bibliografía del curso

DOCENTE(s):

Mg. Roxana Evelyn Limache Calatayud

### Objetivos

### Objetivos, temas y competencias

•  Comprender la diferencia entre problemas P, NP y NP-difíciles.
•  Analizar el problema del vendedor viajero (TSP) y su crecimiento factorial.
•  Implementar una solución por fuerza bruta y evaluar su viabilidad según el tamaño del problema.
•  Implementar y evaluar la búsqueda aleatoria (Monte Carlo) como primera aproximación heurística.

TEMAS:

•  Problemas P, NP y NP-difíciles.
•  El problema del vendedor viajero (TSP).
•  Problema de programación de líneas de producción.
•  Búsqueda aleatoria / Método Monte Carlo.

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

## I. Marco conceptual

### Contenido de la guía

#### 1. Problemas «fáciles» y problemas «muy difíciles» (P, NP y NP-difíciles)

Casi todos los problemas que hemos visto en el curso (ordenar, hallar caminos más cortos, armar un árbol
de expansión mínima) tienen algo en común: existe un método que los resuelve de forma exacta y en un
tiempo razonable, aunque la entrada crezca. A esa familia se le llama clase P.

Hay otros problemas donde pasa algo curioso: si alguien te da una respuesta, comprobar que es correcta
es rápido, pero encontrarla desde cero puede tardar una eternidad. Es como un Sudoku: revisar uno ya
lleno  toma  un  minuto;  llenarlo  probando  combinaciones  puede  tomar  mucho  más.  Esa  familia  se  llama
clase NP. Los más duros de todos son los NP-difíciles: hasta hoy nadie conoce un método rápido que los
resuelva siempre de forma exacta (se sospecha que no existe, pero nadie lo ha demostrado).

Figura 1. Mapa sencillo de los problemas: P, NP y NP-difíciles.

Tabla 1. Las tres clases de problemas en palabras sencillas.

Clase

En palabras sencillas

Ejemplos

¿Qué hacemos?

P

NP

NP-difícil

Se puede resolver de forma exacta y rápida.  Ordenar, caminos más cortos, árbol de

expansión mínima

Usamos un algoritmo exacto.

Una respuesta dada se comprueba rápido,
aunque encontrarla no sea fácil.

Entre los más duros: no se conoce método
exacto rápido. Con muchos datos, ni la
mejor computadora alcanza.

Sudoku, rompecabezas

Depende del problema.

Vendedor viajero (TSP), programación
de líneas de producción

Usamos métodos heurísticos.

Que sean difíciles no significa que no podamos hacer nada. Cuando el problema es grande, renunciamos a
la  garantía  de  la  solución  perfecta  y  usamos  métodos  heurísticos:  métodos  que  buscan  una  solución
buena (aunque no necesariamente la mejor) en un tiempo razonable. De eso trata esta unidad del curso.

#### 2. El problema del vendedor viajero (TSP): un ejemplo con 4 ciudades

Un vendedor sale de la ciudad A, debe visitar las demás ciudades una sola vez cada una y regresar a A,
recorriendo la menor distancia posible. Se llama TSP (Traveling Salesman Problem) y es el ejemplo clásico

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Aprobación:  2022/03/01
de problema NP-difícil.

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Código:  GUIA-PRLD-001

Página: 3

La Figura 2 muestra un ejemplo con 4 ciudades. Como solo hay 3 rutas distintas, podemos calcular el costo
de cada una a mano (Tabla 2) y elegir la mejor.

Figura 2. TSP con 4 ciudades: el mapa con sus distancias y las 3 rutas posibles.

Ruta

Recorrido

Cuenta

Tabla 2. Costo de las 3 rutas del ejemplo.

Ruta 1
Ruta 2
Ruta 3

A → B → C → D → A
A → B → D → C → A
A → C → B → D → A

4 + 2 + 5 + 3
4 + 6 + 5 + 7
7 + 2 + 6 + 3

Costo total
14 (la mejor)
22
18

Con 4 ciudades es muy fácil. El problema aparece cuando las ciudades aumentan.

#### 3. Por qué la fuerza bruta se rinde: el número de rutas explota

La fuerza bruta consiste en probar TODAS las rutas y quedarse con la mejor. Para n ciudades existen (n −
1)! / 2 rutas distintas. El signo ! significa factorial (por ejemplo, 5! = 5 × 4 × 3 × 2 × 1 = 120). Con 4 ciudades
hay 3 rutas, con 5 ciudades hay 12, con 10 hay 181 440 y con 15 hay más de 43 mil millones (Figura 3).

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 4

Figura 3. Crecimiento del número de rutas posibles en el TSP (escala logarítmica: cada marca del eje vale 100 veces más que la anterior).

¿Cuánto tarda esto en la práctica? Supongamos (como valor de ejemplo) una computadora que revisa un
millón de rutas por segundo. La Tabla 3 muestra lo que pasa.

Ciudades
5
8

10
12

15
18
20
25

Tabla 3. Tiempo estimado de la fuerza bruta (a un millón de rutas por segundo).

Rutas distintas

Tiempo estimado

12
2 520

181 440
19 958 400

43 589 145 600
177 843 714 048 000
60 822 550 204 416 000
310 224 200 866 619 719 680 000

instantáneo
0.003 segundos

0.18 segundos
20 segundos

12 horas
5.6 años
1 929 años
unos 9 800 millones de años

Idea para recordar: pasar de 10 a 15 ciudades no es «un poco más difícil»: es 240 240 veces más trabajo.
Por eso la fuerza bruta solo sirve para pocas ciudades.

#### 4. Otro problema difícil: programación de líneas de producción

En una fábrica hay tareas (cada una con su duración) y líneas o máquinas donde pueden hacerse. Hay que
decidir  qué  tarea  va  en  qué  línea  para  que  todo  termine  lo  antes  posible.  Ese  tiempo  total  hasta  que
termina la última tarea se llama makespan.

En la Figura 4 hay 4 tareas de 4, 3, 2 y 5 horas, y 2 líneas. Si ponemos T1 y T2 en la línea 1 y T3 y T4 en la
línea  2,  todo  termina  a  las  7  horas  (Asignación  A).  Si  ponemos  T1  y  T4  juntas,  una  línea  trabaja  9  horas
mientras la otra termina a las 5 y se queda libre (Asignación B). Las dos son válidas, pero la A es mejor.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 5

Figura 4. Las mismas 4 tareas repartidas de dos formas distintas en 2 líneas.

Con solo decidir a qué línea va cada tarea ya hay 2 × 2 × 2 × 2 = 16 asignaciones posibles, y apenas 2 de
ellas logran las 7 horas. Con más tareas o más líneas el número se dispara, igual que en el TSP (Tabla 4).

Tabla 4. Cantidad de formas de asignar las tareas a las líneas.

Tareas

Con 2 líneas (2ⁿ)

Con 3 líneas (3ⁿ)

4
10

20
30

40

16
1 024

1 048 576
1 073 741 824

1 099 511 627 776

81
59 049

3 486 784 401
205 891 132 094 649

12 157 665 459 056 928 801

#### 5. Dos formas de buscar: probar todo (fuerza bruta) o probar al azar (Monte Carlo)

Fuerza bruta: probar todas las posibilidades. Es como revisar una por una todas las llaves de un llavero:
seguro encuentras la correcta, pero si el llavero tuviera millones de llaves no terminarías nunca.

Búsqueda aleatoria o Monte Carlo:  probar solo algunas posibilidades elegidas al azar y quedarse con la
mejor que apareció. Es como probar 10 llaves a ciegas: es rápido, pero quizá ninguna abra la puerta.

Figura 5. Cómo trabajan la fuerza bruta y la búsqueda aleatoria, paso a paso.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Página: 6
Vamos a compararlas con un ejemplo de 5 ciudades (el mismo del ejercicio resuelto). La Tabla 5 muestra
las distancias entre cada par de ciudades.

Código:  GUIA-PRLD-001

0

1

2
3

4

Tabla 5. Distancias entre las 5 ciudades (0 = ciudad de origen).

0

0

10

15
20

25

1

10

0

35
25

30

2

15

35

0
30

5

3

20

25

30
0

15

4

25

30

5
15

0

Con 5 ciudades hay 12 rutas distintas. La Figura 6 las muestra todas, ordenadas por costo: la mejor cuesta
70, la peor 140 y el promedio es 105. Una ruta al azar tiene, en promedio, un costo de 105: bastante peor
que la óptima.

Figura 6. Las 5 ciudades, la ruta óptima (en verde) y el costo de las 12 rutas posibles.

Ahora hagamos Monte Carlo a mano. En cada iteración se mezclan las ciudades (ruta al azar), se calcula su
costo y se guarda la mejor ruta vista hasta el momento. La Tabla 6 muestra una corrida de 8 iteraciones.

Tabla 6. Ejemplo de una corrida de Monte Carlo con 8 iteraciones.

Iteración
1
2
3
4

5
6
7
8

Ruta al azar
0-4-1-3-2-0
0-4-1-2-3-0
0-1-3-2-4-0
0-2-1-3-4-0

0-2-4-3-1-0
0-3-2-4-1-0
0-1-3-4-2-0
0-3-1-4-2-0

Costo
125
140
95
115

70
95
70
95

¿Mejoró?

Mejor hasta ahora
125
125
95
95

Sí (primera ruta)
No
Sí
No

70
70
70
70

Sí (¡la óptima, recorrida al revés!)
No
No (la óptima otra vez, ya no mejora)
No

Observa  que  la  «mejor  hasta  ahora»  solo  cambia  cuando  aparece  una  ruta  mejor.  En  esta  corrida  hubo
suerte y en la iteración 5 ya se tenía la óptima; con otra suerte podría haber tardado mucho más.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 7

#### 6. ¿Qué tan bien funciona Monte Carlo?

En problemas pequeños funciona muy bien. La Figura 7 muestra cómo baja el mejor costo a medida que
pasan  las  iteraciones:  la  línea  azul  es  la  corrida  de  la  Tabla  6  y  la  naranja  es  el  promedio  de  muchas
corridas. El mejor costo nunca empeora (solo mejora o se queda igual), pero nadie puede asegurar en qué
iteración llegará al óptimo.

Figura 7. Convergencia de la búsqueda aleatoria hacia el óptimo en el TSP de 5 ciudades.

El  problema  aparece  cuando  hay  muchas  rutas.  Si  existe  una  sola  ruta  óptima,  cada  intento  al  azar  la
acierta con probabilidad 1 entre el total de rutas: con 5 ciudades es 1 de 12, pero con 10 ciudades es 1 de
181 440. La Figura 8 y la Tabla 7 muestran la probabilidad de haber encontrado la ruta óptima después de
varias iteraciones.

Figura 8. Probabilidad de que Monte Carlo haya encontrado la ruta óptima según el número de iteraciones.

Tabla 7. Probabilidad de encontrar la ruta óptima exacta.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 8

Ciudades

Rutas distintas

Con 200 iteraciones

Con 1 000 iteraciones

Con 10 000 iteraciones

5
8

10

15

12
2 520

181 440

43 589 145 600

≈ 100 %
7.6 %

0.11 %

casi 0 %

≈ 100 %
32.8 %

0.55 %

casi 0 %

≈ 100 %
98.1 %

5.4 %

0.00002 %

Ojo: la tabla mide la probabilidad de dar con la ruta óptima exacta. Monte Carlo sí puede encontrar rutas
muy buenas aunque no sean la óptima; lo que no puede es asegurarlo. Además, no aprende: cada intento
es independiente de los anteriores.

#### 7. Comparación: fuerza bruta frente a búsqueda aleatoria

Criterio

¿Qué hace?
Garantiza el óptimo
Complejidad

Escalabilidad
Analogía

Ventajas

Desventajas

Uso típico

Tabla 8. Fuerza bruta y búsqueda aleatoria (Monte Carlo) lado a lado.

Fuerza bruta

Búsqueda aleatoria (Monte Carlo)

Prueba TODAS las soluciones.
Sí, siempre.
O((n − 1)!)

Prueba k soluciones elegidas al azar.
No, nunca lo garantiza.
O(k), k = número de iteraciones que elige el usuario.

Inviable para n > 12 aproximadamente.
Probar todas las llaves del llavero.

Aplicable a cualquier tamaño (con calidad variable).
Probar algunas llaves a ciegas.

Resultado exacto.

Se vuelve imposible muy pronto.

Instancias pequeñas, verificación.

Muy simple, sirve para casi cualquier problema y siempre
entrega alguna solución.

No garantiza ni siquiera una solución cercana al óptimo y
no aprende de los intentos anteriores.
Primera aproximación rápida.

Si aumentamos el número de iteraciones de Monte Carlo, ¿qué podemos y qué no podemos afirmar? Lo
resume la Tabla 9.

Tabla 9. Qué se puede y qué no se puede afirmar al aumentar las iteraciones.

Sí podemos afirmar

No podemos afirmar

El mejor costo encontrado nunca empeora: solo mejora o se queda
igual.

Que se haya encontrado el óptimo, ni siquiera con muchas
iteraciones.

Cuantas más iteraciones, mayor es la probabilidad de encontrar
una buena ruta.
Con pocas ciudades, 200 iteraciones suelen bastar.

Cuántas iteraciones hacen falta para llegar al óptimo.

Que 200 iteraciones basten con 15 o más ciudades.

#### 8. Resumen

Idea

Tabla 10. Las cinco ideas clave del laboratorio.

En una frase

P y NP-difíciles

Hay problemas que se resuelven rápido (clase P) y otros muy duros (NP-difíciles), como el TSP.

La explosión
Fuerza bruta

Monte Carlo

Heurísticas

Las rutas del TSP crecen como un factorial: con 15 ciudades ya son más de 43 mil millones.
Prueba TODAS las soluciones: garantiza el óptimo, pero solo sirve con pocas ciudades.

Prueba soluciones AL AZAR y guarda la mejor: es rápido y simple, pero sin garantía.

Cuando no se puede garantizar el óptimo, se busca una solución buena en tiempo razonable. Los
siguientes laboratorios mejoran a Monte Carlo.

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 9

## II. Ejercicio/problema resuelto por el docente

Problema: dado un TSP de 5 ciudades con la matriz de distancias del código, calcular la ruta óptima con fuerza
bruta y comparar el resultado contra búsqueda aleatoria (Monte Carlo).

Los datos son los de la Tabla 5 y el mapa está en la Figura 6. Hay 12 rutas distintas y el óptimo es 70. Se
muestran dos programas: el primero prueba todas las rutas (Figura 5, izquierda) y el segundo prueba rutas
al azar (Figura 5, derecha).

### Fuerza bruta (garantiza el óptimo)
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int main() {
    vector<vector<int>> dist = {
        { 0, 10, 15, 20, 25 },
        { 10, 0, 35, 25, 30 },
        { 15, 35, 0, 30, 5 },
        { 20, 25, 30, 0, 15 },
        { 25, 30, 5, 15, 0 }
    };
    vector<int> ciudades = { 1, 2, 3, 4 }; // se fija la ciudad 0 como origen

    int mejorCosto = INT_MAX;
    vector<int> mejorRuta;

    sort(ciudades.begin(), ciudades.end());
    do {
        int costo = dist[0][ciudades[0]];
        for (int i = 0; i < (int)ciudades.size() - 1; i++)
            costo += dist[ciudades[i]][ciudades[i + 1]];
        costo += dist[ciudades.back()][0];

        if (costo < mejorCosto) {
            mejorCosto = costo;
            mejorRuta = ciudades;
        }
    } while (next_permutation(ciudades.begin(), ciudades.end()));

    cout << "Ruta optima (fuerza bruta): 0 -> ";
    for (int c : mejorRuta) cout << c << " -> ";
    cout << "0" << endl;
    cout << "Costo optimo: " << mejorCosto << endl;

    return 0;
}

### Salida del programa de fuerza bruta
Ruta optima (fuerza bruta): 0 -> 1 -> 3 -> 4 -> 2 -> 0

Costo optimo: 70

Siempre  da  esta  ruta  (o  su  equivalente  recorrida  al  revés)  porque  revisa  las  24  permutaciones  de  las
ciudades 1, 2, 3 y 4, que equivalen a las 12 rutas distintas.

### Búsqueda aleatoria / Monte Carlo
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <climits>
using namespace std;

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Código:  GUIA-PRLD-001

Página: 10

int main() {
    vector<vector<int>> dist = {
        { 0, 10, 15, 20, 25 },
        { 10, 0, 35, 25, 30 },
        { 15, 35, 0, 30, 5 },
        { 20, 25, 30, 0, 15 },
        { 25, 30, 5, 15, 0 }
    };
    vector<int> ciudades = { 1, 2, 3, 4 };

    mt19937 rng(random_device{}());
    int mejorCosto = INT_MAX;
    vector<int> mejorRuta;
    int iteraciones = 200;

    for (int it = 0; it < iteraciones; it++) {
        shuffle(ciudades.begin(), ciudades.end(), rng);

        int costo = dist[0][ciudades[0]];
        for (int i = 0; i < (int)ciudades.size() - 1; i++)
            costo += dist[ciudades[i]][ciudades[i + 1]];
        costo += dist[ciudades.back()][0];

        if (costo < mejorCosto) {
            mejorCosto = costo;
            mejorRuta = ciudades;
        }
    }

    cout << "Mejor ruta encontrada (Monte Carlo, " << iteraciones << " iter): 0 -> ";
    for (int c : mejorRuta) cout << c << " -> ";
    cout << "0" << endl;
    cout << "Costo encontrado: " << mejorCosto << endl;

    return 0;
}

### Salida de ejemplo del programa de Monte Carlo
Mejor ruta encontrada (Monte Carlo, 200 iter): 0 -> 2 -> 4 -> 3 -> 1 -> 0

Costo encontrado: 70

Esta ruta es la óptima recorrida al revés (costo 70). Como el programa usa números aleatorios, la salida
puede cambiar cada vez que se ejecuta: en este ejemplo pequeño casi siempre llegará a 70, pero nada lo
asegura.

Método

Ruta encontrada

Costo

Fuerza bruta

0 - 1 - 3 - 4 - 2 - 0

70 (óptimo garantizado)

Monte Carlo (200 iter.)

Converge al óptimo en este caso
pequeño

70 (ver Figura 7)

En este ejemplo, con solo 5 ciudades hay 12 rutas distintas, así que 200 iteraciones al azar son más que
suficientes  para  encontrar  el  óptimo  con  probabilidad  casi  del  100  %  (Figura  8).  Pero  para  15  ciudades
(más  de  43  mil  millones  de  rutas,  Figura  3),  esas  mismas  200  iteraciones  cubrirían  una  fracción
insignificante  del  espacio  de  búsqueda  y  la  mejor  solución  encontrada  sería  casi  siempre  bastante  peor
que la óptima.

## III. Ejercicios/problemas propuestos

Nota:  en  cada  ejercicio,  además  del  código  y  su  ejecución,  incluyan  una  breve  explicación  de  qué  hace  el

UNIVERSIDAD NACIONAL DE SAN AGUSTIN
FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS
ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

Formato: Guía de Práctica de Laboratorio / Talleres / Centros de Simulación

Aprobación:  2022/03/01

Página: 11
código  y  cómo  está  implementada  la  solución  (qué  estructuras  de  datos  usaron,  cómo  adaptaron  el
algoritmo  al  problema,  qué  decisiones  tomaron).  No  se  aceptará  únicamente  el  código  copiado  sin
explicación: la calificación considera qué tan bien pueden justificar y explicar su implementación, no solo si
el programa compila y corre correctamente.

Código:  GUIA-PRLD-001

Ejercicio 1:

Implementa  fuerza  bruta  para  un  TSP  de  10  ciudades  generadas  aleatoriamente,  y  mide  cuánto  tiempo
tarda en encontrar la solución óptima.

Ejercicio 2:

Implementa búsqueda aleatoria (Monte Carlo) para el mismo TSP de 10 ciudades del ejercicio anterior, con
distintos números de iteraciones (100, 1 000, 10 000), y compara qué tan cerca queda del óptimo real en
cada caso.

Ejercicio 3:

Modela una versión simplificada del problema de programación de líneas de producción (por ejemplo, 6
tareas y 2 líneas) y resuélvela con búsqueda aleatoria, minimizando el tiempo total de finalización.

Ejercicio 4:

Genera  la  gráfica  de  crecimiento  del  espacio  de  soluciones  (como  la  Figura  3)  para  un  problema  de
asignación de tareas (n! en vez de (n-1)!/2) y compárala con la del TSP.

Ejercicio 5:

Investiga  y  documenta  un  caso  real  donde  se  use  el  TSP  o  un  problema  de  programación  de  líneas  de
producción  (logística  de  reparto,  planificación  de  manufactura,  diseño  de  circuitos),
indicando
aproximadamente cuántas ciudades o tareas maneja en la práctica.

## IV. Cuestionario

1. ¿Cuál es la diferencia entre un problema de clase P y uno de clase NP?

2. ¿Por qué se dice que el TSP es un problema NP-difícil?

3.  ¿Qué  ventaja  y  qué  desventaja  principal  tiene  la  búsqueda  aleatoria  (Monte  Carlo)  frente  a  la  fuerza
bruta?

4.  Si  se  aumenta  el  número  de  iteraciones  de  Monte  Carlo,  ¿qué  se  puede  afirmar  y  qué  NO  se  puede
afirmar sobre la calidad de la solución encontrada?

5. ¿Por qué la búsqueda aleatoria se considera solo un "primer intento" y no una solución definitiva para
problemas NP-difíciles?

## V. Referencias y bibliografía recomendadas

•  Cormen, T. et al. Introduction to Algorithms (MIT Press, 2022).
•  Sedgewick, R. & Wayne, K. Algorithms (Addison-Wesley, 2011).
•  Brassard, G. & Bratley, P. Fundamentals of Algorithmics (Prentice Hall, 1996).

## Técnicas e instrumentos de evaluación

### Técnicas
Resolución de ejercicios
prácticos
Redacción escrita
### Criterios de evaluación
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

Página: 12

### Instrumentos

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

