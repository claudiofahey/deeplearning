set -ex

docker build -t image_generator .

RELVOLUME="../data"
INDIR="tf_files/flowers/data"
OUTDIR="tf_files/flowers2/data"

VOLUME="$(cd "$(dirname "$RELVOLUME")"; pwd)/$(basename "$RELVOLUME")"

sudo rm -rf "$VOLUME/$OUTDIR"

docker run -v $VOLUME:/data --rm image_generator image_generator.py \
--output_dir "/data/$OUTDIR" \
--output_dir_depth 1 \
--parallelism 6 \
--output_images_per_input_image 1 \
"/data/$INDIR/*/*.jpg"

find "$RELVOLUME/$OUTDIR" | wc -l
du -h "$RELVOLUME/$OUTDIR"
