import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import random

# --- Lore Page Easter Eggs ---
lore_pages = [
    "a tattered page titled 'The Alchemist's Theories I'...",
    "old scrolls mentioning 'The Fall of Pikemead's Reach'...",
    "a child's drawing of a 'Flame Shrine'...",
    "rumors of 'Manathor's experiments'...",
    "a note: 'Sudden Slaughter in the old quarter!'",
    "'On The Flame And Its Murmurs' offering hope...",
    "a map of 'Umbral Hollow - DANGER'...",
    "notes on 'Elixir Well Attenuation'...",
    "the 'Journal of a Bridge Builder'..."
]

# --- MAPPING OF CONCEPTUAL SETTING NAMES TO ACTUAL JSON KEYS ---
JSON_KEYS_MAP = {
    "PlayerHealth": ("gameSettings", "playerHealthFactor"),
    "ResourceYield": ("gameSettings", "resourceDropStackAmountFactor"),
    "EnemyDamage": ("gameSettings", "enemyDamageFactor"),
    "EnemyHealth": ("gameSettings", "enemyHealthFactor"),
    "ShroudTimer": ("gameSettings", "shroudTimeFactor"), 
    "PlayerStamina": ("gameSettings", "playerStaminaFactor") 
}

# --- Special (Secret) Lore Snippets and their Setting Triggers ---
special_lore_triggers = [
    {
        "condition_name": "The Frail Seer", 
        "settings_conditions": {"PlayerHealth": 0.25, "ShroudTimer": 0.5}, 
        "title": "A Visionary's Burden (An Echoed Fate)", # Added (An Echoed Fate) to title for thematic consistency
        "story": ["Elara was born with a delicate constitution (Player Health: Min).", "Yet, her mind blazed, foreseeing the Shroud's suffocatingly quick consumption (Shroud Timer: Min, less time).", "While others relied on brawn, Elara used chilling premonitions, often referencing 'the silence of the coming fog' from a forgotten text.", "She guided a few desperate souls, always a breath ahead of the encroaching doom.", "Her survival was an anomaly, a testament to foresight over frailty.", "Reaching a Cinder Vault felt like the last verse of a prophecy she'd always known.", "The pod's hum was a lullaby against a lifetime of heightened senses.", "She hoped for dreamless sleep, a respite from the visions.", "Attendants, awed, ushered her in with a mix of fear and reverence.", "With a final, quiet sigh, Elara stepped inside, and the pod door hissed closed, encasing her in a deep, protective slumber."]
    },
    {
        "condition_name": "The Unexpected Magnate", 
        "settings_conditions": {"ResourceYield": 2.0, "EnemyDamage": 0.75, "EnemyHealth": 0.75}, 
        "title": "The Gilded Cage (An Echoed Fate)",
        "story": ["Barnaby Chubb was a collector of curios in a world surprisingly benign (Enemy Stats: Low).", "His knack for 'finding things' meant his coffers overflowed with rare materials (Resource Yield: Max).", "While others scrimped, Barnaby's expeditions yielded treasures with almost comical ease, as if the world itself offered its bounty.", "Long before the Shroud was a tangible threat, he'd already secured a luxury Cinder Vault, more out of whim than fear.", "He even debated installing a snack bar, a detail he'd read about in 'Pre-Calamity Comforts'.", "He felt a twinge of guilt seeing the later scramble, offering what aid he could from his vast surplus.", "His pod was an opulent affair, a stark contrast to the utilitarian capsules elsewhere.", "As the mists rolled in, Barnaby double-checked his inventory of fine biscuits.", "A cheerful wave, a slight sigh for the inconvenience, and he was ready.", "With a satisfied nod at his preparations, Barnaby stepped inside, and the pod door hissed closed, encasing him in a deep, protective slumber."]
    },
    {
        "condition_name": "The Last Stand", 
        "settings_conditions": {"PlayerHealth": 1.0, "EnemyDamage": 2.5, "EnemyHealth": 2.5, "PlayerStamina": 0.25}, 
        "title": "Echoes of a Warrior (An Echoed Fate)",
        "story": ["Valerius 'Val' Stone knew only the crucible of a relentlessly hostile world (Enemy Stats: High).", "Every action was a monumental effort, energy a precious, fleeting resource (Player Stamina: Min).", "Their armor was a testament to survival, etched with tales of near-misses and hard-won victories, like those in the 'Ballad of the Scarred'.", "With no innate boons to health, only sheer will, Val carved a path through nightmares made real.", "The Shroud was but the final, overwhelming wave in an ocean of conflict.", "The Cinder Vault wasn't found; it was conquered, its threshold crossed through grit alone.", "They were a legend whispered among the fleeing, the one who faced the storm head-on.", "Rest felt like a foreign concept, an unearned luxury.", "Yet, even the strongest pillar must sometimes lean.", "With a warrior's weary resolve, Val stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."]
    },
    {
        "condition_name": "The Builder of Havens", 
        "settings_conditions": {"ResourceYield": 2.0, "EnemyDamage": 0.75, "EnemyHealth": 0.75, "PlayerStamina": 2.0}, 
        "title": "The Hearth Tender's Legacy (An Echoed Fate)",
        "story": ["Elara Swiftfoot was a beacon in a world that, for a fleeting moment, allowed for kindness (Enemy Stats: Low).", "Resources were abundant (Resource Yield: Max), her spirit tireless (Player Stamina: High), letting her build sanctuaries, not barricades.", "Her 'Principles of Communal Survival' became a whispered guide for many.", "While whispers of the Shroud grew, Elara organized, fortified, and fostered pockets of hope.", "She believed not in singular heroes, but in the strength of interwoven hands.", "Her own pod was a late consideration, a place lovingly prepared by those she'd tirelessly protected.", "She spent her final moments ensuring others were secure, her own safety secondary.", "The Shroud's arrival was a deep sorrow, but her work had laid down anchors of resilience.", "Her monuments were not of stone, but of saved lives and kindled spirits.", "With a heart full of hope for those she'd aided, Elara stepped inside, and the pod door hissed closed, encasing her in a deep, protective slumber."]
    },
    {
        "condition_name": "The One Who Walked Through Time (Almost)", 
        "settings_conditions": {"PlayerHealth": 2.0, "ShroudTimer": 2.0, "EnemyDamage": 1.0, "EnemyHealth": 1.0}, 
        "title": "The Patient Observer (An Echoed Fate)",
        "story": ["For Alistair Thorne, the world's end was a slow, unfolding tapestry (Shroud Timer: Max, more time).", "Blessed with remarkable vitality (Player Health: High), he had an eternity, it seemed, to observe the Shroud's languid, inexorable advance.", "His 'Chronicles of the Creeping Twilight' meticulously detailed the decay, a scholar's lament.", "While others rushed in panicked frenzy, Alistair calmly cataloged, prepared, and philosophized.", "The mundane dangers of a 'normal' world seemed almost quaint against this grand, slow-motion collapse (Enemy Stats: Normal).", "His entry into the Cinder Vault was less an escape, more a planned sabbatical from existence.", "He wondered if his meticulously kept journals, like 'Observations on Ancient Vases and Impending Doom,' would survive him.", "There was a profound, almost melancholic, peace in his unhurried preparations.", "He took one last, long look, a historian bidding adieu to his primary subject.", "With a scholar's sigh, Alistair stepped inside, and the pod door hissed closed, encasing him in a deep, protective slumber."]
    }
]

# --- Standard Lore Archetype Definitions ---
def check_blessed_caitiff(s):
    if None in [s.get("EnemyDamage"), s.get("EnemyHealth"), s.get("PlayerHealth"), s.get("PlayerStamina"), s.get("ResourceYield"), s.get("ShroudTimer")]: return False
    return (s["EnemyDamage"] <= 0.5 and s["EnemyHealth"] <= 0.5 and \
            s["PlayerHealth"] >= 2.5 and s["PlayerStamina"] >= 2.5 and \
            s["ResourceYield"] >= 1.5 and s["ShroudTimer"] >= 1.5)

def check_sheltered_scholar(s):
    if None in [s.get("EnemyDamage"), s.get("EnemyHealth"), s.get("PlayerHealth"), s.get("ResourceYield"), s.get("ShroudTimer")]: return False
    return (s["EnemyDamage"] <= 0.75 and s["EnemyHealth"] <= 0.75 and \
            s["PlayerHealth"] >= 1.0 and s["PlayerHealth"] < 2.5 and \
            s["ResourceYield"] >= 1.0 and s["ShroudTimer"] >= 1.0)

def check_grim_survivor(s):
    if None in [s.get("EnemyDamage"), s.get("EnemyHealth"), s.get("PlayerHealth"), s.get("PlayerStamina"), s.get("ShroudTimer")]: return False
    return (s["EnemyDamage"] >= 2.0 and s["EnemyHealth"] >= 2.0 and \
            s["PlayerHealth"] <= 0.75 and s["PlayerStamina"] <= 0.75 and \
            s["ShroudTimer"] <= 0.75)

def check_resourceful_operative(s):
    if None in [s.get("ResourceYield"), s.get("EnemyDamage"), s.get("EnemyHealth")]: return False
    return (s["ResourceYield"] == 2.0 and \
            (s["EnemyDamage"] > 0.75 and s["EnemyDamage"] < 2.0) and \
            (s["EnemyHealth"] > 0.75 and s["EnemyHealth"] < 2.0))

standard_lore_archetypes = [
    {
        "name": "The Blessed Caitiff",
        "check_func": check_blessed_caitiff,
        "title": "Tale of the Favored One",
        "story_template": [
            "{name} moved through a world that bent to their will, dangers dissolving like mist (Enemy Stats: Very Low).",
            "Their vitality was legendary, their energy boundless (Player Stats: Very High); some whispered they were touched by a benevolent, forgotten god.",
            "Resources practically leaped into their satchels (Resources: Abundant), and even the dreaded Shroud seemed to offer more time than for others (Shroud Timer: Generous).",
            "They had little cause for true struggle, their days filled with mastering skills or grand explorations, a stark contrast to common folk tales like '{easter_egg}'.",
            "The encroaching global panic was, at first, a distant rumor, an almost abstract threat to their charmed existence.",
            "It was only when the skies truly darkened and the air grew thick with despair that the gravity of the situation pierced their bubble of fortune.",
            "Securing a Cinder Vault pod was less a desperate scramble and more a... logical, if somber, next step, arranged with disconcerting ease.",
            "They paused, perhaps for the first time feeling a tremor of uncertainty for a world they had so effortlessly dominated.",
            "The pod's antechamber felt cold, impersonal, a stark contrast to their vibrant life.",
            "With a sigh that mingled surprise with a newfound solemnity, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "name": "The Sheltered Scholar/Artisan",
        "check_func": check_sheltered_scholar,
        "title": "Chronicle of the Quiet Study",
        "story_template": [
            "In a relatively serene corner of the world, {name} dedicated their life to knowledge or craft (Enemy Stats: Low).",
            "Their days were measured by the turning of pages, the stroke of a brush, or the ring of a hammer, not the clang of steel against monster hide.",
            "While not overtly powerful (Player Stats: Normal), their environment was forgiving, allowing focus on their chosen pursuit, perhaps inspired by texts like '{easter_egg}'.",
            "Resources were sufficient for their needs (Resources: Normal), and the Shroud's embrace felt less immediate, more a creeping shadow than a rushing tide (Shroud Timer: Normal/Generous).",
            "News of growing chaos in distant lands arrived like troubling dispatches, discussed in hushed tones but not yet a direct assault on their peaceful enclave.",
            "The call for 'preservation in the Vaults' came as a shock, a directive that tore {name} from their work.",
            "Their skills, though not martial, were deemed valuable enough for a pod, a testament to a world that still valued more than just warriors.",
            "They packed a few precious tools or books, symbols of a life they hoped might one day resume.",
            "The pod felt like a stark, metallic bookmark in the unfinished chapter of their life.",
            "With a mind full of unread pages or unfinished creations, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "name": "The Resourceful Operative",
        "check_func": check_resourceful_operative,
        "title": "The Broker's Gambit",
        "story_template": [
            "{name} had always possessed a keen eye for opportunity and a knack for navigating the intricate dance of supply and demand (Resources: Max).",
            "The world, while possessing its share of dangers (Enemy Stats: Moderate), was a vibrant marketplace for those who knew where to look and how to trade.",
            "They weren't a mighty warrior nor a reclusive scholar, but their network and resourcefulness were legendary, some said they could find 'ice in the Kindlewastes'.",
            "Old tales like '{easter_egg}' often spoke of hidden caches, and {name} had a talent for finding them or making them appear.",
            "When the Shroud began its deadly creep, {name} saw not just disaster, but also the ultimate, desperate market.",
            "Information, safe passage, rare components for the Cinder Vaults – everything had a price, and {name} was positioned to deal.",
            "Their own pod was secured not through heroism, but through a series of shrewd transactions and carefully called-in favors.",
            "They watched the old world's currencies crumble, knowing the only true value left was survival.",
            "The pod was a secure investment, a calculated risk against total annihilation.",
            "With a final ledger closed in their mind, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "name": "The Grim Survivor",
        "check_func": check_grim_survivor,
        "title": "Saga of Scars and Will",
        "story_template": [
            "For {name}, life had always been a bitter struggle against a harsh, unforgiving world (Enemy Stats: High).",
            "Their body was a map of scars, each a testament to a narrowly averted doom (Player Health: Low), their energy a guttering candle in a gale (Player Stamina: Low).",
            "Resources were meager, fought for tooth and nail, and the encroaching Shroud offered little time for respite (Shroud Timer: Short).",
            "They had no grand library or overflowing storehouse; their treasures were a sharp blade and the grim determination to see another sunrise, a sentiment echoed in dark tales like '{easter_egg}'.",
            "The Shroud's arrival was merely an escalation of the daily horrors they already faced, a new, more pervasive predator.",
            "The Cinder Vaults were a rumor of impossible salvation, a whisper in the screams of the dying.",
            "Reaching a pod was not a plan, but a desperate, instinct-driven flight, fueled by sheer, unyielding will.",
            "They carried nothing but the weight of their brutal experiences and a flicker of defiance.",
            "The pod was an alien thing, a sterile haven so unlike the blood-soaked earth they knew.",
            "With a defiant breath drawn against a world that had tried its best to break them, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    { 
        "name": "The Everyman/Everywoman",
        "check_func": lambda s: True, 
        "title": "An Ordinary Dawn, An Extraordinary Twilight",
        "story_template": [
            "{name} lived a life of simple routines and familiar faces in a world that felt, for the most part, stable (All Stats: Balanced/Normal).",
            "Their days were filled with the common toils and small joys of an average citizen, far from heroic deeds or arcane studies.",
            "They might have heard travelers' tales or read an odd passage in '{easter_egg}', but such things were curiosities, not premonitions.",
            "The Shroud crept into their reality like a bad dream, slowly at first, then with terrifying speed, turning normalcy into chaos.",
            "Panic spread, and the familiar world warped into something hostile and strange.",
            "Whispers of the Cinder Vaults, the 'Flameborn' project, began as desperate hopes shared among the fleeing.",
            "{name} found themselves swept up in the tide of events, a common soul facing an uncommon doom.",
            "Perhaps it was luck, a moment of quick thinking, or the kindness of a stranger that led them to an open pod.",
            "The future was a terrifying unknown, a stark departure from their predictable past.",
            "With a heart pounding with fear and a sliver of hope, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    }
]

class LoreGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Enshrouded Lore Generator (JSON Driven)")
        master.geometry("900x700") # Adjusted for better layout

        self.json_data = None 
        self.json_loaded_successfully = False
        self.loaded_filename = None

        info_text = "Enshrouded Backstory Generator\nLoad your server JSON file to generate a world and character backstory."
        self.label_info = tk.Label(master, text=info_text, font=("Arial", 14))
        self.label_info.pack(pady=10)

        self.player_name_label = tk.Label(master, text="Enter Character Name (Optional):")
        self.player_name_label.pack(pady=(5,0))
        self.player_name_entry = tk.Entry(master, width=30)
        self.player_name_entry.pack(pady=2)
        self.player_name_entry.insert(0, "My Flameborn")

        self.json_frame = tk.LabelFrame(master, text="Load Server Settings File", padx=10, pady=10)
        self.json_frame.pack(pady=20, padx=10, fill="x")

        self.btn_load_json = tk.Button(self.json_frame, text="Load JSON Settings File", command=self.load_json_file, font=("Arial", 10, "bold"))
        self.btn_load_json.pack(pady=5)
        self.json_status_label = tk.Label(self.json_frame, text="No JSON file loaded. Please load a file to generate lore.")
        self.json_status_label.pack(pady=5)
        
        self.btn_generate = tk.Button(master, text="Generate Lore from JSON", command=self.generate_and_display_lore, font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.btn_generate.pack(pady=20)
        
        self.lore_text_frame = tk.LabelFrame(master, text="Generated Lore", padx=10, pady=10)
        self.lore_text_frame.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.lore_text = tk.Text(self.lore_text_frame, wrap=tk.WORD, width=80, height=18, relief=tk.SUNKEN, borderwidth=2)
        self.lore_text.pack(pady=5, padx=5, expand=True, fill=tk.BOTH)
        self.lore_text.insert(tk.END, "Please load your Enshrouded server JSON file and click 'Generate Lore'.")
        self.lore_text.config(state=tk.DISABLED)

    def load_json_file(self):
        filepath = filedialog.askopenfilename(
            title="Select your Enshrouded Server JSON file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        self.json_loaded_successfully = False 
        self.json_data = None
        self.loaded_filename = None
        self.btn_generate.config(state=tk.DISABLED)

        if not filepath:
            self.json_status_label.config(text="File selection cancelled. Please load a file.", fg="orange")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
            self.loaded_filename = filepath.split('/')[-1]
            self.json_status_label.config(text=f"JSON Ready: {self.loaded_filename}", fg="green")
            self.json_loaded_successfully = True
            self.btn_generate.config(state=tk.NORMAL)
            self.lore_text.config(state=tk.NORMAL)
            self.lore_text.delete("1.0", tk.END)
            self.lore_text.insert(tk.END, f"JSON file '{self.loaded_filename}' loaded. Click 'Generate Lore from JSON'.")
            self.lore_text.config(state=tk.DISABLED)
        except FileNotFoundError:
            messagebox.showerror("File Error", f"The file was not found at the specified path:\n{filepath}")
            self.json_status_label.config(text="Error: File not found. Load a new file.", fg="red")
        except PermissionError:
            messagebox.showerror("Permission Error", f"Could not open file due to insufficient permissions:\n{filepath}\nPlease check file permissions.")
            self.json_status_label.config(text="Error: Permission denied. Load a new file.", fg="red")
        except json.JSONDecodeError as e:
            err_msg = f"The file is not a valid JSON.\nFile: {self.loaded_filename or filepath.split('/')[-1]}\nDetails: {e.args[0]}"
            if hasattr(e, 'lineno') and hasattr(e, 'colno'):
                err_msg += f" (near line {e.lineno} column {e.colno})"
            messagebox.showerror("JSON Parsing Error", err_msg)
            self.json_status_label.config(text="Error: Invalid JSON format. Load a new file.", fg="red")
        except Exception as e:
            error_type = type(e).__name__
            messagebox.showerror("Unexpected Error", f"An unexpected {error_type} occurred while processing the file: {self.loaded_filename or filepath.split('/')[-1]}\nDetails: {str(e)}")
            self.json_status_label.config(text=f"Error: {error_type} during load. Load a new file.", fg="red")

    def get_settings_from_json(self):
        if not self.json_loaded_successfully or not self.json_data:
            return None
        extracted_settings = {}
        missing_keys_messages = []
        type_errors_messages = []
        parent_object_name = "gameSettings"
        game_settings_obj = self.json_data.get(parent_object_name)

        if not isinstance(game_settings_obj, dict):
            messagebox.showerror("JSON Structure Error", f"The crucial '{parent_object_name}' object was not found or is not a valid dictionary in '{self.loaded_filename}'.\nCannot generate lore.")
            self.json_status_label.config(text=f"JSON Error: '{parent_object_name}' missing/invalid in {self.loaded_filename}.", fg="red")
            return None
        for conceptual_key, (parent_key_in_map, actual_json_key) in JSON_KEYS_MAP.items():
            if parent_key_in_map != parent_object_name: continue
            value = game_settings_obj.get(actual_json_key)
            if value is None:
                missing_keys_messages.append(f"'{conceptual_key}' (\"{parent_object_name}\".\"{actual_json_key}\")")
                extracted_settings[conceptual_key] = None 
            else:
                try:
                    extracted_settings[conceptual_key] = float(value)
                except (ValueError, TypeError):
                    type_errors_messages.append(f"Value for \"{actual_json_key}\" ('{value}') is not a number.")
                    extracted_settings[conceptual_key] = None 
        if missing_keys_messages:
            messagebox.showwarning("JSON Data Warning - Missing Keys",
                                   "Could not find the following expected keys under 'gameSettings':\n- " + "\n- ".join(missing_keys_messages) +
                                   "\nDefault values (typically 1.0) will be assumed for lore generation where these settings are influential.")
        if type_errors_messages:
            messagebox.showwarning("JSON Data Warning - Type Errors",
                                   "Found non-numeric values for the following keys under 'gameSettings':\n- " + "\n- ".join(type_errors_messages) +
                                   "\nThese settings will be treated as default/average (typically 1.0) for lore generation.")
        # Ensure all conceptual keys are in extracted_settings, defaulting to 1.0 if missing/invalid
        # This helps simplify the check_func logic for standard archetypes
        for conceptual_key in JSON_KEYS_MAP.keys():
            if extracted_settings.get(conceptual_key) is None:
                 extracted_settings[conceptual_key] = 1.0 # Default to 1.0 if missing or type error
        return extracted_settings

    def check_secret_lore_conditions(self, extracted_settings):
        if not extracted_settings: return None
        for trigger_def in special_lore_triggers:
            match = True
            for setting_name, required_value in trigger_def["settings_conditions"].items():
                json_value = extracted_settings.get(setting_name)
                if json_value is None: match = False; break 
                op_type = "exact" 
                if setting_name in ["EnemyDamage", "EnemyHealth"]:
                    if trigger_def["condition_name"] in ["The Unexpected Magnate", "The Builder of Havens"]: op_type = "lte" 
                    elif trigger_def["condition_name"] == "The Last Stand": op_type = "gte" 
                if op_type == "exact":
                    if not (abs(json_value - required_value) < 0.001): match = False; break
                elif op_type == "lte":
                    if not (json_value <= required_value + 0.001): match = False; break
                elif op_type == "gte":
                    if not (json_value >= required_value - 0.001): match = False; break
            if match: return trigger_def
        return None

    def determine_standard_lore_archetype(self, extracted_settings):
        if not extracted_settings: 
            extracted_settings = {key: 1.0 for key in JSON_KEYS_MAP.keys()}
            
        for archetype in standard_lore_archetypes:
            if archetype["check_func"](extracted_settings):
                return archetype
        return standard_lore_archetypes[-1] 

    def generate_and_display_lore(self):
        player_name = self.player_name_entry.get() if self.player_name_entry.get() else "The Flameborn"
        final_story_sentences = []
        lore_title = "Lore Generation Result"
        status_message = f"Processing {self.loaded_filename}..."
        status_color = "blue"
        self.json_status_label.config(text=status_message, fg=status_color)
        self.master.update_idletasks() 

        if not self.json_loaded_successfully or not self.json_data:
            messagebox.showerror("Error", "No JSON file loaded or file is invalid. Please load a valid Enshrouded server JSON file.")
            self.json_status_label.config(text="Error: No valid JSON. Load file.", fg="red")
            self.btn_generate.config(state=tk.DISABLED)
            return

        extracted_settings = self.get_settings_from_json()
        if extracted_settings is None: 
            self.json_status_label.config(text=f"Critical error processing {self.loaded_filename}. See warnings.", fg="red")
            return 

        triggered_secret_lore = self.check_secret_lore_conditions(extracted_settings)

        if triggered_secret_lore:
            lore_title = triggered_secret_lore["title"]
            final_story_sentences = triggered_secret_lore["story"]
            status_message = f"An Echoed Fate revealed in {self.loaded_filename}!"
            status_color = "purple" 
            
            # Thematic notification for secret lore
            messagebox.showinfo("A Twist in the Weave!", 
                                "Hark, Flameborn! The currents of Embervale have shifted in a most curious way, revealing a destiny few could have foreseen. A veiled chapter of your arrival unfurls...\n\n*(This is but one of five such extraordinary fates whispered to exist before the Great Slumber.)*")
        else:
            standard_archetype = self.determine_standard_lore_archetype(extracted_settings)
            lore_title = standard_archetype["title"]
            selected_easter_egg = random.choice(lore_pages)
            for sentence_template in standard_archetype["story_template"]:
                final_story_sentences.append(sentence_template.format(name=player_name, easter_egg=selected_easter_egg))
            status_message = f"Lore generated from {self.loaded_filename}."
            status_color = "darkgreen"
            
        final_story_str = " ".join(final_story_sentences)
        self.json_status_label.config(text=status_message, fg=status_color)
        self.lore_text_frame.config(text=lore_title)
        self.lore_text.config(state=tk.NORMAL)
        self.lore_text.delete("1.0", tk.END)
        self.lore_text.insert(tk.END, final_story_str)
        self.lore_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = LoreGeneratorApp(root)
    root.mainloop()