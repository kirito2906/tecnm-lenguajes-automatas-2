# Bitácora de Requerimientos y Auditoría IA — Sesión 19

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Estructuras (struct) y Offsets de Miembros  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Cálculo de offsets y distribución de memoria dentro de estructuras.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> El principal problema que encontré fue entender cómo se acomodan los campos dentro de una estructura, especialmente por el padding y la alineación de memoria. No todos los tipos de datos pueden comenzar en cualquier posición.
>
> Por ejemplo, en una estructura `{char a; int b;}`, el primer campo ocupa la posición 0, pero el segundo no puede comenzar inmediatamente en la posición 1. Como el tipo `int` necesita una alineación de 4 bytes, su offset debe ajustarse hasta la posición 4.
>
> También tuve que considerar el espacio que se agrega al final de la estructura. Por ejemplo, cuando se tiene `{double a; char b;}`, el tamaño no se queda en 9 bytes, sino que se ajusta a 16 para mantener la alineación correspondiente.
>
> Otro aspecto importante fue identificar correctamente los tipos de datos y sus tamaños, ya que un tipo desconocido debe producir un resultado de -1. También se debe contemplar cuando la lista es NULL, cuando se busca un miembro inexistente y cuando la estructura no contiene campos.
>
> Lo que más se me dificultó fue comprender que el padding no solamente aparece entre los campos, sino que también puede ser necesario al finalizar la estructura.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 con GCC, utilizando la cabecera `api_sesion19.h` y las funciones definidas para trabajar con estructuras. |
| **Rol (R)** | Ingeniero de software enfocado en programación de sistemas, estructuras de datos y organización de memoria. |
| **Especificación (E)** | Calcular la ubicación de los miembros y el tamaño de una estructura mediante reglas de alineación y padding. |
| **Output (O)** | Implementación modular en C, respetando las firmas originales, sin utilizar `main()` y compatible con las opciones de compilación solicitadas. |

### 2.2 Prompt Estructurado

```text
CONTEXTO: C11 con GCC, utilizando la cabecera
api_sesion19.h, que contiene la estructura Campo y
las declaraciones de las funciones correspondientes.

ROL: Actúa como un programador especializado en
sistemas, compiladores y administración de memoria.

ESPECIFICACIÓN:
Desarrolla las funciones:

int offset_campo(const Campo *campos, int total,
                 const char *nombre);

int tamano_struct(const Campo *campos, int total);

REGLAS:
- Reconocer los tipos de datos mediante una tabla
  con sus respectivos tamaños.
- Alinear cada campo antes de asignar su posición.
- Considerar el padding entre los miembros.
- Ajustar el tamaño final de acuerdo con la
  alineación del campo de mayor tamaño.
- Devolver -1 cuando el miembro no exista.
- Devolver -1 si la lista es NULL o hay tipos
  que no se encuentran registrados.
- Una estructura sin campos debe tener tamaño 0.
- Validar los valores negativos de total.
- Evitar accesos inválidos al buscar nombres.
- Mantener las firmas establecidas en la cabecera.

OUTPUT:
Código C modular, sin main(), compatible con
-std=c11 -Wall -Wextra -Werror y un análisis
breve de la complejidad de las funciones.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion19_c.c - Fase 2 */
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

### Análisis de complejidad

- `ancho_de()`: O(1), debido a que consulta una tabla fija de tipos de datos.
- `recorrer()`: O(n), porque realiza un recorrido de los campos para calcular sus posiciones y el tamaño.
- `offset_campo()`: O(n), ya que necesita revisar los miembros hasta encontrar el solicitado.
- `tamano_struct()`: O(n), porque recorre los campos para determinar el tamaño total.

El espacio adicional es O(1), porque se utilizan variables auxiliares y no se crean estructuras dinámicas.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Se verificaron diferentes distribuciones de campos para comprobar que los offsets y el tamaño final se calcularan correctamente, incluyendo los espacios de padding.

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

- [x] Los casos principales y las estructuras vacías fueron comprobados.
- [x] No se presentaron errores ni *Crash* durante las seis pruebas del harness.
- [x] Se revisó el comportamiento de los offsets y el padding.
- [x] La complejidad teórica corresponde con los recorridos realizados por el código.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar la implementación, observé que las seis pruebas del harness se habían superado, pero todavía existían algunas entradas que necesitaban una comprobación adicional.
>
> Uno de los puntos fue la cantidad negativa de campos, porque si se recibía un valor menor que cero, la función podía interpretar la estructura como si estuviera vacía y devolver 0.
>
> También consideré necesario revisar los siguientes casos:
>
> - **Lista NULL:** comprobar que las funciones no intenten recorrer una lista que no existe.
> - **Tipo desconocido:** verificar que un campo con un tipo no registrado en la tabla sea rechazado.
> - **Nombre NULL:** evitar que la búsqueda utilice `strcmp` cuando el nombre del campo no está disponible.
> - **Total negativo:** impedir que una cantidad negativa de campos sea considerada una estructura vacía.
>
> Para atender estos detalles agregué validaciones antes de realizar los recorridos y mantuve la comprobación de los nombres antes de compararlos. De esta manera, los campos sin nombre no provocan una comparación inválida y las cantidades incorrectas se rechazan.
>
> La complejidad se mantiene en O(n) para las funciones principales, ya que se sigue realizando un solo recorrido de los campos, mientras que el espacio adicional permanece en O(1).

---

**Firma digital:** `kirito2906`
