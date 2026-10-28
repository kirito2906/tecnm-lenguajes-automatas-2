# Bitácora de Requerimientos y Auditoría IA — Sesión 02
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Gestión en GitHub Web y Nodos Dinámicos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** María Jesús Fuentes Valdez  
**Matrícula:** 24531315  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lista enlazada de tokens en Heap  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Me costó trabajo entender que cada nodo tiene que vivir en el heap con malloc porque si lo declaraba normal se perdía al salir de la función También se me complicó agregar al final de la lista ya que había que recorrerla hasta el último nodo y no perder la cabeza Al liberar tuve que guardar el siguiente nodo antes de hacer free para no usar memoria ya liberada y además tenía que copiar el lexema sin pasarme de los 16 caracteres del arreglo

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
Contexto: Trabajo en C99 con GCC y las banderas -Wall -Wextra -Werror sin bibliotecas no estándar Tengo la estructura NodoToken con un arreglo lexema de 16 caracteres y un puntero siguiente
Rol: Eres un ingeniero de software de sistemas y compiladores
Especificación: Escribe las funciones NodoToken *agregar_token(NodoToken *cabeza const char *lexema) int contar_tokens(NodoToken *cabeza) y void liberar_lista(NodoToken *cabeza) usando memoria dinámica Cada nodo se crea con malloc y el siguiente del último nodo debe ser NULL agregar_token regresa la cabeza de la lista y si estaba vacía regresa el nuevo nodo contar_tokens(NULL) regresa 0 y liberar_lista(NULL) no debe fallar Valida que lexema no sea NULL y que malloc no regrese NULL Sin main()
Output: Solo código modular con las firmas exactas y el análisis de complejidad de cada función
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
[Pega aquí la salida real de tu celda del harness]
RESULTADO: 6/6 pruebas superadas
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No se detectaron accesos fuera de límites ni *Memory Leaks* en las pruebas.
* [x] La complejidad teórica coincide con la implementada: agregar_token O(n) contar_tokens O(n) liberar_lista O(n).

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> En mi primera versión del prompt no pedí validar un lexema NULL ni un malloc que fallara y por eso la respuesta no los tenía Tampoco había considerado lexemas de más de 15 caracteres que se pasarían del arreglo de 16 Lo noté al revisar el código y con los casos 1 5 y 6 del harness Lo arreglé pidiendo esas validaciones en el prompt y usando strncpy con el cierre '\0' al final

---
**Firma digital:** Mary-X
