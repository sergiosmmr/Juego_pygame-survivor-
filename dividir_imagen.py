from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen: str, carpeta_destino: str, divisiones_por_columna: int) -> None:
    """
    Divide una imagen en una cuadrícula y guarda cada fragmento por separado.

    Parámetros:
        ruta_imagen (str): Ruta del archivo de imagen original.
        carpeta_destino (str): Carpeta donde se guardarán las partes generadas.
        divisiones_por_columna (int): Número de divisiones horizontales (columnas).

    Retorno:
        None: La función guarda las imágenes directamente en la carpeta destino.
    """
    # Cargar imagen
    img = Image.open(ruta_imagen)
    ancho, alto = img.size

    # Calcular el tamaño de cada cuadrado
    tamanio_cuadrado = ancho // divisiones_por_columna
    divisiones_por_fila = alto // tamanio_cuadrado

    # Crear carpeta de destino si no existe
    os.makedirs(carpeta_destino, exist_ok=True)

    # Dividir y guardar cada tile
    contador = 0
    for i in range(divisiones_por_fila):
        for j in range(divisiones_por_columna):
            izquierda = j * tamanio_cuadrado
            superior = i * tamanio_cuadrado
            derecha = izquierda + tamanio_cuadrado
            inferior = superior + tamanio_cuadrado

            cuadrado = img.crop((izquierda, superior, derecha, inferior))
            nombre_archivo = f"tile_{contador + 1}.png"
            cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
            contador += 1

    img.close()
    print(f"✅ Se guardaron {contador} tiles en '{carpeta_destino}'")

# Ejemplo de uso
dividir_guardar_imagen("assets/images/tiles/Dungeon_Tileset.png", "assets/images/tiles", 10)
