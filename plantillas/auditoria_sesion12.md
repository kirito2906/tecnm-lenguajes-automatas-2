# Bitácora de Requerimientos y Auditoría IA — Sesión 12
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Atributos de Símbolos y Memoria  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Estructura de registro de símbolos  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo más difícil fue sacar la fórmula para redondear el cursor al siguiente múltiplo del ancho del tipo porque no basta con sumar tamaños y tuve que usar cursor más ancho menos uno dividido entre ancho por ancho también tuve que acordarme de que la función guarda el offset alineado en el registro pero devuelve el cursor del siguiente que es el offset más el ancho y validar el tipo desconocido antes de calcular para no dividir entre un ancho inválido

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Cálculo de desplazamientos y alineación |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy construyendo la tabla de símbolos de un compilador en C11. La estructura es Simbolo con const char *nombre, const char *tipo e int offset, declarada en api_sesion12.h.
Rol: Actúa como ingeniero de software de sistemas y compiladores.
Especificación: Implementa int ancho_de_tipo(const char *tipo) con char=1, short=2, int=4, float=4, double=8 y puntero=8, y cualquier otro tipo devuelve -1. Implementa también int asignar_offset(Simbolo *simbolo, int cursor), que alinea el cursor al múltiplo del ancho del tipo, guarda el offset en el registro y devuelve el cursor del siguiente símbolo. Debe devolver -1 si el registro es NULL, el cursor es negativo o el tipo es desconocido. El cursor nunca retrocede. Debe compilar con -Wall -Wextra -Werror y no debe tener main().
Output: Solo código C modular con las firmas idénticas a api_sesion12.h y un análisis breve de la complejidad.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion12.h"
#include <string.h>

int ancho_de_tipo(const char *tipo) {
    if (strcmp(tipo, "char") == 0) return 1;
    if (strcmp(tipo, "short") == 0) return 2;
    if (strcmp(tipo, "int") == 0) return 4;
    if (strcmp(tipo, "float") == 0) return 4;
    if (strcmp(tipo, "double") == 0) return 8;
    if (strcmp(tipo, "puntero") == 0) return 8;
    return -1;
}

int asignar_offset(Simbolo *simbolo, int cursor) {
    if (!simbolo || cursor < 0) return -1;
    int ancho = ancho_de_tipo(simbolo->tipo);
    int offset = ((cursor + ancho - 1) / ancho) * ancho;
    simbolo->offset = offset;
    return offset + ancho;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Alineación de tipos y tamaños en bytes

### Salida del harness
```text
=== AUDITORIA SESION 12 - Registro de simbolo y offsets alineados ===
Caso                               esperado:              obtenido:              resultado
[ 1] ancho_de_tipo("int")               esperado: 4            obtenido: 4            OK
[ 2] ancho_de_tipo("double")            esperado: 8            obtenido: 8            OK
[ 3] int en cursor 0                    esperado: 4            obtenido: 4            OK
[ 4] char e int: offset de b            esperado: 4            obtenido: 4            OK
[ 5] double desde cursor 4              esperado: 8            obtenido: 8            OK
[ 6] registro NULL                      esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion12.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA pasó los 6 casos pero no revisó si ancho_de_tipo devolvía -1 antes de calcular el offset así que con un tipo desconocido como long hace la cuenta con ancho -1 escribe un offset basura en el registro y devuelve un cursor que retrocede en lugar de -1 con cursor 8 devolvió 5 además strcmp recibe el tipo sin revisar si es NULL y el programa se cae el harness no prueba ninguno de esos casos por eso salió en verde lo detecté probando un símbolo con tipo long y otro con tipo NULL y lo solucioné validando que el tipo no sea NULL y que el ancho sea distinto de -1 antes de alinear

---
**Firma digital:** [kirito2906]
