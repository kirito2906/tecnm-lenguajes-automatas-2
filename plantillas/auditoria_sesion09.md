# Bitácora de Requerimientos y Auditoría IA — Sesión 09
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Reporte Formal de Errores Semánticos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Diagnóstico con línea y columna  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo que más me costó fue respetar el límite del buffer para no escribir más de cap-1 caracteres y que el resultado siempre quedara terminado con el caracter nulo por eso usé snprintf en lugar de sprintf también tuve que cuidar que el formato fuera exacto sin espacios extra ni punto final y revisar que salida no fuera NULL

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Estructura estándar de errores GCC |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Trabajo en C99 con GCC y la cabecera api_sesion09.h que declara void reportar(const char *archivo int linea int columna const char *mensaje char *salida int cap)
Rol: Actúa como ingeniero de software de sistemas y compiladores
Especificación: Implementa reportar para que arme en el buffer salida el texto archivo:linea:columna: error: mensaje con el formato exacto del estilo de GCC sin espacios extra ni punto final nunca escribas más de cap-1 caracteres y el resultado siempre debe terminar en el caracter nulo
Output: Entrega solo el código modular en C sin main con la misma firma del encabezado y un análisis breve de complejidad
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion09_c.c - Fase 2: El Cientifico
 * Propuesta de la IA con la misma firma de api_sesion09.h
 */
#include <stdio.h>
#include "api_sesion09.h"

void reportar(const char *archivo, int linea, int columna, const char *mensaje, char *salida, int cap) {
    const char *arch = (archivo != NULL) ? archivo : "(null)";
    const char *msg = (mensaje != NULL) ? mensaje : "(null)";

    if (salida == NULL || cap <= 0) {
        return;
    }

    snprintf(salida, (size_t)cap, "%s:%d:%d: error: %s", arch, linea, columna, msg);
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Múltiples errores sin abortar parser

### Salida del harness
```text
=== AUDITORIA SESION 09 - Diagnostico con linea y columna ===
Caso                               esperado:              obtenido:              resultado
[ 1] main.c:14:5
     esperado: main.c:14:5: error: tipo incompatible
     obtenido: main.c:14:5: error: tipo incompatible
     -> OK
[ 2] a.c:1:1
     esperado: a.c:1:1: error: x
     obtenido: a.c:1:1: error: x
     -> OK
[ 3] linea 0
     esperado: x.c:0:0: error: y
     obtenido: x.c:0:0: error: y
     -> OK
[ 4] cap=10 trunca                      esperado: main.c:14    obtenido: main.c:14    OK

RESULTADO: 4/4 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion09.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> El caso borde que suele omitir la IA es cuando cap es cero o negativo porque un cap negativo al convertirse a size_t se vuelve un número enorme y snprintf escribiría fuera del buffer y con cap cero no se debe escribir nada ni siquiera el caracter nulo también faltan los punteros NULL en archivo mensaje y salida el harness no prueba nada de eso lo detecté agregando casos extra con cap=0 cap=-1 y mensaje=NULL y lo solucioné revisando salida y cap al inicio de la función y poniendo (null) cuando archivo o mensaje son NULL

---
**Firma digital:** [Kirito2906]
