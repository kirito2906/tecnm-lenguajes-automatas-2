# Bitácora de Requerimientos y Auditoría IA — Sesión 11
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Arquitectura de la Tabla de Símbolos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Tabla Hash con encadenamiento  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo más difícil fue cuidar que no se duplicara ningún nombre porque había que recorrer toda la cadena de la cubeta antes de crear el nodo nuevo y además copiar el nombre al campo de 16 bytes sin pasarme del tamaño también tuve que validar que las cubetas no fueran cero antes de sacar el módulo para evitar una división entre cero y que cuando hay colisión el nodo nuevo se enlace sin perder los que ya estaban

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Función de dispersión y colisiones O(1) |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy construyendo la tabla de símbolos de un compilador en C11 como tabla hash con encadenamiento. La estructura es Simbolo con nombre[16], tipo, offset y sig, declarada en api_sesion11.h.
Rol: Actúa como ingeniero de software de sistemas y compiladores.
Especificación: Implementa unsigned int hash_djb2(const char *clave), que empieza en 5381 y multiplica por 33 en cada byte, e int insertar_simbolo(Simbolo *tabla[], unsigned int cubetas, const char *nombre, int tipo, int offset). insertar_simbolo devuelve 1 si insertó, 0 si el nombre ya existía en cualquier cubeta y -1 si tabla es NULL, nombre es NULL o cubetas es 0. Una colisión se encadena y nunca se sobrescribe una entrada existente. Debe compilar con -Wall -Wextra -Werror y no debe tener main().
Output: Solo código C modular con las firmas idénticas a api_sesion11.h y un análisis breve de la complejidad.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion11.h"
#include <stdlib.h>
#include <string.h>

unsigned int hash_djb2(const char *clave) {
    unsigned int hash = 5381;
    int c;
    if (!clave) return 0;
    while ((c = (unsigned char)*clave++))
        hash = hash * 33 + c;
    return hash;
}

int insertar_simbolo(Simbolo *tabla[], unsigned int cubetas, const char *nombre, int tipo, int offset) {
    if (!tabla || !nombre || cubetas == 0) return -1;

    unsigned int idx = hash_djb2(nombre) % cubetas;

    for (Simbolo *p = tabla[idx]; p; p = p->sig)
        if (strcmp(p->nombre, nombre) == 0) return 0;

    Simbolo *nuevo = malloc(sizeof(Simbolo));
    if (!nuevo) return -1;

    strcpy(nuevo->nombre, nombre);
    nuevo->tipo = tipo;
    nuevo->offset = offset;
    nuevo->sig = tabla[idx];
    tabla[idx] = nuevo;
    return 1;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Manejo de claves duplicadas y colisiones

### Salida del harness
```text
=== AUDITORIA SESION 11 - Tabla hash con encadenamiento ===
Caso                               esperado:              obtenido:              resultado
[ 1] hash_djb2("")                      esperado: 5381         obtenido: 5381         OK
[ 2] hash_djb2("abc")                   esperado: 193485963    obtenido: 193485963    OK
[ 3] insertar x dos veces               esperado: 0            obtenido: 0            OK
[ 4] dos claves, una cubeta             esperado: 2            obtenido: 2            OK
[ 5] offset de beta en cadena           esperado: 4            obtenido: 4            OK
[ 6] insertar en tabla NULL             esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion11.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA pasó los 6 casos pero usó strcpy para copiar el nombre al campo de 16 bytes sin limitar la longitud así que con un nombre de más de 15 caracteres se desborda el arreglo y escribe fuera del nodo el harness no tiene ningún caso con nombres largos y por eso salió en verde lo detecté insertando un nombre largo y compilando con fsanitize address que marcó el desbordamiento en el heap lo solucioné copiando con strncpy y cerrando el último byte con el carácter nulo además los nodos se reservan con malloc y el contrato de la sesión no incluye una función para liberarlos así que quedan sin liberar al terminar el programa

---
**Firma digital:** [kirito2906]
