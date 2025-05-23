# enshrouded-lore-generator
Generate unique character backstories for Enshrouded! This app creates personalized lore leading up to the Shroud event, with a few hidden fates to uncover.  This tool is a Python and Tkinter application that reads your `enshrouded_server.json` file.

**Will your tale be one of an ordinary citizen caught in the chaos, a hardened survivor from a brutal land, or perhaps something far more ... peculiar?**

## Features

* **JSON-Driven Lore:** Your server's settings directly shape the generated backstory. The lore reflects the kind of world you've configured, from player power and resource availability to enemy difficulty and the nature of the Shroud itself.
* **Dynamic Standard Archetypes:** Based on your `gameSettings` in the JSON file, the script categorizes your world and generates a fitting standard origin story. Archetypes include:
    * **The Blessed Caitiff:** For worlds with very easy settings and a powerful player character.
    * **The Sheltered Scholar/Artisan:** For easy worlds where peaceful pursuits were possible.
    * **The Resourceful Operative:** For balanced worlds with a focus on resource abundance.
    * **The Grim Survivor:** For very difficult worlds that demand resilience.
    * **The Everyman/Everywoman:** For balanced/default settings, or as a general fallback.
* **Echoed Fates (Secret Lore):** If your server settings align with one of five specific and rare configurations, a unique "Echoed Fate" lore will be unveiled! This special narrative will be presented with a thematic notification:
* **Personalized Touch:** Enter your character's name to have it woven into the narrative.
* **In-Game Easter Eggs:** Keep an eye out for subtle references to lore pages found within Enshrouded!
* **GUI Interface:** Easy-to-use Tkinter interface for loading your JSON file and displaying the generated lore.
* **No External Dependencies:** Runs with a standard Python 3 installation (includes Tkinter, JSON, and Random modules).

## How to Use

1.  **Ensure Python 3 is installed.**
2.  **Download `enshrouded_origin.py`.**
3.  **Run the script:** `python enshrouded_origin.py`
4.  Click the "**Load JSON Settings File**" button and select your `enshrouded_server.json` file.
    * The script expects the standard Enshrouded server configuration structure, particularly the `gameSettings` object.
5.  Optionally, enter your desired character name.
6.  Click the "**Generate Lore from JSON**" button.
7.  Read your character's unique origin story! If your settings trigger an "Echoed Fate," you'll receive a special notification.

## Understanding the Lore Generation

* **Standard Lore:** The script analyzes various factors from your `gameSettings` (like `playerHealthFactor`, `resourceDropStackAmountFactor`, `enemyDamageFactor`, `shroudTimeFactor`, etc.) to determine a general "feel" for your world and character's likely experiences pre-Shroud.
* **Echoed Fates (Secret Lore):** These are triggered by very specific combinations of settings in your `gameSettings`. Discovering them is part of the fun!

## Important Notes

* **JSON File Structure:** The script is designed based on the `enshrouded_server.json` structure detailed in official Enshrouded server documentation (up to around Update 0.8.1.0 as of the script's knowledge cutoff). If the JSON structure changes significantly in future game updates, the script's parsing logic might need adjustments. The script primarily looks for numerical values within the `gameSettings` object.
* **Error Handling:** The script includes error handling for common issues like file not found, invalid JSON format, or missing `gameSettings`. It will attempt to provide informative messages. If critical data is missing or unparseable, lore generation may not be possible.

## License & Contribution

This script (`enshrouded_origin.py`) is provided as-is without any formal license. You are absolutely free to use, modify, and distribute it however you wish for personal or community use.

While not required, if you find this tool enjoyable or build something cool upon it, a small credit or shout-out would be greatly appreciated!

---

*Disclaimer: This tool is a fan-made project and is not officially affiliated with Keen Games GmbH or Enshrouded.*
