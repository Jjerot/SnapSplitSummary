# SnapSplitSummary
Looks at CollectionState.json to get information about your Marvel Snap collection. This will generate two text files:

output.txt contains a raw alphabetized list of all of your splits.

summary.txt contains information about your ink/gold/kirby splits, as well as your total split count per character in order of most splits.

It will also generate an HTML file that will pop open in a browser tab to give you a quick overview of the results after running the script.
# Warning
This program does not share your information; everything is run locally on your machine. Always be wary of running unknown code. This program was written with the help of AI; run at your own risk. This does not read or edit your game files directly, you must manually locate the file and create a copy in this program's directory for it to work.  
# Requirements
-Windows PC 

-Python 3.11 or later (probably works on earlier versions, untested) (Download from Python.org)

-Marvel Snap installed through Steam, may have to play a game for information to update. 
# Usage
1. Locate your CollectionState.json, this is typically found in C:\Users\\{current user}\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod
2. Copy and paste your CollectionState file into the same folder as ImportSnap.py (Do not delete or modify the original file)
3. Run RunImport.bat
# What the code does exactly;
CollectionState.json contains a wide variety of information, including a full list of all of your cards, variants, and splits. This script looks specifically at the "Cards" subsection and creates an alphabetical list of cards with a foil, prism, ink, or gold background, disregarding any custom cards. This is simplified to (name) (background) (flare), such as "AmericaChavez GoldFoil KirbyRed". It then adds tags to Rainbow splits as they aren't displayed in the JSON the same way colors are, for example, Red Krackle flare appears as "SurfaceEffectDefId": "KirbyRed" but Rainbow Krackle flare is simply "Kirby". 

It then goes through the cleaned output to generate a summary, which includes your total number of splits, the number of splits per character sorted from most to least, and how many of those splits had the potential to roll ink, gold, or krackle. This is calculated by looking at the total number of splits for a card, with split 4 onwards counting towards ink rolls, 5 onwards for gold rolls, and 6+ for kirby rolls. It will also count your total ink, gold, and kirby splits, as well those that hit both ink/gold and kirby as "god splits". A short summary will pop open in a browser window which looks like this;

![output](https://github.com/Jjerot/SnapSplitSummary/assets/172853898/bb7faecc-86f9-4bca-8a74-cf80798953a6)
