# SnapSplitSummary
Looks at CollectionState.json to get information about your Marvel Snap collection and various split statistics. This will generate a raw alphabetized list of all of your splits in output.txt as well as an HTML file that will pop open in a browser tab to give you a quick overview of the results after running the script.

![output](https://github.com/Jjerot/SnapSplitSummary/assets/172853898/bb7faecc-86f9-4bca-8a74-cf80798953a6)
# Warning
This program does not collect or share your information; everything is run locally on your machine. It will not modify your game files, it simply reads from them. Always be wary of running unknown code. This program was written with the help of AI; run at your own risk.
# Requirements
-Windows PC 

-Python 3.11 or later (probably works on earlier versions, untested) (Download from Python.org)

-Marvel Snap installed through Steam, may have to play a game for information to update. 
# Usage
1. Unzip folder
2. Run RunImport.bat
# What the code does exactly;
CollectionState.json contains a wide variety of information, including a full list of all of your cards, variants, and splits. This script looks specifically at the "Cards" subsection and creates an alphabetical list of cards with a foil, prism, ink, or gold background, disregarding any custom cards. This is simplified to (name) (background) (flare), such as "AmericaChavez GoldFoil KirbyRed". Additional formatting lists default flare names like "Sparkle" as "SparkleRainbow" for clarity as it isn't labeled by default like the other colors.

It then goes through the cleaned output to generate a summary, which includes your total number of splits, the number of splits per character sorted from most to least, and how many of those splits had the potential to roll ink, gold, or krackle. This is calculated by looking at the total number of splits for a card, with split 4 onwards counting towards ink rolls, 5 onwards for gold rolls, and 6+ for kirby rolls. It will also count your total ink, gold, and kirby splits, as well those that hit both ink/gold and kirby as "god splits". This summary is displayed in a browser window with the results saved as summary.html. Rerunning the script will overwrite previous results. 

