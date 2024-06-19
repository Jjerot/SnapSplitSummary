import json
import re
import subprocess
import os
from datetime import datetime

# Define paths for the output files
OUTPUT_PATH = 'output.txt'
SUMMARY_PATH = 'summary.html'

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

    # Get additional statistics
    luckiest_card, unluckiest_card, streaks, longest_ink_drought, longest_gold_drought, longest_kirby_drought = additional_stats(input_file)

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Data Summary</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <div class="popup">
            <div class="header">
                <h1>Game Data Summary</h1>
            </div>
            <div class="columns">
                <div class="column left">
                    <h2>Your Lucky Character:</h2>
                    <p>{luckiest_card}</p>
                    <br>
                    <p>Highest Ink Streak: {streaks['highest_ink_streak']['length']}</p>
                    <p class="cards">{', '.join(streaks['highest_ink_streak']['cards'])}</p>
                    <p>Highest Gold Streak: {streaks['highest_gold_streak']['length']}</p>
                    <p class="cards">{', '.join(streaks['highest_gold_streak']['cards'])}</p>
                    <p>Highest Kirby Streak: {streaks['highest_kirby_streak']['length']}</p>
                    <p class="cards">{', '.join(streaks['highest_kirby_streak']['cards'])}</p>
                </div>
                <div class="column center">
                    <h2>Statistics</h2>
                    <p>Total splits: {total_splits}</p>
                    <p>Ink Rolls: {ink_rolls}</p>
                    <p>Ink Hits: {ink_hits} ({ink_hits_percentage:.2f}%)</p>
                    <p>Gold Rolls: {gold_rolls}</p>
                    <p>Gold Hits: {gold_hits} ({gold_hits_percentage:.2f}%)</p>
                    <p>Kirby Rolls: {krackle_rolls}</p>
                    <p>Kirby Hits: {krackle_hits} ({krackle_hits_percentage:.2f}%)</p>
                    <p>Ink & Kirby Hits: {ink_krackle_hits} ({ink_krackle_hits_percentage:.2f}%)</p>
                    <p>Gold & Kirby Hits: {gold_krackle_hits} ({gold_krackle_hits_percentage:.2f}%)</p>
                    <h2>Most Split Characters</h2>
                    <ul>
    """

    # Get top 3 cards with the most copies
    sorted_card_counts = sorted(card_counts.items(), key=lambda item: item[1], reverse=True)[:3]
    for card, count in sorted_card_counts:
        html_content += f"<li>{card} - {count} copies</li>"

    html_content += "</ul><h2>Flare Color Breakdown</h2><ul>"

    # Add sorted color counts to HTML content
    for color, count in sorted_colors:
        percentage = (count / total_splits) * 100
        html_content += f"<li>{color}: {count} ({percentage:.2f}%)</li>"

    # Append additional stats to HTML content
    html_content += f"""
                    </ul>
                </div>
                <div class="column right">
                    <h2>Your Nemesis:</h2>
                    <p>{unluckiest_card}</p>
                    <br>
                    <p>Longest Ink drought: {longest_ink_drought[1]['Max Ink Drought']}</p>
                    <p class="cards">{longest_ink_drought[0]}</p>
                    <p>Longest Gold drought: {longest_gold_drought[1]['Max Gold Drought']}</p>
                    <p class="cards">{longest_gold_drought[0]}</p>
                    <p>Longest Kirby drought: {longest_kirby_drought[1]['Max Kirby Drought']}</p>
                    <p class="cards">{longest_kirby_drought[0]}</p>
                </div>
            </div>
        </div>
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

    summary_text += f"""
Your lucky character is {luckiest_card}
Your nemesis is {unluckiest_card}

Highest Ink Streak: {streaks['highest_ink_streak']['length']} ({', '.join(streaks['highest_ink_streak']['cards'])})
Longest Ink drought: {longest_ink_drought[1]['Max Ink Drought']} ({longest_ink_drought[0]})
Highest Gold Streak: {streaks['highest_gold_streak']['length']} ({', '.join(streaks['highest_gold_streak']['cards'])})
Longest Gold drought: {longest_gold_drought[1]['Max Gold Drought']} ({longest_gold_drought[0]})
Highest Kirby Streak: {streaks['highest_kirby_streak']['length']} ({', '.join(streaks['highest_kirby_streak']['cards'])})
Longest Kirby drought: {longest_kirby_drought[1]['Max Kirby Drought']} ({longest_kirby_drought[0]})
"""

    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
            outfile.write(summary_text)
            for line in lines:
                outfile.write(line)
        print("Summary statistics added to output.txt")
    except IOError as e:
        print(f"Error: IOError - {e}")

def additional_stats(input_file):
    cards = parse_output_file(input_file)
    card_luck, card_rolls = calculate_luck(cards)
    streaks = find_streaks(cards, card_rolls)
    longest_ink_drought, longest_gold_drought, longest_kirby_drought = track_droughts(cards)

    luckiest_card = format_card_name(max(card_luck, key=card_luck.get))
    unluckiest_card = format_card_name(min(card_luck, key=card_luck.get))

    longest_ink_drought = (format_card_name(longest_ink_drought[0]), longest_ink_drought[1])
    longest_gold_drought = (format_card_name(longest_gold_drought[0]), longest_gold_drought[1])
    longest_kirby_drought = (format_card_name(longest_kirby_drought[0]), longest_kirby_drought[1])

    return luckiest_card, unluckiest_card, streaks, longest_ink_drought, longest_gold_drought, longest_kirby_drought

def parse_output_file(file_path):
    cards = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and is_valid_date(parts[2]):
                card_def_id, surface_effect_def_id, time_created = parts
                reveal_effect_def_id = ""
            elif len(parts) == 4 and is_valid_date(parts[3]):
                card_def_id, surface_effect_def_id, reveal_effect_def_id, time_created = parts
            else:
                continue  # Skip lines that don't match the expected format
            cards.append((card_def_id, surface_effect_def_id, reveal_effect_def_id, time_created))
    return cards

def is_valid_date(date_str):
    try:
        datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def calculate_luck(cards):
    card_luck = {}
    card_rolls = {}
    for card in cards:
        card_def_id = card[0]
        reveal_effect_def_id = card[2]
        surface_effect_def_id = card[1]
        
        if card_def_id not in card_rolls:
            card_rolls[card_def_id] = 0
        card_rolls[card_def_id] += 1

        if card_def_id not in card_luck:
            card_luck[card_def_id] = 0

        # Calculate expected rolls
        roll_number = card_rolls[card_def_id]
        if roll_number >= 4:
            card_luck[card_def_id] -= 1  # Negative for every possible roll
        if roll_number >= 6:
            card_luck[card_def_id] -= 1  # Additional negative for Kirby roll

        # Calculate actual outcomes
        if "Ink" in surface_effect_def_id:
            card_luck[card_def_id] += 5  # Positive for hitting Ink
        if "Gold" in surface_effect_def_id:
            card_luck[card_def_id] += 5  # Positive for hitting Gold
        if "Kirby" in reveal_effect_def_id:
            card_luck[card_def_id] += 5  # Positive for hitting Kirby
        if "Ink" in surface_effect_def_id and "Kirby" in reveal_effect_def_id:
            card_luck[card_def_id] += 5  # Additional bonus for both
        if "Gold" in surface_effect_def_id and "Kirby" in reveal_effect_def_id:
            card_luck[card_def_id] += 5  # Additional bonus for both

    return card_luck, card_rolls

def format_card_name(card_name):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', card_name)

def track_droughts(cards):
    card_stats = {}

    for card in cards:
        card_def_id = card[0]
        surface_effect_def_id = card[1]
        reveal_effect_def_id = card[2]

        if card_def_id not in card_stats:
            card_stats[card_def_id] = {
                "Eligibility counter": 1,
                "Ink Drought": 0,
                "Max Ink Drought": 0,
                "Gold Drought": 0,
                "Max Gold Drought": 0,
                "Kirby Drought": 0,
                "Max Kirby Drought": 0,
            }
        else:
            card_stats[card_def_id]["Eligibility counter"] += 1

        # Ink Drought
        if card_stats[card_def_id]["Eligibility counter"] >= 4:
            if "Ink" not in surface_effect_def_id:
                card_stats[card_def_id]["Ink Drought"] += 1
                if card_stats[card_def_id]["Ink Drought"] > card_stats[card_def_id]["Max Ink Drought"]:
                    card_stats[card_def_id]["Max Ink Drought"] = card_stats[card_def_id]["Ink Drought"]
            else:
                card_stats[card_def_id]["Ink Drought"] = 0

        # Gold Drought
        if card_stats[card_def_id]["Eligibility counter"] >= 5:
            if "Gold" not in surface_effect_def_id:
                card_stats[card_def_id]["Gold Drought"] += 1
                if card_stats[card_def_id]["Gold Drought"] > card_stats[card_def_id]["Max Gold Drought"]:
                    card_stats[card_def_id]["Max Gold Drought"] = card_stats[card_def_id]["Gold Drought"]
            else:
                card_stats[card_def_id]["Gold Drought"] = 0

        # Kirby Drought
        if card_stats[card_def_id]["Eligibility counter"] >= 6:
            if "Kirby" not in reveal_effect_def_id:
                card_stats[card_def_id]["Kirby Drought"] += 1
                if card_stats[card_def_id]["Kirby Drought"] > card_stats[card_def_id]["Max Kirby Drought"]:
                    card_stats[card_def_id]["Max Kirby Drought"] = card_stats[card_def_id]["Kirby Drought"]
            else:
                card_stats[card_def_id]["Kirby Drought"] = 0

    longest_ink_drought = max(card_stats.items(), key=lambda x: x[1]["Max Ink Drought"])
    longest_gold_drought = max(card_stats.items(), key=lambda x: x[1]["Max Gold Drought"])
    longest_kirby_drought = max(card_stats.items(), key=lambda x: x[1]["Max Kirby Drought"])

    return longest_ink_drought, longest_gold_drought, longest_kirby_drought

def find_streaks(cards, card_rolls):
    streaks = {
        "highest_ink_streak": {"length": 0, "cards": []},
        "highest_gold_streak": {"length": 0, "cards": []},
        "highest_kirby_streak": {"length": 0, "cards": []}
    }

    current_streak = {
        "ink": [],
        "gold": [],
        "kirby": []
    }

    for card in cards:
        card_def_id = format_card_name(card[0])
        reveal_effect_def_id = card[2]
        surface_effect_def_id = card[1]
        roll_number = card_rolls[card[0]]

        # Handle ink streaks
        if "Ink" in surface_effect_def_id:
            current_streak["ink"].append(card_def_id)
            if len(current_streak["ink"]) > streaks["highest_ink_streak"]["length"]:
                streaks["highest_ink_streak"] = {"length": len(current_streak["ink"]), "cards": current_streak["ink"]}
        else:
            current_streak["ink"] = []

        # Handle gold streaks
        if "Gold" in surface_effect_def_id:
            current_streak["gold"].append(card_def_id)
            if len(current_streak["gold"]) > streaks["highest_gold_streak"]["length"]:
                streaks["highest_gold_streak"] = {"length": len(current_streak["gold"]), "cards": current_streak["gold"]}
        else:
            current_streak["gold"] = []

        # Handle kirby streaks
        if "Kirby" in reveal_effect_def_id:
            current_streak["kirby"].append(card_def_id)
            if len(current_streak["kirby"]) > streaks["highest_kirby_streak"]["length"]:
                streaks["highest_kirby_streak"] = {"length": len(current_streak["kirby"]), "cards": current_streak["kirby"]}
        else:
            current_streak["kirby"] = []

    return streaks

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
