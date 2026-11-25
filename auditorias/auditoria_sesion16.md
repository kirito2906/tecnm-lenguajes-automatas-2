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

> El principal problema fue controlar correctamente la búsqueda de funciones y diferenciar los resultados que debe devolver el programa. La función tiene que identificar si el nombre existe y después comprobar si la cantidad de argumentos corresponde con la aridad registrada. También tuve que considerar algunos casos especiales:
>
> - Cuando una función no está registrada, debe regresar -1 y no confundirse con una llamada que tiene argumentos incorrectos.
> - Si la función existe, pero recibe una cantidad diferente de argumentos, el resultado debe ser 0.
> - Una función sin parámetros, como `main`, solamente debe aceptar cero argumentos.
> - Fue necesario evitar errores al comparar nombres, comprobando que las entradas no fueran `NULL` antes de utilizar `strcmp`.
> - También consideré que un catálogo vacío o un total negativo no deben provocar errores durante la búsqueda.
>
> Lo que más tuve que cuidar fue separar la búsqueda del nombre y la comparación de argumentos. Por eso decidí utilizar una función auxiliar llamada `buscar_funcion()`, que permite localizar primero la función y después verificar si su aridad coincide con los argumentos recibidos.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC con bibliotecas estándar y un catálogo de funciones que contiene nombres y aridades. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y desarrollo de compiladores. |
| **Especificación (E)** | Localización de funciones mediante su nombre exacto, comprobación de parámetros y validación de las entradas recibidas. |
| **Output (O)** | Código modular en C, utilizando la interfaz de `api_sesion16.h`, sin incluir `main()` y acompañado de un análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO: Se requiere trabajar con C11 utilizando GCC y las opciones
-Wall -Wextra -Werror. Se cuenta con el archivo api_sesion16.h,
que contiene la estructura Funcion con los campos nombre y aridad.

ROL: Actúa como un ingeniero de software especializado en sistemas
y compiladores.

ESPECIFICACIÓN: Desarrolla la función verificar_llamada() para
comprobar que las llamadas a funciones respeten los parámetros
establecidos en el catálogo.

- Realiza una búsqueda exacta del nombre solicitado.
- Comprueba la cantidad de argumentos con la aridad registrada.
- Regresa 1 cuando el nombre existe y los argumentos coinciden.
- Regresa 0 cuando la función existe, pero la cantidad de
  argumentos es diferente.
- Regresa -1 cuando el catálogo o el nombre son NULL,
  cuando el total o los argumentos son negativos, o cuando
  no se encuentra la función.
- Permite llamadas sin argumentos cuando la aridad sea cero.
- Mantén la firma original definida en api_sesion16.h.
- No agregues una función main().
- Utiliza una función auxiliar si ayuda a organizar el código.

OUTPUT: Entrega el código fuente modular en C y una explicación
breve de su complejidad temporal y espacial.
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

*Pruebas ejecutadas:* Llamadas con diferente cantidad de argumentos, búsqueda de funciones registradas y no registradas, y validación de entradas NULL.

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

* [x] Los casos de prueba ejecutados finalizaron correctamente y sin errores de ejecución.
* [x] No se observaron fallos durante las pruebas realizadas.
* [x] La complejidad teórica corresponde con el funcionamiento del código.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Aunque el programa logró superar las seis pruebas del harness, al revisar con más detalle la implementación encontré algunas situaciones que no fueron consideradas completamente. Una de ellas es el registro de dos funciones con el mismo nombre, pero con diferentes cantidades de parámetros. Como la función auxiliar `buscar_funcion()` se detiene al encontrar la primera coincidencia, podría devolver una aridad incorrecta aunque exista otra entrada con el mismo nombre que sí coincida.
>
> Otro caso que quedó pendiente fue comprobar un catálogo vacío con `total` igual a cero. El código contempla esta situación y devuelve -1, pero no aparece como una prueba independiente en los resultados del harness.
>
> También observé que no se realizaron pruebas individuales para todas las entradas inválidas, como el total negativo o una aridad negativa dentro del catálogo. Para evitar estos problemas sería conveniente ampliar las pruebas y establecer validaciones adicionales al momento de registrar las funciones. En cuanto a los nombres duplicados, una solución sería impedir que se agregue una función cuando su nombre ya se encuentre registrado.
>
> La búsqueda utiliza una estrategia lineal, por lo que su complejidad temporal es O(n), dependiendo de la cantidad de funciones almacenadas. En espacio adicional utiliza O(1), ya que solamente trabaja con variables auxiliares y no necesita crear estructuras adicionales.

---

**Firma digital:** `kirito2906`
