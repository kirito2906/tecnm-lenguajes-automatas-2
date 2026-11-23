# Bitácora de Requerimientos y Auditoría IA — Sesión 07
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Evaluación de Expresiones Aritméticas  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Evaluador recursivo de operaciones  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más me costó fue acordarme de revisar el divisor antes de hacer la división y lograr que el error se pasara hacia arriba sin seguir calculando los padres también tuve que cuidar el caso del árbol NULL para que el programa no se cayera

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Manejo estricto de división entre cero |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Trabajo en C99 con GCC y la cabecera api_sesion07.h que define ASTNode con tipo valor op izq y der
Rol: Actúa como ingeniero de software de sistemas y compiladores
Especificación: Implementa int evaluar(ASTNode *n, int *error) de forma recursiva con error=1 si hay división o módulo entre cero y error=2 si el nodo es NULL o inválido no ejecutes la división antes de revisar el divisor y no recalcules los padres si un hijo ya marcó error
Output: Entrega solo el código modular en C sin main y un análisis breve de complejidad
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion07_c.c - Fase 2: El Cientifico
 * Propuesta de la IA con la misma firma de api_sesion07.h
 */
#include <stdio.h>
#include "api_sesion07.h"

int evaluar(ASTNode *n, int *error) {
    int a, b;

    if (n == NULL) {
        *error = 2;
        return 0;
    }
    if (n->tipo == NODO_NUM) {
        return n->valor;
    }
    if (n->tipo != NODO_BINOP) {
        *error = 2;
        return 0;
    }

    a = evaluar(n->izq, error);
    if (*error) return 0;
    b = evaluar(n->der, error);
    if (*error) return 0;

    if ((n->op == '/' || n->op == '%') && b == 0) {
        *error = 1;
        return 0;
    }

    switch (n->op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return a / b;
        case '%': return a % b;
        default:
            *error = 2;
            return 0;
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Expresiones complejas y división por 0

### Salida del harness
```text
=== AUDITORIA SESION 07 - Evaluador recursivo con deteccion de errores ===
Caso                               esperado:              obtenido:              resultado
[ 1] (2+3)*4                            esperado: 20           obtenido: 20           OK
[ 2] 7/0 -> error 1                     esperado: 1            obtenido: 1            OK
[ 3] 7%0 -> error 1                     esperado: 1            obtenido: 1            OK
[ 4] arbol NULL -> error 2              esperado: 2            obtenido: 2            OK
[ 5] 10-2-3                             esperado: 5            obtenido: 5            OK
[ 6] (8/2)+1                            esperado: 5            obtenido: 5            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion07.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA omitió el desbordamiento con INT_MIN porque solo revisó que el divisor no fuera cero pero INT_MIN dividido entre -1 y INT_MIN módulo -1 también hacen que el programa se caiga con una excepción de punto flotante lo detecté agregando un caso extra al harness con un árbol INT_MIN / -1 y viendo que el programa terminaba con crash en lugar de marcar error lo solucioné agregando una comprobación antes de dividir que marca error cuando el divisor es -1 y el dividendo es INT_MIN

---
**Firma digital:** [kirito2906]
