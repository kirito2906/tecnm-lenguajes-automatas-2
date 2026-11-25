# Bitácora de Requerimientos y Auditoría IA — Sesión 10
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Hito 1: Mini-Evaluador de Expresiones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Integración AST y Tipado Estático  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más me costó fue lograr que la precedencia saliera bien separando expr termino y primaria para que la multiplicación y la división se resolvieran antes que la suma y la resta también tuve que cuidar que el error se propagara hacia arriba y que las funciones dejaran de seguir leyendo en cuanto algún nivel marcaba error además de distinguir el error 1 de división entre cero del error 2 de sintaxis y de revisar que el paréntesis de cierre existiera

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Contrato formal de Frontend Semántico |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Trabajo en C99 con GCC y la cabecera api_sesion10.h que declara long evaluar_expresion(const char *fuente int *error)
Rol: Actúa como ingeniero de software de sistemas y compiladores
Especificación: Implementa evaluar_expresion como un analizador descendente recursivo que lea enteros los operadores + - * / paréntesis y espacios respetando la precedencia y sin variables ni menos unario usa error=1 para división entre cero y error=2 para sintaxis inválida y si hay error no sigas calculando
Output: Entrega solo el código modular en C sin main con la misma firma del encabezado y un análisis breve de complejidad
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion10_c.c - Fase 2: El Cientifico
 * Propuesta de la IA con la misma firma de api_sesion10.h
 */
#include <ctype.h>
#include <stdio.h>
#include "api_sesion10.h"

typedef struct {
    const char *s;
    int error;
} Lector;

static void espacios(Lector *l) {
    while (*l->s == ' ') l->s++;
}

static long suma(Lector *l);

static long factor(Lector *l) {
    long v = 0;
    espacios(l);
    if (*l->s == '(') {
        l->s++;
        v = suma(l);
        if (l->error) return 0;
        espacios(l);
        if (*l->s != ')') {
            l->error = 2;
            return 0;
        }
        l->s++;
        return v;
    }
    if (!isdigit((unsigned char)*l->s)) {
        l->error = 2;
        return 0;
    }
    while (isdigit((unsigned char)*l->s)) {
        v = v * 10 + (*l->s - '0');
        l->s++;
    }
    return v;
}

static long producto(Lector *l) {
    long v = factor(l);
    if (l->error) return 0;
    for (;;) {
        char op;
        long d;
        espacios(l);
        op = *l->s;
        if (op != '*' && op != '/') break;
        l->s++;
        d = factor(l);
        if (l->error) return 0;
        if (op == '/' && d == 0) {
            l->error = 1;
            return 0;
        }
        v = (op == '*') ? v * d : v / d;
    }
    return v;
}

static long suma(Lector *l) {
    long v = producto(l);
    if (l->error) return 0;
    for (;;) {
        char op;
        long d;
        espacios(l);
        op = *l->s;
        if (op != '+' && op != '-') break;
        l->s++;
        d = producto(l);
        if (l->error) return 0;
        v = (op == '+') ? v + d : v - d;
    }
    return v;
}

long evaluar_expresion(const char *fuente, int *error) {
    Lector l;
    long v;
    int local = 0;

    if (error == NULL) error = &local;
    *error = 0;
    if (fuente == NULL) {
        *error = 2;
        return 0;
    }

    l.s = fuente;
    l.error = 0;
    v = suma(&l);
    espacios(&l);
    if (l.error == 0 && *l.s != '\0') l.error = 2;

    *error = l.error;
    return l.error ? 0 : v;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Batería de 10 expresiones mixtas complejas

### Salida del harness
```text
=== AUDITORIA SESION 10 - Mini-evaluador de expresiones (Hito 1) ===
Caso                               esperado:              obtenido:              resultado
[ 1] "2+3*4"                            esperado: 14           obtenido: 14           OK
[ 2] "(2+3)*4"                          esperado: 20           obtenido: 20           OK
[ 3] "10/0" -> error 1                  esperado: 1            obtenido: 1            OK
[ 4] "2+" -> error 2                    esperado: 2            obtenido: 2            OK
[ 5] "  7 "                             esperado: 7            obtenido: 7            OK
[ 6] "5-10"                             esperado: -5           obtenido: -5           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion10.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA omitió el desbordamiento de un número muy grande porque acumula los dígitos en un long sin revisar el límite así que una expresión como 99999999999999999999 se desborda y regresa un valor basura sin marcar ningún error lo detecté agregando una prueba extra con ese número y viendo que no salía error 2 lo solucioné revisando antes de acumular cada dígito que el número cupiera en un long y marcando error 2 si no cabe

---
**Firma digital:** [kirito2906]
