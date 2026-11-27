# Bitácora de Requerimientos y Auditoría IA — Sesión 26
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** TAC para Llamadas a Funciones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Instrucciones param, call y return  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Tuve que cuidar que los PARAM se emitieran en el mismo orden de los argumentos (a1, a2) y que el entero del CALL fuera la cantidad real de PARAM emitidos, por eso cuento solo los argumentos que no son NULL. También manejé el caso en que `resultado` es NULL, donde el CALL no asigna a ningún temporal, y el caso en que el valor de retorno es NULL, donde se escribe solo `RETURN`. Antes de escribir revisé que el arreglo tuviera espacio para los PARAM más el CALL y usé `snprintf` para no desbordar las líneas de 64 caracteres.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Convención de paso de argumentos TAC |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto:
Estoy trabajando en Lenguajes y Autómatas II y necesito implementar en C la
generación de código intermedio TAC para llamadas a funciones y retornos.
Compilo con gcc -std=c11 -Wall -Wextra -Werror.

Rol:
Actúa como un ingeniero de software especializado en C y compiladores.

Especificación:
Implementa estas funciones con la firma exacta:
int emitir_llamada(char lineas[][64], int max, int *n, const char *funcion, const char *a1, const char *a2, const char *resultado);
void emitir_return(char *dst, int cap, const char *valor);

Las funciones deben:
- Generar un PARAM por cada argumento no NULL, en el orden a1, a2.
- Agregar el CALL después de los PARAM y actualizar *n.
- Usar como número del CALL la cantidad real de PARAM emitidos.
- Si resultado es NULL, el CALL no asigna: "CALL f, n"; si no, "_t0 = CALL f, n".
- En emitir_return, escribir "RETURN valor", o solo "RETURN" si valor es NULL.
- Soportar llamadas anidadas sin sobrescribir el temporal de la llamada interna.
- Validar parámetros, comprobar que haya espacio y usar snprintf.
- No incluir main().

Output:
Entrega el código modular en C y respeta todas las condiciones indicadas.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion26.h"
#include <stdio.h>

#define ANCHO 64

/* Escribe "PARAM arg" en destino. */
static void escribir_param(char destino[ANCHO], const char *arg) {
    snprintf(destino, ANCHO, "PARAM %s", arg);
}

int emitir_llamada(char lineas[][64], int max, int *n, const char *funcion, const char *a1, const char *a2, const char *resultado) {
    const char *args[2];
    int total = 0;
    int inicio;

    if (lineas == NULL || n == NULL || funcion == NULL)
        return 0;

    /* Junta solo los argumentos no NULL, conservando el orden a1, a2 */
    if (a1 != NULL) args[total++] = a1;
    if (a2 != NULL) args[total++] = a2;

    if (*n < 0 || max - *n < total + 1)
        return 0;

    inicio = *n;
    for (int i = 0; i < total; i++)
        escribir_param(lineas[(*n)++], args[i]);

    if (resultado != NULL)
        snprintf(lineas[*n], ANCHO, "%s = CALL %s, %d", resultado, funcion, total);
    else
        snprintf(lineas[*n], ANCHO, "CALL %s, %d", funcion, total);
    (*n)++;

    return *n - inicio;
}

void emitir_return(char *dst, int cap, const char *valor) {
    if (dst == NULL || cap <= 0)
        return;
    if (valor != NULL)
        snprintf(dst, (size_t)cap, "RETURN %s", valor);
    else
        snprintf(dst, (size_t)cap, "RETURN");
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Llamadas anidadas f(g(x))

### Salida del harness
```text
=== AUDITORIA SESION 26 - Llamadas, parametros y retorno ===
Caso                               esperado:              obtenido:              resultado
[ 1] PARAM x                            esperado: PARAM x      obtenido: PARAM x      OK
[ 2] PARAM y                            esperado: PARAM y      obtenido: PARAM y      OK
[ 3] CALL con dos argumentos
     esperado: _t0 = CALL f, 2
     obtenido: _t0 = CALL f, 2
     -> OK
[ 4] llamada anidada f(g(x))
     esperado: _t1 = CALL f, 1
     obtenido: _t1 = CALL f, 1
     -> OK
[ 5] CALL sin argumentos
     esperado: _t0 = CALL p, 0
     obtenido: _t0 = CALL p, 0
     -> OK
[ 6] RETURN con valor                   esperado: RETURN _t0   obtenido: RETURN _t0   OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion26.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> Revisé principalmente que el entero del CALL coincidiera con los PARAM realmente emitidos y que en la llamada anidada `f(g(x))` el temporal de la llamada interna (`_t0`) se conservara y se pasara como argumento de la externa, que termina en `_t1 = CALL f, 1`. También comprobé el caso sin argumentos (`CALL p, 0`) y el retorno con valor. Un punto que la IA no contempló es que el contrato no define qué devuelve `emitir_llamada()`, y que cuando no hay espacio en el arreglo la función regresa 0 sin emitir nada, sin avisar con un error distinto; además, un nombre de función o argumento de más de 63 caracteres se corta en silencio por el límite de 64. Al ejecutar el harness, los seis casos pasaron correctamente.

---
**Firma digital:** [kirito2906]
