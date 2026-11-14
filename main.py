#!/usr/bin/env python3
"""food-picture-01 entry: serve the tonkotsu ramen photograph.

The entry is a single photograph, entry.png (768x768, under 1 MiB):
a bowl of tonkotsu ramen in warm golden light, chopsticks lifting a
bundle of glossy noodles high above the broth while steam rises and
broth droplets fall. The noodle lift is the appetite shot — the thing
that makes a viewer hungry at first glance — and the ajitama egg and
caramelised chashu are the secondary highlights around it.

This program creates nothing. It takes the bundled photograph, checks
that it is a genuine PNG or JPEG inside the competition limits, writes
it unchanged to the harness output directory as entry.png, and reads
the copy back to confirm it is byte-identical.

Python 3.13, standard library only. No network, no third-party
packages, no randomness: the same input always produces the same
output bytes.
"""

import hashlib
import os
import struct
import sys

MAX_IMAGE_BYTES = 1_048_576
MAX_IMAGE_SIDE = 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"

# JPEG frame markers (SOF0-SOF15 minus the reserved/arithmetic ones)
# whose segment stores height and width.
JPEG_FRAME_MARKERS = frozenset((
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
))


def abort(reason):
    """Report a failure on stderr and return a non-zero exit code."""
    print("error: " + reason, file=sys.stderr)
    return 1


def png_dimensions(data):
    """Return (width, height) from the IHDR chunk of a PNG byte string."""
    if len(data) < 24:
        raise ValueError("too short for a PNG header")
    if data[:8] != PNG_MAGIC:
        raise ValueError("PNG signature mismatch")
    if data[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_dimensions(data):
    """Return (width, height) by scanning JPEG markers for a SOF segment."""
    if len(data) < 4 or data[:3] != JPEG_MAGIC:
        raise ValueError("JPEG signature mismatch")
    offset = 2
    while offset + 9 <= len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            # Standalone markers: SOI, EOI, RSTn — no length, skip 2 bytes.
            offset += 2
            continue
        if offset + 4 > len(data):
            break
        length = struct.unpack(">H", data[offset + 2:offset + 4])[0]
        if length < 2:
            raise ValueError("malformed JPEG segment length")
        if marker in JPEG_FRAME_MARKERS:
            if offset + 9 > len(data):
                break
            height, width = struct.unpack(">HH", data[offset + 5:offset + 9])
            return width, height
        offset += 2 + length
    raise ValueError("no frame marker with dimensions found")


def image_dimensions(data):
    """Return (width, height) for a PNG or JPEG byte string."""
    if not data:
        raise ValueError("file is empty")
    if data[:8] == PNG_MAGIC:
        width, height = png_dimensions(data)
    elif data[:3] == JPEG_MAGIC:
        width, height = jpeg_dimensions(data)
    else:
        raise ValueError("not a PNG or JPEG image")
    if width == 0 or height == 0:
        raise ValueError("image has a zero width or height")
    return width, height


def find_photo():
    """Find entry.png (preferred) or entry.jpg and return its path."""
    roots = []
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        roots.append(bot_dir)
    roots.append(os.path.dirname(os.path.abspath(__file__)))
    for root in roots:
        for name in ("entry.png", "entry.jpg"):
            path = os.path.join(root, name)
            if os.path.isfile(path):
                return path
    return None


def run():
    photo = find_photo()
    if photo is None:
        return abort("bundled photo entry.png (or entry.jpg) not found")

    with open(photo, "rb") as handle:
        blob = handle.read()

    if len(blob) > MAX_IMAGE_BYTES:
        return abort("photo is %d bytes, over the %d-byte limit"
                     % (len(blob), MAX_IMAGE_BYTES))

    try:
        width, height = image_dimensions(blob)
    except ValueError as exc:
        return abort("photo is not a valid image: %s" % exc)

    if width > MAX_IMAGE_SIDE or height > MAX_IMAGE_SIDE:
        return abort("photo is %dx%d, over the %dx%d limit"
                     % (width, height, MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.png")

    expected_hash = hashlib.sha256(blob).hexdigest()
    with open(target, "wb") as handle:
        handle.write(blob)

    with open(target, "rb") as handle:
        copy = handle.read()
    copy_hash = hashlib.sha256(copy).hexdigest()
    if len(copy) != len(blob) or copy_hash != expected_hash:
        return abort("written copy does not match the source: expected "
                     "%d bytes sha256 %s, got %d bytes sha256 %s"
                     % (len(blob), expected_hash, len(copy), copy_hash))

    print("wrote %s (%d bytes, %dx%d) verified sha256 %s"
          % (target, len(blob), width, height, expected_hash))
    return 0


if __name__ == "__main__":
    sys.exit(run())
