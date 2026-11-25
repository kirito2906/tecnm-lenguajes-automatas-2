# Bitácora de Requerimientos y Auditoría IA — Sesión 13
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Manejo de Ámbitos (Scope Global/Local)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Pila de tablas de símbolos (Stack Scopes)  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Las restricciones que tuve que resolver al codificar a mano fueron:
> - **Shadowing:** `declarar()` solo revisa el ámbito actual y no consulta a los padres, de modo que el mismo nombre puede existir una vez en cada nivel.
> - **Límite de memoria:** cada ámbito guarda como máximo `AMBITO_MAX` (8) nombres en un arreglo fijo, así que hay que validar `total >= AMBITO_MAX` antes de insertar y devolver -1.
> - **Entradas inválidas:** ámbito `NULL`, nombre `NULL` o nombre vacío devuelven -1 en `declarar()`; en `buscar()` un nombre `NULL` devuelve `NULL`.
> - **Qué se devuelve:** `buscar()` regresa el nombre del ámbito más cercano que declara el símbolo, no el símbolo, y sube por `padre` hasta la raíz.
> - **Punto en que me atoré:** [escribe aquí en qué te atoraste realmente, o "no me atoré"]

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Ocultamiento de variables (Shadowing) |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy en C (compilado con gcc -std=c11 -Wall -Wextra -Werror), sin
bibliotecas no estándar. Tengo esta cabecera api_sesion13.h:
  #define AMBITO_MAX 8
  typedef struct Ambito { const char *nombre; const char *nombres[AMBITO_MAX];
                          int total; struct Ambito *padre; } Ambito;

Rol: Eres un ingeniero de software de sistemas y compiladores.

Especificación: Implementa
  int declarar(Ambito *ambito, const char *nombre);
  const char *buscar(const Ambito *ambito, const char *nombre);
- declarar() guarda el nombre solo en el ámbito actual, sin consultar a los
  padres (permite shadowing). Devuelve 1 si insertó, 0 si el nombre ya estaba
  en ese ámbito y -1 si el ámbito está lleno o recibe NULL o nombre vacío.
- buscar() empieza en el ámbito actual y sube por padre hasta la raíz.
  Devuelve el nombre del ámbito más cercano que declara el símbolo (no el
  símbolo). Si no existe, devuelve NULL.
- Usa un helper para la búsqueda dentro de un ámbito y recursión en buscar().

Output: Solo el código modular del archivo .c, sin main(), con las firmas
exactas, y un breve análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion13_c.c - Fase 2: El Cientifico
 * Version con helper y recursion.
 */
#include "api_sesion13.h"
#include <string.h>

static int esta_en_ambito(const Ambito *a, const char *nombre) {
    for (int i = 0; i < a->total; i++) {
        if (strcmp(a->nombres[i], nombre) == 0)
            return 1;
    }
    return 0;
}

int declarar(Ambito *ambito, const char *nombre) {
    if (ambito == NULL || nombre == NULL || *nombre == '\0')
        return -1;
    if (esta_en_ambito(ambito, nombre))
        return 0;
    if (ambito->total >= AMBITO_MAX)
        return -1;
    ambito->nombres[ambito->total++] = nombre;
    return 1;
}

const char *buscar(const Ambito *ambito, const char *nombre) {
    if (ambito == NULL || nombre == NULL)
        return NULL;
    if (esta_en_ambito(ambito, nombre))
        return ambito->nombre;
    return buscar(ambito->padre, nombre);
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Búsqueda jerárquica de identificadores

### Salida del harness
```text
=== AUDITORIA SESION 13 - Pila de ambitos y busqueda jerarquica ===
Caso                               esperado:              obtenido:              resultado
[ 1] declarar(&g, "x")                  esperado: 1            obtenido: 1            OK
[ 2] buscar en el mismo ambito          esperado: global       obtenido: global       OK
[ 3] buscar subiendo al padre           esperado: global       obtenido: global       OK
[ 4] shadowing en el hijo               esperado: bloque       obtenido: bloque       OK
[ 5] tres niveles hasta la raiz         esperado: raiz         obtenido: raiz         OK
[ 6] nombre no declarado                esperado: (nulo)       obtenido: (nulo)       OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion13.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> El harness pasó 6/6 con la versión de la IA, pero al revisar el código encontré casos que la IA no contempló y que el harness no prueba:
> - **Símbolo `NULL` dentro de `nombres[]`:** `esta_en_ambito()` llama a `strcmp` sin revisar cada entrada, así que un puntero `NULL` en el arreglo causaría un fallo de segmentación. Se corregiría con `a->nombres[i] != NULL &&` antes del `strcmp`.
> - **Recursión sin límite:** `buscar()` recursivo usa una llamada por nivel; una cadena de ámbitos muy larga o con un ciclo en `padre` no terminaría o desbordaría la pila. La versión iterativa del Artesano evita el desborde.
> - **Nombre sin copia:** `declarar()` guarda el puntero, no una copia de la cadena; si el nombre viene de un buffer temporal, el puntero quedaría colgante.
> - **Cómo lo detecté:** leyendo el código contra los criterios de aceptación y comparando la versión de la IA con la mía. [Si además ejecutaste pruebas para confirmarlo, anótalo aquí.]

---
**Firma digital:** [kirito2906]
