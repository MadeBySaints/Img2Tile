# Img2Tile
A python script that merges many single images into a larger tileset!


Img2Tile finds all images within a specified size range in the current folder, and combines them into a larger tileset, making it easier to use in game engines like Godot. This means you can just drop this script in any folder full of images you want to combine, run it, and you're golden. Very minor edits may be needed to the final file depending on your taste.

It uses a grid to determine the start location of each tile ensuring theres no overlapping of tiles.

You can toggle tile deletion by setting:
DELETE_SOURCE_FILES = True/False

Future Ideas:
- add alpha trimming (Remove alpha from source images before importing)