# Bitácora de Requerimientos y Auditoría IA — Sesión 16

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Firmas de Función y Parámetros Formales
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Registro de prototipos y aridad

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar la función de forma manual tuve que tener cuidado con la búsqueda del nombre dentro del catálogo y con la comparación de la aridad ya que no es lo mismo que una función no exista a que tenga un número incorrecto de argumentos. También fue necesario validar las entradas como el catálogo NULL el nombre NULL y los valores negativos para evitar resultados incorrectos.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                                                                                                         |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C11 / GCC sin bibliotecas no estándar. Uso de un catálogo de funciones con nombre y aridad.                                                                                                                                |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores.                                                                                                                                                                          |
| **Especificación (E)** | Buscar el nombre exacto dentro del catálogo y comparar la aridad declarada con la cantidad de argumentos recibidos. Devolver 1 si coincide, 0 si no coincide y -1 si la función no existe o se reciben entradas inválidas. |
| **Output (O)**         | Código modular en C que implemente `verificar_llamada()` y cumpla con el contrato definido en `api_sesion16.h`.                                                                                                            |

### 2.2 Prompt Estructurado

```text
Contexto:
Estoy desarrollando un verificador de llamadas a funciones
en C para un compilador. Utilizo un catálogo de funciones
que contiene el nombre y la aridad declarada de cada función.

Rol:
Actúa como un ingeniero de software especializado en C
y sistemas de compiladores.

Especificación:
Implementa la función verificar_llamada() utilizando
la siguiente firma:

int verificar_llamada(const Funcion *catalogo, int total,
                     const char *nombre, int nargs);

Debe buscar el nombre exacto dentro del catálogo y
comparar la aridad declarada con los argumentos recibidos.

Debe devolver:
1 si la llamada es válida.
0 si la función existe pero la aridad no coincide.
-1 si el catálogo es NULL, el nombre es NULL, la aridad
es negativa, el total es negativo o la función no existe.

Debe respetar la interfaz api_sesion16.h y no incluir main().
El código debe ser compatible con C11 y compilar usando
-Wall -Wextra -Werror.

Output:
Entrega el código modular en C y evita bibliotecas
no estándar.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion16.h"
#include <string.h>

static const Funcion *buscar_funcion(const Funcion *cat,
                                     int total,
                                     const char *nombre) {
    for (int i = 0; i < total; i++) {
        if (cat[i].nombre != NULL &&
            strcmp(cat[i].nombre, nombre) == 0)
            return &cat[i];
    }
    return NULL;
}

int verificar_llamada(const Funcion *catalogo,
                     int total,
                     const char *nombre,
                     int nargs) {
    if (catalogo == NULL || nombre == NULL ||
        nargs < 0 || total < 0)
        return -1;

    const Funcion *f = buscar_funcion(catalogo,
                                     total,
                                     nombre);

    if (f == NULL)
        return -1;

    return f->aridad == nargs ? 1 : 0;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Llamadas con número incorrecto de argumentos, funciones no registradas, llamada válida y entrada NULL.

### Salida del harness

```text
=== AUDITORIA SESION 16 - Registro de prototipos y aridad ===
Caso                               esperado:              obtenido:              resultado
[ 1] suma con 3 argumentos              esperado: 1            obtenido: 1            OK
[ 2] suma con 2 argumentos              esperado: 0            obtenido: 0            OK
[ 3] suma con 4 argumentos              esperado: 0            obtenido: 0            OK
[ 4] funcion no registrada              esperado: -1           obtenido: -1           OK
[ 5] main sin argumentos                esperado: 1            obtenido: 1            OK
[ 6] nombre NULL                        esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion16.md
```

- [x] Caso base y límites contemplados en las pruebas superadas sin Crash.
- [x] No existen accesos fuera de límites ni Memory Leaks (no se realizó una auditoría específica de memoria).
- [x] La complejidad teórica coincide con la implementada: búsqueda lineal O(n) en el catálogo y comparación de aridad O(1).

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> La IA no incluyó pruebas para todos los posibles casos de borde como un catálogo vacío o registros con nombres duplicados. Sin embargo la función sí contempla algunas entradas inválidas como el catálogo NULL el nombre NULL y los valores negativos. Las seis pruebas del harness fueron superadas y estos casos adicionales quedaron como posibles pruebas futuras ya que no fueron comprobados en la auditoría ejecutada.

---

**Firma digital:** `kirito2906`
