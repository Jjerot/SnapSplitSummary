import json
import re
import subprocess

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

        if card_def_id and surface_effect_def_id:
            if reveal_effect_def_id:
                # Check if the reveal effect is one of the known colors
                if any(color in reveal_effect_def_id for color in ["Black", "Gold", "Green", "Blue", "Red", "White", "Purple"]):
                    cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id}")
                else:
                    # Append "Rainbow" to specific card types
                    if reveal_effect_def_id in ["Comic", "Glimmer", "Kirby", "Sparkle"]:
                        cards_info.append(f"{card_def_id} {surface_effect_def_id} {reveal_effect_def_id}Rainbow")
                    else:
                        cards_info.append(f"{card_def_id} {surface_effect_def_id} Rainbow")
            else:
                cards_info.append(f"{card_def_id} {surface_effect_def_id}")

    # Sort the cards alphabetically by CardDefId
    cards_info.sort()

    # Write sorted information to a text file
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
            for card_info in cards_info:
                outfile.write(f"{card_info}\n")

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

    for line in lines:
        total_splits += 1
        card_name = line.split()[0]
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

    # Calculate God Splits
    god_splits = ink_krackle_hits + gold_krackle_hits
    god_splits_percentage = (god_splits / krackle_rolls) * 100 if krackle_rolls > 0 else 0

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
        <p><strong>Number of God Splits:</strong> {god_splits} ({god_splits_percentage:.2f}%)</p>
        <h3>Most Split Characters</h3>
        <ul>
    """

    # Get top 3 cards with the most copies
    sorted_card_counts = sorted(card_counts.items(), key=lambda item: item[1], reverse=True)[:3]
    for card, count in sorted_card_counts:
        html_content += f"<li>{card} - {count} copies</li>"

    html_content += """
        </ul>
    </body>
    </html>
    """

    # Write HTML content to file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML summary written to {output_file}")

def main():
    # Assuming CollectionState.json is placed in the same directory as this script
    file_path = 'CollectionState.json'

    # Process the JSON file and generate the output.txt
    if not process_collection_state(file_path):
        return
    
    # Generate the summary as HTML
    summarize_cards(OUTPUT_PATH, SUMMARY_PATH)

    # Open the generated HTML file in a web browser
    subprocess.Popen(['start', '', SUMMARY_PATH], shell=True)

if __name__ == "__main__":
    main()
