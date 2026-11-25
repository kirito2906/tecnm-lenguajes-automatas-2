# Bitácora de Requerimientos y Auditoría IA — Sesión 05
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Recorridos del AST y Notación Polaca  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Impresión en Postorden / RPN  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo más difícil fue escribir los tokens en el buffer sin imprimir con printf y sin pasarme de la capacidad además de que no quedara un espacio sobrando al final ni al inicio Lo resolví llevando un contador de longitud y revisando antes de copiar cada token que cupiera dentro de cap-1 caracteres para dejar lugar al terminador y solo pongo el espacio separador cuando ya hay algo escrito en el buffer También tuve que acordarme de poner buf[0] en '\0' desde el inicio para que un árbol nulo diera cadena vacía

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Invariantes de recorrido recursivo |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: C con GCC compilando con -Wall -Wextra -Werror y usando el archivo api_sesion05.h con la estructura ASTNode (tipo valor op izq der)
Rol: Eres un ingeniero de software de sistemas y compiladores
Especificación: Implementa void postorden(ASTNode *n, char *buf, int cap) con la firma exacta del contrato El recorrido debe ser izquierdo derecho raíz y escribir la notación polaca inversa en el buffer con los tokens separados por un solo espacio y sin espacio al final Sin usar printf y sin escribir más de cap-1 caracteres más el terminador Un árbol nulo debe dar cadena vacía y no debe tener main()
Output: Solo el código del archivo ia_sesion05_c.c de forma modular y un breve análisis de complejidad
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion05_c.c - Fase 2: El Cientifico */
#include "api_sesion05.h"
#include <stdio.h>
#include <string.h>

static int emitir(ASTNode *n, char *buf, int cap, int len) {
    char tok[16];
    int largo;
    int necesita;

    if (n == NULL) {
        return len;
    }
    len = emitir(n->izq, buf, cap, len);
    len = emitir(n->der, buf, cap, len);

    if (n->tipo == NODO_NUM) {
        snprintf(tok, sizeof(tok), "%d", n->valor);
    } else {
        tok[0] = n->op;
        tok[1] = '\0';
    }
    largo = (int)strlen(tok);
    necesita = (len > 0) ? largo + 1 : largo;
    if (len + necesita > cap - 1) {
        return len;
    }
    if (len > 0) {
        buf[len] = ' ';
        len++;
    }
    memcpy(buf + len, tok, (size_t)largo);
    len += largo;
    buf[len] = '\0';
    return len;
}

void postorden(ASTNode *n, char *buf, int cap) {
    if (buf == NULL || cap <= 0) {
        return;
    }
    buf[0] = '\0';
    emitir(n, buf, cap, 0);
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Validación contra desbordamiento de pila

### Salida del harness
```text
=== AUDITORIA SESION 05 - Recorrido postorden y RPN ===
Caso                               esperado:              obtenido:              resultado
[ 1] hoja 42                            esperado: 42           obtenido: 42           OK
[ 2] 3+(5*2)                            esperado: 3 5 2 * +    obtenido: 3 5 2 * +    OK
[ 3] arbol NULL                         esperado:              obtenido:              OK
[ 4] (1+2)*(3+4)
     esperado: 1 2 + 3 4 + *
     obtenido: 1 2 + 3 4 + *
     -> OK
[ 5] 8-3                                esperado: 8 3 -        obtenido: 8 3 -        OK

RESULTADO: 5/5 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion05.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> El harness solo prueba buffers grandes y la IA no contempló qué pasa cuando el buffer es muy chico Cuando un token no cabe la función solo lo salta con un return y el recorrido sigue así que un token más corto que viene después sí puede entrar y la salida queda incompleta pero con apariencia válida por ejemplo un RPN al que le falta un número pero conserva el operador Lo detecté al leer el código con calma y probar a mano con un cap muy pequeño y la solución es dejar de escribir por completo en cuanto un token no cabe para que el resultado sea un prefijo exacto del RPN completo o dejar la cadena vacía

---
**Firma digital:** [kirito2906]
