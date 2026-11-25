Bitácora de Requerimientos y Auditoría IA — Sesión 14Materia: Lenguajes y Autómatas II (SCD-1016)Tema: Declaración vs Uso de VariablesDocente Titular: MCC. Iván Márquez Larios (ijmarquezl)Estudiante: Héctor Iván Varguez AndradeMatrícula: 24531321Track: C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)1. Fase 1: El Artesano (Dificultad Manual)Reto: Detección de variables no declaradasDescribe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:Las restricciones que tuve que resolver al codificar a mano fueron:Declaración previa y redeclaración: declarar() solo inserta si el nombre no existe en la tabla y devuelve 1; si ya estaba, devuelve 0 sin modificar tabla->total.Comparación exacta: usar strcmp(...) == 0 para que prefijos o extensiones como "x" y "xy" no se confundan como el mismo nombre.Capacidad fija: la tabla tiene tamaño máximo TABLA_MAX (16), así que hay que validar tabla->total >= TABLA_MAX antes de insertar y devolver -1 si está llena.Entradas inválidas: tabla == NULL, nombre == NULL o cadena vacía (nombre[0] == '\0') devuelven -1 en declarar(); en usar(), punteros NULL o nombres no declarados devuelven 0.Punto en que me atoré: no me atoré.2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)2.1 Matriz de Especificación FormalElemento C-R-E-ODefinición TécnicaContexto (C)C99 / GCC o Rust 2021 sin bibliotecas no estándarRol (R)Ingeniero de software de sistemas y compiladoresEspecificación (E)Invariante de definición previaOutput (O)Solo código modular y análisis de complejidad2.2 Prompt EstructuradoPlaintextContexto: Estoy en C (compilado con gcc -std=c11 -Wall -Wextra -Werror), sin
bibliotecas no estándar. Tengo esta cabecera api_sesion14.h:
  #define TABLA_MAX 16
  typedef struct Tabla { const char *nombres[TABLA_MAX]; int total; } Tabla;

Rol: Eres un ingeniero de software de sistemas y compiladores.

Especificación: Implementa
  int declarar(Tabla *tabla, const char *nombre);
  int usar(const Tabla *tabla, const char *nombre);
- declarar() devuelve 1 si insertó, 0 si el nombre ya estaba y -1 si recibe
  NULL, un nombre vacío o si la tabla está llena (sin modificar total en
  duplicado o error).
- usar() devuelve 1 solo si el nombre ya fue declarado exactamente; en
  cualquier otro caso devuelve 0.
- La comparación es exacta ("x" y "xy" son nombres distintos).
- Usa una función auxiliar estática para buscar el índice.

Output: Solo el código modular del archivo .c, sin main(), con las firmas
exactas, y un breve análisis de complejidad.
3. Código Devuelto por el ModeloC/* ia_sesion14_c.c - Fase 2: El Cientifico
- Version con funcion auxiliar de busqueda.
 */
#include "api_sesion14.h"
#include <string.h>

static int buscar_indice(const Tabla *t, const char *nombre) {
    for (int i = 0; i < t->total; i++) {
        if (strcmp(t->nombres[i], nombre) == 0)
            return i;
    }
    return -1;
}

int declarar(Tabla *tabla, const char *nombre) {
    if (tabla == NULL || nombre == NULL || *nombre == '\0')
        return -1;
    if (buscar_indice(tabla, nombre) >= 0)
        return 0;
    if (tabla->total >= TABLA_MAX)
        return -1;
    tabla->nombres[tabla->total++] = nombre;
    return 1;
}

int usar(const Tabla *tabla, const char *nombre) {
    if (tabla == NULL || nombre == NULL)
        return 0;
    return buscar_indice(tabla, nombre) >= 0;
}
4. Fase 3: El Auditor (Resultados del Test Harness)Pruebas ejecutadas: Uso antes de declarar y redeclaraciónSalida del harnessPlaintext=== AUDITORIA SESION 14 - Declaracion previa y redeclaracion ===
Caso                               esperado:              obtenido:              resultado
[ 1] usar sin declarar                  esperado: 0            obtenido: 0            OK
[ 2] usar despues de declarar           esperado: 1            obtenido: 1            OK
[ 3] redeclarar el mismo nombre         esperado: 0            obtenido: 0            OK
[ 4] total tras redeclarar              esperado: 1            obtenido: 1            OK
[ 5] prefijo no es el mismo nombre      esperado: 0            obtenido: 0            OK
[ 6] declarar nombre vacio              esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion14.md
[x] Caso base y límites superados sin Crash.[x] No existen accesos fuera de límites ni Memory Leaks.[x] La complejidad teórica coincide con la implementada.Reporte Crítico¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?El harness pasó 6/6 con la versión de la IA, pero al revisar el código encontré casos que la IA no contempló y que el harness no prueba:Símbolo NULL dentro de nombres[]: buscar_indice() llama a strcmp sin revisar cada entrada, así que un puntero NULL en el arreglo causaría un fallo de segmentación. Se corregiría validando t->nombres[i] != NULL antes del strcmp.Cadena vacía en usar(): usar() no descarta *nombre == '\0' antes de buscar, por lo que recorre la tabla antes de devolver 0.Nombre sin copia: declarar() guarda el puntero, no una copia de la cadena; si el nombre viene de un buffer temporal, el puntero quedaría colgante.Cómo lo detecté: leyendo el código contra las condiciones de frontera y la compilación con -Wall -Wextra -Werror.Firma digital: [kirito2906]
