# Bitácora de Requerimientos y Auditoría IA — Sesión 21

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Fundamentos de Código de Tres Direcciones (TAC)
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Generación de temporales únicos y representación en cuádruplos.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Las restricciones que tuve que resolver al codificar a mano fueron:
>
> - **Generación de temporales:** `nuevo_temporal()` debe utilizar el contador para generar nombres consecutivos como `_t0`, `_t1` y `_t2`, incrementándolo después de cada llamada.
> - **Uso del buffer:** fue necesario utilizar correctamente el tamaño del buffer para evitar escribir fuera de la memoria disponible.
> - **Formato de cuádruplos:** `emitir_cuadruplo()` debe respetar el formato `(op, a1, a2, res)` y mantener el orden de los cuatro elementos.
> - **Argumentos NULL:** cuando alguno de los argumentos no existe, se debe representar con un guion bajo (`_`) en lugar de dejar el espacio vacío.
> - **Uso de snprintf():** utilicé esta función para escribir las cadenas dentro del buffer respetando su capacidad.
> - **Punto en que me atoré:** tuve que tener cuidado con el incremento del contador y con la representación de los argumentos NULL, porque un error en cualquiera de esas partes podía provocar que los resultados no coincidieran con los esperados.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                                                                                             |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C11 / GCC sin bibliotecas no estándar, utilizando buffers de texto y funciones para generar temporales y cuádruplos.                                                                                           |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores.                                                                                                                                                              |
| **Especificación (E)** | Generación de temporales únicos mediante un contador y construcción de cuádruplos con el formato `(op, a1, a2, res)`, sustituyendo los argumentos NULL por guiones bajos y respetando la capacidad del buffer. |
| **Output (O)**         | Solo código modular en C, respetando la interfaz del archivo `api_sesion21.h`, sin `main()` y utilizando `snprintf()` para escribir en los buffers.                                                            |

### 2.2 Prompt Estructurado

```text
CONTEXTO: C11 con GCC (-Wall -Wextra -Werror), solo libc.
La cabecera api_sesion21.h declara las funciones
nuevo_temporal() y emitir_cuadruplo().

ROL: Ingeniero de software especializado en sistemas y compiladores.

ESPECIFICACIÓN:

Implementa las siguientes funciones:

void nuevo_temporal(char *dst, int cap, int *contador);

void emitir_cuadruplo(char *dst, int cap, const char *op,
                      const char *a1, const char *a2,
                      const char *res);

- nuevo_temporal() debe generar nombres como _t0, _t1,
  _t2 utilizando el contador recibido.
- El contador debe incrementarse después de generar
  cada temporal.
- emitir_cuadruplo() debe generar el formato
  (op, a1, a2, res).
- Los argumentos NULL deben representarse con un guion
  bajo (_).
- Utiliza snprintf() respetando la capacidad del buffer.
- No utilices memoria dinámica ni variables globales.
- No incluyas main().
- Respeta exactamente las firmas de api_sesion21.h.
- El código debe compilar sin advertencias.

OUTPUT: Entrega las dos funciones completas en C,
listas para utilizarse en ia_sesion21_c.c.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion21_c.c - Fase 2: El Cientifico */
#include "api_sesion21.h"
#include <stdio.h>
#include <stddef.h>

void nuevo_temporal(char *dst, int cap, int *contador) {
    if (dst == NULL || contador == NULL || cap <= 0) {
        return;
    }

    snprintf(dst, (size_t)cap, "_t%d", *contador);
    (*contador)++;
}

void emitir_cuadruplo(char *dst, int cap, const char *op,
                      const char *a1, const char *a2,
                      const char *res) {
    if (dst == NULL || cap <= 0) {
        return;
    }

    snprintf(dst, (size_t)cap, "(%s, %s, %s, %s)",
             op != NULL ? op : "_",
             a1 != NULL ? a1 : "_",
             a2 != NULL ? a2 : "_",
             res != NULL ? res : "_");
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Generación de temporales, operaciones aritméticas, asignación simple y salto sin operandos.

### Salida del harness

```text
=== AUDITORIA SESION 21 - Cuadruplos y temporales unicos ===
Caso                               esperado:              obtenido:              resultado
[ 1] nuevo_temporal(_t0)                esperado: _t0          obtenido: _t0          OK
[ 2] nuevo_temporal(_t7)                esperado: _t7          obtenido: _t7          OK
[ 3] cuadruplo de a + b
     esperado: (+, a, b, _t0)
     obtenido: (+, a, b, _t0)
     -> OK
[ 4] cuadruplo de _t0 * c
     esperado: (*, _t0, c, _t1)
     obtenido: (*, _t0, c, _t1)
     -> OK
[ 5] asignacion simple                  esperado: (=, a, _, x) obtenido: (=, a, _, x) OK
[ 6] goto sin operandos
     esperado: (goto, L1, _, _)
     obtenido: (goto, L1, _, _)
     -> OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion21.md
```

- [x] Casos incluidos en las pruebas superados sin *Crash*.
- [x] No se realizó una auditoría específica para comprobar todos los accesos fuera de límites o posibles *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó 6/6 pruebas con la implementación de la IA, pero al revisar el código encontré algunos detalles que las pruebas no contemplan completamente:
>
> - **Contador en 10:** aunque la implementación permite generar `_t10`, el harness no incluye una prueba específica para comprobar ese valor, a pesar de que aparece en los criterios de aceptación.
> - **Buffers pequeños:** no se realizó una prueba con un buffer de poca capacidad para comprobar qué sucede cuando la cadena generada no cabe completamente.
> - **Argumentos NULL:** se probaron algunos argumentos NULL en los cuádruplos, pero no se comprobaron todas las posiciones posibles individualmente.
> - **Validación de entradas:** el código contempla situaciones como un destino NULL, una capacidad inválida o un contador NULL, pero estos casos no aparecen en las seis pruebas principales.
> - **Cómo lo detecté:** revisando el código de la IA y comparando sus validaciones con los casos que realmente ejecutó el harness.

---

**Firma digital:** `kirito2906`
