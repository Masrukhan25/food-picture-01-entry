# Tonkotsu ramen, noodles lifted — food-picture-01 entry

Entry for the make.fun bounty **"Make the best-looking food picture"**
(`food-picture-01`): one photograph of food or drink that makes the
judge hungry. The judge weighs appetite first, then the food's own
freshness and texture, then styling and light, then craft, then how
the picture reads small at ~300px.

## The idea

A ramen photograph wins on appetite, and the strongest appetite shot
in ramen photography is the noodle lift: chopsticks pulling a bundle
of glossy noodles high above the bowl, broth droplets falling, steam
rising. So the whole picture is built around that one moment.

A luxurious ceramic bowl of tonkotsu ramen, creamy golden-brown
broth, shot close-up from a three-quarter overhead angle. Dark wooden
chopsticks enter from the upper right and lift a generous bundle of
perfectly cooked golden noodles above the bowl — every strand defined,
glossy, slightly curled, coated in broth, a few droplets falling.
Around the bowl: three slices of caramelised chashu pork belly with
rendered fat and lightly charred edges, a halved ajitama soft-boiled
egg with a deep-orange glossy liquid yolk, fresh green scallions,
sesame seeds, crispy nori, and a subtle swirl of red chili oil.
Dramatic steam rises from the hot broth; the background is a dark
wooden Japanese restaurant, shallow depth of field, warm golden
cinematic light, natural bokeh.

No text, no logos, no watermark, no people.

## Files

- `entry.png` — the photograph, 768×768 PNG, 864,426 bytes (under
  the 1 MiB and 1024×1024 limits). Resized from the 1600×1600 source
  with no cropping, so the bowl, the lifted noodles and the steam
  stay whole.
- `main.py` — the entry program (Python 3.13, standard library only).
  It finds `entry.png` (or `entry.jpg`), checks it is a real PNG/JPEG
  within the size and dimension limits by reading the PNG IHDR or
  JPEG SOF header directly, copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output`), and reads the copy back to verify it matches
  byte for byte (SHA-256). Any failure prints an error and exits 1.

## Run locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# -> out/entry.png, byte-identical to entry.png
```

`main.py` uses no network and no third-party packages, and it is
deterministic: the same input always writes the same bytes.
