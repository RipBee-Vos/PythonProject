# doom_style_game.py — Full DOOM-style raycasting FPS
# ================================================
# Author: James + Steve
# Engine: Pygame + raycasting + full-screen scaling + retro UI

import pygame, sys, math, json, os

pygame.init()

# === Screen & Internal Render Setup ===
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Extinction Protocol")
clock = pygame.time.Clock()

INTERNAL_WIDTH, INTERNAL_HEIGHT = 320, 200
render_surf = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
HALF_INT_HEIGHT = INTERNAL_HEIGHT // 2

# === Game State ===
player_x = 2.5
player_y = 3.5
player_angle = 0.0
player_health = 100
player_ammo = 50
player_speed = 0.05
rot_speed = math.radians(3)
current_weapon = "1"
last_fired = {"1": 0, "2": 0, "3": 0}
weapon_cooldowns = {"1": 500, "2": 1000, "3": 750}
unlocked_weapons = ["1", "2", "3"]

# === Load Sounds ===
sound_shoot = pygame.mixer.Sound("assets/sounds/pistol_shot.wav")
sound_enemy_dead = pygame.mixer.Sound("assets/sounds/enemy_dead.wav")
sound_player_hurt = pygame.mixer.Sound("assets/sounds/player_hurt.wav")
sound_door = pygame.mixer.Sound("assets/sounds/door_open.wav")
pygame.mixer.music.load("assets/sounds/background_music.wav")
pygame.mixer.music.play(-1)

# === Assets ===
weapon_sprites = {
    "1": pygame.image.load("assets/blade_icon.png"),
    "2": pygame.image.load("assets/bomb_icon.png"),
    "3": pygame.image.load("assets/shotgun_icon.jpg")
}
weapon_scale = {
    "1": (64, 32),
    "2": (64, 32),
    "3": (96, 48)
}

# === Map ===
world_map = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,0,1,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],
]
MAP_WIDTH = len(world_map[0])
MAP_HEIGHT = len(world_map)

# === Colors ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
DARK_GRAY = (40, 40, 40)

# === Constants ===
FOV = math.radians(60)
HALF_FOV = FOV / 2
wall_color_light = (180, 0, 0)
wall_color_dark = (100, 0, 0)
floor_color = DARK_GRAY
ceiling_color = GRAY

# === Menu ===
def show_menu():
    font_title = pygame.font.SysFont("Courier", 28, bold=True)
    font_item = pygame.font.SysFont("Courier", 18)
    options = ["Start Game", "Save Game", "Continue Game", "Load Game", "Controller Options", "Quit"]
    selected = 0
    while True:
        render_surf.fill(BLACK)
        title = font_title.render("EXTINCTION PROTOCOL", True, RED)
        render_surf.blit(title, (INTERNAL_WIDTH//2 - title.get_width()//2, 30))
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected else WHITE
            text = font_item.render(opt, True, color)
            render_surf.blit(text, (INTERNAL_WIDTH//2 - text.get_width()//2, 80 + i*25))
        screen.blit(pygame.transform.scale(render_surf, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    selected = (selected - 1) % len(options)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    selected = (selected + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return options[selected]

# === Game Loop ===
def game_loop():
    global player_x, player_y, player_angle, player_health, player_ammo, current_weapon
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    current_weapon = str(event.key - pygame.K_0)
            if event.type == pygame.MOUSEMOTION:
                player_angle += event.rel[0] * 0.002

        keys = pygame.key.get_pressed()
        cos_a = math.cos(player_angle)
        sin_a = math.sin(player_angle)
        move_step = player_speed * dt

        if keys[pygame.K_UP]:
            new_x = player_x + cos_a * move_step
            new_y = player_y + sin_a * move_step
            if 0 <= int(new_x) < MAP_WIDTH and world_map[int(player_y)][int(new_x)] == 0:
                player_x = new_x
            if 0 <= int(new_y) < MAP_HEIGHT and world_map[int(new_y)][int(player_x)] == 0:
                player_y = new_y

        if keys[pygame.K_DOWN]:
            new_x = player_x - cos_a * move_step
            new_y = player_y - sin_a * move_step
            if 0 <= int(new_x) < MAP_WIDTH and world_map[int(player_y)][int(new_x)] == 0:
                player_x = new_x
            if 0 <= int(new_y) < MAP_HEIGHT and world_map[int(new_y)][int(player_x)] == 0:
                player_y = new_y

        render_surf.fill(ceiling_color)
        pygame.draw.rect(render_surf, floor_color, (0, HALF_INT_HEIGHT, INTERNAL_WIDTH, HALF_INT_HEIGHT))

        for col in range(INTERNAL_WIDTH):
            ray_angle = player_angle - HALF_FOV + (col / INTERNAL_WIDTH) * FOV
            ray_dir_x = math.cos(ray_angle)
            ray_dir_y = math.sin(ray_angle)
            map_x = int(player_x)
            map_y = int(player_y)
            delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else float('inf')
            delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else float('inf')

            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (player_x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - player_x) * delta_dist_x
            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (player_y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - player_y) * delta_dist_y

            hit = False
            side = 0
            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1
                if map_x < 0 or map_x >= MAP_WIDTH or map_y < 0 or map_y >= MAP_HEIGHT:
                    break
                if world_map[map_y][map_x] > 0:
                    hit = True

            if hit:
                if side == 0:
                    perp_dist = (map_x - player_x + (1 - step_x) / 2) / (ray_dir_x or 1e-6)
                else:
                    perp_dist = (map_y - player_y + (1 - step_y) / 2) / (ray_dir_y or 1e-6)
                line_height = int(INTERNAL_HEIGHT / (perp_dist or 0.0001))
                draw_start = max(0, HALF_INT_HEIGHT - line_height // 2)
                draw_end = min(INTERNAL_HEIGHT, HALF_INT_HEIGHT + line_height // 2)
                color = wall_color_light if side == 0 else wall_color_dark
                pygame.draw.line(render_surf, color, (col, draw_start), (col, draw_end))

        font = pygame.font.SysFont("Courier New", 12)
        ammo_text = font.render(f"Ammo: {player_ammo}", True, WHITE)
        hp_text = font.render(f"Health: {player_health}", True, WHITE)
        render_surf.blit(ammo_text, (5, 5))
        render_surf.blit(hp_text, (5, 20))

        weapon_img = weapon_sprites.get(current_weapon)
        if weapon_img:
            w, h = weapon_scale[current_weapon]
            weapon_img = pygame.transform.scale(weapon_img, (w, h))
            render_surf.blit(weapon_img, ((INTERNAL_WIDTH - w) // 2, INTERNAL_HEIGHT - h))

        screen.blit(pygame.transform.scale(render_surf, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    return

# === Run Game ===
if __name__ == '__main__':
    while True:
        result = show_menu()
        if result == "Quit":
            break
        elif result in ["Start Game", "Continue Game", "Load Game"]:
            game_loop()
    pygame.quit()
    sys.exit()
