# Bitácora de Requerimientos y Auditoría IA — Sesión 18

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Arreglos y Verificación de Límites  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Cálculo de tamaño de arreglos y validación de índices.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

Al realizar este ejercicio identifiqué varios puntos que debía cuidar para que las funciones trabajaran correctamente:

- **Identificación de tipos:** `bytes_arreglo()` necesita reconocer los tipos permitidos y asignarles su tamaño en bytes: char, short, int, float, double y puntero.
- **Cálculo de memoria:** es necesario multiplicar el número de elementos por el tamaño correspondiente al tipo de dato para obtener el espacio total del arreglo.
- **Tipos desconocidos:** si se recibe un tipo que no está registrado, la función debe devolver `-1`.
- **Dimensiones inválidas:** una cantidad negativa de elementos debe devolver `-1`, mientras que una cantidad igual a cero debe dar como resultado `0`.
- **Validación de índices:** `indice_en_rango()` debe aceptar únicamente índices desde cero hasta `elementos - 1`.
- **Índices negativos:** se deben rechazar para evitar que sean considerados como posiciones válidas.
- **Dificultad principal:** tuve que distinguir entre la cantidad total de elementos y el último índice permitido, además de cuidar que el cálculo del tamaño se realizara correctamente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 con GCC, sin bibliotecas no estándar. Se utiliza una tabla para identificar los tamaños de los tipos de datos. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores. |
| **Especificación (E)** | Calcular el tamaño de un arreglo según su tipo y cantidad de elementos. También validar que los índices estén dentro del rango permitido y rechazar entradas inválidas. |
| **Output (O)** | Código modular en C, respetando las funciones declaradas en `api_sesion18.h`, sin incluir `main()` y acompañado de un análisis de complejidad. |

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

- `bytes_arreglo()`: O(1), porque recorre una tabla que siempre contiene seis tipos de datos.
- `indice_en_rango()`: O(1), porque solamente realiza dos comparaciones para comprobar si el índice pertenece al rango permitido.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Se verificaron cálculos de memoria, dimensiones negativas, índices válidos e índices fuera del rango permitido.

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

- [x] Los casos ejecutados fueron superados sin presentar errores ni cierres inesperados.
- [x] No se observaron problemas de acceso fuera de límites en las pruebas realizadas. No se efectuó una auditoría específica de memoria.
- [x] La complejidad teórica corresponde con las operaciones implementadas.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

El harness logró superar las seis pruebas, pero al revisar el código encontré algunas situaciones que no fueron comprobadas directamente:

- **Arreglo con cero elementos:** no se ejecutó una prueba específica para verificar que `bytes_arreglo()` devuelva `0` cuando la cantidad de elementos sea cero.
- **Tipos desconocidos:** tampoco se probó con un nombre de tipo que no estuviera registrado en la tabla. Sin embargo, al revisar el código comprobé que devuelve `-1` cuando no encuentra coincidencias.
- **Puntero NULL:** no se realizó una prueba enviando `NULL` como tipo, aunque existe una condición para rechazar esa entrada.
- **Cantidad negativa en la validación de índices:** se probó un índice negativo, pero no se comprobó por separado qué sucede cuando la cantidad de elementos es negativa.
- **Cómo lo detecté:** comparé las condiciones del código con los seis casos ejecutados por el harness. Así identifiqué que todavía faltaban algunas pruebas para revisar mejor los límites y las entradas no válidas.

---

**Firma digital:** `kirito2906`
