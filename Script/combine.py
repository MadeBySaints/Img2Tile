# combine.py

import os
import time
from PIL import Image

# --- Configuration ---
MAX_WIDTH = 256
MAX_HEIGHT = 256

GRID_SIZE = 48 # <--- Align sprites to a specific grid size? (will not overlap sprites)
MAX_SPRITE_WIDTH = 96
MAX_SPRITE_HEIGHT = 96

DELETE_SOURCE_FILES = True  # <--- Toggle this as needed. Deletes original files after putting them in the tileset.

# Unique tileset prefix per run
TILESET_PREFIX = f"tileset_{GRID_SIZE}_{int(time.time())}_"
# -----------------------

def get_source_images():
    return [
        f for f in os.listdir()
        if f.lower().endswith(".png")
        and os.path.isfile(f)
        and not f.startswith("tileset_")
    ]

def create_tileset_canvas():
    return Image.new("RGBA", (MAX_WIDTH, MAX_HEIGHT), (0, 0, 0, 0))

def create_grid(w, h):
    cols = w // GRID_SIZE
    rows = h // GRID_SIZE
    return [[False for _ in range(cols)] for _ in range(rows)]

def check_fit(grid, x, y, img_w, img_h):
    cols = len(grid[0])
    rows = len(grid)
    w_cells = -(-img_w // GRID_SIZE)
    h_cells = -(-img_h // GRID_SIZE)

    if x + w_cells > cols or y + h_cells > rows:
        return False

    for j in range(h_cells):
        for i in range(w_cells):
            if grid[y + j][x + i]:
                return False
    return True

def mark_grid(grid, x, y, img_w, img_h):
    w_cells = -(-img_w // GRID_SIZE)
    h_cells = -(-img_h // GRID_SIZE)
    for j in range(h_cells):
        for i in range(w_cells):
            grid[y + j][x + i] = True

def pack_images_to_tilesets(image_paths):
    tilesets = []
    used_images = set()
    remaining = image_paths.copy()

    while remaining:
        canvas = create_tileset_canvas()
        grid = create_grid(MAX_WIDTH, MAX_HEIGHT)
        cols = MAX_WIDTH // GRID_SIZE
        rows = MAX_HEIGHT // GRID_SIZE

        placed_this_sheet = []

        for img_path in remaining[:]:
            img = Image.open(img_path)
            w, h = img.size

            if w > MAX_SPRITE_WIDTH or h > MAX_SPRITE_HEIGHT:
                print(f"Skipping '{img_path}' - too large ({w}x{h})")
                remaining.remove(img_path)
                continue

            placed = False
            for y in range(rows):
                for x in range(cols):
                    if check_fit(grid, x, y, w, h):
                        px = x * GRID_SIZE
                        py = y * GRID_SIZE
                        canvas.paste(img, (px, py))
                        mark_grid(grid, x, y, w, h)
                        placed_this_sheet.append(img_path)
                        used_images.add(img_path)
                        remaining.remove(img_path)
                        placed = True
                        break
                if placed:
                    break

        if placed_this_sheet:
            tilesets.append((canvas, placed_this_sheet))
        else:
            break

    return tilesets, used_images

def main():
    source_images = get_source_images()
    if not source_images:
        print("No PNG source images found.")
        return

    tilesets, used_images = pack_images_to_tilesets(source_images)

    for i, (tileset, contents) in enumerate(tilesets):
        filename = f"{TILESET_PREFIX}{i + 1}.png"
        tileset.save(filename)
        print(f"Saved '{filename}' with {len(contents)} sprites.")

    if DELETE_SOURCE_FILES:
        for path in used_images:
            try:
                os.remove(path)
                print(f"Deleted '{path}'")
            except Exception as e:
                print(f"Error deleting '{path}': {e}")

if __name__ == "__main__":
    main()
