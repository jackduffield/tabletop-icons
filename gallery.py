import os
import sys

def format_alt_text(filename):
    """
    Remove the .svg extension, replace hyphens with spaces,
    and convert to title case.
    """
    base = os.path.splitext(filename)[0]
    return base.replace('-', ' ').title()

def generate_picture_tag(white_path, image_width=100):
    """
    Given the relative path (from repo root) to the white image,
    generate a <picture> tag that uses the white image for dark mode
    and the corresponding black image (obtained by replacing 'white' with 'black')
    for light mode. The default <img> uses the white image.
    """
    # Construct the black version by replacing '/white/' with '/black/'
    black_path = white_path.replace("/white/", "/black/")
    # For systems using os.sep in the file paths, convert to forward slashes
    white_url = white_path.replace(os.sep, '/')
    black_url = black_path.replace(os.sep, '/')
    filename = os.path.basename(white_url)
    alt_text = format_alt_text(filename)
    picture = f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{white_url}">
  <source media="(prefers-color-scheme: light)" srcset="{black_url}">
  <img alt="{alt_text}" src="{white_url}" width="{image_width}">
</picture>'''
    return picture

def generate_table(cells, cells_per_row=8):
    """
    Generate an HTML table given a list of cell contents, with the specified
    number of cells per row.
    """
    table_lines = []
    table_lines.append("<table>")
    for i in range(0, len(cells), cells_per_row):
        row_cells = cells[i:i+cells_per_row]
        table_lines.append("  <tr>")
        for cell in row_cells:
            table_lines.append(f'    <td align="center">{cell}</td>')
        table_lines.append("  </tr>")
    table_lines.append("</table>")
    return "\n".join(table_lines)

def generate_readme(root_dir, output_file="README.md", image_width=100):
    """
    Walk through the 'white' folder (assumed to be inside the root directory)
    and generate a Markdown file that contains a header for each folder and
    a table with the images (using the <picture> tag for dark/light mode switching).
    """
    # Define the white icons root folder.
    white_root = os.path.join(root_dir, "white")
    readme_lines = []
    readme_lines.append("# Icons Gallery")
    readme_lines.append("")
    readme_lines.append("All image paths are relative to the repository root.")
    readme_lines.append("")
    
    # Walk through the white icons folder.
    for current_dir, dirs, files in os.walk(white_root):
        dirs.sort()
        files.sort()
        # Only process if there are .svg files in the folder.
        svg_files = [f for f in files if f.lower().endswith(".svg")]
        if not svg_files:
            continue

        # Determine the folder's relative path from the white root.
        rel_dir = os.path.relpath(current_dir, white_root)
        if rel_dir == ".":
            # This is the white root folder itself.
            heading = "## White"
        else:
            # Use the last part of the relative path.
            # The heading level: first-level subfolders (under white) get h3, second-level h4, etc.
            parts = rel_dir.split(os.sep)
            heading_level = 2 + len(parts)  # h3 for one part, h4 for two parts, etc.
            heading = f"{'#' * heading_level} {parts[-1].title()}"
        
        readme_lines.append("")
        readme_lines.append(heading)
        readme_lines.append("")

        # Build a list of picture tags for each SVG file.
        cells = []
        for filename in svg_files:
            white_file_path = os.path.join(current_dir, filename)
            # Create a relative path from the repository root.
            rel_path = os.path.relpath(white_file_path, root_dir).replace(os.sep, '/')
            picture = generate_picture_tag(rel_path, image_width)
            cells.append(picture)
        # Generate a table for this folder.
        table_md = generate_table(cells, cells_per_row=8)
        readme_lines.append(table_md)
        readme_lines.append("")
    
    # Write the resulting Markdown to the output file.
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))
    print(f"Gallery generated in {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gallery.py <root_directory>")
        sys.exit(1)
    root_directory = sys.argv[1]
    generate_readme(root_directory)
