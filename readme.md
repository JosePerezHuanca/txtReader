# txt reader:

Este complemento para NVDA es un lector de archivos de textos sin interfaz.

## ¿Cómo funciona?

Al abrir un archivo, el complemento copia el contenido en memoria y cierra el archivo, permitiendo la lectura mediante atajos de teclado. El contenido se envía al lector, por lo que se puede leer sin que se muestre nada en pantalla.

## Atajos: 

Nota: todos los atajos se pueden personalizar en la categoría Txt reader del diálogo gestos de entrada.

- NVDA+alt+f: Muestra el diálogo para abrir un archivo.
- NVDA+alt+flecha abajo: Navega a la siguiente línea.
- NVDA+alt+flecha arriba: Navega a la línea anterior.
- NVDA+alt+espacio: Lee la línea actual.
- NVDA+alt+inicio o fin: Ir al principio o fin del texto.
- NVDA+alt+flecha derecha: Si se abrió mas de un archivo, navega al siguiente texto en la lista.
- NVDA+alt+flecha izquierda: Si se abrió mas de un archivo, navega al texto anterior en la lista.
- NVDA+alt+retroceso: Elimina el texto actual de la lista.
- NVDA+alt+t: Lee el título del archivo
- NVDA+alt+c: Copia la línea actual al portapapeles.
- NVDA+alt+l: Si se abrió previamente uno o mas archivos, vacía la lista de textos.
- NVDA+alt+g: Muestra un diálogo para ir a una línea específica.
- NVDA+alt+b: Muestra un diálogo para buscar en el texto actual.


## Registro de cambios

### 0.4

- Ahora el complemento permite leer mas de un texto. Con los atajos NVDA+alt+flechas izquierda y derecha se puede navegar entre los textos en la lista. NVDA+alt+retroceso elimina el texto actual.
- Se añadió un diálogo para ir a una línea específica en el texto actual: NVDA+alt+g.
- Se añadió un diálogo para buscar en el texto actual: NVDA+alt+b.
- Algunas correcciones

### 0.3

- Se solucionó un error que permitía la ejecución del complemento en el modo seguro.
- El complemento ya se puede traducir

### 0.2

- Los atajos de teclado ahora están agrupados en la categoría Txt reader de los gestos de entrada.
- Se agregó un atajo para vaciar el contenido en memoria

### 0.1

Versión inicial.
