# Anna's Archive ISBN Visualization - Utils

## Download data

Download:

    - [aa_isbn13_codes_20241204T185335Z.benc.zst](https://software.annas-archive.li/AnnaArchivist/annas-archive/-/blob/main/isbn_images/aa_isbn13_codes_20241204T185335Z.benc.zst)

or other snapshot and place it in the root

Install:
    - [vips](https://www.libvips.org/)

Create folders:
    - images
    - tiles

## Create images

Create 1-bit PNG images with transparency

```bash
python make_isbn_images_with_transparency.py
```

## Create tiles

Create tiles (1-bit PNG with transparency)

```bash
bash make_tiles.sh
python convert_tiles_to_1bit.py
```