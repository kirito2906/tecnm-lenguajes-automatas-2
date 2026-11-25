# Bitácora de Requerimientos y Auditoría IA — Sesión 20

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Hito 2: Analizador Semántico y Scopes  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Integración de Tabla de Símbolos y AST

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar esta parte, noté que las dos funciones necesitaban recorridos diferentes. En `profundidad_de` debía revisar primero el ámbito actual y después continuar con sus padres, aumentando el nivel en cada recorrido para identificar correctamente dónde se encontraba el nombre. Para `contar_visibles`, el reto fue evitar que los identificadores repetidos aumentaran el resultado. Por eso consideré utilizar un arreglo auxiliar que conservara los nombres encontrados y permitiera comprobar si ya habían sido registrados. También tuve que cuidar que los espacios con valor `NULL` no llegaran a compararse mediante `strcmp`. Una restricción que identifiqué fue que el arreglo auxiliar solamente puede guardar 256 nombres, lo cual podría afectar el resultado cuando se supera esa cantidad. Finalmente, tomé en cuenta los valores especiales del contrato: -2 para argumentos NULL y -1 cuando no se encuentra el identificador.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Contrato de Validación Semántica Integral |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
CONTEXTO: C11 con GCC (-Wall -Wextra -Werror), solo libc. La cabecera
api_sesion20.h define:
  #define AMBITO_MAX 8
  typedef struct Ambito { const char *nombre; const char *simbolos[AMBITO_MAX];
                          int total; struct Ambito *padre; } Ambito;
  int profundidad_de(const Ambito *actual, const char *nombre);
  int contar_visibles(const Ambito *actual);

ROL: Ingeniero de software de sistemas y compiladores.

ESPECIFICACIÓN: Resolución de nombres con shadowing (Hito 2).
 - profundidad_de: niveles hacia arriba donde está el nombre (0 = actual);
   -1 si no existe; -2 si algún argumento es NULL. El más interno gana.
 - contar_visibles: nombres distintos visibles desde el actual; cada nombre
   cuenta una sola vez aunque esté en varios ámbitos.
 - Ignorar las entradas de símbolos NULL.
 - Respetar AMBITO_MAX y las firmas originales.
 - Sin main() y sin cambiar las firmas.

OUTPUT: Solo código C modular y un análisis breve de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion20_c.c - Fase 2: El Cientifico */
#include "api_sesion20.h"
#include <string.h>

#define MAX_NOMBRES 256

static int esta_en_lista(const char *lista[], int n,
                         const char *s) {
    for (int i = 0; i < n; i++) {
        if (strcmp(lista[i], s) == 0)
            return 1;
    }
    return 0;
}

int profundidad_de(const Ambito *actual,
                   const char *nombre) {
    if (actual == NULL || nombre == NULL)
        return -2;

    int nivel = 0;
    const Ambito *a = actual;

    while (a != NULL) {
        int limite = a->total < AMBITO_MAX
                   ? a->total : AMBITO_MAX;

        for (int i = 0; i < limite; i++) {
            if (a->simbolos[i] != NULL &&
                strcmp(a->simbolos[i], nombre) == 0)
                return nivel;
        }

        a = a->padre;
        nivel++;
    }

    return -1;
}

int contar_visibles(const Ambito *actual) {
    if (actual == NULL)
        return -2;

    const char *vistos[MAX_NOMBRES];
    int n = 0;

    for (const Ambito *a = actual;
         a != NULL; a = a->padre) {

        int limite = a->total < AMBITO_MAX
                   ? a->total : AMBITO_MAX;

        for (int i = 0; i < limite; i++) {
            const char *s = a->simbolos[i];

            if (s == NULL)
                continue;

            if (!esta_en_lista(vistos, n, s) &&
                n < MAX_NOMBRES) {
                vistos[n++] = s;
            }
        }
    }

    return n;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Casos complejos de shadowing y ámbito.

### Salida del harness

```text
=== AUDITORIA SESION 20 - Resolucion de nombres y visibilidad ===
Caso                               esperado:              obtenido:              resultado
[ 1] nombre en el ambito actual         esperado: 0            obtenido: 0            OK
[ 2] nombre dos niveles arriba          esperado: 2            obtenido: 2            OK
[ 3] shadowing gana el interno          esperado: 0            obtenido: 0            OK
[ 4] nombre no visible                  esperado: -1           obtenido: -1           OK
[ 5] visibles sin repetir               esperado: 3            obtenido: 3            OK
[ 6] ambito NULL                        esperado: -2           obtenido: -2           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion20.md
```

- [x] Caso base y límites superados sin *Crash*. (en los casos del harness; el reporte describe una limitación fuera de ellos)
- [x] Se comprobó el tratamiento de los símbolos NULL antes de realizar comparaciones.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al analizar la solución generada, encontré que `contar_visibles` depende de un arreglo auxiliar con capacidad para 256 identificadores. El inconveniente aparece cuando se tienen más nombres diferentes que los que permite almacenar, porque la función deja de agregar elementos al llegar al límite y devuelve una cantidad incompleta. Aunque las seis pruebas del harness fueron satisfactorias, este escenario representa una situación que no queda cubierta por ellas. Para evitar esa restricción, se podría modificar la implementación y utilizar memoria dinámica, de manera que el almacenamiento no dependa de una cantidad establecida previamente. También revisé el tratamiento de los símbolos NULL y observé que se descartan antes de compararlos, por lo que no representan un problema en el código recibido.

> Respecto a la complejidad, `profundidad_de` tiene un costo temporal O(p·k), porque puede recorrer todos los ámbitos y revisar sus símbolos. En `contar_visibles` el costo es O((p·k)²), debido a que cada identificador nuevo se compara con los que ya fueron almacenados. El espacio auxiliar es O(1), ya que utiliza un arreglo de tamaño fijo de 256 posiciones.

---

**Firma digital:** `[kirito2906]`
