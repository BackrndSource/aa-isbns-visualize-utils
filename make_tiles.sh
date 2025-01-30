#!/bin/bash

#!/bin/bash
set -e
set -o pipefail

tile_size=5000
input_path=images
output_path=tiles

for filename in $input_path/*.png; do
    if [[ $filename == *"smaller"* ]]; then
        continue
    fi
    echo "Creating tile set for $filename..."
    vips dzsave $filename $output_path/$(basename "$filename" .png) --tile-size $tile_size --depth onetile --overlap 0 --suffix .png
done