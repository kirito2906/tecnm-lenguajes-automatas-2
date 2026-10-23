# Bitácora de Requerimientos y Auditoría IA — Sesión 01
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Encuadre, Diagnóstico de Punteros y Metodología IA  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Hector Ivan Varguez Andrade]  
**Matrícula:** [24531321]  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Inversión de buffer in-place (char*)  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> La restricción principal fue invertir la cadena sin malloc ni arreglos auxiliares usando solo dos índices y un char temporalEl problema más delicado fue la cadena vacía porque strlen("") devuelve 0 y como size_t no tiene signo restar 1 da un número enorme en lugar de -1 y se saldría del buffer Lo resolví revisando que la longitud no fuera 0 antes de restar También protegí el caso NULL con un return anticipado y comprobé que con "a" el ciclo while (i < j) no entra y la cadena queda igual

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Punteros, O(n) tiempo, O(1) memoria |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[CONTEXTO: Curso de Lenguajes y Autómatas
Trabajo en C con gcc -std=c11 -Wall -Wextra -Werror (las advertencias cuentan como error) y sin bibliotecas no estándar
Mi archivo se compila junto con un harness que ya tiene su propio main()

ROL: Actúa como ingeniero de software de sistemas y compiladores experto en punteros y manejo de memoria en C

ESPECIFICACIÓN: Implementa void invertir(char *s); con esta firma exacta
- Inversión in-place sin malloc ni arreglos auxiliares: solo dos punteros o índices y un char temporal
- Complejidad O(n) en tiempo y O(1) en memoria
- invertir(NULL) debe terminar sin caerse
- Debe funcionar con "" y con "a"
- Casos esperados:
  "HOLA" -> "ALOH"
  "abc" -> "cba"
  "AB" -> "BA"
- Cuidado con size_t: no restar 1 a una longitud de 0Pega aquí el prompt formal que redactaste para la IA]
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion01.h"
#include <string.h>

void invertir(char *s) {
    /* Protege contra NULL y cadena vacia */
    if (s == NULL || *s == '\0') {
        return;
    }

    char *inicio = s;
    char *fin = s + strlen(s) - 1;

    /* Intercambia extremos hasta que se cruzan */
    while (inicio < fin) {
        char tmp = *inicio;
        *inicio = *fin;
        *fin = tmp;
        inicio++;
        fin--;
    }
}// Código devuelto por el LLM
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Valores NULL, buffers vacios y longitudes impares

### Salida del harness
```text
=== AUDITORIA SESION 01 - Inversion de buffer in-place ===
Caso                              esperado:         obtenido:         resultado
[ 1] invertir("HOLA")             esperado: ALOH    obtenido: ALOH    OK
[ 2] invertir("abc")              esperado: cba     obtenido: cba     OK
[ 3] invertir("")                 esperado:         obtenido:         OK
[ 4] invertir("AB")               esperado: BA      obtenido: BA      OK
[ 5] invertir("a")                esperado: a       obtenido: a       OK
[ 6] invertir(NULL)               esperado: sin crash obtenido: sin crash OK

RESULTADO: 6/6 pruebas superadasPega aquí la salida de la celda del harness. Debe terminar con:
RESULTADO: n/n pruebas superadas
```

* [ ] Caso base y límites superados sin *Crash*.
* [ ] No existen accesos fuera de límites ni *Memory Leaks*.
* [ ] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> Con el prompt que usé la IA no omitió ningún caso del harness pues cubrió NULL y cadena vacía y un solo carácter y pasó 6/6 pruebas
Lo verifiqué revisando el código contra cada caso y confirmándolo con la ejecución del harness El resultado dependió de la calidad de la especificación porque incluí la advertencia sobre size_t y longitud 0 y sin ella es un error común hacer strlen(s) - 1 sin validar La IA tampoco devolvió análisis de complejidad porque mi prompt no incluyó la parte de Output así que lo redacté yo Además la función asume que s termina en '\0' y que es modificable pues un literal como char *p = "HOLA" es comportamiento indefinido y normalmente da fallo de segmentación y el contrato no puede verificarlo así que es responsabilidad de quien la llama Complejidad: O(n) en tiempo porque se recorren n/2 pares y O(1) en memoria porque solo usa dos punteros y un char

---
**Firma digital:** [kirito2906]
