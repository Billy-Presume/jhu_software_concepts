"""
Module: generate_css_color_and_text_utils.py
Author: Billy Presume
Created: 2025-05-30
Modified: 2025-05-30
Description: Generate Tailwind-compatible CSS utility classes for custom color palettes.

Note: This is a one time use file, but I did not exclude it from being committed because I might need to use it for feature projects.
"""

from typing import List


def generate_color_utilities(color_groups: List[str], shades: List[str]) -> List[str]:
    """Generates CSS classes for background and text colors.

    Args:
        color_groups: A list of color group names.
        shades: A list of shade values (typically from 50 to 900).

    Returns:
        A list of CSS class definitions as strings.
    """
    css_lines: List[str] = []

    for group in color_groups:
        css_lines.append(f"/* {group.capitalize()} background and text */")
        for shade in shades:
            css_lines.append(f".bg-{group}-{shade} {{ background-color: var(--{group}-{shade}); }}")
        for shade in shades:
            css_lines.append(f".text-{group}-{shade} {{ color: var(--{group}-{shade}); }}")
        css_lines.append("")  # Add a newline for spacing

    return css_lines


def write_to_file(filename: str, lines: List[str]) -> None:
    """Writes a list of strings to a file, each on a new line.

    Args:
        filename: Name of the file to write to.
        lines: List of strings representing the file content.
    """
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"CSS utility classes generated in '{filename}'")


def main() -> None:
    """Main function that initializes data and triggers the generation process."""
    color_groups: List[str] = [
        "primary", "secondary", "tertiary", "success", "warning", "error", "surface", "nowayrose",
        "momopeach", "briarrose", "princelyviolet", "matisse", "draculaorchid", "turqiosetower",
        "salmonrose", "aqualake", "carrobugcrimson", "chered", "mandarinorange", "darkgray",
        "flurescentred", "verdigris", "neonfuchsia", "azuregreen", "neongreen", "hltpink"
    ]

    shades: List[str] = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900"]

    css_output: List[str] = generate_color_utilities(color_groups, shades)
    write_to_file("color-utilities.css", css_output)


if __name__ == "__main__":
    main()
