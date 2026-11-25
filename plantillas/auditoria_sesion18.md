# Bitácora de Requerimientos y Auditoría IA — Sesión 18

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Arreglos y Verificación de Límites
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Cálculo de tamaño de arreglos y validación de índices

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Las restricciones que tuve que resolver al codificar a mano fueron:
>
> - **Identificación de tipos:** `bytes_arreglo()` debe reconocer los tipos válidos y asignarles su tamaño correspondiente en bytes: char, short, int, float, double y puntero.
> - **Cálculo de memoria:** se debe multiplicar la cantidad de elementos por el tamaño del tipo para obtener el total de bytes del arreglo.
> - **Tipos desconocidos:** si se recibe un tipo que no está dentro de los permitidos, la función debe devolver `-1`.
> - **Dimensiones inválidas:** si la cantidad de elementos es negativa, debe devolver `-1`, mientras que con cero elementos debe devolver `0`.
> - **Validación de índices:** `indice_en_rango()` debe aceptar índices desde cero hasta `elementos - 1`, sin permitir que el índice sea igual a la cantidad de elementos.
> - **Índices negativos:** se deben rechazar los índices negativos sin realizar comparaciones incorrectas.
> - **Punto en que me atoré:** tuve que tener cuidado al calcular el tamaño total del arreglo y al distinguir entre el último índice válido y el número total de elementos, porque no representan lo mismo.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                                                    |
| :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C11 / GCC sin bibliotecas no estándar, utilizando una tabla con los tamaños de los tipos de datos.                                                                    |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores.                                                                                                                     |
| **Especificación (E)** | Calcular el tamaño total de un arreglo según su tipo y cantidad de elementos. Validar índices dentro del rango permitido y rechazar dimensiones o entradas inválidas. |
| **Output (O)**         | Solo código modular en C, respetando la interfaz del archivo `api_sesion18.h`, sin `main()` y con análisis de complejidad.                                            |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy trabajando en C, compilado con gcc -std=c11
-Wall -Wextra -Werror, sin bibliotecas no estándar.
Tengo una cabecera api_sesion18.h que define las funciones
para calcular el tamaño de arreglos y validar índices.

Rol: Eres un ingeniero de software de sistemas y compiladores.

Especificación: Implementa las funciones:

long bytes_arreglo(const char *tipo, int elementos);
int indice_en_rango(int indice, int elementos);

- bytes_arreglo() debe calcular el tamaño total en bytes
  multiplicando la cantidad de elementos por el tamaño
  correspondiente al tipo de dato.
- Los tipos válidos son char, short, int, float, double
  y puntero.
- Los tamaños utilizados son: char = 1, short = 2,
  int = 4, float = 4, double = 8 y puntero = 8.
- Si el tipo es NULL, desconocido o la cantidad de
  elementos es negativa, devuelve -1.
- Si la cantidad de elementos es cero, devuelve 0.
- indice_en_rango() devuelve 1 cuando el índice es
  mayor o igual a cero y menor que la cantidad de
  elementos.
- Devuelve 0 cuando el índice está fuera del rango.
- El último índice válido debe ser elementos - 1.
- Respeta las firmas exactas de api_sesion18.h.
- No incluyas main().
- Utiliza una tabla para identificar los tamaños de
  los tipos y evita advertencias al compilar.

Output: Solo el código modular del archivo .c y un breve
análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion18_c.c - Fase 2: El Cientifico
 * Version con tabla de tipos.
 */
#include "api_sesion18.h"
#include <string.h>
#include <stddef.h>

typedef struct {
    const char *nombre;
    int bytes;
} TipoAncho;

static const TipoAncho TABLA[] = {
    {"char", 1}, {"short", 2}, {"int", 4},
    {"float", 4}, {"double", 8}, {"puntero", 8}
};

long bytes_arreglo(const char *tipo, int elementos) {
    if (tipo == NULL || elementos < 0)
        return -1;

    for (size_t i = 0; i < sizeof TABLA / sizeof TABLA[0]; i++) {
        if (strcmp(TABLA[i].nombre, tipo) == 0)
            return (long)elementos * TABLA[i].bytes;
    }

    return -1;
}

int indice_en_rango(int indice, int elementos) {
    return indice >= 0 && indice < elementos;
}
```

**Análisis de complejidad:**

- `bytes_arreglo()`: O(1), porque recorre una tabla de tamaño fijo con seis tipos de datos.
- `indice_en_rango()`: O(1), porque realiza comparaciones directas para comprobar si el índice está dentro del rango.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Límites estáticos y dimensiones inválidas, incluyendo cálculo de memoria, índices válidos, índices fuera de rango y cantidades negativas.

### Salida del harness

```text
=== AUDITORIA SESION 18 - Tamano de arreglo y limites ===
Caso                               esperado:              obtenido:              resultado
[ 1] int[10]                            esperado: 40           obtenido: 40           OK
[ 2] double[3]                          esperado: 24           obtenido: 24           OK
[ 3] int[-4]                            esperado: -1           obtenido: -1           OK
[ 4] indice 0 de 5                      esperado: 1            obtenido: 1            OK
[ 5] indice 5 de 5                      esperado: 0            obtenido: 0            OK
[ 6] indice negativo                    esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion18.md
```

- [x] Caso base y límites contemplados en las pruebas superadas sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks* (no se realizó una auditoría específica de memoria).
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó 6/6 con la versión de la IA, pero al revisar el código encontré algunos detalles que se deben considerar y que las pruebas no contemplan completamente:
>
> - **Arreglo con cero elementos:** no se realizó una prueba específica para comprobar que `bytes_arreglo()` devuelva cero cuando la cantidad de elementos es cero.
> - **Tipos desconocidos:** no se probó qué sucede cuando se recibe un nombre de tipo que no está registrado en la tabla, aunque el código contempla devolver `-1`.
> - **Puntero NULL:** no se realizó una prueba específica enviando un tipo `NULL` para comprobar que la función rechace esa entrada.
> - **Cantidad de elementos negativa en índices:** el harness prueba un índice negativo, pero no comprueba por separado qué sucede cuando la cantidad de elementos es negativa.
> - **Cómo lo detecté:** revisando el código de la IA y comparando sus condiciones con los seis casos que realmente ejecutó el harness. Identifiqué que todavía se pueden agregar pruebas para comprobar esas situaciones.

---

**Firma digital:** `kirito2906`
