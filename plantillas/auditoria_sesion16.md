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

> Las restricciones que tuve que resolver al codificar a mano fueron:
> - **Búsqueda exacta:** `verificar_llamada()` debe buscar el nombre exacto de la función dentro del catálogo para evitar confundir funciones diferentes.
> - **Comparación de aridad:** se debe comparar la cantidad de argumentos recibidos con la aridad declarada de la función y no con el número de funciones que existen en el catálogo.
> - **Funciones sin parámetros:** una función con aridad cero solo debe aceptar llamadas que también tengan cero argumentos.
> - **Funciones inexistentes:** si el nombre no se encuentra en el catálogo se debe devolver `-1`, sin confundirlo con una aridad incorrecta.
> - **Entradas inválidas:** si el catálogo o el nombre son `NULL`, o si la aridad o el total son negativos, la función debe devolver `-1`.
> - **Punto en que me atoré:** tuve que tener cuidado al distinguir entre una función que no existe y una función que sí existe pero que recibe una cantidad incorrecta de argumentos, ya que cada situación tiene un resultado diferente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC sin bibliotecas no estándar, utilizando un catálogo de funciones con nombre y aridad. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores. |
| **Especificación (E)** | Búsqueda exacta del nombre de la función, comparación de aridad y validación de entradas para distinguir llamadas válidas, aridad incorrecta y funciones inexistentes. |
| **Output (O)** | Solo código modular en C, respetando la interfaz del archivo `api_sesion16.h`, sin `main()` y con análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy trabajando en C, compilado con gcc -std=c11
-Wall -Wextra -Werror, sin bibliotecas no estándar.
Tengo una cabecera api_sesion16.h que define la estructura
Funcion con el nombre y la aridad declarada.

Rol: Eres un ingeniero de software de sistemas y compiladores.

Especificación: Implementa la función:

int verificar_llamada(const Funcion *catalogo, int total,
                     const char *nombre, int nargs);

- Busca el nombre exacto dentro del catálogo completo.
- Si encuentra la función, compara la aridad declarada
  con el número de argumentos recibidos.
- Devuelve 1 si la llamada es válida.
- Devuelve 0 si la función existe pero la aridad no coincide.
- Devuelve -1 si el catálogo es NULL, el nombre es NULL,
  la aridad es negativa, el total es negativo o la función
  no existe.
- Una función con aridad cero solo acepta cero argumentos.
- Respeta las firmas exactas de api_sesion16.h.
- No incluyas main().

Output: Solo el código modular del archivo .c y un breve
análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion16_c.c - Fase 2: El Cientifico
 * Version con busqueda separada de la comparacion.
 */
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

- [x] Caso base y límites contemplados en las pruebas superadas sin *Crash*.
- [ ] No existen accesos fuera de límites ni *Memory Leaks* (no se realizó una auditoría específica de memoria).
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó 6/6 con la versión de la IA, pero al revisar el código encontré algunos detalles que se deben considerar y que las pruebas no contemplan completamente:
> - **Catálogo vacío:** no se realizó una prueba específica con un catálogo vacío y `total` igual a cero, por lo que quedó como un caso adicional pendiente de comprobar.
> - **Nombres duplicados:** no se contempló qué ocurre si existen dos funciones registradas con el mismo nombre pero con aridades diferentes; la búsqueda devuelve la primera coincidencia.
> - **Validación de entradas:** el código contempla entradas como catálogo `NULL`, nombre `NULL`, aridad negativa y total negativo, pero no todas fueron probadas individualmente en el harness.
> - **Cómo lo detecté:** revisando el código de la IA y comparando las condiciones de la función con los casos que realmente ejecutó el harness.

---

**Firma digital:** `kirito2906`
