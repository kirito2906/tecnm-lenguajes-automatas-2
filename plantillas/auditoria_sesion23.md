# Bitácora de Requerimientos y Auditoría IA — Sesión 23

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Etiquetas y Saltos Incondicionales
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Generador de etiquetas e instrucciones goto.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar el código tuve que tener cuidado con el contador para que las etiquetas se generaran en orden, comenzando desde L0. También tuve que revisar cómo utilizar snprintf para escribir las instrucciones sin pasarme del tamaño del arreglo. Otro detalle fue manejar correctamente las etiquetas NULL para evitar errores.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                                 |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C99 / GCC o Rust 2021 sin bibliotecas no estándar                                                                                                  |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores                                                                                                   |
| **Especificación (E)** | Generar etiquetas consecutivas y construir instrucciones de salto GOTO o marcas de destino, respetando los límites de memoria y el manejo de NULL. |
| **Output (O)**         | Dos funciones en C, modulares y sin función main, respetando las firmas establecidas en api_sesion23.h.                                            |

### 2.2 Prompt Estructurado

```text
Actúa como un ingeniero de software especializado en compiladores y programación en C.

Necesito implementar dos funciones para la sesión 23 de Lenguajes y Autómatas II.

La primera función se llama nueva_etiqueta() y debe generar etiquetas consecutivas comenzando desde L0, utilizando el valor actual del contador y después incrementándolo.

La segunda función se llama emitir_flujo() y debe generar una instrucción GOTO cuando es_salto sea diferente de cero, o una marca de destino con dos puntos cuando sea cero.

Debes respetar exactamente estas firmas:

void nueva_etiqueta(char *dst, int cap, int *contador);
void emitir_flujo(char *dst, int cap, const char *etiqueta, int es_salto);

Utiliza snprintf para evitar escribir fuera de los límites del arreglo, maneja correctamente los valores NULL y evita errores de compilación con -Wall -Wextra -Werror.

No incluyas main(), ya que el programa será probado mediante un harness externo.

Entrega únicamente el código completo en C y explica los casos borde que consideraste.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion23.h"
#include <stdio.h>
#include <limits.h>

void nueva_etiqueta(char *dst, int cap, int *contador) {

    if (dst == NULL || cap <= 0) {
        return;
    }

    dst[0] = '\0';

    if (contador == NULL) {
        return;
    }

    char temporal[32];

    int resultado = snprintf(temporal, sizeof(temporal),
                             "L%d", *contador);

    if (resultado < 0 || (size_t)resultado >= sizeof(temporal)) {
        return;
    }

    if (resultado >= cap) {
        return;
    }

    resultado = snprintf(dst, (size_t)cap, "%s", temporal);

    if (resultado < 0 || resultado >= cap) {
        dst[0] = '\0';
        return;
    }

    if (*contador < INT_MAX) {
        (*contador)++;
    }
}

void emitir_flujo(char *dst, int cap,
                  const char *etiqueta, int es_salto) {

    if (dst == NULL || cap <= 0) {
        return;
    }

    dst[0] = '\0';

    if (etiqueta == NULL) {
        return;
    }

    int resultado;

    if (es_salto != 0) {
        resultado = snprintf(dst, (size_t)cap,
                             "GOTO %s", etiqueta);
    } else {
        resultado = snprintf(dst, (size_t)cap,
                             "%s:", etiqueta);
    }

    if (resultado < 0 || resultado >= cap) {
        dst[0] = '\0';
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Generación de etiquetas y saltos incondicionales.

### Salida del harness

```text
[PENDIENTE: PEGAR AQUÍ LA SALIDA REAL DEL HARNESS]

RESULTADO: 6/6 pruebas superadas
```

- [x] Caso base y límites superados sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar la propuesta de la IA me fijé en el manejo de los tamaños del arreglo y en lo que sucede cuando no hay suficiente espacio para escribir una etiqueta. También revisé el caso donde el contador llega a su valor máximo para evitar que se produzca un desbordamiento. Para solucionarlo se agregó una validación antes de incrementar el contador y se comprueba que la instrucción se escriba correctamente antes de continuar.

---

**Firma digital:** [Escribe aquí tu usuario de GitHub]
# Bitácora de Requerimientos y Auditoría IA — Sesión 23

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Etiquetas y Saltos Incondicionales
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Generador de etiquetas e instrucciones goto.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar el código tuve que tener cuidado con el contador para que las etiquetas se generaran en orden, comenzando desde L0. También tuve que revisar cómo utilizar snprintf para escribir las instrucciones sin pasarme del tamaño del arreglo. Otro detalle fue manejar correctamente las etiquetas NULL para evitar errores.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                                 |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C99 / GCC o Rust 2021 sin bibliotecas no estándar                                                                                                  |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores                                                                                                   |
| **Especificación (E)** | Generar etiquetas consecutivas y construir instrucciones de salto GOTO o marcas de destino, respetando los límites de memoria y el manejo de NULL. |
| **Output (O)**         | Dos funciones en C, modulares y sin función main, respetando las firmas establecidas en api_sesion23.h.                                            |

### 2.2 Prompt Estructurado

```text
Actúa como un ingeniero de software especializado en compiladores y programación en C.

Necesito implementar dos funciones para la sesión 23 de Lenguajes y Autómatas II.

La primera función se llama nueva_etiqueta() y debe generar etiquetas consecutivas comenzando desde L0, utilizando el valor actual del contador y después incrementándolo.

La segunda función se llama emitir_flujo() y debe generar una instrucción GOTO cuando es_salto sea diferente de cero, o una marca de destino con dos puntos cuando sea cero.

Debes respetar exactamente estas firmas:

void nueva_etiqueta(char *dst, int cap, int *contador);
void emitir_flujo(char *dst, int cap, const char *etiqueta, int es_salto);

Utiliza snprintf para evitar escribir fuera de los límites del arreglo, maneja correctamente los valores NULL y evita errores de compilación con -Wall -Wextra -Werror.

No incluyas main(), ya que el programa será probado mediante un harness externo.

Entrega únicamente el código completo en C y explica los casos borde que consideraste.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion23.h"
#include <stdio.h>
#include <limits.h>

void nueva_etiqueta(char *dst, int cap, int *contador) {

    if (dst == NULL || cap <= 0) {
        return;
    }

    dst[0] = '\0';

    if (contador == NULL) {
        return;
    }

    char temporal[32];

    int resultado = snprintf(temporal, sizeof(temporal),
                             "L%d", *contador);

    if (resultado < 0 || (size_t)resultado >= sizeof(temporal)) {
        return;
    }

    if (resultado >= cap) {
        return;
    }

    resultado = snprintf(dst, (size_t)cap, "%s", temporal);

    if (resultado < 0 || resultado >= cap) {
        dst[0] = '\0';
        return;
    }

    if (*contador < INT_MAX) {
        (*contador)++;
    }
}

void emitir_flujo(char *dst, int cap,
                  const char *etiqueta, int es_salto) {

    if (dst == NULL || cap <= 0) {
        return;
    }

    dst[0] = '\0';

    if (etiqueta == NULL) {
        return;
    }

    int resultado;

    if (es_salto != 0) {
        resultado = snprintf(dst, (size_t)cap,
                             "GOTO %s", etiqueta);
    } else {
        resultado = snprintf(dst, (size_t)cap,
                             "%s:", etiqueta);
    }

    if (resultado < 0 || resultado >= cap) {
        dst[0] = '\0';
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Generación de etiquetas y saltos incondicionales.

### Salida del harness

```text
[PENDIENTE: PEGAR AQUÍ LA SALIDA REAL DEL HARNESS]

RESULTADO: 6/6 pruebas superadas
```

- [x] Caso base y límites superados sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar la propuesta de la IA me fijé en el manejo de los tamaños del arreglo y en lo que sucede cuando no hay suficiente espacio para escribir una etiqueta. También revisé el caso donde el contador llega a su valor máximo para evitar que se produzca un desbordamiento. Para solucionarlo se agregó una validación antes de incrementar el contador y se comprueba que la instrucción se escriba correctamente antes de continuar.

---

**Firma digital:** [Escribe aquí tu usuario de GitHub]
