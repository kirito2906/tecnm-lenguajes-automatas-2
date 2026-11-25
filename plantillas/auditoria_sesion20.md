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

> Lo que más me costó fue `contar_visibles`, porque un nombre que aparece en varios ámbitos solamente debe contarse una vez. `profundidad_de` fue más directa: comienzo desde el ámbito actual y voy subiendo por los `padre` con un contador de nivel, así el shadowing funciona correctamente (si `x` está en el bloque actual y también en el global, regresa 0). Para contar los nombres utilicé una lista de los símbolos que ya fueron encontrados, evitando que se repitan. También tuve que considerar las entradas `NULL`, porque no se pueden comparar directamente con `strcmp`. Otro detalle que identifiqué fue que el arreglo utilizado por la IA tiene un límite de 256 nombres, por lo que puede dejar de contar si se supera esa cantidad. Los argumentos `NULL` regresan -2 en las funciones correspondientes y un nombre que no existe regresa -1.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| **Elemento C-R-E-O**   | **Definición Técnica**                            |
| ---------------------- | ------------------------------------------------- |
| **Contexto (C)**       | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)**            | Ingeniero de software de sistemas y compiladores  |
| **Especificación (E)** | Contrato de Validación Semántica Integral         |
| **Output (O)**         | Solo código modular y análisis de complejidad     |

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

*Pruebas ejecutadas:* Casos complejos de shadowing y ámbito

### Salida del harness

```text
=== AUDITORIA SESION 20 - Resolucion de nombres y visibilidad ===
Caso                               esperado:              obtenido:              resultado
[ 1] nombre en el ambito actual         esperado: 0            obtenido: 0            OK
[ 2] nombre dos niveles arriba          esperado: 2            obtenido: 2            OK
[ 3] shadowing gana el interno          esperado: 0            obtenido: 0            OK
[ 4] nombre no visible                  esperado: -1           obtenido: -1           OK
[ 5] visibles sin repetir               esperado: 3            obtenido: 3            OK
[ 6] ambito NULL                        esperado: -2           obtenido: -2            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion20.md
```

- [x] Caso base y límites superados sin *Crash*. (en los casos del harness; el reporte describe una limitación fuera de ellos)
- [x] Se comprueba que las entradas de símbolos NULL se ignoran antes de compararlas.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> La IA pasó los 6 casos, pero encontré una limitación importante. El primero es que `contar_visibles` guarda los nombres en un arreglo fijo `vistos[256]` y, cuando se llena, deja de registrar los siguientes nombres. Lo identifiqué al revisar la condición `n < MAX_NOMBRES`, porque si existen más de 256 símbolos diferentes el resultado puede quedar incompleto. El contrato no establece un límite de 256 nombres visibles, por lo que esto puede provocar un resultado incorrecto. La posible solución sería utilizar memoria dinámica para almacenar todos los nombres sin depender de un arreglo fijo. También revisé el manejo de las entradas `NULL` y comprobé que el código sí las omite antes de realizar las comparaciones con `strcmp`. Complejidad: `profundidad_de` es O(p·k) y `contar_visibles` es O((p·k)²), donde p es la profundidad y k ≤ 8 los símbolos por ámbito. El espacio auxiliar de la IA es O(1), porque utiliza un arreglo fijo de 256 posiciones.

---

**Firma digital:** `kirito2906`
