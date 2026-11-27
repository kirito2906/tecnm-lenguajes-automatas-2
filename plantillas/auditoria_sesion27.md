# Bitácora de Requerimientos y Auditoría IA — Sesión 27
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Indexación de Arreglos en TAC  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Cálculo de desplazamientos base + offset  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Tuve que cuidar que el índice siempre se multiplicara por el ancho del elemento antes de usarlo como offset. En el arreglo 2D respeté el orden `i * filas + j`, porque intercambiar las dimensiones lee otra celda, y después multipliqué ese índice aplanado por el ancho. También manejé los temporales: cada uno nuevo incrementa `*temporales` para no repetir nombres, y cuando `base` es NULL no se emite ninguna instrucción y la función regresa 0. Antes de escribir revisé que el arreglo tuviera espacio suficiente y usé `snprintf` para no desbordar las líneas de 64 caracteres.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Aplanado de direcciones unidimensionales |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto:
Estoy trabajando en Lenguajes y Autómatas II y necesito implementar en C la
generación de código intermedio TAC para acceder a arreglos de una y dos
dimensiones. Compilo con gcc -std=c11 -Wall -Wextra -Werror.

Rol:
Actúa como un ingeniero de software especializado en C y compiladores.

Especificación:
Implementa estas funciones con la firma exacta:
int emitir_acceso(char lineas[][64], int max, const char *base, const char *indice, int ancho, int *temporales);
int emitir_acceso_2d(char lineas[][64], int max, const char *base, const char *i, const char *j, int filas, int ancho, int *temporales);

Las funciones deben:
- En 1D, emitir "_tK = indice * ancho" y luego la lectura "_tK = base[_tK]".
- En 2D, aplanar primero con i * filas + j, multiplicar por el ancho y leer base[offset].
- Respetar el orden i * filas + j (no intercambiar dimensiones).
- Numerar los temporales desde *temporales, incrementándolo en cada uno nuevo, sin repetir nombres.
- Si base es NULL, no emitir instrucciones y devolver 0.
- Validar parámetros, comprobar que haya espacio y usar snprintf.
- No incluir main().

Output:
Entrega el código modular en C y respeta todas las condiciones indicadas.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion27.h"
#include <stdarg.h>
#include <stdio.h>

#define ANCHO_LINEA 64

/* Escribe una linea formateada en destino. */
static void linea(char destino[ANCHO_LINEA], const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(destino, ANCHO_LINEA, fmt, ap);
    va_end(ap);
}

/* Reserva un temporal nuevo y avanza el contador. */
static int nuevo_temporal(int *temporales) {
    return (*temporales)++;
}

int emitir_acceso(char lineas[][64], int max, const char *base, const char *indice, int ancho, int *temporales) {
    int desplazamiento, valor;

    if (lineas == NULL || base == NULL || indice == NULL || temporales == NULL)
        return 0;
    if (ancho <= 0 || max < 2)
        return 0;

    desplazamiento = nuevo_temporal(temporales);
    valor = nuevo_temporal(temporales);

    linea(lineas[0], "_t%d = %s * %d", desplazamiento, indice, ancho);
    linea(lineas[1], "_t%d = %s[_t%d]", valor, base, desplazamiento);
    return 2;
}

int emitir_acceso_2d(char lineas[][64], int max, const char *base, const char *i, const char *j, int filas, int ancho, int *temporales) {
    int fila_x_filas, lineal, desplazamiento, valor;

    if (lineas == NULL || base == NULL || i == NULL || j == NULL || temporales == NULL)
        return 0;
    if (filas <= 0 || ancho <= 0 || max < 4)
        return 0;

    fila_x_filas = nuevo_temporal(temporales);
    lineal = nuevo_temporal(temporales);
    desplazamiento = nuevo_temporal(temporales);
    valor = nuevo_temporal(temporales);

    linea(lineas[0], "_t%d = %s * %d", fila_x_filas, i, filas);
    linea(lineas[1], "_t%d = _t%d + %s", lineal, fila_x_filas, j);
    linea(lineas[2], "_t%d = _t%d * %d", desplazamiento, lineal, ancho);
    linea(lineas[3], "_t%d = %s[_t%d]", valor, base, desplazamiento);
    return 4;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Arreglos multidimensionales en TAC

### Salida del harness
```text
=== AUDITORIA SESION 27 - Desplazamientos para arreglos 1D y 2D ===
Caso                               esperado:              obtenido:              resultado
[ 1] 1D: i * 4                          esperado: _t0 = i * 4  obtenido: _t0 = i * 4  OK
[ 2] 1D: A[_t0]                         esperado: _t1 = A[_t0] obtenido: _t1 = A[_t0] OK
[ 3] 2D: i * 3                          esperado: _t0 = i * 3  obtenido: _t0 = i * 3  OK
[ 4] 2D: offset por ancho
     esperado: _t2 = _t1 * 4
     obtenido: _t2 = _t1 * 4
     -> OK
[ 5] 2D: M[_t2]                         esperado: _t3 = M[_t2] obtenido: _t3 = M[_t2] OK
[ 6] base NULL (sin acceso)             esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion27.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> Revisé principalmente que el offset incluyera siempre la multiplicación por el ancho, que en 2D el índice lineal fuera `i * filas + j` en ese orden, y que cada acceso consumiera temporales nuevos (`_t0` a `_t3` en 2D) sin repetir nombres. También comprobé que una `base` NULL no emitiera instrucciones y devolviera 0. Un punto que la IA no contempló es que el contrato no define qué devuelven las funciones, y que cuando hay un error (por ejemplo un `max` pequeño o un `ancho` en 0) regresan 0 sin avisar la causa; además, un nombre de arreglo o de índice de más de 63 caracteres se corta en silencio por el límite de 64. Al ejecutar el harness, los seis casos pasaron correctamente.

---
**Firma digital:** [kirito2906]
