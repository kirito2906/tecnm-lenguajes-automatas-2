# Bitácora de Requerimientos y Auditoría IA — Sesión 19
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Estructuras (struct) y Offsets de Miembros  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Cálculo de offsets y alineación de campos en estructuras.  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Lo que más se me complicó fue entender cómo funciona el **padding**, porque no todos los campos pueden colocarse uno seguido del otro sin dejar espacios en memoria. Por ejemplo, en `{char a; int b;}`, el campo `char` comienza en la posición 0, pero el `int` debe comenzar en la posición 4 porque necesita una alineación de 4 bytes. Para resolverlo se debe ajustar la posición antes de colocar cada campo. También hay que considerar el tamaño final de la estructura, ya que se redondea utilizando la alineación del campo más grande. Por eso `{double a; char b;}` ocupa 16 bytes y no solamente 9. Otra dificultad fue identificar los tipos de datos mediante una tabla y controlar los casos en los que se recibe un tipo desconocido, una lista `NULL` o un miembro que no existe, ya que deben regresar -1. Cuando la estructura no tiene campos, su tamaño debe ser 0.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 con GCC, utilizando la cabecera `api_sesion19.h` y la estructura `Campo`. |
| **Rol (R)** | Ingeniero de software especializado en programación de sistemas y manejo de memoria. |
| **Especificación (E)** | Cálculo de offsets de miembros y tamaño de estructuras aplicando alineación natural y padding. |
| **Output (O)** | Código modular en C, respetando las firmas originales y acompañado de un análisis de complejidad. |

### 2.2 Prompt Estructurado
```text
CONTEXTO: C11 con GCC (-Wall -Wextra -Werror), x86-64,
utilizando la cabecera api_sesion19.h, que define:

typedef struct {
    const char *nombre;
    const char *tipo;
} Campo;

int offset_campo(const Campo *campos, int total,
                 const char *nombre);
int tamano_struct(const Campo *campos, int total);

ROL: Ingeniero de software especializado en sistemas
y organización de memoria.

ESPECIFICACIÓN: Implementar el cálculo de offsets
de miembros mediante alineación natural.

- Tipos: char 1, unsigned char 1, short 2,
  unsigned short 2, int 4, unsigned int 4,
  float 4, long 8, unsigned long 8,
  long long 8, double 8 y punteros 8.
- Cada campo debe alinearse según su propio ancho.
- El tamaño final debe ajustarse al campo de mayor
  alineación.
- Los campos inexistentes deben devolver -1.
- Una lista NULL o un tipo desconocido deben devolver -1.
- Una estructura sin campos debe medir 0.
- Los nombres NULL no deben provocar accesos inválidos.
- Las cantidades negativas deben rechazarse.
- No modificar las firmas ni incluir main().

OUTPUT: Código C modular y análisis breve
de complejidad temporal y espacial.
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion19.h"
#include <string.h>
#include <stddef.h>

typedef struct {
    const char *tipo;
    int ancho;
} TipoInfo;

static const TipoInfo TABLA[] = {
    {"char", 1}, {"unsigned char", 1},
    {"short", 2}, {"unsigned short", 2},
    {"int", 4}, {"unsigned int", 4}, {"float", 4},
    {"long", 8}, {"unsigned long", 8},
    {"long long", 8}, {"double", 8},
    {"pointer", 8}, {"char *", 8}, {"void *", 8}
};

static int ancho_de(const char *tipo) {
    if (tipo == NULL) return -1;

    for (size_t i = 0; i < sizeof(TABLA) / sizeof(TABLA[0]); i++) {
        if (strcmp(tipo, TABLA[i].tipo) == 0)
            return TABLA[i].ancho;
    }

    return -1;
}

static int recorrer(const Campo *campos, int total,
                    const char *nombre, int *offset, int *tamano) {
    int pos = 0;
    int mayor = 1;

    *offset = -1;
    *tamano = 0;

    if (campos == NULL || total < 0) return -1;

    for (int i = 0; i < total; i++) {
        int w = ancho_de(campos[i].tipo);

        if (w < 0) return -1;

        pos = ((pos + w - 1) / w) * w;

        if (*offset < 0 && nombre != NULL &&
            campos[i].nombre != NULL &&
            strcmp(campos[i].nombre, nombre) == 0) {
            *offset = pos;
        }

        pos += w;

        if (w > mayor) mayor = w;
    }

    *tamano = ((pos + mayor - 1) / mayor) * mayor;

    return 0;
}

int offset_campo(const Campo *campos, int total,
                 const char *nombre) {
    int off, tam;

    if (campos == NULL || nombre == NULL || total <= 0)
        return -1;

    if (recorrer(campos, total, nombre, &off, &tam) != 0)
        return -1;

    return off;
}

int tamano_struct(const Campo *campos, int total) {
    int off, tam;

    if (campos == NULL || total < 0) return -1;
    if (total == 0) return 0;

    if (recorrer(campos, total, NULL, &off, &tam) != 0)
        return -1;

    return tam;
}
```

**Análisis de complejidad:**

- `ancho_de()`: O(1), porque consulta una tabla fija de tipos.
- `recorrer()`: O(n), debido a que revisa cada campo para calcular su posición.
- `offset_campo()`: O(n), porque necesita recorrer los miembros hasta localizar el solicitado.
- `tamano_struct()`: O(n), ya que calcula el tamaño total mediante un recorrido.

El espacio adicional es O(1), porque solamente utiliza variables auxiliares y no reserva memoria dinámica.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Cálculo de offsets, alineación de campos, padding y búsqueda de miembros inexistentes.

### Salida del harness
```text
=== AUDITORIA SESION 19 - Offsets de miembros y tamano de struct ===
Caso                               esperado:              obtenido:              resultado
[ 1] struct char e int: b               esperado: 4            obtenido: 4            OK
[ 2] struct de tres campos: c           esperado: 8            obtenido: 8            OK
[ 3] tamano total con padding           esperado: 12           obtenido: 12           OK
[ 4] double seguido de char             esperado: 16           obtenido: 16           OK
[ 5] miembro inexistente                esperado: -1           obtenido: -1           OK
[ 6] struct sin campos                  esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion19.md
```

* [x] Los casos principales de alineación y padding fueron superados.
* [x] No se presentaron errores durante las seis pruebas del harness.
* [x] Se contemplaron validaciones para entradas incorrectas en la revisión del código.
* [x] La complejidad teórica corresponde con la implementación.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar el código encontré que todavía era necesario comprobar algunas situaciones que no aparecieron en las seis pruebas del harness. Una de ellas era recibir una cantidad negativa de campos, porque en ese caso la función podía devolver 0 como si se tratara de una estructura vacía. También revisé el manejo de nombres NULL, ya que utilizar `strcmp` sin comprobar primero el nombre puede provocar un error durante la ejecución. En mi revisión mantuve la condición `campos[i].nombre != NULL` antes de realizar la comparación. De esta manera, un campo sin nombre puede seguir ocupando espacio dentro de la estructura, pero no se utiliza para buscar un miembro. Además, agregué la validación de `total < 0` para evitar que una cantidad inválida sea considerada como una estructura sin campos. Los tipos desconocidos y las listas NULL también deben rechazarse con un resultado de -1. La complejidad se mantiene en O(n) en tiempo y O(1) en espacio adicional.

---
**Firma digital:** [kirito2906]
