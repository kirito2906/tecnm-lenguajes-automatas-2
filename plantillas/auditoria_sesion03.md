# Bitácora de Requerimientos y Auditoría IA — Sesión 03
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Google Colab, Mágicos y Flujo de Entrega  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Manipulación de archivos y llamadas OS  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más me costó fue acordarme de que una última línea sin salto de línea también cuenta como línea y no basta con contar los saltos que encuentra el programa
> También tuve que cuidar que el archivo se cierre en todos los caminos con fclose y que una ruta que no se puede abrir devuelva -1 en lugar de dejar que el programa se caiga

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Salida estándar y códigos de retorno ABI |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy programando en C11 y compilo con gcc -Wall -Wextra -Werror
El archivo no debe tener main() porque el main es de un harness externo
Debo respetar la cabecera api_sesion03.h

Rol: Actúa como programador de C especializado en manejo de archivos y casos borde

Especificación:
- int escribir_texto(const char *ruta, const char *texto) devuelve 0 si escribe bien y -1 si no puede abrir la ruta
- int contar_lineas(const char *ruta) devuelve el número de líneas
- La última línea sin salto de línea también cuenta
- Un archivo vacío devuelve 0
- Un archivo inexistente devuelve -1 y no debe abortar
- Cerrar siempre el archivo con fclose

Output: Solo el código en C con las dos funciones sin explicación y con la misma firma de la cabecera
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion03.h"
#include <stdio.h>

int escribir_texto(const char *ruta, const char *texto) {
    FILE *f;

    if (ruta == NULL || texto == NULL) {
        return -1;
    }
    f = fopen(ruta, "w");
    if (f == NULL) {
        return -1;
    }
    if (fputs(texto, f) < 0) {
        fclose(f);
        return -1;
    }
    if (fclose(f) != 0) {
        return -1;
    }
    return 0;
}

int contar_lineas(const char *ruta) {
    FILE *f;
    int c;
    int prev = '\n';
    int lineas = 0;

    if (ruta == NULL) {
        return -1;
    }
    f = fopen(ruta, "r");
    if (f == NULL) {
        return -1;
    }
    while ((c = fgetc(f)) != EOF) {
        if (c == '\n') {
            lineas++;
        }
        prev = c;
    }
    fclose(f);
    if (prev != '\n') {
        lineas++;
    }
    return lineas;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Detección de errores de compilación GCC

### Salida del harness
```text
=== AUDITORIA SESION 03 - Archivos: escribir y contar lineas ===
Caso                                 esperado:              obtenido:              resultado
[ 1] escribir_texto(...)==0          esperado: 0            obtenido: 0            OK
[ 2] contar_lineas(3 lineas)         esperado: 3            obtenido: 3            OK
[ 3] contar_lineas(sin salto final)  esperado: 2            obtenido: 2            OK
[ 4] contar_lineas(archivo vacio)    esperado: 0            obtenido: 0            OK
[ 5] contar_lineas(inexistente)      esperado: -1           obtenido: -1           OK
[ 6] escribir_texto(ruta invalida)   esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion03.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA no omitió ningún caso borde porque en el contrato le pedí de forma explícita el archivo vacío el archivo sin salto final y la ruta inexistente y su código los resolvió igual que mi versión
> Incluso agregó una validación de punteros NULL que yo no había puesto
> Lo detecté ejecutando el harness con las dos versiones y comparando que las 6 líneas salieran en OK además de revisar que ambas cierren el archivo con fclose en todos los caminos
> La complejidad es O(n) en las dos porque solo recorren el archivo una vez

---
**Firma digital:** kirito2906
