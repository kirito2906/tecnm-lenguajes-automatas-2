# Bitácora de Requerimientos y Auditoría IA — Sesión 18

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Arreglos y Verificación de Límites
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness).

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Cálculo de tamaño de arreglo en memoria.

Al realizar el código manualmente, identifiqué que era necesario conocer el tamaño que ocupa cada tipo de dato para poder calcular correctamente la memoria de un arreglo. También tuve que cuidar que no se aceptaran cantidades negativas de elementos ni tipos desconocidos.

Otra dificultad fue comprobar los índices, porque el último índice válido siempre es uno menos que la cantidad de elementos. Por ejemplo, en un arreglo de cinco elementos, el índice 4 es válido, pero el índice 5 ya está fuera de rango.

También tomé en cuenta que un arreglo con cero elementos debe devolver cero bytes.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                       |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C11 / GCC, utilizando únicamente bibliotecas estándar de C.                                                                              |
| **Rol (R)**            | Ingeniero de software especializado en programación de sistemas y compiladores.                                                          |
| **Especificación (E)** | Calcular el tamaño de arreglos según el tipo y número de elementos. Validar índices no negativos y menores que la cantidad de elementos. |
| **Output (O)**         | Código C modular, respetando las firmas del contrato, sin `main()` y con análisis de complejidad.                                        |

### 2.2 Prompt Estructurado

```text
Actúa como un ingeniero de software especializado en C y
desarrolla dos funciones para la Sesión 18 de Lenguajes y
Autómatas II.

La primera función debe llamarse bytes_arreglo() y recibir
el nombre de un tipo de dato y la cantidad de elementos.
Debe calcular el tamaño total del arreglo en bytes.

Los tipos válidos son char, short, int, float, double y
puntero. Si el tipo es desconocido, el puntero es NULL o
la cantidad de elementos es negativa, debe devolver -1.
Si la cantidad de elementos es cero, debe devolver 0.

La segunda función debe llamarse indice_en_rango() y recibir
un índice y la cantidad de elementos. Debe devolver 1 si el
índice está dentro del rango válido y 0 si está fuera.

Respeta exactamente las firmas declaradas en
api_sesion18.h. Utiliza una tabla para identificar los
tamaños de los tipos y evita advertencias al compilar.

No agregues main(). El código debe compilar con:
-std=c11 -Wall -Wextra -Werror.

Incluye un análisis breve de la complejidad de ambas funciones.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion18.h"
#include <string.h>
#include <stddef.h>

typedef struct {
    const char *nombre;
    int bytes;
} TipoAncho;

static const TipoAncho TABLA[] = {
    {"char", 1},
    {"short", 2},
    {"int", 4},
    {"float", 4},
    {"double", 8},
    {"puntero", 8}
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

**Complejidad:**

- `bytes_arreglo()`: O(1), porque recorre una tabla de tamaño fijo de seis tipos.
- `indice_en_rango()`: O(1), porque realiza comparaciones directas.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Límites estáticos y dimensiones inválidas.

### Salida del harness

**Resultados registrados en la práctica para el código Artesano y el código Científico:**

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

- [x] Caso base y límites superados sin Crash.
- [x] No existen accesos fuera de límites ni Memory Leaks (no se realizó una auditoría específica de memoria).
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

Al revisar el código generado por la IA, observé que la función `indice_en_rango()` no realiza una validación separada para comprobar si la cantidad de elementos es cero o negativa. Aunque su condición `indice >= 0 && indice < elementos` rechaza correctamente esos casos, considero que se podría agregar una validación explícita para que el código sea más claro.

También identifiqué que el harness no prueba todos los tipos de datos ni contempla casos como un tipo desconocido, un nombre de tipo NULL o un arreglo de cero elementos. Estos casos serían necesarios para comprobar mejor el funcionamiento de las funciones.

Como mejora, se pueden agregar pruebas adicionales para verificar esas situaciones. Los seis casos proporcionados sí aparecen como superados en el material de la sesión.

En conclusión, aprendí a calcular el tamaño de un arreglo y a validar sus índices, además de comprender la importancia de revisar los casos límite y no depender únicamente de las pruebas del harness.

---

**Firma digital:** `kirito2906`
