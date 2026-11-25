# Bitácora de Requerimientos y Auditoría IA — Sesión 19

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Estructuras (struct) y Offsets de Miembros
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Calcular los offsets de los campos y el tamaño total de una estructura aplicando alineación y padding.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Las restricciones que tuve que resolver al codificar a mano fueron:
>
> - **Identificación de tipos:** reconocer el tamaño y la alineación de cada tipo de dato, como char, short, int, float y double.
> - **Alineación de campos:** antes de asignar una posición a cada campo, se debe ajustar el offset al múltiplo correspondiente al tamaño del tipo.
> - **Padding:** algunos espacios de memoria quedan libres entre los campos para respetar la alineación.
> - **Tamaño total:** al terminar de recorrer los campos, se debe aplicar el padding final tomando como referencia el campo de mayor tamaño.
> - **Campos inexistentes:** si se busca un miembro que no está dentro de la estructura, la función debe devolver `-1`.
> - **Estructuras vacías:** cuando no hay campos, el tamaño total debe ser `0`.
> - **Punto en que me atoré:** tuve que tener cuidado al calcular los espacios de relleno entre los campos, porque no todos los tipos ocupan el mismo tamaño ni necesitan la misma alineación.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                               |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | Programación en C11 con GCC, utilizando la estructura `Campo` definida en `api_sesion19.h`.                                      |
| **Rol (R)**            | Ingeniero de software especializado en programación de sistemas y manejo de memoria.                                             |
| **Especificación (E)** | Implementar funciones para calcular el offset de un miembro y el tamaño total de una estructura, aplicando alineación y padding. |
| **Output (O)**         | Código modular en C que respete las firmas de `api_sesion19.h`, sin incluir `main()`, y que compile sin advertencias.            |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy trabajando en C11 con GCC y tengo una
cabecera llamada api_sesion19.h que define la estructura
Campo y las funciones necesarias para calcular offsets
y tamaños de estructuras.

Rol: Eres un ingeniero de software especializado en
programación de sistemas y manejo de memoria.

Especificación: Implementa las funciones:

int offset_campo(const Campo *campos, int total,
                 const char *nombre);
int tamano_struct(const Campo *campos, int total);

- Cada campo debe alinearse a su propio ancho antes
  de asignarle un offset.
- El tamaño total debe redondearse al múltiplo del
  campo de mayor tamaño.
- Si el campo solicitado no existe, devuelve -1.
- Si la lista es NULL o existe un tipo desconocido,
  devuelve -1.
- Si la estructura no tiene campos, devuelve 0.
- Utiliza una tabla para reconocer los tipos y sus
  respectivos tamaños.
- Respeta las firmas exactas de api_sesion19.h.
- No incluyas main().
- El código debe compilar con -std=c11
  -Wall -Wextra -Werror.

Output: Código completo del archivo .c y un breve
análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion19_c.c - Fase 2: El Cientifico */
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

    if (campos == NULL) return -1;

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

    if (nombre == NULL || total <= 0)
        return -1;

    if (recorrer(campos, total, nombre, &off, &tam) != 0)
        return -1;

    return off;
}

int tamano_struct(const Campo *campos, int total) {
    int off, tam;

    if (campos == NULL) return -1;
    if (total <= 0) return 0;

    if (recorrer(campos, total, NULL, &off, &tam) != 0)
        return -1;

    return tam;
}
```

**Análisis de complejidad:**

- `ancho_de()`: O(1), porque recorre una tabla de tamaño fijo con los tipos permitidos.
- `recorrer()`: O(n), porque recorre una vez todos los campos de la estructura.
- `offset_campo()`: O(n), porque necesita recorrer los campos para encontrar el miembro solicitado.
- `tamano_struct()`: O(n), porque calcula los offsets y el tamaño total recorriendo todos los campos.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Se comprobaron los offsets de los miembros, el tamaño total de las estructuras, el padding, la búsqueda de campos inexistentes y las estructuras sin campos.

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

- [x] Se comprobaron los casos base y los límites de las estructuras.
- [x] Las seis pruebas se ejecutaron sin errores ni *Crash*.
- [x] No se realizó una auditoría específica de memoria.
- [x] La complejidad teórica coincide con la implementación.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó las seis pruebas, pero al revisar el código encontré algunos casos que no se probaron:
>
> - **Lista NULL:** no se realizó una prueba específica para comprobar que las funciones rechacen una lista de campos NULL.
> - **Tipo desconocido:** no se comprobó qué sucede cuando un campo tiene un tipo que no está registrado en la tabla.
> - **Nombre NULL:** no se probó qué sucede cuando se busca un campo utilizando un nombre NULL.
> - **Cantidad negativa de campos:** no se comprobó cómo se comportan las funciones cuando reciben un total negativo.
> - **Cómo lo detecté:** revisando las condiciones del código de la IA y comparándolas con los seis casos que ejecutó el harness. Así identifiqué que todavía se pueden agregar pruebas para verificar esas entradas.

---

**Firma digital:** `kirito2906`
