import json
import re
import subprocess
import os
from datetime import datetime

# Define paths for the output files
OUTPUT_PATH = 'output.txt'
SUMMARY_PATH = 'summary.html'  # Changed to HTML file

def extract_cards_section(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        json_content = file.read()

    # Regular expression to find the "Cards": [ section that follows a closing square bracket
    pattern = re.compile(r'\],\s*"Cards":\s*\[([^]]*)\]', re.DOTALL)
    match = pattern.search(json_content)

    if match:
        cards_section = match.group(1)
        try:
            cards_data = json.loads(f"[{cards_section.strip()}]")
            return cards_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No matching section found")
        return None

def process_collection_state(file_path):
    """Process the JSON file and output a simplified list of information."""
    try:
        data = extract_cards_section(file_path)
        if data is None:
            return False
    except FileNotFoundError:
        print(f"Error: FileNotFoundError - CollectionState.json file not found at {file_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: JSONDecodeError - {e}")
        return False

    # Extract relevant information and filter out entries with "Custom": true
    cards_info = []
    for card in data:
        if "Custom" in card and card["Custom"]:
            continue  # Skip entries where Custom is true

        card_def_id = card.get('CardDefId', '')
        surface_effect_def_id = card.get('SurfaceEffectDefId', '')
        reveal_effect_def_id = card.get('CardRevealEffectDefId', '')
        time_created = card.get('TimeCreated', '')

        if card_def_id and surface_effect_def_id:
            reveal_effect = reveal_effect_def_id
            if reveal_effect_def_id:
                # Check if the reveal effect is one of the known colors
                if any(color in reveal_effect_def_id for color in ["Black", "Gold", "Green", "Blue", "Red", "White", "Purple"]):
                    reveal_effect = f"{reveal_effect_def_id}"
                else:
                    # Append "Rainbow" to specific card types
                    if reveal_effect_def_id in ["Comic", "Glimmer", "Kirby", "Sparkle"]:
                        reveal_effect = f"{reveal_effect_def_id}Rainbow"
                    else:
                        reveal_effect = "Rainbow"
            cards_info.append((card_def_id, surface_effect_def_id, reveal_effect, time_created))

    # Sort the cards by TimeCreated
    cards_info.sort(key=lambda x: x[3])

    # Write sorted information to a text file
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
            for card_info in cards_info:
                card_str = f"{card_info[0]} {card_info[1]} {card_info[2]} {card_info[3]}"
                outfile.write(f"{card_str}\n")

        print("Output written to output.txt")
        return True
    except IOError as e:
        print(f"Error: IOError - {e}")
        return False

def summarize_cards(input_file, output_file):
    """Summarize the card information and generate HTML output."""
    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Dictionary to count occurrences of each card
    card_counts = {}
    total_splits = 0
    ink_hits = 0
    gold_hits = 0
    krackle_hits = 0
    ink_krackle_hits = 0
    gold_krackle_hits = 0

    # Dictionary to count color occurrences
    color_counts = {
        "Black": 0,
        "Gold": 0,
        "Green": 0,
        "Blue": 0,
        "Red": 0,
        "White": 0,
        "Purple": 0,
        "Rainbow": 0
    }

    for line in lines:
        total_splits += 1
        parts = line.split()
        card_name = parts[0]

        if card_name in card_counts:
            card_counts[card_name] += 1
        else:
            card_counts[card_name] = 1

        # Check for additional criteria
        if "Ink" in line:
            ink_hits += 1
        if "GoldFoil" in line:
            gold_hits += 1
        if "Kirby" in line:
            krackle_hits += 1
        if "Ink" in line and "Kirby" in line:
            ink_krackle_hits += 1
        if "GoldFoil" in line and "Kirby" in line:
            gold_krackle_hits += 1

        # Check for colors in the reveal effect
        for color in color_counts.keys():
            if color in parts[2]:
                color_counts[color] += 1

    # Calculate Ink Rolls, Gold Rolls, and Krackle Rolls
    ink_rolls = 0
    gold_rolls = 0
    krackle_rolls = 0
    for count in card_counts.values():
        if count >= 4:
            ink_rolls += (count - 3)
        if count >= 5:
            gold_rolls += (count - 4)
        if count >= 6:
            krackle_rolls += (count - 5)

    # Calculate percentages relative to their respective rolls
    ink_hits_percentage = (ink_hits / ink_rolls) * 100 if ink_rolls > 0 else 0
    gold_hits_percentage = (gold_hits / gold_rolls) * 100 if gold_rolls > 0 else 0
    krackle_hits_percentage = (krackle_hits / krackle_rolls) * 100 if krackle_rolls > 0 else 0
    ink_krackle_hits_percentage = (ink_krackle_hits / krackle_rolls) * 100 if krackle_rolls > 0 else 0
    gold_krackle_hits_percentage = (gold_krackle_hits / krackle_rolls) * 100 if krackle_rolls > 0 else 0

    # Sort colors by count in descending order
    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Data Summary</title>
        <style>
            body {{
                background-color: #222;
                color: #fff;
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 10px;
                max-width: 600px; /* Limit width to 600px */
            }}
            h2 {{
                border-bottom: 2px solid #ccc;
                padding-bottom: 5px;
            }}
            p {{
                margin: 5px 0;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <h2>Game Data Summary</h2>
        <p><strong>Total splits:</strong> {total_splits}</p>
        <p><strong>Ink Rolls:</strong> {ink_rolls}</p>
        <p><strong>Ink Hits:</strong> {ink_hits} ({ink_hits_percentage:.2f}%)</p>
        <p><strong>Gold Rolls:</strong> {gold_rolls}</p>
        <p><strong>Gold Hits:</strong> {gold_hits} ({gold_hits_percentage:.2f}%)</p>
        <p><strong>Kirby Rolls:</strong> {krackle_rolls}</p>
        <p><strong>Kirby Hits:</strong> {krackle_hits} ({krackle_hits_percentage:.2f}%)</p>
        <p><strong>Ink & Kirby Hits:</strong> {ink_krackle_hits} ({ink_krackle_hits_percentage:.2f}%)</p>
        <p><strong>Gold & Kirby Hits:</strong> {gold_krackle_hits} ({gold_krackle_hits_percentage:.2f}%)</p>
        <h3>Most Split Characters</h3>
        <ul>
    """

    # Get top 3 cards with the most copies
    sorted_card_counts = sorted(card_counts.items(), key=lambda item: item[1], reverse=True)[:3]
    for card, count in sorted_card_counts:
        html_content += f"<li>{card} - {count} copies</li>"

    html_content += "</ul><h3>Color Counts</h3><ul>"

    # Add sorted color counts to HTML content
    for color, count in sorted_colors:
        percentage = (count / total_splits) * 100
        html_content += f"<li>{color}: {count} ({percentage:.2f}%)</li>"

    html_content += """
        </ul>
    </body>
    </html>
    """

    # Write HTML content to file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML summary written to {output_file}")

    # Write summary statistics to the top of the output.txt
    summary_text = f"""
Total splits: {total_splits}
Ink Rolls: {ink_rolls}
Ink Hits: {ink_hits} ({ink_hits_percentage:.2f}%)
Gold Rolls: {gold_rolls}
Gold Hits: {gold_hits} ({gold_hits_percentage:.2f}%)
Kirby Rolls: {krackle_rolls}
Kirby Hits: {krackle_hits} ({krackle_hits_percentage:.2f}%)
Ink & Kirby Hits: {ink_krackle_hits} ({ink_krackle_hits_percentage:.2f}%)
Gold & Kirby Hits: {gold_krackle_hits} ({gold_krackle_hits_percentage:.2f}%)

Most Split Characters
"""

    # Add most split characters to summary
    for card, count in sorted_card_counts:
        summary_text += f"{card} - {count} copies\n"

    summary_text += "Color Counts\n"

    # Add sorted color counts to summary
    for color, count in sorted_colors:
        percentage = (count / total_splits) * 100
        summary_text += f"{color}: {count} ({percentage:.2f}%)\n"

    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
            outfile.write(summary_text)
            for line in lines:
                outfile.write(line)
        print("Summary statistics added to output.txt")
    except IOError as e:
        print(f"Error: IOError - {e}")

def main():
    # Assuming CollectionState.json is located at ~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/
    file_path = os.path.expanduser('~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json')

    # Process the JSON file and generate the output.txt
    if not process_collection_state(file_path):
        return
    
    # Generate the summary as HTML
    summarize_cards(OUTPUT_PATH, SUMMARY_PATH)

    # Open the generated HTML file in a web browser
    subprocess.Popen(['start', '', SUMMARY_PATH], shell=True)

if __name__ == "__main__":
    main()
