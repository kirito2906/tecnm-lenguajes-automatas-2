# Bitácora de Requerimientos y Auditoría IA — Sesión 24
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Control de Flujo: Sentencia if-else  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Héctor Iván Varguez Andrade  
**Matrícula:** 24531321  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Saltos condicionales y evaluación booleana  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Tuve que tener cuidado con el operador lógico para generar el salto correcto. También revisé que cada instrucción tuviera espacio suficiente en el arreglo y que, cuando el segundo operando fuera NULL, solamente se generara un salto.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Cortocircuito lógico en expresiones |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto:
Estoy trabajando en Lenguajes y Autómatas II y necesito implementar una función en C para generar saltos condicionales.

Rol:
Actúa como un ingeniero de software especializado en C y compiladores.

Especificación:
Implementa la función emitir_condicion con esta firma:
int emitir_condicion(char lineas[][64], int max, const char *a, const char *b, char op, const char *etiqueta);

La función debe:
- Usar IFFALSE cuando el operador sea '&'.
- Usar IFTRUE cuando el operador sea '|'.
- Generar un salto para el primer operando.
- Generar un segundo salto únicamente si b no es NULL.
- Utilizar el formato "IFFALSE operando GOTO etiqueta" o "IFTRUE operando GOTO etiqueta".
- Validar los parámetros recibidos.
- Comprobar que el arreglo tenga espacio suficiente.
- Utilizar snprintf para evitar desbordamientos.
- Respetar la firma original y no incluir main().

Output:
Entrega el código modular en C y respeta todas las condiciones indicadas.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion24.h"
#include <stdio.h>

static int crear_salto(char destino[64],
                       const char *tipo,
                       const char *operando,
                       const char *etiqueta) {

    if (destino == NULL || tipo == NULL ||
        operando == NULL || etiqueta == NULL) {
        return 0;
    }

    int resultado = snprintf(destino, 64,
                             "%s %s GOTO %s",
                             tipo, operando, etiqueta);

    if (resultado < 0 || resultado >= 64) {
        destino[0] = '\0';
        return 0;
    }

    return 1;
}

int emitir_condicion(char lineas[][64], int max,
                     const char *a, const char *b,
                     char op, const char *etiqueta) {

    if (lineas == NULL || max <= 0 ||
        a == NULL || etiqueta == NULL ||
        (op != '&' && op != '|')) {
        return 0;
    }

    int cantidad = 1;

    if (b != NULL) {
        cantidad = 2;
    }

    if (max < cantidad) {
        return 0;
    }

    const char *tipo = (op == '&') ? "IFFALSE" : "IFTRUE";

    if (!crear_salto(lineas[0], tipo, a, etiqueta)) {
        return 0;
    }

    if (b != NULL) {
        if (!crear_salto(lineas[1], tipo, b, etiqueta)) {
            lineas[0][0] = '\0';
            lineas[1][0] = '\0';
            return 0;
        }
    }

    return cantidad;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Condiciones compuestas con AND y OR

### Salida del harness
```text
=== AUDITORIA SESION 24 - Saltos condicionales con cortocircuito ===
Caso                               esperado:              obtenido:              resultado
[ 1] a && b (primer salto)
     esperado: IFFALSE a GOTO L9
     obtenido: IFFALSE a GOTO L9
     -> OK
[ 2] a && b (segundo salto)
     esperado: IFFALSE b GOTO L9
     obtenido: IFFALSE b GOTO L9
     -> OK
[ 3] a && b (dos saltos)                esperado: 2            obtenido: 2            OK
[ 4] a || b (primer salto)
     esperado: IFTRUE a GOTO L9
     obtenido: IFTRUE a GOTO L9
     -> OK
[ 5] a || b (segundo salto)
     esperado: IFTRUE b GOTO L9
     obtenido: IFTRUE b GOTO L9
     -> OK
[ 6] condicion simple (b NULL)
     esperado: IFFALSE a GOTO L0
     obtenido: IFFALSE a GOTO L0
     -> OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion24.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> Revisé principalmente el caso en el que el segundo operando es NULL, porque no se debe generar un segundo salto. También comprobé que el arreglo tuviera espacio suficiente para guardar las instrucciones. Al ejecutar el harness, los seis casos pasaron correctamente.

---
**Firma digital:** [Usuario de GitHub]
