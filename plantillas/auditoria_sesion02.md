# Bitácora de Requerimientos y Auditoría IA — Sesión 02
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Gestión en GitHub Web y Nodos Dinámicos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lista enlazada de tokens en Heap  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más se me complicó fue no perder el puntero al siguiente nodo al liberar la lista porque si hacía free primero ya no podía seguir recorriendo así que guardé el siguiente antes de liberar También tuve que cuidar que el lexema cupiera en el arreglo de 16 caracteres y que la cabeza cambiara solo cuando la lista estaba vacía Otro detalle fue recordar que cada nodo se reserva con malloc y que el siguiente del último nodo debe quedar en NULL

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Gestión de memoria dinámica C99/Rust |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy programando en C99 compilado con GCC usando -Wall -Wextra -Werror y sin bibliotecas no estándar Tengo un struct NodoToken con un arreglo lexema de 16 caracteres y un puntero siguiente
Rol: Actúa como ingeniero de software de sistemas y compiladores
Especificación: Implementa NodoToken *agregar_token(NodoToken *cabeza const char *lexema) int contar_tokens(NodoToken *cabeza) y void liberar_lista(NodoToken *cabeza) con memoria dinámica en el heap Cada nodo se reserva con malloc y el siguiente del último nodo vale NULL agregar_token devuelve la cabeza y si la lista estaba vacía el nuevo nodo es la cabeza contar_tokens(NULL) devuelve 0 y liberar_lista(NULL) no debe caerse No incluyas main()
Output: Solo código modular con las firmas exactas y un análisis de complejidad de cada función
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion02.h"
#include <stdlib.h>
#include <string.h>

NodoToken *agregar_token(NodoToken *cabeza, const char *lexema) {
    if (lexema == NULL) return cabeza;
    NodoToken *nuevo = (NodoToken *)malloc(sizeof(NodoToken));
    if (nuevo == NULL) return cabeza;
    strncpy(nuevo->lexema, lexema, sizeof(nuevo->lexema) - 1);
    nuevo->lexema[sizeof(nuevo->lexema) - 1] = '\0';
    nuevo->siguiente = NULL;
    if (cabeza == NULL) return nuevo;
    NodoToken *p = cabeza;
    while (p->siguiente != NULL) p = p->siguiente;
    p->siguiente = nuevo;
    return cabeza;
}

int contar_tokens(NodoToken *cabeza) {
    int n = 0;
    for (NodoToken *p = cabeza; p != NULL; p = p->siguiente) n++;
    return n;
}

void liberar_lista(NodoToken *cabeza) {
    while (cabeza != NULL) {
        NodoToken *sig = cabeza->siguiente;
        free(cabeza);
        cabeza = sig;
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Prevención de Use-After-Free y cadenas nulas

### Salida del harness
```text
=== AUDITORIA SESION 02 - Lista enlazada de tokens en heap ===
Caso                                  esperado:           obtenido:           resultado
[ 1] agregar_token(NULL,"if")         esperado: if        obtenido: if        OK
[ 2] contar_tokens(3 tokens)          esperado: 3         obtenido: 3         OK
[ 3] orden: segundo token             esperado: dos       obtenido: dos       OK
[ 4] ultimo->siguiente == NULL        esperado: 1         obtenido: 1         OK
[ 5] contar_tokens(NULL)              esperado: 0         obtenido: 0         OK
[ 6] liberar_lista(NULL)              esperado: sin crash obtenido: sin crash OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion02.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA no validó que el lexema fuera NULL ni que malloc pudiera fallar en su primera propuesta y tampoco consideró lexemas de más de 15 caracteres que desbordarían el arreglo de 16 Lo detecté al revisar el código antes de compilar y con los casos 1 5 y 6 del harness que prueban la lista vacía y los NULL Lo solucioné agregando la revisión de NULL y copiando con strncpy dejando siempre el cierre '\0' al final

---
**Firma digital:** kirito2906
