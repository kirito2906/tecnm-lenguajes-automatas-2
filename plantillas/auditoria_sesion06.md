# Bitácora de Requerimientos y Auditoría IA — Sesión 06
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Sistema de Tipos Primitivos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Chequeo de compatibilidad de tipos  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo más difícil fue decidir cómo comparar los tipos sin escribir un montón de condiciones y me di cuenta de que el enum ya trae los valores 1 2 y 3 en orden de menor a mayor así que bastaba comparar destino mayor o igual que origen pero TIPO_ERROR vale 0 y eso lo dejaría pasar en algunos casos por eso lo rechacé primero antes de comparar en nombre_tipo usé un switch con un default de desconocido para no devolver basura con un valor fuera del enum también tuve un atoro con Colab porque me marcó SyntaxError al no poner la línea %%writefile al inicio de la celda y después se me sobrescribió el archivo al volver a ejecutar la celda con el TODO y tuve que pegar otra vez mi código

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Matriz de compatibilidad estática |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: estoy en un curso de Lenguajes y Autómatas II implementando un verificador de tipos en C sin bibliotecas no estándar el archivo incluye api_sesion06.h con el enum Tipo donde TIPO_ERROR vale 0 TIPO_CHAR vale 1 TIPO_INT vale 2 y TIPO_FLOAT vale 3
Rol: eres un ingeniero de software de sistemas y compiladores
Especificación: implementa int compatible(Tipo destino Tipo origen) y const char *nombre_tipo(Tipo t) con la jerarquía CHAR menor que INT menor que FLOAT rechaza asignar a un tipo más angosto y trata TIPO_ERROR como incompatible con todo sin main y con las firmas idénticas al header debe compilar con Wall Wextra y Werror
Output: solo el código C modular y un breve análisis de complejidad
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion06.h"

static int rango(Tipo t) {
    switch (t) {
        case TIPO_CHAR:  return 1;
        case TIPO_INT:   return 2;
        case TIPO_FLOAT: return 3;
        default:         return 0;
    }
}

int compatible(Tipo destino, Tipo origen) {
    int rd = rango(destino);
    int ro = rango(origen);

    if (rd == 0 || ro == 0) {
        return 0;
    }
    return rd >= ro ? 1 : 0;
}

const char *nombre_tipo(Tipo t) {
    switch (t) {
        case TIPO_CHAR:  return "char";
        case TIPO_INT:   return "int";
        case TIPO_FLOAT: return "float";
        case TIPO_ERROR: return "error";
        default:         return "desconocido";
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Rechazo de asignaciones incompatibles

### Salida del harness
```text
=== AUDITORIA SESION 06 - Tabla de compatibilidad de tipos ===
Caso                               esperado:              obtenido:              resultado
[ 1] compatible(INT,INT)                esperado: 1            obtenido: 1            OK
[ 2] compatible(FLOAT,INT)              esperado: 1            obtenido: 1            OK
[ 3] compatible(INT,FLOAT)              esperado: 0            obtenido: 0            OK
[ 4] compatible(INT,ERROR)              esperado: 0            obtenido: 0            OK
[ 5] nombre_tipo(INT)                   esperado: int          obtenido: int          OK
[ 6] nombre_tipo(ERROR)                 esperado: error        obtenido: error        OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion06.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> El caso borde que más fácil se omite es compatible(TIPO_ERROR TIPO_ERROR) porque TIPO_ERROR vale 0 y una comparación simple de destino mayor o igual que origen daría 1 y aceptaría un error como si fuera compatible el harness solo prueba compatible(INT ERROR) así que no lo detecta lo revisé probando aparte ese caso y también nombre_tipo con un valor fuera del enum y confirmé que la versión de la IA lo resuelve con la función rango que devuelve 0 para cualquier tipo inválido y mi versión lo resuelve rechazando TIPO_ERROR antes de comparar en ambas la complejidad es O(1) porque solo hay comparaciones y un switch sin ciclos ni memoria dinámica

---
**Firma digital:** [kirito2906]
