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

> Una de las dificultades que encontré fue organizar las validaciones para que el programa pudiera identificar correctamente los errores relacionados con los tipos de retorno y las rutas de ejecución. Primero tuve que establecer una forma de comparar los tipos de datos, utilizando una tabla con diferentes niveles de ancho: `char`, `int`, `long`, `float` y `double`. De esta manera, una función puede aceptar un tipo de origen cuando su tipo de destino tiene un ancho igual o mayor.
>
> También tuve que considerar algunos casos especiales:
>
> - Una función de tipo `void` no debe devolver un valor, por lo que es necesario comprobar el tipo de la expresión.
> - Si una expresión tiene un tipo incompatible con el de la función, se debe devolver 1.
> - Cuando alguna ruta de ejecución no contiene un retorno, el resultado debe ser 2.
> - Si todos los tipos son compatibles y las rutas están completas, la función debe regresar 0.
> - Las entradas con tipos `NULL`, cero rutas o cantidades incoherentes deben identificarse como inválidas y devolver -1.
>
> Lo que más trabajo me dio fue establecer el orden de las condiciones, porque primero se debe revisar la compatibilidad de los tipos y después comprobar las rutas de ejecución. Así se evita confundir un error de tipo con una ruta que no tiene una sentencia `return`.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC con bibliotecas estándar, utilizando una tabla de tipos y datos sobre las rutas de ejecución. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y compiladores. |
| **Especificación (E)** | Comprobación de compatibilidad entre tipos de retorno y validación de que las rutas de ejecución cumplan con las condiciones de retorno. |
| **Output (O)** | Código modular en C, respetando la interfaz de `api_sesion17.h`, sin `main()` y acompañado de un análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO: Trabajar con C11 utilizando GCC y las opciones
-Wall -Wextra -Werror, empleando únicamente bibliotecas estándar.
Se dispone del archivo api_sesion17.h, que contiene la
declaración de diagnosticar_retorno().

ROL: Actúa como un ingeniero de software con conocimientos
en sistemas y desarrollo de compiladores.

ESPECIFICACIÓN: Implementa la función encargada de verificar
los tipos de retorno y las rutas de ejecución.

- Devuelve 0 cuando los tipos sean compatibles y todas
  las rutas tengan un retorno.
- Devuelve 1 cuando exista incompatibilidad entre los tipos.
- Devuelve 2 cuando al menos una ruta no tenga retorno.
- Devuelve -1 cuando los tipos sean NULL, existan cero
  rutas, los conteos sean incoherentes o se encuentre
  un tipo que no esté registrado.
- Una función void no debe devolver expresiones con valor.
- Utiliza una tabla para identificar los tipos y sus anchos.
- Acepta conversiones cuando el tipo destino tenga
  un ancho igual o mayor al tipo de origen.
- Realiza primero la comprobación de tipos y después
  la validación de las rutas.
- Conserva exactamente la firma definida en api_sesion17.h.
- No incluyas main().

OUTPUT: Entrega únicamente el código modular en C y un
análisis breve de su complejidad temporal y espacial.
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

*Pruebas ejecutadas:* Compatibilidad entre tipos de retorno, funciones `void`, comprobación de rutas incompletas y validación de cero rutas de ejecución.

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

* [x] Caso base y límites contemplados en las pruebas superadas sin *Crash*.
* [x] No se observaron fallos durante las pruebas realizadas.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> La IA logró superar las seis pruebas del harness, pero al revisar su funcionamiento encontré algunas situaciones que sería importante comprobar con pruebas adicionales:
>
> - **Tipos no registrados:** la tabla solamente contiene `char`, `int`, `long`, `float` y `double`. Si se utiliza otro tipo, como `short`, la función devuelve -1. Sería conveniente ampliar la tabla para reconocer otros tipos de datos permitidos.
> - **Entradas NULL:** el código comprueba si los nombres de los tipos son NULL, pero no se realizaron pruebas individuales para verificar cada una de estas condiciones.
> - **Conteos de rutas:** también sería necesario probar cantidades negativas de retornos y casos donde las rutas con retorno sean mayores que las rutas totales.
> - **Funciones void:** observé que cuando la función y la expresión son de tipo `void`, el programa devuelve 0 directamente, sin comprobar si todas las rutas tienen retorno. Esto puede ser válido dependiendo de cómo se interprete la sentencia `return` en una función void, pero sería conveniente confirmar ese comportamiento con el docente.
>
> Al revisar estas condiciones pude identificar que las seis pruebas realizadas no cubren todos los posibles casos de la función. Para mejorar la implementación sería necesario agregar más pruebas y revisar las validaciones especiales, principalmente las relacionadas con los tipos desconocidos y las funciones sin valor de retorno.
>
> La complejidad temporal es O(1), porque la búsqueda se realiza sobre una tabla de tipos de tamaño fijo. El espacio adicional también es O(1), ya que no se crean estructuras dinámicas ni se necesita memoria adicional durante la ejecución.

---

**Firma digital:** `kirito2906`
