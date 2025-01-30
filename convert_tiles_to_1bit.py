from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import glob


def convert_to_1bit(image_path):
    """Convierte una imagen PNG a 1-bit usando PIL."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("1")  # Convertir a 1-bit (bilevel)
            img.info["transparency"] = 0  # Definir el índice 0 (negro) como transparente
            img.save(image_path, format="PNG")
        print(f"✅ Convertido: {image_path}")
    except Exception as e:
        print(f"❌ Error en {image_path}: {e}")


if __name__ == "__main__":
    tiles_dir = "tiles"
    tile_paths = glob.glob(f"{tiles_dir}/**/*.png", recursive=True)

    with ProcessPoolExecutor() as executor:
        executor.map(convert_to_1bit, tile_paths)
