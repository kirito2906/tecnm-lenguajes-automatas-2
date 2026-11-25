# Bitácora de Requerimientos y Auditoría IA — Sesión 20

**Materia:** Lenguajes y Autómatas II (SCD-1016)
**Tema:** Hito 2: Analizador Semántico Completo y Scopes
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)
**Estudiante:** Héctor Iván Varguez Andrade
**Matrícula:** 24531321
**Track:** C (el harness evalúa C; la versión en Rust es opcional)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Resolver nombres dentro de diferentes ámbitos y contar los símbolos visibles sin repetirlos.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Las restricciones que tuve que resolver al codificar a mano fueron:
>
> - **Recorrido de ámbitos:** se debe recorrer el ámbito actual y continuar por sus padres hasta encontrar el nombre solicitado.
> - **Profundidad:** el ámbito actual tiene nivel 0 y cada ámbito padre aumenta un nivel.
> - **Shadowing:** cuando un nombre aparece en varios ámbitos, siempre se debe tomar el que está declarado en el ámbito más interno.
> - **Nombres inexistentes:** si el nombre no se encuentra en ningún ámbito, la función debe devolver `-1`.
> - **Argumentos NULL:** si el ámbito o el nombre recibido es NULL, se debe devolver `-2`.
> - **Símbolos visibles:** al contar los nombres disponibles, no se deben repetir los que aparecen en diferentes ámbitos.
> - **Punto en que me atoré:** tuve que tener cuidado al contar los símbolos repetidos, porque un mismo nombre puede aparecer en varios ámbitos y solamente debe contarse una vez.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O       | Definición Técnica                                                                                                                                           |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contexto (C)**       | Programación en C11 utilizando la estructura `Ambito` definida en `api_sesion20.h`, con una cadena de ámbitos relacionados mediante punteros padre.          |
| **Rol (R)**            | Ingeniero de software especializado en compiladores y análisis semántico.                                                                                    |
| **Especificación (E)** | Implementar funciones para encontrar la profundidad de un nombre y contar los símbolos visibles sin duplicados, respetando el shadowing y las entradas NULL. |
| **Output (O)**         | Código modular en C que respete las firmas de `api_sesion20.h`, sin incluir `main()` y que compile sin advertencias.                                         |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy trabajando en C11 con GCC y tengo una
cabecera llamada api_sesion20.h que define la estructura
Ambito, sus símbolos y el puntero al ámbito padre.

Rol: Eres un ingeniero de software especializado en
compiladores y análisis semántico.

Especificación: Implementa las funciones:

int profundidad_de(const Ambito *actual,
                   const char *nombre);
int contar_visibles(const Ambito *actual);

- profundidad_de() debe buscar el nombre desde el
  ámbito actual hacia sus padres.
- El ámbito actual tiene profundidad 0.
- Cada ámbito padre aumenta un nivel.
- Si el nombre aparece en varios ámbitos, debe ganar
  el más interno (shadowing).
- Si el nombre no existe, devuelve -1.
- Si algún argumento es NULL, devuelve -2.
- contar_visibles() debe contar los nombres distintos
  que se pueden ver desde el ámbito actual.
- No debe contar dos veces un mismo nombre aunque
  aparezca en varios ámbitos.
- Respeta la estructura y las firmas exactas de
  api_sesion20.h.
- No incluyas main().
- Utiliza código compatible con -std=c11
  -Wall -Wextra -Werror.

Output: Código completo del archivo .c y un breve
análisis de complejidad.
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

**Análisis de complejidad:**

- `esta_en_lista()`: O(n), porque revisa los nombres que ya se encuentran registrados.
- `profundidad_de()`: O(n), porque recorre los ámbitos y sus símbolos hasta encontrar el nombre.
- `contar_visibles()`: O(n²) en el peor caso, porque revisa los nombres de cada ámbito y compara si ya fueron registrados anteriormente.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Se comprobaron los nombres del ámbito actual, los nombres de ámbitos superiores, el shadowing, los nombres inexistentes, el conteo de símbolos sin repetir y los argumentos NULL.

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

- [x] Se comprobaron los casos base y la resolución de nombres.
- [x] Las seis pruebas se ejecutaron sin errores ni *Crash*.
- [ ] No se realizó una auditoría específica de memoria.
- [x] La complejidad teórica coincide con la implementación.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> El harness pasó las seis pruebas, pero al revisar el código de la IA encontré un detalle que no se contempló completamente:
>
> - **Límite de nombres:** la IA utiliza un arreglo fijo de 256 posiciones llamado `MAX_NOMBRES`. Si existen más de 256 nombres distintos visibles, los nombres adicionales no se agregan y el conteo puede quedar incompleto.
> - **Pruebas adicionales:** el harness no comprueba qué sucede cuando existen más de 256 nombres distintos ni cuando se reciben nombres NULL dentro de los símbolos.
> - **Cómo lo detecté:** revisando el arreglo `vistos` y la condición `n < MAX_NOMBRES`. Identifiqué que el contador tiene un límite fijo que podría afectar programas con muchos símbolos.
> - **Posible solución:** utilizar una estructura que permita almacenar todos los nombres visibles sin depender de un límite fijo de 256 posiciones.

---

**Firma digital:** `kirito2906`
