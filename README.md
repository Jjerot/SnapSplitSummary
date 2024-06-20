# SnapSplitSummary
Looks at CollectionState.json to get information about your Marvel Snap collection and various split statistics. This will generate a raw chronological list of all of your splits in rawlist.txt, output useful statistics to statistics.txt as well as summary.html that will open in a browser tab to give you a quick overview of the results after running the script.

![sumv5](https://github.com/Jjerot/SnapSplitSummary/assets/172853898/8d514ec4-6297-4b7d-b983-d1e294fbe566)

# Disclaimer
This program does not collect or share your information; everything is run locally on your machine. It will not modify your game files, it simply reads from CollectionState.json found in AppData\LocalLow. Always be wary of running unknown code. This program was written with the help of AI; run at your own risk. If you're uncomfortable with the idea of this script looking into your game folder directly, you can switch to the version 1 branch which reads from a copy of your collectionstate.json that you will have to provide manually. (Copy pasting it into the folder with the script) 
# Requirements
-Windows PC 

-Marvel Snap installed through Steam, may have to play a game for information to update. 

# Usage
Release version:
1. Unzip folder
2. Run ImportSnap.exe
   
Alternatively, if you are uncomfortable downloading it as an .exe, I've included a batch file with the python script version. 

1. Unzip folder
2. Click ImportSnap.bat

Note: This will require Python 3.11 or later (probably works on earlier versions, untested) (Download from Python.org)

# What the code does exactly;
CollectionState.json contains a wide variety of information, including a full list of all of your cards, variants, and splits. This script looks specifically at the "Cards" subsection and creates a chronological list of cards with a foil, prism, ink, or gold background, disregarding any custom cards. This is simplified to (CardDefId) (SurfaceEffectDefId) (CardRevealEffectDefId) (TimeCreated), E.g. "AmericaChavez GoldFoil KirbyRed 2023-02-16T03\:24:41.045Z". Additional formatting changes are made to non-specific flare names such as "Sparkle" to "SparkleRainbow" for clarity as Rainbow isn't listed like other flare colors. This is saved to rawlist.txt

It then goes through the cleaned output to generate a summary which includes; 

-Total splits

-The number of each background and flare and total number of possible rolls for each

-A count of all flare colors

-Number of Splits per character (top 3 are displayed)

-A breakdown of what you've found on splits 2-3, 4, 5, and 6 precisely. (How many times you hit ink/gold/krackle on the first possible split, useful stats for data collection should you wish to share them)

-Calculates your "luckiest" and "unluckiest" (nemesis) cards based on their total number of splits and how many desirable outcomes they've rolled. 

This is saved to summary.html and displayed after the program is run
