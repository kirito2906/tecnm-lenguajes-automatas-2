# Bitácora de Requerimientos y Auditoría IA — Sesión 25
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Control de Flujo: Bucles while y for  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Estructura de ciclo en instrucciones TAC  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Tuve que cuidar que cada ciclo consumiera dos etiquetas distintas (inicio y fin) y que el segundo ciclo no las reutilizara, por eso el contador `*etiquetas` se incrementa en cada reserva. En el `for` coloqué la actualización del iterador antes del GOTO de regreso y omití `inicio` y `post` cuando son NULL. También revisé que el arreglo tuviera espacio suficiente antes de escribir y usé `snprintf` para no desbordar las líneas de 64 caracteres.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Garantía de actualización de iterador |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto:
Estoy trabajando en Lenguajes y Autómatas II y necesito implementar en C la
generación del esqueleto TAC de un while y de un for. Compilo con
gcc -std=c11 -Wall -Wextra -Werror.

Rol:
Actúa como un ingeniero de software especializado en C y compiladores.

Especificación:
Implementa estas funciones con la firma exacta:
void emitir_while(char lineas[][64], int max, int *n, const char *cond, int *etiquetas);
void emitir_for(char lineas[][64], int max, int *n, const char *inicio, const char *cond, const char *post, int *etiquetas);

Las funciones deben:
- Agregar líneas en lineas[*n] y avanzar *n.
- Emitir para el while cuatro líneas: marca de inicio, "IFFALSE cond GOTO fin",
  "GOTO inicio" y marca de fin.
- Emitir para el for: init, marca, salto condicional, post, GOTO y marca de fin.
- Omitir init o post cuando inicio o post sean NULL.
- Consumir dos etiquetas por ciclo desde *etiquetas, sin reutilizar nombres.
- Validar parámetros, comprobar que haya espacio y usar snprintf.
- No incluir main().

Output:
Entrega el código modular en C y respeta todas las condiciones indicadas.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion25.h"
#include <stdarg.h>
#include <stdio.h>

/* Agrega una linea formateada en lineas[*n] y avanza *n.
 * Devuelve 1 si la agrego, 0 si no hay espacio. */
static int agregar(char lineas[][64], int max, int *n, const char *fmt, ...) {
    va_list ap;
    if (*n >= max) return 0;
    va_start(ap, fmt);
    vsnprintf(lineas[*n], 64, fmt, ap);
    va_end(ap);
    (*n)++;
    return 1;
}

/* Reserva dos etiquetas consecutivas: *ini y *fin. */
static void reservar(int *etiquetas, int *ini, int *fin) {
    *ini = (*etiquetas)++;
    *fin = (*etiquetas)++;
}

void emitir_while(char lineas[][64], int max, int *n, const char *cond, int *etiquetas) {
    int ini, fin;
    if (lineas == NULL || n == NULL || cond == NULL || etiquetas == NULL)
        return;
    if (max - *n < 4) return;

    reservar(etiquetas, &ini, &fin);
    agregar(lineas, max, n, "L%d:", ini);
    agregar(lineas, max, n, "IFFALSE %s GOTO L%d", cond, fin);
    agregar(lineas, max, n, "GOTO L%d", ini);
    agregar(lineas, max, n, "L%d:", fin);
}

void emitir_for(char lineas[][64], int max, int *n, const char *inicio, const char *cond, const char *post, int *etiquetas) {
    int ini, fin;
    int necesarias = 4;
    if (lineas == NULL || n == NULL || cond == NULL || etiquetas == NULL)
        return;
    if (inicio != NULL) necesarias++;
    if (post != NULL) necesarias++;
    if (max - *n < necesarias) return;

    reservar(etiquetas, &ini, &fin);
    if (inicio != NULL) agregar(lineas, max, n, "%s", inicio);
    agregar(lineas, max, n, "L%d:", ini);
    agregar(lineas, max, n, "IFFALSE %s GOTO L%d", cond, fin);
    if (post != NULL) agregar(lineas, max, n, "%s", post);
    agregar(lineas, max, n, "GOTO L%d", ini);
    agregar(lineas, max, n, "L%d:", fin);
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Bucles anidados y condiciones de parada

### Salida del harness
```text
=== AUDITORIA SESION 25 - Esqueleto TAC de while y for ===
Caso                               esperado:              obtenido:              resultado
[ 1] while: marca de inicio             esperado: L0:          obtenido: L0:          OK
[ 2] while: condicion
     esperado: IFFALSE a < b GOTO L1
     obtenido: IFFALSE a < b GOTO L1
     -> OK
[ 3] dos ciclos sin colision            esperado: L2:          obtenido: L2:          OK
[ 4] for: inicializacion                esperado: i = 0        obtenido: i = 0        OK
[ 5] for: actualizacion                 esperado: i = i + 1    obtenido: i = i + 1    OK
[ 6] for sin post (NULL)                esperado: 5            obtenido: 5            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion25.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> Revisé principalmente que el `for` sin `post` (NULL) emitiera solo cinco líneas y que la actualización del iterador quedara antes del GOTO de regreso. También comprobé que dos ciclos seguidos usaran etiquetas distintas (L0/L1 y L2/L3) y que el arreglo tuviera espacio suficiente antes de escribir. Un punto que la IA no contempló es que `emitir_for` y `emitir_while` no avisan cuando no hay espacio: simplemente regresan sin emitir nada, y una condición de más de 63 caracteres se corta en silencio. Al ejecutar el harness, los seis casos pasaron correctamente.

---
**Firma digital:** [kirito2906]
