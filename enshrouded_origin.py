import tkinter as tk
from tkinter import ttk, filedialog, messagebox # Added ttk
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
    "the 'Journal of a Bridge Builder'...",
    "a faded inscription: 'Only the Flame can cleanse the Shroud.'",
    "the 'Lay of the Land' survey, marking fertile grounds now lost."
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
# Each now tied to an NPC
special_lore_triggers = [
    {
        "condition_name": "The Frail Seer (Balthazar's Apprentice)", 
        "settings_conditions": {"PlayerHealth": 0.25, "ShroudTimer": 0.5}, 
        "title": "A Visionary's Burden, with Balthazar (An Echoed Fate)",
        "story": [
            "{name} was Balthazar's most curious apprentice, frail of body (Player Health: Min) but possessing a mind that touched the ethereal.",
            "While Balthazar delved into volatile alchemy, {name}'s unsettling visions painted futures choked by a swift, suffocating Shroud (Shroud Timer: Min).",
            "Many dismissed {name}'s whispers as side effects of the Alchemist's fumes, but Balthazar, a man of arcane science, saw a disturbing clarity in them.",
            "It was {name}'s foresight, coupled with Balthazar's desperate ingenuity, that led them to a secluded Cinder Vault when the first true horrors manifested.",
            "They worked feverishly, Balthazar on unstable concoctions for preservation, {name} on deciphering the fragmented prophecies found in texts like '{easter_egg}'.",
            "The Alchemist often muttered about 'unintended consequences' and 'the price of knowledge,' his gaze distant.",
            "Balthazar ensured {name}'s entry into a pod, believing their fragile life held a unique key to understanding the calamity.",
            "He spoke of ancient pacts and the Flame's guidance, a heavy burden for his young, seer apprentice.",
            "The pod felt like a crucible, promising either oblivion or a rebirth into a world {name} had already seen in terrifying detail.",
            "With Balthazar's final, sorrowful nod, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "condition_name": "The Unexpected Magnate (Emily Fray's Partner)", 
        "settings_conditions": {"ResourceYield": 2.0, "EnemyDamage": 0.75, "EnemyHealth": 0.75}, 
        "title": "The Gilded Valley, with Emily Fray (An Echoed Fate)",
        "story": [
            "{name} was a landowner in a valley so fertile it was legendary, a place where Emily Fray's agricultural genius truly blossomed (Enemy Stats: Low).",
            "Together, they transformed the land into a paradise of abundance, its yields unmatched (Resource Yield: Max), its larders always overflowing.",
            "While whispers of blight reached other lands, their valley remained a vibrant sanctuary, almost untouched by the early signs of decay.",
            "Emily often shared ancient farming secrets, gleaned from texts like '{easter_egg}', that made their harvests miraculous.",
            "Their wealth, derived from this boundless bounty, allowed them to secure positions in the most advanced Cinder Vaults with little effort.",
            "It was a strange, insulated existence; they heard of the encroaching Shroud but saw little of its direct horror until the very end.",
            "{name} and Emily Fray ensured their community's key members also had pods, using their influence for this quiet exodus.",
            "The irony was not lost on {name} – a life of plenty leading to a sterile, metallic sleep, all to escape a world starving for hope.",
            "Emily's last words to {name} were about preserving seeds, a promise of a new spring.",
            "With a heart strangely heavy despite their fortune, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "condition_name": "The Last Stand (Oswald's Shieldmate)", 
        "settings_conditions": {"PlayerHealth": 1.0, "EnemyDamage": 2.5, "EnemyHealth": 2.5, "PlayerStamina": 0.25}, 
        "title": "The Siege of Anders' Forge, with Oswald (An Echoed Fate)",
        "story": [
            "In a war-ravaged borderland where every sunrise was a battle cry (Enemy Stats: High), {name} stood as a shield against the encroaching dark.",
            "Their stamina was pushed to its limits daily (Player Stamina: Min), but their resolve, like Oswald Anders' steel, never broke (Player Health: Normal).",
            "Oswald's forge was the heart of their dwindling fortress, its fires a defiant glow against the gloom, tirelessly mending the weapons {name} and others wielded.",
            "They say Oswald could hammer resilience into metal, a skill sorely needed as the Shroud empowered their human and inhuman foes.",
            "The last Cinder Vault in their region was within the fortress. Its defense was their final, impossible stand.",
            "{name} fought alongside Oswald, the clang of his hammer a rhythm to the chaos, inspired by tales of legendary smiths in '{easter_egg}'.",
            "The Blacksmith, grimy and exhausted, forced {name} towards the pod, bellowing that some spark of defiance must survive.",
            "He spoke of a 'purer Flame' that might one day reforge the world, his words almost lost in the din of battle.",
            "The pod represented not just survival, but a debt to those who fell protecting it.",
            "With the roar of the siege echoing in their ears, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "condition_name": "The Builder of Havens (Cade's Colleague)", 
        "settings_conditions": {"ResourceYield": 2.0, "EnemyDamage": 0.75, "EnemyHealth": 0.75, "PlayerStamina": 2.0}, 
        "title": "The Carpenter's Sanctuary, with Cade (An Echoed Fate)",
        "story": [
            "{name} possessed a vision for structure and safety in a world that was, for a time, blessedly calm (Enemy Stats: Low).",
            "Working alongside Cade, the pragmatic Carpenter, they utilized the land's rich bounty (Resource Yield: Max) with seemingly limitless energy (Player Stamina: High).",
            "While Cade focused on sturdy homes and functional workshops, {name} helped design and secretly reinforce hidden Cinder Vaults, their shared project.",
            "They were driven by an unspoken understanding, perhaps from studying '{easter_egg}' which hinted at cyclical destructions.",
            "Their community thrived, unaware that beneath their foundations, {name} and Cade were preparing arks against a coming flood of shadow.",
            "Cade, with his gruff practicality, ensured the Vaults were not just secure but also held essential tools for rebuilding.",
            "He often remarked that 'a good foundation saves more than just the house.'",
            "When the Shroud finally descended, their hidden sanctuaries became beacons of hope for their chosen few.",
            "Ensuring others were sealed away safely was their last act before their own preservation.",
            "With a shared nod of grim accomplishment with Cade, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "condition_name": "The Patient Observer (Athalan's Companion)", 
        "settings_conditions": {"PlayerHealth": 2.0, "ShroudTimer": 2.0, "EnemyDamage": 1.0, "EnemyHealth": 1.0}, 
        "title": "The Hunter's Vigil, with Athalan (An Echoed Fate)",
        "story": [
            "Deep within the quieter forests, {name} lived a life attuned to the land's subtle rhythms, a companion to Athalan Skjerderson, the keen-eyed Hunter.",
            "Their health was robust (Player Health: High), and the world's dangers seemed manageable (Enemy Stats: Normal), allowing for contemplation.",
            "Athalan provided for their sparse needs, his tracking skills legendary, while {name} chronicled the slow, almost imperceptible changes in the flora and fauna.",
            "They both noticed the 'Long Dusk,' as {name} termed the Shroud's glacial advance (Shroud Timer: Max), its signs read in the flight of birds and the silence of beasts.",
            "Athalan would share ancient hunting lore, some ofwhich mirrored passages {name} found in '{easter_egg}' about world cycles.",
            "Their preparation for the Cinder Vaults was methodical, unhurried, a hunter's patient wait in a well-chosen blind.",
            "Athalan, ever practical, ensured their chosen Vault was stocked with dried meats and clean water, alongside {name}'s journals.",
            "He believed that understanding the land was key to its eventual healing.",
            "Their entry into the pods was not an escape, but a strategic retreat, a promise to return and observe the world's rebirth.",
            "With a final, shared glance at the ancient trees, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    }
]

# --- Standard Lore Archetype Definitions ---
def check_blessed_caitiff(s): # Very Easy, Powerful Player
    if None in [s.get("EnemyDamage"), s.get("EnemyHealth"), s.get("PlayerHealth"), s.get("PlayerStamina"), s.get("ResourceYield"), s.get("ShroudTimer")]: return False
    return (s["EnemyDamage"] <= 0.5 and s["EnemyHealth"] <= 0.5 and \
            s["PlayerHealth"] >= 2.5 and s["PlayerStamina"] >= 2.5 and \
            s["ResourceYield"] >= 1.5 and s["ShroudTimer"] >= 1.5)

def check_sheltered_scholar(s): # Easy World, Average Player
    if None in [s.get("EnemyDamage"), s.get("EnemyHealth"), s.get("PlayerHealth"), s.get("ResourceYield"), s.get("ShroudTimer")]: return False
    return (s["EnemyDamage"] <= 0.75 and s["EnemyHealth"] <= 0.75 and \
            s["PlayerHealth"] >= 1.0 and s["PlayerHealth"] < 2.5 and \
            s["ResourceYield"] >= 1.0 and s["ShroudTimer"] >= 1.0)

def check_grim_survivor(s): # Hard World, Struggling Player
    if None in [s.get("EnemyDamage"), s.get("EnemyHealth"), s.get("PlayerHealth"), s.get("PlayerStamina"), s.get("ShroudTimer")]: return False
    return (s["EnemyDamage"] >= 2.0 and s["EnemyHealth"] >= 2.0 and \
            s["PlayerHealth"] <= 0.75 and s["PlayerStamina"] <= 0.75 and \
            s["ShroudTimer"] <= 0.75) # Lower shroudTimeFactor is harder

def check_resourceful_operative(s): # Balanced World, Max Resources
    if None in [s.get("ResourceYield"), s.get("EnemyDamage"), s.get("EnemyHealth")]: return False
    return (s["ResourceYield"] == 2.0 and \
            (s["EnemyDamage"] > 0.75 and s["EnemyDamage"] < 2.0) and \
            (s["EnemyHealth"] > 0.75 and s["EnemyHealth"] < 2.0))

def check_elixir_well_attendant(s): # New
    if None in [s.get("ResourceYield"), s.get("EnemyDamage"), s.get("ShroudTimer"), s.get("PlayerHealth")]: return False
    return (s["ResourceYield"] >= 1.0 and s["ResourceYield"] < 2.0 and \
            s["EnemyDamage"] >= 1.0 and s["EnemyDamage"] < 1.5 and \
            s["ShroudTimer"] <= 0.75 and \
            s["PlayerHealth"] >= 0.75 and s["PlayerHealth"] <= 1.25)

def check_ancient_spire_keeper(s): # New
    if None in [s.get("PlayerStamina"), s.get("ShroudTimer"), s.get("EnemyDamage"), s.get("PlayerHealth")]: return False
    return (s["PlayerStamina"] >= 1.5 and s["PlayerStamina"] < 2.5 and \
            s["ShroudTimer"] >= 1.25 and \
            s["EnemyDamage"] >= 0.75 and s["EnemyDamage"] <= 1.25 and \
            s["PlayerHealth"] >= 1.0 and s["PlayerHealth"] <= 1.5)


standard_lore_archetypes = [
    { # Very specific, so check first
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
        "name": "The Elixir Well Attendant", # New
        "check_func": check_elixir_well_attendant,
        "title": "Echoes from the Elixir Well",
        "story_template": [
            "{name} toiled near an Elixir Well, a place of strange power and even stranger whispers (Resources: Moderate from well, Shroud Timer: Challenging).",
            "The air hummed with raw magic, and those who worked there, like {name}, often bore subtle marks of its influence, sometimes discussed in hushed tones with alchemists.",
            "Guards patrolled, not just against bandits, but against the twisted creatures the Elixir's effluence sometimes birthed (Enemies: Slightly Tougher).",
            "They had seen firsthand the iridescent sheen of early Shroud corruption, long before it became a world-ending tide, maybe even read '{easter_egg}' about similar blights.",
            "Survival wasn't about heroism but about being at the right place, right time, when a heavily guarded convoy to a Cinder Vault made an unscheduled stop.",
            "Perhaps {name} was a conscripted laborer, a low-level guard, or a data-gatherer for a greedy mage studying the Well's output.",
            "Their knowledge of the Well's erratic nature, or a hastily bartered Elixir-infused trinket, might have been their ticket to a pod.",
            "The pod felt like an escape from one kind of prison into another, colder one.",
            "They wondered if the Elixir's song would still echo in their dreams during the long sleep.",
            "With a lingering scent of ozone and something...else...in their nostrils, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    {
        "name": "The Ancient Spire Keeper", # New
        "check_func": check_ancient_spire_keeper,
        "title": "Vigil at the Spire's Peak",
        "story_template": [
            "From a lineage of guardians or a secluded order, {name} was a Keeper of an Ancient Spire, those towering monuments to a forgotten age (Player Stamina: High).",
            "Their life was one of discipline, study, and the quiet maintenance of failing Ancient technologies, a solitary vigil against the encroaching darkness.",
            "The Spire itself seemed to hold the Shroud at bay longer than elsewhere (Shroud Timer: Generous), its Flame-attuned energies a fragile shield.",
            "They understood more of the 'Great Cycles' and the nature of the Flame than most, often deciphering warnings in texts like '{easter_egg}'.",
            "While the world below descended into chaos (Enemies: Normal), {name}'s focus was on a specific contingency: the activation of a deep, hidden Cinder Vault.",
            "This Vault was not for the masses, but for those like {name}, entrusted with preserving the most vital knowledge or Ancient artifacts.",
            "Their journey to the pod was less a flight, more a solemn, ritualistic progression through the Spire's defended heart.",
            "They carried with them not just hope, but the weight of forgotten eons and the Ancients' desperate, final gamble.",
            "The pod was an extension of the Spire's own preservation technology, cold but familiar.",
            "With a silent vow to remember and one day rekindle the Spire's light, {name} stepped inside, and the pod door hissed closed, encasing them in a deep, protective slumber."
        ]
    },
    { # Must be after more specific "easy world" types
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
        "name": "The Everyman/Everywoman", # Catch-all, should be last
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
        master.title("Enshrouded Origin Generator")
        master.configure(bg="#2E2E2E") # Dark background for main window

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam') # A theme that tends to look a bit more modern than default
        
        # Configure main frame style
        style.configure("Main.TFrame", background="#2E2E2E")
        # Configure LabelFrame style
        style.configure("Custom.TLabelframe", background="#3C3C3C", bordercolor="#555555")
        style.configure("Custom.TLabelframe.Label", background="#3C3C3C", foreground="white", font=("Helvetica", 12, "bold"))
        # Configure Label style
        style.configure("Custom.TLabel", background="#3C3C3C", foreground="white", font=("Helvetica", 10))
        style.configure("Status.TLabel", background="#2E2E2E", foreground="white", font=("Helvetica", 9))
        style.configure("Info.TLabel", background="#2E2E2E", foreground="#CCCCCC", font=("Helvetica", 14, "bold"))
        # Configure Button style
        style.configure("Custom.TButton", background="#5A5A5A", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=1)
        style.map("Custom.TButton", background=[('active', '#6A6A6A'), ('disabled', '#4A4A4A')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        # Configure Entry style
        style.configure("Custom.TEntry", fieldbackground="#5A5A5A", foreground="white", insertcolor="white")
         # Configure Text widget (not directly stylable by ttk, but setting frame bg helps)
        text_frame_bg = "#333333" # Background for the Text widget's frame
        text_bg = "#1E1E1E" # Background for the Text widget itself
        text_fg = "#E0E0E0" # Foreground for Text widget


        self.json_data = None 
        self.json_loaded_successfully = False
        self.loaded_filename = None
        
        main_frame = ttk.Frame(master, padding="10 10 10 10", style="Main.TFrame")
        main_frame.pack(expand=True, fill=tk.BOTH)

        info_text = "Enshrouded Backstory Generator"
        self.label_info = ttk.Label(main_frame, text=info_text, style="Info.TLabel", anchor="center")
        self.label_info.pack(pady=(0, 20), fill=tk.X)
        
        # --- Player Name Input ---
        name_frame = ttk.Frame(main_frame, style="Main.TFrame")
        name_frame.pack(pady=5, fill=tk.X)
        self.player_name_label = ttk.Label(name_frame, text="Character Name (Optional):", style="Custom.TLabel", background="#2E2E2E")
        self.player_name_label.pack(side=tk.LEFT, padx=(0,5))
        self.player_name_entry = ttk.Entry(name_frame, width=30, style="Custom.TEntry")
        self.player_name_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.player_name_entry.insert(0, "My Flameborn")

        # --- JSON File Loading ---
        self.json_frame = ttk.LabelFrame(main_frame, text="Load Server Settings", style="Custom.TLabelframe", padding="10 10 10 10")
        self.json_frame.pack(pady=10, padx=0, fill="x")

        self.btn_load_json = ttk.Button(self.json_frame, text="Load JSON Settings File", command=self.load_json_file, style="Custom.TButton")
        self.btn_load_json.pack(pady=5, fill=tk.X)
        self.json_status_label = ttk.Label(self.json_frame, text="No JSON file loaded. Please load a file.", style="Custom.TLabel", anchor="center")
        self.json_status_label.pack(pady=5, fill=tk.X)
        
        # --- Generate Button ---
        self.btn_generate = ttk.Button(main_frame, text="Generate Lore from JSON", command=self.generate_and_display_lore, style="Custom.TButton", state=tk.DISABLED)
        self.btn_generate.pack(pady=20, ipady=5, fill=tk.X)
        
        # --- Lore Display Area ---
        self.lore_text_frame_outer = ttk.LabelFrame(main_frame, text="Generated Lore", style="Custom.TLabelframe", padding="10 10 10 10")
        self.lore_text_frame_outer.pack(pady=10, padx=0, expand=True, fill="both")
        
        # Inner frame for Text widget to control its background better
        self.text_widget_frame = tk.Frame(self.lore_text_frame_outer, bg=text_frame_bg, bd=1, relief=tk.SUNKEN)
        self.text_widget_frame.pack(expand=True, fill="both")

        self.lore_text = tk.Text(self.text_widget_frame, wrap=tk.WORD, width=80, height=15, 
                                 relief=tk.FLAT, borderwidth=0,
                                 bg=text_bg, fg=text_fg, insertbackground="white",
                                 font=("Helvetica", 10), padx=5, pady=5)
        self.lore_text.pack(expand=True, fill="both")
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
            self.json_status_label.config(text="File selection cancelled. Please load a file.", foreground="#FFA500") # Orange
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
            self.loaded_filename = filepath.split('/')[-1]
            self.json_status_label.config(text=f"JSON Ready: {self.loaded_filename}", foreground="#90EE90") # LightGreen
            self.json_loaded_successfully = True
            self.btn_generate.config(state=tk.NORMAL)
            self.lore_text.config(state=tk.NORMAL)
            self.lore_text.delete("1.0", tk.END)
            self.lore_text.insert(tk.END, f"JSON file '{self.loaded_filename}' loaded. Click 'Generate Lore from JSON'.")
            self.lore_text.config(state=tk.DISABLED)
        except FileNotFoundError:
            messagebox.showerror("File Error", f"The file was not found at the specified path:\n{filepath}")
            self.json_status_label.config(text="Error: File not found. Load a new file.", foreground="#FF6347") # Tomato Red
        except PermissionError:
            messagebox.showerror("Permission Error", f"Could not open file due to insufficient permissions:\n{filepath}\nPlease check file permissions.")
            self.json_status_label.config(text="Error: Permission denied. Load a new file.", foreground="#FF6347")
        except json.JSONDecodeError as e:
            err_msg = f"The file is not a valid JSON.\nFile: {self.loaded_filename or filepath.split('/')[-1]}\nDetails: {e.args[0]}"
            if hasattr(e, 'lineno') and hasattr(e, 'colno'):
                err_msg += f" (near line {e.lineno} column {e.colno})"
            messagebox.showerror("JSON Parsing Error", err_msg)
            self.json_status_label.config(text="Error: Invalid JSON format. Load a new file.", foreground="#FF6347")
        except Exception as e:
            error_type = type(e).__name__
            messagebox.showerror("Unexpected Error", f"An unexpected {error_type} occurred while processing the file: {self.loaded_filename or filepath.split('/')[-1]}\nDetails: {str(e)}")
            self.json_status_label.config(text=f"Error: {error_type} during load. Load a new file.", foreground="#FF6347")

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
            self.json_status_label.config(text=f"JSON Error: '{parent_object_name}' missing/invalid in {self.loaded_filename}.", foreground="#FF6347")
            return None
        for conceptual_key, (parent_key_in_map, actual_json_key) in JSON_KEYS_MAP.items():
            if parent_key_in_map != parent_object_name: continue
            value = game_settings_obj.get(actual_json_key)
            if value is None:
                missing_keys_messages.append(f"'{conceptual_key}' (\"{parent_object_name}\".\"{actual_json_key}\")")
                extracted_settings[conceptual_key] = 1.0 # Default if missing for archetype checks
            else:
                try:
                    extracted_settings[conceptual_key] = float(value)
                except (ValueError, TypeError):
                    type_errors_messages.append(f"Value for \"{actual_json_key}\" ('{value}') is not a number.")
                    extracted_settings[conceptual_key] = 1.0 # Default if type error
        
        # Show warnings but proceed with defaults
        if missing_keys_messages:
            messagebox.showwarning("JSON Data Warning - Missing Keys",
                                   "Could not find the following expected keys under 'gameSettings':\n- " + "\n- ".join(missing_keys_messages) +
                                   "\nDefault values (1.0) will be assumed for these settings in lore generation.")
        if type_errors_messages:
            messagebox.showwarning("JSON Data Warning - Type Errors",
                                   "Found non-numeric values for the following keys under 'gameSettings':\n- " + "\n- ".join(type_errors_messages) +
                                   "\nThese settings will be treated as default (1.0) for lore generation.")
        return extracted_settings

    def check_secret_lore_conditions(self, extracted_settings):
        if not extracted_settings: return None
        for trigger_def in special_lore_triggers:
            match = True
            for setting_name, required_value in trigger_def["settings_conditions"].items():
                json_value = extracted_settings.get(setting_name) # Will use default 1.0 if key was bad/missing
                if json_value is None: json_value = 1.0 # Should already be handled by get_settings, but double check

                op_type = "exact" 
                if setting_name in ["EnemyDamage", "EnemyHealth"]:
                    if trigger_def["condition_name"].startswith("The Unexpected Magnate") or \
                       trigger_def["condition_name"].startswith("The Builder of Havens"): op_type = "lte" 
                    elif trigger_def["condition_name"].startswith("The Last Stand"): op_type = "gte" 
                
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
            extracted_settings = {key: 1.0 for key in JSON_KEYS_MAP.keys()} # Should not happen if get_settings_from_json is robust
            
        for archetype in standard_lore_archetypes:
            if archetype["check_func"](extracted_settings):
                return archetype
        return standard_lore_archetypes[-1] 

    def generate_and_display_lore(self):
        player_name = self.player_name_entry.get() if self.player_name_entry.get() else "The Flameborn"
        final_story_sentences = []
        lore_title = "Lore Generation Result"
        status_message = f"Processing {self.loaded_filename}..."
        status_color = "#ADD8E6" # LightBlue for processing
        self.json_status_label.config(text=status_message, foreground=status_color)
        self.master.update_idletasks() 

        if not self.json_loaded_successfully or not self.json_data:
            messagebox.showerror("Error", "No JSON file loaded or file is invalid. Please load a valid Enshrouded server JSON file.")
            self.json_status_label.config(text="Error: No valid JSON. Load file.", foreground="#FF6347")
            self.btn_generate.config(state=tk.DISABLED)
            return

        extracted_settings = self.get_settings_from_json()
        if extracted_settings is None: 
            self.json_status_label.config(text=f"Critical error processing {self.loaded_filename}. See warnings.", foreground="#FF6347")
            return 

        triggered_secret_lore = self.check_secret_lore_conditions(extracted_settings)

        if triggered_secret_lore:
            lore_title = triggered_secret_lore["title"]
            final_story_sentences = [] # Ensure it's a list
            for sentence_template in triggered_secret_lore["story"]: # Stories are now lists of sentences
                 final_story_sentences.append(sentence_template.format(name=player_name, easter_egg=random.choice(lore_pages)))


            status_message = f"An Echoed Fate revealed in {self.loaded_filename}!"
            status_color = "#DA70D6" # Orchid (Purple)
            
            messagebox.showinfo("A Twist in the Weave!", 
                                "Hark, Flameborn! The currents of Embervale have shifted in a most curious way, revealing a destiny few could have foreseen. A veiled chapter of your arrival unfurls...\n\n*(This is but one of five such extraordinary fates whispered to exist before the Great Slumber.)*")
        else:
            standard_archetype = self.determine_standard_lore_archetype(extracted_settings)
            lore_title = standard_archetype["title"]
            selected_easter_egg = random.choice(lore_pages)
            for sentence_template in standard_archetype["story_template"]:
                final_story_sentences.append(sentence_template.format(name=player_name, easter_egg=selected_easter_egg))
            status_message = f"Lore generated from {self.loaded_filename}."
            status_color = "#90EE90" # LightGreen
            
        final_story_str = " ".join(final_story_sentences)
        self.json_status_label.config(text=status_message, foreground=status_color)
        self.lore_text_frame_outer.config(text=lore_title) # Update LabelFrame title
        self.lore_text.config(state=tk.NORMAL)
        self.lore_text.delete("1.0", tk.END)
        self.lore_text.insert(tk.END, final_story_str)
        self.lore_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = LoreGeneratorApp(root)
    root.mainloop()
