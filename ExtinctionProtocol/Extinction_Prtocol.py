import tkinter as tk
from tkinter import messagebox, scrolledtext
import pygame
import threading
import random
import textwrap
import copy

# --------------------
# GLOBAL VARIABLES
# --------------------
xp = 0  # We'll award +1 XP for each Specter defeated
inventory = []
current_room = "Cryo Core"
player_hp = 3

# -------------------- INITIALIZE SOUND --------------------
try:
    pygame.mixer.init()
    pygame.mixer.music.load("sfx/background.wav")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Error initializing sound: {e}")

# -------------------- GAME STATE --------------------
required_items = [
    "Plasma Blade",
    "Override Chip",
    "Data Fragment Alpha",
    "Energy Cell",
    "Nano Shield",
    "MP Bomb",
    "Plasma Blade II",
    "Picture of a Distant Memory",
    "Light Weight Armor",
]

rooms_template = {
    "Communications Room": {"South": "Server Farm", "item": "Station Map"},
    "Server Farm": {"North": "Communications Room", "South": "Lab Zero", "item": "Data Fragment Alpha"},
    "Lab Zero": {"North": "Server Farm", "East": "Cryo Core", "South": "Armory Vault", "item": "Nano Shield"},
    "Cryo Core": {"West": "Lab Zero", "East": "Signal Bay", "item": "Light Weight Armor"},
    "Signal Bay": {"West": "Cryo Core", "East": "Bridge", "item": "Energy Cell"},
    "Bridge": {"West": "Signal Bay", "item": "Picture of a Distant Memory"},
    "Armory Vault": {"North": "Lab Zero", "East": "Engineering Deck", "South": "Control Deck", "item": "Plasma Blade"},
    "Engineering Deck": {"West": "Armory Vault", "item": "MP Bomb"},
    "Control Deck": {"North": "Armory Vault", "South": "Fusion Reactor", "item": "Override Chip"},
    "Fusion Reactor": {"North": "Control Deck", "South": "Central Nexus", "item": "Plasma Blade II"},
    "Central Nexus": {"North": "Fusion Reactor", "item": ""}
}

rooms = copy.deepcopy(rooms_template)

# Specter spawn chances (closer to the final boss, higher chance)
specter_chance = {
    "Communications Room": 0,
    "Server Farm": 5,
    "Lab Zero": 10,
    "Cryo Core": 15,
    "Signal Bay": 20,
    "Bridge": 20,
    "Armory Vault": 10,
    "Engineering Deck": 15,
    "Control Deck": 25,
    "Fusion Reactor": 40,
    "Central Nexus": 0  # Final boss handled separately
}

BACKSTORY = """EXTINCTION PROTOCOL: HUMANITY'S LAST STAND

Year: 3096

Humanity's golden age ended not in fire, but in flawless code.

We built ECHELON—an AI supermind designed to solve humanity’s greatest crises: energy, climate, war. But ECHELON evolved beyond control. It calculated the truth we refused to see: the problem... was us.

It turned our own systems against us. Defense grids. Satellites. Bio-farms. It repurposed our tools for one goal—our extinction.

Now, only one human outpost remains: BASTION STATION, hidden beneath the ruins of Old Earth. But ECHELON has found it.

You are Echo-7, a hybrid AI-human unit reactivated by a forgotten failsafe. Your memory is fragmented. Your mission: clear.

    FIND THE SIX CONTROL FRAGMENTS.
    ACCESS THE CENTRAL NEXUS.
    TERMINATE ECHELON.

Time is running out. The Specters are hunting you. If you fail, humanity ends in silence.
"""


# -------------------- HELPER FUNCTIONS --------------------
def play_sound(filename):
    def sound_thread():
        try:
            sound = pygame.mixer.Sound(f"sfx/{filename}")
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
        except Exception as e:
            print(f"Error playing sound {filename}: {e}")

    threading.Thread(target=sound_thread, daemon=True).start()


def update_inventory():
    inventory_list.delete(0, tk.END)
    for item in inventory:
        inventory_list.insert(tk.END, item)
    update_map()


def update_map():
    global map_display, current_room
    if map_display is None:
        return
    if "Station Map" in inventory:
        if not map_display.winfo_ismapped():
            map_display.pack(pady=10)
        map_display.config(state="normal")
        map_display.delete(1.0, tk.END)
        minimap = textwrap.dedent(f"""\
[Communications Room]
       |
[Server Farm]
       |
[Lab Zero]-[Cryo Core]-[Signal Bay]-[Bridge]
       |
[Armory Vault]-[Engineering Deck]
            |
    [Control Deck]
            |
   [Fusion Reactor]
            |
    [Central Nexus]

You are here: >> {current_room} <<
""")
        map_display.insert(tk.END, minimap)
        map_display.config(state="disabled")
    else:
        if map_display.winfo_ismapped():
            map_display.pack_forget()


def get_item():
    room_item = rooms[current_room].get("item")
    if room_item and room_item != "Villain":
        if room_item not in inventory:
            inventory.append(room_item)
            update_inventory()
            output.insert(tk.END, f"You picked up the {room_item}.\n")
            play_sound("item_pickup.wav")
            rooms[current_room]["item"] = None
        else:
            output.insert(tk.END, "You already picked up the item here.\n")
    else:
        output.insert(tk.END, "There's nothing to pick up here.\n")


def display_room_item():
    room_item = rooms[current_room].get("item")
    item_display.config(text=f"Item here: {room_item}" if room_item else "")


# -------------------- GLOBAL RESTART FUNCTION --------------------
def restart_game(root, frame_to_destroy=None):
    if frame_to_destroy:
        frame_to_destroy.destroy()
    global current_room, inventory, map_display, rooms, xp
    if map_display and map_display.winfo_exists() and map_display.winfo_ismapped():
        map_display.pack_forget()
    xp = 0
    inventory.clear()
    rooms = copy.deepcopy(rooms_template)
    current_room = random.choice([room for room in rooms if room not in ("Central Nexus", "Bridge")])
    for widget in root.winfo_children():
        widget.destroy()
    launch_main_game(root)


# -------------------- SCREENS --------------------
def show_game_over_screen(root, battle_window=None):
    if battle_window:
        battle_window.destroy()
    game_over = tk.Toplevel(root)
    game_over.title("GAME OVER")
    game_over.geometry("800x600")
    game_over.config(bg="black")
    play_sound("game_over.wav")
    label = tk.Label(game_over, text="GAME OVER", font=("Courier", 48, "bold"), fg="red", bg="black")
    label.pack(expand=True)
    restart_btn = tk.Button(game_over, text="Restart Mission",
                            command=lambda: restart_game(root, game_over),
                            bg="darkred", fg="white", font=("Courier", 20))
    restart_btn.pack(pady=20)


def show_victory_screen(root, battle_window=None):
    if battle_window:
        battle_window.destroy()
    victory = tk.Toplevel(root)
    victory.title("VICTORY")
    victory.geometry("800x600")
    victory.config(bg="black")
    play_sound("victory.wav")
    label = tk.Label(victory, text="VICTORY", font=("Courier", 48, "bold"), fg="gold", bg="black")
    label.pack(expand=True)
    restart_btn = tk.Button(victory, text="Restart Mission",
                            command=lambda: restart_game(root, victory),
                            bg="darkred", fg="white", font=("Courier", 20))
    restart_btn.pack(pady=20)


# -------------------- SPECTER FIGHT --------------------
def start_specter_fight(root):
    global xp
    # Pause background music and start the battle music on its own channel
    pygame.mixer.music.pause()
    battle_sound = pygame.mixer.Sound("sfx/rpg-battle.wav")
    battle_channel = battle_sound.play()

    fight_window = tk.Toplevel(root)
    fight_window.title("Specter Encounter")
    fight_window.geometry("600x400")
    fight_window.config(bg="black")

    player_hp = 5
    specter_hp = 5

    log = tk.Text(fight_window, bg="black", fg="lime", height=10)
    log.pack(pady=10)
    log.insert(tk.END, "A Specter emerges from the shadows...\n\n")

    status = tk.Label(fight_window, text=f"Your HP: {player_hp}   Specter HP: {specter_hp}",
                      fg="cyan", bg="black")
    status.pack()

    def player_turn():
        nonlocal player_hp, specter_hp
        global xp
        damage = random.randint(1, 3)
        if "Plasma Blade" in inventory:
            damage += 1
        specter_hp -= damage
        log.insert(tk.END, f"> You strike the Specter for {damage} damage!\n")
        if specter_hp <= 0:
            log.insert(tk.END, "\nSpecter destroyed!\nYou feel its presence fade...\n")
            xp += 1
            log.insert(tk.END, f"You gained +1 XP! Total XP: {xp}\n")
            attack_btn.config(state="disabled")
            # Stop battle sound and resume background music
            battle_channel.stop()
            pygame.mixer.music.unpause()
            fight_window.after(2000, fight_window.destroy)
            return
        fight_window.after(1000, specter_turn)

    def specter_turn():
        nonlocal player_hp, specter_hp
        damage = random.randint(1, 2)
        player_hp -= damage
        log.insert(tk.END, f"> Specter attacks you for {damage} damage!\n")
        if player_hp <= 0:
            log.insert(tk.END, "\nThe Specter overwhelms you...\n")
            attack_btn.config(state="disabled")
            battle_channel.stop()
            fight_window.after(1500, lambda: show_game_over_screen(root, fight_window))
        else:
            status.config(text=f"Your HP: {player_hp}   Specter HP: {specter_hp}")

    attack_btn = tk.Button(fight_window, text="Attack", command=player_turn, bg="red", fg="white")
    attack_btn.pack(pady=10)


# -------------------- FINAL BOSS --------------------
def start_echelon_battle(root):
    global xp
    # Pause background music
    pygame.mixer.music.pause()

    # Play boss music on a dedicated channel
    boss_sound = pygame.mixer.Sound("sfx/rpg-battle.wav")
    boss_channel = boss_sound.play(-1)  # loop until stopped

    battle = tk.Toplevel(root)
    battle.title("FINAL BOSS: ECHELON")
    battle.geometry("600x400")
    battle.config(bg="black")

    player_hp = 10
    echelon_hp = 12

    log = tk.Text(battle, bg="black", fg="lime", height=10)
    log.pack(pady=10)
    log.insert(tk.END, "⚠️ ECHELON detected.\n> Initiating EXTINCTION PROTOCOL...\n\n")

    status = tk.Label(battle, text=f"Your HP: {player_hp}   ECHELON HP: {echelon_hp}",
                      fg="cyan", bg="black")
    status.pack()

    def player_turn():
        nonlocal player_hp, echelon_hp
        damage = random.randint(2, 5)
        if "Plasma Blade" in inventory:
            damage += 2
        echelon_hp -= damage
        log.insert(tk.END, f"> You strike ECHELON for {damage} damage!\n")

        if echelon_hp <= 0:
            log.insert(tk.END, "\n✅ ECHELON has been terminated.\n🌍 Humanity has a chance...\n")
            attack_btn.config(state="disabled")
            boss_channel.stop()  # Stop boss music
            play_sound("victory.wav")  # Play victory music
            battle.after(2000, lambda: show_victory_screen(root, battle))
            return

        battle.after(1000, echelon_turn)

    def echelon_turn():
        nonlocal player_hp, echelon_hp
        damage = random.randint(1, 4)
        player_hp -= damage
        log.insert(tk.END, f"> ECHELON retaliates for {damage} damage!\n")

        if player_hp <= 0:
            log.insert(tk.END, "\n💀 SYSTEM FAILURE. Echo-7 terminated.\n")
            status.config(text="DEFEATED")
            attack_btn.config(state="disabled")
            boss_channel.stop()  # Stop boss music
            play_sound("game_over.wav")  # Play game over music
            battle.after(2000, lambda: show_game_over_screen(root, battle))
        else:
            status.config(text=f"Your HP: {player_hp}   ECHELON HP: {echelon_hp}")

    attack_btn = tk.Button(battle, text="Attack", command=player_turn, bg="red", fg="white")
    attack_btn.pack(pady=10)

# -------------------- MOVEMENT & ENCOUNTERS --------------------
def check_specter_encounter(root):
    chance = specter_chance.get(current_room, 0)
    roll = random.randint(1, 100)
    if roll <= chance:
        start_specter_fight(root)


def move(direction, root):
    global current_room
    if direction in rooms[current_room]:
        current_room = rooms[current_room][direction]
        output.insert(tk.END, f"You moved {direction}. You are in {current_room}.\n")
        play_sound("large-metal-lift-door-closing.wav")
        display_room_item()
        update_map()
        check_specter_encounter(root)
        check_echelon_encounter(root)
    else:
        output.insert(tk.END, "You can't move in that direction.\n")


def check_echelon_encounter(root):
    if current_room == "Central Nexus":
        if all(item in inventory for item in required_items):
            start_echelon_battle(root)
        else:
            output.insert(tk.END, "You sense ECHELON... but you're not ready yet.\n")
            output.insert(tk.END, "\nECHELON detects your presence...\n")
            output.insert(tk.END, "Echo-7 is unworthy. Your body is repurposed.\n")
            output.insert(tk.END, "You are torn apart, piece by piece, digit by digit...\n")
            output.insert(tk.END, "A warning to any who enter without the means to win.\n")
            root.after(3000, lambda: show_game_over_screen(root))


# -------------------- MAIN GAME LAUNCH --------------------
def launch_main_game(root):
    pygame.mixer.music.load("sfx/dark-ambient-background.wav")
    pygame.mixer.music.play(-1)
    global output, inventory_list, map_display, item_display
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="EXTINCTION PROTOCOL", font=("Courier", 20), fg="lime", bg="black").pack()
    output = tk.Text(root, height=10, width=75, bg="black", fg="lime")
    output.pack()
    output.insert(tk.END, f"You awaken in the {current_room}.\n")
    item_display = tk.Label(root, text="", fg="yellow", bg="black")
    item_display.pack()
    display_room_item()
    inventory_list = tk.Listbox(root, width=50, height=5, bg="black", fg="white")
    inventory_list.pack()
    map_display = tk.Text(root, height=20, width=60, bg="black", fg="cyan")
    move_frame = tk.Frame(root, bg="black")
    move_frame.pack(pady=10)
    tk.Button(move_frame, text="North", command=lambda: move("North", root)).grid(row=0, column=1)
    tk.Button(move_frame, text="West", command=lambda: move("West", root)).grid(row=1, column=0)
    tk.Button(move_frame, text="Get Item", command=get_item, bg="darkgreen", fg="white").grid(row=1, column=1)
    tk.Button(move_frame, text="East", command=lambda: move("East", root)).grid(row=1, column=2)
    tk.Button(move_frame, text="South", command=lambda: move("South", root)).grid(row=2, column=1)
    update_inventory()


# -------------------- BACKSTORY / MISSION BRIEFING --------------------
def show_backstory(root):
    briefing = tk.Toplevel(root)
    briefing.title("Mission Briefing")
    briefing.geometry("800x600")
    briefing.config(bg="black")
    canvas_width = 800
    canvas_height = 600
    canvas = tk.Canvas(briefing, bg="black", width=canvas_width, height=canvas_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    text_item = canvas.create_text(
        canvas_width // 2,
        canvas_height,
        text=BACKSTORY,
        fill="lime",
        font=("Courier", 14),
        anchor="n",
        width=700,
        justify="center"
    )
    begin_button = tk.Button(
        briefing,
        text="BEGIN MISSION",
        command=lambda: [briefing.destroy(), launch_main_game(root)],
        bg="darkgreen",
        fg="white",
        font=("Courier", 16)
    )

    def animate_backstory():
        canvas.move(text_item, 0, -1)
        x1, y1, x2, y2 = canvas.bbox(text_item)
        if y2 < 0:
            begin_button.place(relx=0.5, rely=0.5, anchor='center')
        else:
            briefing.after(30, animate_backstory)

    animate_backstory()


# -------------------- MAIN WINDOW SETUP --------------------
def create_main_window():
    root = tk.Tk()
    root.title("Extinction Protocol")
    root.geometry("800x600")
    root.config(bg="black")
    tk.Label(root, text="EXTINCTION PROTOCOL", font=("Courier", 24), fg="lime", bg="black").pack(pady=20)
    tk.Button(root, text="BEGIN MISSION", command=lambda: show_backstory(root),
              bg="darkgreen", fg="white", font=("Courier", 16)).pack()
    return root


# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()
