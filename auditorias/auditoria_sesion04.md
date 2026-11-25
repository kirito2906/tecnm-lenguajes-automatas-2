# Bitácora de Requerimientos y Auditoría IA — Sesión 04
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Anatomía de un Árbol Sintáctico (AST)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Estructura de nodo binario (ASTNode)  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más me costó fue acordarme de que cada nodo se tiene que reservar en el heap con malloc y que hay que incluir stdlib.h porque sin ese encabezado el compilador marca error al usar -Werror
> También tuve que cuidar el orden de los hijos para que el izquierdo y el derecho quedaran bien enlazados y dejar en NULL los hijos de los nodos numéricos para que no quedaran valores basura
> En evaluar necesité revisar primero que el nodo no sea NULL para devolver -1 y calcular los dos hijos antes de aplicar el operador

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Gramática E -> E + T | T con tipos de nodo |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy programando en C11 y compilo con gcc -Wall -Wextra -Werror
El archivo no debe tener main() porque el main es de un harness externo
Debo respetar la cabecera api_sesion04.h que define ASTNode y TipoNodo

Rol: Actúa como programador de C especializado en estructuras dinámicas y árboles

Especificación:
- ASTNode *crear_numero(int v) reserva un nodo NODO_NUM en el heap con el valor v
- ASTNode *crear_binario(char op, ASTNode *izq, ASTNode *der) reserva un nodo NODO_BINOP en el heap y respeta el orden izquierdo y derecho
- int evaluar(ASTNode *n) evalúa de forma recursiva los operadores + - y *
- evaluar aplica el operador después de evaluar ambos hijos
- evaluar(NULL) devuelve -1 y no debe caerse

Output: Solo el código en C con las tres funciones y con la misma firma de la cabecera
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion04.h"
#include <stdlib.h>

static ASTNode *nuevo_nodo(TipoNodo tipo) {
    ASTNode *n = (ASTNode *)calloc(1, sizeof(ASTNode));
    if (n != NULL) {
        n->tipo = tipo;
    }
    return n;
}

ASTNode *crear_numero(int v) {
    ASTNode *n = nuevo_nodo(NODO_NUM);
    if (n == NULL) {
        return NULL;
    }
    n->valor = v;
    return n;
}

ASTNode *crear_binario(char op, ASTNode *izq, ASTNode *der) {
    ASTNode *n = nuevo_nodo(NODO_BINOP);
    if (n == NULL) {
        return NULL;
    }
    n->op = op;
    n->izq = izq;
    n->der = der;
    return n;
}

int evaluar(ASTNode *n) {
    int a;
    int b;

    if (n == NULL) {
        return -1;
    }
    if (n->tipo == NODO_NUM) {
        return n->valor;
    }
    a = evaluar(n->izq);
    b = evaluar(n->der);
    if (n->op == '+') {
        return a + b;
    }
    if (n->op == '-') {
        return a - b;
    }
    if (n->op == '*') {
        return a * b;
    }
    return -1;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Árbol vacío y evaluación de nodo raíz

### Salida del harness
```text
=== AUDITORIA SESION 04 - Nodo binario de AST ===
Caso                                 esperado:              obtenido:              resultado
[ 1] evaluar(nodo 42)                esperado: 42           obtenido: 42           OK
[ 2] evaluar(3+5*2)                  esperado: 13           obtenido: 13           OK
[ 3] hijo izquierdo de (* 5 2)       esperado: 5            obtenido: 5            OK
[ 4] operador guardado               esperado: *            obtenido: *            OK
[ 5] evaluar(NULL)                   esperado: -1           obtenido: -1           OK
[ 6] evaluar(10-4)                   esperado: 6            obtenido: 6            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion04.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA no omitió ningún caso borde porque en el contrato le pedí de forma explícita que evaluar(NULL) devuelva -1 y que se respete el orden de los hijos y su código lo resolvió igual que mi versión
> Usó calloc en lugar de malloc así que todos los campos del nodo empiezan en cero y no quedan valores basura en op izq o der
> Lo detecté ejecutando el harness con las dos versiones y comparando que las 6 líneas salieran en OK además de revisar que ambas validen el NULL de la reserva y evalúen los dos hijos antes de aplicar el operador
> La complejidad es O(n) en las dos porque evaluar visita cada nodo una sola vez

---
**Firma digital:** kirito2906
