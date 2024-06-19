# SnapSplitSummary
Looks at CollectionState.json to get information about your Marvel Snap collection and various split statistics. This will generate a raw chronological list of all of your splits in output.txt as well as an HTML file that will pop open in a browser tab to give you a quick overview of the results after running the script.

![sumv4](https://github.com/Jjerot/SnapSplitSummary/assets/172853898/0000240b-047f-4997-bf85-302c9255cefc)

# Warning
This program does not collect or share your information; everything is run locally on your machine. It will not modify your game files, it simply reads from them. Always be wary of running unknown code. This program was written with the help of AI; run at your own risk. If you're uncomfortable with the idea of this script looking into your game folder directly, you can switch to the version 1 branch which reads from a copy of your collectionstate.json that you will have to provide manually. (Copy pasting it into the folder with the script) 
# Requirements
-Windows PC 

-Python 3.11 or later (probably works on earlier versions, untested) (Download from Python.org)

-Marvel Snap installed through Steam, may have to play a game for information to update. 
# Usage
1. Unzip folder
2. Run RunImport.bat
# What the code does exactly;
CollectionState.json contains a wide variety of information, including a full list of all of your cards, variants, and splits. This script looks specifically at the "Cards" subsection and creates a chronological list of cards with a foil, prism, ink, or gold background, disregarding any custom cards. This is simplified to (CardDefId) (SurfaceEffectDefId) (CardRevealEffectDefId) (TimeCreated), E.g. "AmericaChavez GoldFoil KirbyRed 2023-02-16T03\:24:41.045Z". Additional formatting changes are made to non-specific flare names such as "Sparkle" to "SparkleRainbow" for clarity as Rainbow isn't listed like other flare colors. This is saved to output.txt in the same directory the script was run in.

It then goes through the cleaned output to generate a summary, which includes your total number of splits, the number of splits per card to find your top 3 most split characters, how many of each flare color you have found, and how many splits had the potential to roll ink, gold, or krackle. This is calculated by looking at the total number of splits for a card, with split 4 onwards counting towards ink rolls, 5 onwards for gold rolls, and 6+ for kirby rolls. It will also count your total ink, gold, and kirby splits, as well those that hit both ink or gold and kirby. This summary is displayed in a browser window and saved as summary.html. Rerunning the script will overwrite previous saved results.

Update; Added some fancy code to approximate which character is your luckiest and unluckiest (based on total splits and how many "good" outcomes you roll). This also goes through the output.txt and calculates your longest lucky streaks and droughts for each split type, updating the summary.html and output.txt with all of this information for easy browsing/sharing.  

