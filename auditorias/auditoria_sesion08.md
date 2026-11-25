# Bitácora de Requerimientos y Auditoría IA — Sesión 08
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Inferencia y Promoción de Tipos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Reglas de casteo implícito  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más me costó fue notar que TIPO_ERROR vale 0 en el enum y por eso si solo comparaba los números el error se iba a tratar como el tipo más angosto así que tuve que revisar primero si alguno de los dos tipos era error antes de comparar también tuve que acordarme de poner un default en nombre_tipo para que no regresara NULL con un valor raro

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Promoción entera y ensanchamiento |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Trabajo en C99 con GCC y la cabecera api_sesion08.h que define el enum Tipo con TIPO_ERROR TIPO_CHAR TIPO_INT y TIPO_FLOAT
Rol: Actúa como ingeniero de software de sistemas y compiladores
Especificación: Implementa promover(Tipo a Tipo b) que devuelve el tipo más ancho con la jerarquía CHAR < INT < FLOAT y que si alguno es ERROR devuelve ERROR también implementa hay_perdida(Tipo destino Tipo origen) que devuelve 1 solo cuando el destino es más angosto que el origen y nombre_tipo(Tipo t) que devuelve el nombre en texto
Output: Entrega solo el código modular en C sin main con las mismas firmas del encabezado y un análisis breve de complejidad
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion08_c.c - Fase 2: El Cientifico
 * Propuesta de la IA con la misma firma de api_sesion08.h
 */
#include <stdio.h>
#include "api_sesion08.h"

static int tipo_valido(Tipo t) {
    return t == TIPO_CHAR || t == TIPO_INT || t == TIPO_FLOAT;
}

Tipo promover(Tipo a, Tipo b) {
    if (!tipo_valido(a) || !tipo_valido(b)) {
        return TIPO_ERROR;
    }
    return (a >= b) ? a : b;
}

int hay_perdida(Tipo destino, Tipo origen) {
    if (!tipo_valido(destino) || !tipo_valido(origen)) {
        return 0;
    }
    return (destino < origen) ? 1 : 0;
}

const char *nombre_tipo(Tipo t) {
    switch (t) {
        case TIPO_ERROR: return "error";
        case TIPO_CHAR:  return "char";
        case TIPO_INT:   return "int";
        case TIPO_FLOAT: return "float";
        default:         return "desconocido";
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Mezcla de tipos enteros y flotantes

### Salida del harness
```text
=== AUDITORIA SESION 08 - Reglas de promocion y perdida ===
Caso                               esperado:              obtenido:              resultado
[ 1] promover(CHAR,INT)                 esperado: int          obtenido: int          OK
[ 2] promover(INT,FLOAT)                esperado: float        obtenido: float        OK
[ 3] promover(FLOAT,FLOAT)              esperado: float        obtenido: float        OK
[ 4] promover(ERROR,INT)                esperado: error        obtenido: error        OK
[ 5] hay_perdida(CHAR,INT)              esperado: 1            obtenido: 1            OK
[ 6] hay_perdida(INT,CHAR)              esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion08.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> El caso borde es TIPO_ERROR porque vale 0 y una comparación directa lo trata como el tipo más angosto de modo que hay_perdida con destino ERROR y origen INT daría 1 cuando debería ser 0 y el harness no prueba ese caso lo detecté agregando una prueba extra con hay_perdida(TIPO_ERROR TIPO_INT) y lo solucioné revisando el centinela ERROR antes de comparar los rangos en las dos funciones además agregué un default en nombre_tipo para valores fuera del enum

---
**Firma digital:** [kirito2906]
