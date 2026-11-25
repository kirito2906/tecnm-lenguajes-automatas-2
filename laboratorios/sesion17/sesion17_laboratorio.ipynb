# Bitácora de Requerimientos y Auditoría IA — Sesión 17

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Comprobación Semántica de Retornos y Rutas de Control
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Validación de tipos de retorno y rutas de ejecución.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Las restricciones que tuve que resolver al codificar a mano fueron:
>
> - **Comparación de tipos:** `diagnosticar_retorno()` debe comprobar que el tipo de la expresión devuelta sea compatible con el tipo que promete la función.
> - **Conversión de tipos:** solamente se debe aceptar una conversión cuando el tipo destino sea igual o más ancho que el tipo de origen.
> - **Funciones void:** una función de tipo `void` no puede devolver un valor y debe comprobarse que la expresión también sea `void`.
> - **Validación de rutas:** se debe comprobar que todas las rutas de ejecución terminen en un retorno, especialmente cuando existe un `if` sin `else`.
> - **Entradas inválidas:** si alguno de los tipos es `NULL`, si existen cero rutas o si las rutas con retorno son mayores que las rutas totales, se debe devolver `-1`.
> - **Orden de validación:** primero se debe revisar si los tipos son compatibles y después comprobar las rutas, para no reportar una ruta faltante cuando realmente existe un error de tipo.
> - **Punto en que me atoré:** tuve que organizar las condiciones para diferenciar un tipo incompatible de una ruta que no tiene retorno, porque cada situación debe devolver un resultado diferente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| **Elemento C-R-E-O**   | **Definición Técnica**                                                                                                                       |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | C11 / GCC sin bibliotecas no estándar, utilizando tipos de datos y conteo de rutas de ejecución.                                             |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores.                                                                                            |
| **Especificación (E)** | Comparación de tipos de retorno, validación de conversiones permitidas y comprobación de que todas las rutas de ejecución tengan un retorno. |
| **Output (O)**         | Solo código modular en C, respetando la interfaz del archivo `api_sesion17.h`, sin `main()` y con análisis de complejidad.                   |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy trabajando en C, compilado con gcc -std=c11
-Wall -Wextra -Werror, sin bibliotecas no estándar.
Tengo una cabecera api_sesion17.h que define la función
diagnosticar_retorno() para validar los tipos de retorno
y las rutas de ejecución.

Rol: Eres un ingeniero de software especializado en
sistemas y compiladores.

Especificación: Implementa la función:

int diagnosticar_retorno(const char *tipo_funcion,
                         const char *tipo_expresion,
                         int rutas_totales,
                         int rutas_con_return);

- Devuelve 0 si los tipos son compatibles y todas las
  rutas tienen return.
- Devuelve 1 si existe un tipo incompatible.
- Devuelve 2 si existe alguna ruta sin retorno.
- Devuelve -1 si alguno de los tipos es NULL, hay cero
  rutas, el conteo es incoherente o el tipo es desconocido.
- Una función void no puede devolver un valor.
- Las conversiones solamente se aceptan cuando el tipo
  destino es igual o más ancho que el tipo de origen.
- Compara primero los tipos y después las rutas.
- Respeta exactamente la firma de api_sesion17.h.
- No incluyas main().

Output: Entrega únicamente el código modular en C,
utilizando una tabla para comparar los tipos de datos,
sin modificar la interfaz del harness.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion17.h"
#include <string.h>
#include <stddef.h>

typedef struct {
    const char *nombre;
    int ancho;
} TipoInfo;

static const TipoInfo TIPOS[] = {
    {"char", 1},
    {"int", 2},
    {"long", 3},
    {"float", 4},
    {"double", 5}
};

static int ancho_de(const char *t) {
    for (size_t i = 0; i < sizeof TIPOS / sizeof TIPOS[0]; i++) {
        if (strcmp(TIPOS[i].nombre, t) == 0)
            return TIPOS[i].ancho;
    }
    return -1;
}

int diagnosticar_retorno(const char *tipo_funcion,
                         const char *tipo_expresion,
                         int rutas_totales,
                         int rutas_con_return) {
    if (!tipo_funcion || !tipo_expresion)
        return -1;

    if (rutas_totales <= 0 || rutas_con_return < 0 ||
        rutas_con_return > rutas_totales)
        return -1;

    int f_void = strcmp(tipo_funcion, "void") == 0;
    int e_void = strcmp(tipo_expresion, "void") == 0;

    if (f_void)
        return e_void ? 0 : 1;

    if (e_void)
        return 1;

    int destino = ancho_de(tipo_funcion);
    int origen = ancho_de(tipo_expresion);

    if (destino < 0 || origen < 0)
        return -1;

    if (destino < origen)
        return 1;

    return rutas_con_return < rutas_totales ? 2 : 0;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Funciones con tipos de retorno compatibles e incompatibles, funciones `void`, rutas sin retorno y entradas con cero rutas de ejecución.

### Salida del harness

```text
=== AUDITORIA SESION 17 - Validacion de retornos y rutas ===
Caso                               esperado:              obtenido:              resultado
[ 1] int con int y dos rutas            esperado: 0            obtenido: 0            OK
[ 2] void devuelve valor                esperado: 1            obtenido: 1            OK
[ 3] ruta sin retorno                   esperado: 2            obtenido: 2            OK
[ 4] double acepta int                  esperado: 0            obtenido: 0            OK
[ 5] int no acepta double               esperado: 1            obtenido: 1            OK
[ 6] cero rutas de ejecucion            esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion17.md
```

- [x] Caso base y límites contemplados en las pruebas superadas sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks* (no se realizó una auditoría específica de memoria).
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó 6/6 con la versión de la IA, pero al revisar el código encontré algunos detalles que se deben considerar y que las pruebas no contemplan completamente:
>
> - **Tipos desconocidos:** no se realizó una prueba específica con nombres de tipos que no estén dentro de la tabla, aunque el código los identifica y devuelve `-1`.
> - **Entradas NULL:** no se probaron individualmente los casos donde `tipo_funcion` o `tipo_expresion` son `NULL`, aunque la implementación contiene esa validación.
> - **Conteos incoherentes:** no se probaron todos los casos donde las rutas con retorno son negativas o mayores que las rutas totales.
> - **Función void sin retorno:** el código de la IA acepta `void` con `void` sin exigir que todas las rutas tengan `return`. Esto sigue la condición especial de la implementación, pero sería importante confirmar con el docente si ese comportamiento es el esperado.
> - **Cómo lo detecté:** revisando las condiciones del código de la IA y comparándolas con los seis casos que ejecutó el harness.

---

**Firma digital:** `kirito2906`
