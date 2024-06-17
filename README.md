# SnapSplitSummary
Looks at CollectionState.json to give you information about your collection. This will generate two text files;

output.txt contains a raw alphabetized list of all of your splits.

summary.txt contains information about your ink/gold/kirby splits, as well as your total split count per character in order of most splits.

It will also generates an html file which will pop open in a browser tab to give you a quick overview of the results after running the script
# Warning
This program does not share your information, everything is run locally on your machine. Always be wary of running unknown code, this program was written with the help of AI, run at your own risk. This does not edit or read your game files directly, you must manually locate the file and create a copy in this programs directory for it to work.  
# Usage
1. Locate your CollectionState.json, this is typically found in C:\Users\<current user>\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod
2. Copy and paste your CollectionState file into the same folder as ImportSnap.py
3. Run RunImport.bat
# What the code does exactly;
CollectionState.json contains a wide variety of information including a full list of all of your cards, variants, and splits. This script looks specifically at the "Cards" subsection and creates a simplified list of splits (Cards with a Foil, Prism, Ink, or Gold background), it disregards any custom cards. Then it does some correcting to improve readability as Rainbow splits aren't specifically mentioned in the json the same way colors are, for example Red Krackle flare appears as "KirbyRed" but Rainbow Krackle flare is simply "Kirby". This is simplified to (name) (background) (flare) such as "AmericaChavez GoldFoil KirbyRainbow"

It then goes through the cleaned output to generate a summary, this includes your total number of splits, number of splits per character, and how many of those splits had the potential to roll ink, gold, or krackle. This is calculated by looking at the total number of splits for a card, split 4 onwards counts towards ink rolls, 5 onwards for gold rolls, and 6 for kirby rolls. It will also count your Ink, Gold, and Kirby splits, and splits that hit both ink/gold and kirby as "god splits". A short summary will pop open in a browser window; 
![output](https://github.com/Jjerot/SnapSplitSummary/assets/172853898/bb7faecc-86f9-4bca-8a74-cf80798953a6)
