# 📝 Análisis: Gramática MiniLang y Driver.py

## 1. ¿Qué es ANTLR?

**ANTLR** (ANother Tool for Language Recognition) es un generador de analizadores. A
partir de una gramática escrita en un archivo `.g4`, genera automáticamente el código de
un **lexer** (analizador léxico) y un **parser** (analizador sintáctico). En este
laboratorio genera código Python.

---

## 2. Estructura de un archivo `.g4`

Un archivo de gramática ANTLR se compone principalmente de:

1. **Declaración de la gramática:** `grammar MiniLang;` — el nombre debe coincidir con el
   nombre del archivo (`MiniLang.g4`).
2. **Reglas del parser (sintaxis):** empiezan con **minúscula** (`prog`, `stat`, `expr`).
   Describen *cómo se combinan* los tokens para formar estructuras válidas.
3. **Reglas del lexer (tokens):** empiezan con **MAYÚSCULA** (`INT`, `ID`, `NEWLINE`,
   `WS`). Describen *cómo se agrupan los caracteres* en piezas mínimas con significado.

Convención clave: **minúscula = regla del parser**, **MAYÚSCULA = token del lexer**.

---

## 3. Análisis de la gramática `MiniLang.g4`

```antlr
grammar MiniLang;

prog:   stat+ ;

stat:   expr NEWLINE                 # printExpr
    |   ID '=' expr NEWLINE          # assign
    |   NEWLINE                      # blank
    ;

expr:   expr ('*'|'/') expr          # MulDiv
    |   expr ('+'|'-') expr          # AddSub
    |   INT                          # int
    |   ID                           # id
    |   '(' expr ')'                 # parens
    ;

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
ID  : [a-zA-Z]+ ;
INT : [0-9]+ ;
NEWLINE : '\r'? '\n' ;
WS  : [ \t]+ -> skip ;
```

### Reglas del parser

- **`prog: stat+ ;`** → un programa es **una o más** sentencias. El `+` significa "uno o
  más". (`*` sería "cero o más" y `?` "opcional").
- **`stat`** → una sentencia puede ser tres cosas, separadas por `|` (alternativas):
  - `expr NEWLINE` → una expresión suelta (ej. `5 * 5`).
  - `ID '=' expr NEWLINE` → una asignación (ej. `a = 4`).
  - `NEWLINE` → una línea en blanco.
- **`expr`** → una expresión, definida de forma **recursiva**:
  - `expr ('*'|'/') expr` → multiplicación o división.
  - `expr ('+'|'-') expr` → suma o resta.
  - `INT` → un número literal.
  - `ID` → una variable.
  - `'(' expr ')'` → una expresión entre paréntesis.

### El símbolo `#` (etiquetas de alternativas)

El `#` asigna una **etiqueta** a cada alternativa de una regla (ej. `# printExpr`,
`# assign`, `# MulDiv`). ANTLR usa estas etiquetas para generar un **método distinto por
cada alternativa** en el Visitor/Listener. Así, más adelante, podremos escribir código
específico para cada caso (por ejemplo, un método `visitMulDiv` separado de `visitAddSub`)
en vez de un solo método gigante. No cambian *qué* reconoce la gramática, solo organizan
el código generado.

### Precedencia de operadores

En `expr`, el **orden de las alternativas define la precedencia**. Como `MulDiv` aparece
**antes** que `AddSub`, la multiplicación y división tienen mayor prioridad que la suma y
resta — igual que en matemáticas. La recursividad por la izquierda (`expr op expr`) la
resuelve ANTLR automáticamente.

### Reglas del lexer (tokens)

- `MUL`, `DIV`, `ADD`, `SUB` → definen tokens con nombre para los operadores `* / + -`.
- `ID : [a-zA-Z]+ ;` → un identificador: una o más letras.
- `INT : [0-9]+ ;` → un entero: uno o más dígitos.
- `NEWLINE : '\r'? '\n' ;` → un salto de línea. El `'\r'?` hace **opcional** el retorno de
  carro, para que funcione tanto en Windows (`\r\n`) como en Unix (`\n`). Es el token que
  marca el **fin de cada sentencia**.
- `WS : [ \t]+ -> skip ;` → espacios y tabulaciones. El operador **`-> skip`** le dice al
  lexer que **descarte** estos caracteres: no se pasan al parser. Por eso los espacios
  entre símbolos no afectan el análisis.

---

## 4. Análisis del `Driver.py`

```python
import sys
from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniLangParser(stream)
    tree = parser.prog()

if __name__ == '__main__':
    main(sys.argv)
```

Línea por línea:

1. **`import sys`** → para leer los argumentos de la línea de comandos.
2. **`from antlr4 import *`** → importa el runtime de ANTLR para Python.
3. **`from MiniLangLexer / MiniLangParser`** → importa el lexer y el parser
   **generados** por el comando `antlr -Dlanguage=Python3 MiniLang.g4`. (Por eso hay que
   generarlos antes de correr el driver).
4. **`FileStream(argv[1])`** → abre el archivo de entrada (ej. `program_test.txt`) como un
   flujo de caracteres.
5. **`MiniLangLexer(input_stream)`** → el lexer convierte los caracteres en **tokens**.
6. **`CommonTokenStream(lexer)`** → agrupa esos tokens en un flujo que el parser puede
   consumir.
7. **`MiniLangParser(stream)`** → crea el parser a partir del flujo de tokens.
8. **`parser.prog()`** → arranca el análisis desde la **regla inicial** `prog` (la primera
   regla de la gramática) y construye el **árbol de análisis sintáctico** (parse tree).

### ¿Por qué no imprime nada cuando el código es correcto?

El driver **construye el árbol pero no lo imprime ni lo recorre**. Si el archivo es válido,
el análisis termina en silencio. Si hay un **error de sintaxis**, el runtime de ANTLR lo
detecta durante `parser.prog()` y lo reporta automáticamente en la consola (indicando línea
y columna). Por eso: **sin salida = éxito**, **salida = error**.

---

## 5. Flujo completo (resumen)

```
archivo.txt → FileStream → Lexer → Tokens → TokenStream → Parser → prog() → Parse Tree
```

1. Se genera el lexer/parser desde la gramática: `antlr -Dlanguage=Python3 MiniLang.g4`
2. El driver lee el archivo, lo tokeniza y lo parsea: `python3 Driver.py program_test.txt`
3. Correcto → nada; incorrecto → ANTLR muestra el error.

---

## 6. Casos de prueba

### ✅ Compila (sin salida)
```
5 * 5
a = 4
b = 6
c = a + b
```

### ❌ No compila (ANTLR reporta error)
```
3 + + 4        # dos operadores seguidos
= 5            # asignación sin identificador
(3 + 4         # paréntesis sin cerrar
```
