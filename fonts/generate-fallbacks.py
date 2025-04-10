"""
generate-fallbacks.py

This script analyzes a main font and a set of fallback fonts to determine their Unicode codepoint coverage.
It generates LaTeX commands for setting up the fonts with `unicode-math` in a way that ensures maximum
coverage of mathematical symbols. The script also provides a summary of the fonts' glyph coverage and
their contribution to the LaTeX setup.

Features:
- Runs `otfinfo -u` to extract Unicode codepoints supported by each font.
- Parses the output to identify unique and overlapping codepoints between fonts.
- Generates LaTeX commands for `unicode-math` with appropriate `range` options for fallback fonts.
- Outputs a summary table showing total glyphs, unique glyphs, and glyphs used in LaTeX for each font.
- Handles errors gracefully, such as missing fonts or the `otfinfo` command.

Requirements:
- Python 3.6+
- `otfinfo` command-line tool (part of `lcdf-typetools` package) must be installed and available in the PATH.

Configuration:
- Edit the `main_font_config` and `fallback_fonts_config` dictionaries to specify the main font and fallback fonts.
- Adjust the `output_latex_file` and `scale_option` variables as needed.

Usage:
1. Ensure `otfinfo` is installed and accessible.
2. Update the font paths and names in the configuration section.
3. Run the script: `python generate-fallbacks.py`.
4. Check the generated LaTeX file (`math_font_fallbacks.tex`) for the commands to include in your LaTeX document.

Output:
- A LaTeX file containing the generated font setup commands.
- A summary table printed to the console showing font statistics.

Error Handling:
- If a font file is missing or `otfinfo` fails, the script will log an error and skip that font.
- If no LaTeX commands can be generated, the script will notify the user.

Author: [Your Name]
Date: April 10, 2025
"""

import subprocess
import re
import os
import sys
from typing import List, Dict, Set, Tuple, Optional, Any

# --- Constants ---
OTFINFO_CMD = 'otfinfo'

# --- Helper Functions (run_otfinfo, parse_otfinfo_output, group_consecutive_codepoints) ---
# (These functions remain the same as in the previous version)
def run_otfinfo(font_path: str) -> Optional[List[str]]:
    """Runs 'otfinfo -u' on the font path and returns stdout lines."""
    print(f"Running otfinfo on: {font_path}", file=sys.stderr)
    if not os.path.exists(font_path):
        print(f"Error: Font file not found at '{font_path}'", file=sys.stderr)
        return None
    try:
        process = subprocess.run(
            [OTFINFO_CMD, '-u', font_path],
            capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore'
        )
        return process.stdout.splitlines()
    except FileNotFoundError:
        print(f"Error: '{OTFINFO_CMD}' command not found.", file=sys.stderr)
        print("Please ensure lcdf-typetools is installed and in your PATH.", file=sys.stderr)
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running {OTFINFO_CMD} on '{font_path}': {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred while running {OTFINFO_CMD} on '{font_path}': {e}", file=sys.stderr)
        return None

def parse_otfinfo_output(output_lines: Optional[List[str]]) -> Set[int]:
    """Parses otfinfo -u output lines and returns a set of integer codepoints."""
    codepoints: Set[int] = set()
    pattern = re.compile(r'^(?:uni|U\+|0x)([0-9A-Fa-f]{4,6})\b', re.IGNORECASE)
    if output_lines is None:
        return codepoints
    for line in output_lines:
        line_content = line.split('#')[0].strip()
        match = pattern.match(line_content)
        if match:
            hex_code = match.group(1)
            try:
                codepoints.add(int(hex_code, 16))
            except ValueError:
                print(f"Warning: Could not parse hex code '{hex_code}' from line: {line.strip()}", file=sys.stderr)
        elif re.match(r'^[0-9A-Fa-f]{4,6}$', line_content):
             try:
                 codepoints.add(int(line_content, 16))
             except ValueError:
                 print(f"Warning: Could not parse potential hex code '{line_content}' from line: {line.strip()}", file=sys.stderr)
    # Don't print count here, do it in the calling context
    # print(f"Parsed {len(codepoints)} unique codepoints.", file=sys.stderr)
    return codepoints

def group_consecutive_codepoints(codepoints: Set[int]) -> List[str]:
    """Groups sorted codepoints into ranges for the unicode-math 'range' option,
       adding required double quotes around each item (e.g., "XXXX" or "XXXX-"YYYY")."""
    if not codepoints:
        return []
    sorted_codes = sorted(list(codepoints))
    ranges: List[str] = []
    if not sorted_codes:
        return []
    start_range = sorted_codes[0]
    end_range = sorted_codes[0]
    for i in range(1, len(sorted_codes)):
        if sorted_codes[i] == end_range + 1:
            end_range = sorted_codes[i]
        else:
            if start_range == end_range:
                # Format single codepoint correctly (pad to at least 4 hex digits)
                ranges.append(f'"{start_range:04X}')
            else:
                # Format range correctly (pad to at least 4 hex digits)
                ranges.append(f'"{start_range:04X}-"{end_range:04X}')
            start_range = sorted_codes[i]
            end_range = sorted_codes[i]
    # Append the last range
    if start_range == end_range:
        ranges.append(f'"{start_range:04X}')
    else:
        ranges.append(f'"{start_range:04X}-"{end_range:04X}')
    return ranges


# --- NEW: Function to get font data including codepoints ---
def get_font_data(font_info: Dict[str, str]) -> Dict[str, Any]:
    """Gets font path/name and calculates its codepoint set."""
    path = font_info.get('path', 'N/A')
    name = font_info.get('name', os.path.basename(path) if path != 'N/A' else 'Unknown')
    codepoints: Optional[Set[int]] = None
    status = "OK"

    if path == 'N/A' or not os.path.exists(path):
        print(f"Error: Font file not found for '{name}' at '{path}'", file=sys.stderr)
        status = "File Not Found"
    else:
        output_lines = run_otfinfo(path)
        if output_lines is None:
            print(f"Failed to get info for font: {name}", file=sys.stderr)
            status = "otfinfo Failed"
        else:
            codepoints = parse_otfinfo_output(output_lines)
            print(f"Parsed {len(codepoints)} codepoints for {name}.", file=sys.stderr)

    return {
        "name": name,
        "path": path,
        "codepoints": codepoints,
        "status": status,
        "latex_used_count": 0 # Initialize count of codepoints used in LaTeX generation
    }

# --- Configuration ---

# --- !!! EDIT THIS SECTION !!! ---
main_font_config = {
    "path": "/usr/local/texlive/2025/texmf-dist/fonts/opentype/public/libertinus-fonts/LibertinusMath-Regular.otf",
    "name": "Libertinus Math"
}

fallback_fonts_config = [
    {
        "path": "/usr/local/texlive/2025/texmf-dist/fonts/opentype/public/tex-gyre-math/texgyrepagella-math.otf",
        "name": "texgyrepagella-math"
    },
    {
        "path": "/usr/local/texlive/2025/texmf-dist/fonts/opentype/public/newcomputermodern/NewCMMath-Regular.otf",
        "name": "NewCMMath-Regular.otf"
    },
    # {
    #     "path": "/usr/share/texlive/texmf-dist/fonts/opentype/public/tex-gyre-math/texgyretermes-math.otf",
    #     "name": "texgyretermes-math"
    # },
    # {   # Example: Non-existent font for testing error handling
    #     "path": "/path/to/nonexistent/font.otf",
    #     "name": "NonExistent Font"
    # },
]

output_latex_file = "math_font_fallbacks.tex"
scale_option = "Scale=MatchUppercase"
# --- !!! END EDIT SECTION !!! ---

# --- Main Execution ---
print("Starting font analysis for main font and fallbacks...")

all_fonts_data: List[Dict[str, Any]] = [] # To store data for the final table
all_latex_commands: List[str] = []
covered_codepoints_for_latex: Set[int] = set() # Tracks coverage for LaTeX command generation
processed_font_names_for_latex: List[str] = [] # Tracks names for LaTeX comments

# 1. Process the main font
print(f"\n--- Processing Main Font: {main_font_config['name']} ---")
main_font_data = get_font_data(main_font_config)
all_fonts_data.append(main_font_data)

if main_font_data["status"] == "OK" and main_font_data["codepoints"] is not None:
    # For the main font, *all* its codepoints are initially used for LaTeX
    main_font_codepoint_count = len(main_font_data["codepoints"])
    main_font_data["latex_used_count"] = main_font_codepoint_count # Store this count
    covered_codepoints_for_latex.update(main_font_data["codepoints"])
    processed_font_names_for_latex.append(main_font_data['name'])
    all_latex_commands.append(f"\\setmathfont{{{main_font_data['name']}}}")
    print(f"Main font '{main_font_data['name']}' covers {len(covered_codepoints_for_latex)} codepoints for LaTeX setup.")
else:
    print(f"Critical Error: Could not process main font '{main_font_data['name']}'. LaTeX setup might be incomplete.", file=sys.stderr)
    main_font_data["latex_used_count"] = 0 # Or mark as N/A later in table
    # Continue processing other fonts for the table, but LaTeX output will be affected.

# 2. Process fallback fonts sequentially (for LaTeX generation AND data collection)
for i, fallback_config in enumerate(fallback_fonts_config):
    fallback_name = fallback_config.get('name', f"Fallback {i+1}")
    print(f"\n--- Processing Fallback {i+1}: {fallback_name} ---")

    fallback_data = get_font_data(fallback_config)
    all_fonts_data.append(fallback_data) # Add data regardless of status for the summary table

    if fallback_data["status"] != "OK" or fallback_data["codepoints"] is None:
        print(f"Warning: Skipping LaTeX command generation for fallback '{fallback_name}' due to processing errors.")
        fallback_data["latex_used_count"] = 0 # Mark as 0 contribution for LaTeX
        continue # Skip LaTeX generation for this font

    # --- LaTeX Command Generation Logic (uses sequential comparison) ---
    fallback_codepoints = fallback_data["codepoints"]
    # Find codepoints in this fallback NOT covered by *previous* fonts in the sequence
    unique_to_this_fallback_for_latex = fallback_codepoints.difference(covered_codepoints_for_latex)
    num_unique_for_latex = len(unique_to_this_fallback_for_latex)

    # ** Store the number of codepoints this font contributes to the LaTeX sequence **
    fallback_data["latex_used_count"] = num_unique_for_latex

    print(f"Found {num_unique_for_latex} codepoints in {fallback_name} not covered by previous fonts ({', '.join(processed_font_names_for_latex)}) for LaTeX range.")

    if not unique_to_this_fallback_for_latex:
        print(f"No unique codepoints needed from {fallback_name} for LaTeX range.")
        # Add name to processed list for accurate reporting in next iteration
        processed_font_names_for_latex.append(fallback_name)
        continue # Move to the next fallback for LaTeX generation

    range_strings = group_consecutive_codepoints(unique_to_this_fallback_for_latex)
    range_argument = ",".join(range_strings)
    options = f"range={{{range_argument}}}"
    if scale_option:
        options += f", {scale_option}"

    latex_command = f"\\setmathfont{{{fallback_name}}}[{options}]"
    all_latex_commands.append(latex_command)
    print(f"Generated LaTeX command for {fallback_name}.")

    # Update the set of codepoints covered *for LaTeX generation purposes*
    covered_codepoints_for_latex.update(unique_to_this_fallback_for_latex)
    processed_font_names_for_latex.append(fallback_name)
    print(f"Total covered codepoints for LaTeX after adding {fallback_name}: {len(covered_codepoints_for_latex)}")
    # --- End LaTeX Command Generation Logic ---


# 3. Generate and Save LaTeX file (if commands were generated)
print("\n--- Generated LaTeX Commands ---")
if not all_latex_commands:
    print("No LaTeX commands were generated (check font paths and otfinfo).")
elif main_font_data["status"] != "OK":
     print("LaTeX commands generated, but main font failed. Commands might not work correctly.")
     for cmd in all_latex_commands:
         print(cmd)
else:
    # Print commands to console
    for cmd in all_latex_commands:
        print(cmd)
    # Save the commands to the output file
    try:
        with open(output_latex_file, "w", encoding='utf-8') as f:
            f.write(f"% LaTeX commands generated by script\n")
            f.write(f"% Main Font: {main_font_data['name']}\n")
            # List only fonts that *successfully contributed* to the LaTeX ranges
            successful_latex_fonts = [main_font_data['name']] + \
                                     [fb['name'] for fb in all_fonts_data[1:] if fb.get('latex_used_count', 0) > 0 and fb['status'] == 'OK']
            f.write(f"% Fonts Used (in order for ranges): {', '.join(successful_latex_fonts)}\n")
            f.write(f"% Total codepoints covered by sequential ranges: {len(covered_codepoints_for_latex)}\n")
            f.write("% Add these lines to your LaTeX preamble after loading unicode-math.\n\n")
            for cmd in all_latex_commands:
                f.write(cmd + "\n")
        print(f"\nLaTeX commands saved to '{output_latex_file}'")
    except Exception as e:
        print(f"\nError saving commands to file '{output_latex_file}': {e}", file=sys.stderr)


# 4. Calculate Uniqueness Statistics and Generate Table
print("\n--- Font Statistics Summary ---")

# We now use all_fonts_data directly, as it contains the latex_used_count and status
if not all_fonts_data:
    print("No fonts were processed. Cannot generate statistics table.")
else:
    summary_data = []
    # Filter valid fonts *only* for the 'unique' calculation
    valid_font_data_for_uniqueness = [f for f in all_fonts_data if f["status"] == "OK" and f["codepoints"] is not None]

    print("Calculating unique glyphs for each font against all others...")
    for i, current_font in enumerate(all_fonts_data):
        current_name = current_font['name']
        status = current_font['status']
        total_count_str = "N/A"
        unique_count_str = "N/A"
        latex_used_count_str = "N/A" # Default for failed fonts

        if status == "OK" and current_font["codepoints"] is not None:
            current_codepoints = current_font['codepoints']
            total_count = len(current_codepoints)
            total_count_str = str(total_count)
            latex_used_count_str = str(current_font.get("latex_used_count", 0)) # Get stored value

            # Calculate uniqueness against OTHER *valid* fonts
            other_valid_codepoints_union = set().union(*[
                valid_font_data_for_uniqueness[j]['codepoints']
                for j in range(len(valid_font_data_for_uniqueness))
                if valid_font_data_for_uniqueness[j]['name'] != current_name # Compare by name just in case
            ])

            unique_to_current = current_codepoints.difference(other_valid_codepoints_union)
            unique_count = len(unique_to_current)
            unique_count_str = str(unique_count)
        else:
            # Font failed, use status message for total count
            total_count_str = f"({status})"
            # Unique and LaTeX Used remain N/A

        summary_data.append({
            "name": current_name,
            "total": total_count_str,
            "unique": unique_count_str,
            "latex_used": latex_used_count_str # Add the new data point
        })

    # --- Print Table ---
    if summary_data:
        # Determine column widths
        max_name_len = max(len(str(row['name'])) for row in summary_data)
        max_total_len = max(len(str(row['total'])) for row in summary_data)
        max_unique_len = max(len(str(row['unique'])) for row in summary_data)
        max_latex_used_len = max(len(str(row['latex_used'])) for row in summary_data) # New column width

        # Ensure minimum width for headers
        name_col_width = max(max_name_len, len("Font Name"))
        total_col_width = max(max_total_len, len("Total Glyphs"))
        unique_col_width = max(max_unique_len, len("Unique Glyphs*"))
        latex_used_col_width = max(max_latex_used_len, len("LaTeX Used**")) # New column width

        # Header
        header = (f"{'Font Name':<{name_col_width}} | "
                  f"{'Total Glyphs':>{total_col_width}} | "
                  f"{'Unique Glyphs*':>{unique_col_width}} | "
                  f"{'LaTeX Used**':>{latex_used_col_width}}") # Add new header
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)

        # Rows
        for row in summary_data:
            print(f"{str(row['name']):<{name_col_width}} | "
                  f"{str(row['total']):>{total_col_width}} | "
                  f"{str(row['unique']):>{unique_col_width}} | "
                  f"{str(row['latex_used']):>{latex_used_col_width}}") # Add new column data

        print(separator)
        print(f"* Unique Glyphs: Count of glyphs present in this font but not in ANY other successfully processed font listed.")
        print(f"** LaTeX Used: Count of codepoints this font contributes in the sequential LaTeX `range` generation.") # Add footnote for new column
    else:
        print("No data available to generate the summary table.")


print("\nScript finished.")
