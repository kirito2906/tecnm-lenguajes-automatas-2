# Bitácora de Requerimientos y Auditoría IA — Sesión 15

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Bloques Anidados y Ciclo de Vida  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Operaciones Push y Pop de ámbito

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Las restricciones que tuve que resolver al codificar a mano fueron:
> - **Enlace con el padre:** `push_ambito()` debe crear un nuevo ámbito y enlazarlo con el ámbito actual mediante el puntero `padre`, conservando la relación entre los bloques.
> - **Asignación de memoria:** al crear un ámbito nuevo se necesita reservar memoria con `malloc()` y comprobar si la asignación fue exitosa antes de utilizarla.
> - **Liberación de memoria:** `pop_ambito()` debe guardar el padre antes de liberar el ámbito actual, para poder regresar al nivel anterior sin perder la referencia.
> - **Protección de la raíz:** si el ámbito actual es la raíz, `pop_ambito()` debe devolver `NULL` sin liberar la raíz, porque no fue creada por la función `push_ambito()`.
> - **Entradas inválidas:** si el ámbito actual o el nombre recibido son `NULL`, `push_ambito()` devuelve `NULL`; en `pop_ambito()`, si el ámbito es `NULL` o es la raíz, devuelve `NULL`.
> - **Punto en que me atoré:** [completa según tu experiencia real].

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Liberación de memoria al cerrar bloque |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy en C (compilado con gcc -std=c11 -Wall -Wextra -Werror),
sin bibliotecas no estándar. Tengo esta cabecera api_sesion15.h:

  typedef struct Ambito {
      const char *nombre;
      struct Ambito *padre;
  } Ambito;

Rol: Eres un ingeniero de software de sistemas y compiladores.

Especificación: Implementa
  Ambito *push_ambito(Ambito *actual, const char *nombre);
  Ambito *pop_ambito(Ambito *actual);

- push_ambito() reserva memoria para un nuevo ámbito, conserva el nombre
  recibido y enlaza el nuevo ámbito con el actual como padre.
- push_ambito() devuelve NULL si el ámbito actual o el nombre son NULL
  o si falla la asignación de memoria.
- pop_ambito() guarda el padre, libera el ámbito actual y devuelve el padre.
- pop_ambito() devuelve NULL sobre la raíz y no libera memoria que no
  le pertenece.
- Cada push se empareja con un pop para no dejar ámbitos colgando.
- Respeta las firmas exactas de la cabecera api_sesion15.h.

Output: Solo el código modular del archivo .c, sin main(), y un breve
análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion15_c.c - Fase 2: El Cientifico
 * Version con calloc y comentarios de propiedad de memoria.
 */
#include "api_sesion15.h"
#include <stdlib.h>

Ambito *push_ambito(Ambito *actual, const char *nombre) {
    if (actual == NULL || nombre == NULL)
        return NULL;

    Ambito *nuevo = calloc(1, sizeof *nuevo);
    if (nuevo == NULL)
        return NULL;

    nuevo->nombre = nombre;
    nuevo->padre = actual;
    return nuevo;
}

Ambito *pop_ambito(Ambito *actual) {
    /* La raiz (padre == NULL) no fue creada por push: no se libera. */
    if (actual == NULL || actual->padre == NULL)
        return NULL;

    Ambito *padre = actual->padre;
    free(actual);
    return padre;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Aislamiento de variables fuera de bloque

### Salida del harness

```text
=== AUDITORIA SESION 15 - Push y pop de ambitos ===
Caso                               esperado:              obtenido:              resultado
[ 1] nombre del ambito nuevo            esperado: if           obtenido: if           OK
[ 2] profundidad con dos push           esperado: 3            obtenido: 3            OK
[ 3] pop devuelve el padre              esperado: 1            obtenido: 1            OK
[ 4] pop sobre la raiz                  esperado: 1            obtenido: 1            OK
[ 5] push con padre NULL                esperado: 1            obtenido: 1            OK
[ 6] profundidad tras pop               esperado: 2            obtenido: 2            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion15.md
```

- [x] Caso base y límites superados sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó 6/6 con la versión de la IA, pero al revisar el código encontré algunos detalles que se deben considerar y que las pruebas no contemplan completamente:
> - **Nombre sin copia:** `push_ambito()` guarda el puntero del nombre directamente en la estructura y no una copia de la cadena. Esto significa que la memoria original debe seguir siendo válida mientras se utilice el ámbito.
> - **Liberación de memoria:** `pop_ambito()` libera el ámbito actual con `free()`, por lo que solo debe utilizarse sobre ámbitos que hayan sido creados dinámicamente y que pertenezcan a esta cadena.
> - **Pop sobre la raíz:** la función devuelve `NULL` cuando recibe la raíz, lo cual evita liberarla. Este comportamiento debe respetarse para no perder ni liberar memoria que no le pertenece.
> - **Cómo lo detecté:** revisando el código de la IA y comparando la forma en que reserva y libera memoria con los criterios de aceptación del ejercicio.

---

**Firma digital:** [kirito2906]
