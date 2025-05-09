# I - Import and Initialize
# Major patches and fixes
import pygame, pygame.locals, sprite_module, random, os
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
            
def game_over_screen(screen):
    '''Displays the Game Over screen with a retry button, background, and sound.'''
    font = pygame.font.Font("American Captain.ttf", 100)  # Use American Captain font
    option_font = pygame.font.Font("American Captain.ttf", 50)  # Use American Captain font
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    retry_text = option_font.render("Retry", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Load game over background image and sound
    game_over_bg = pygame.transform.scale(pygame.image.load('./img/GameOverBG.png'), (1920, 1080))
    pygame.mixer.music.load("./sound/gameover.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Load hover and click sounds
    hover_sound = pygame.mixer.Sound("./sound/Button hover.ogg")
    click_sound = pygame.mixer.Sound("./sound/Button click.mp3")
    hovered = False  # Track hover state

    while True:
        screen.blit(game_over_bg, (0, 0))  # Display game over background
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - 150))

        # Check for hover effect
        if retry_rect.collidepoint(pygame.mouse.get_pos()):
            if not hovered:
                hover_sound.play()  # Play hover sound only once
                hovered = True
            pygame.draw.rect(screen, (255, 215, 0), retry_rect.inflate(30, 15))  # Toggle button style
        else:
            hovered = False
            pygame.draw.rect(screen, (139, 69, 19), retry_rect.inflate(30, 15))  # Default button style

        screen.blit(retry_text, retry_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and retry_rect.collidepoint(event.pos):
                click_sound.play()  # Play click sound
                pygame.mixer.music.stop()  # Stop game over music
                pygame.mixer.music.unload()  # Unload game over music
                loading_screen(screen)
                return True  # Return True to indicate retry

        pygame.display.flip()

def loading_screen(screen):
    '''Displays a loading screen.'''
    font = pygame.font.Font("American Captain.ttf", 100)  # Use American Captain font
    loading_text = font.render("Loading...", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(loading_text, (screen.get_width() // 2 - loading_text.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Simulate loading time

def main_menu(screen):
    '''Displays the main menu with game mode options.'''
    font = pygame.font.Font("American Captain.ttf", 100)
    option_font = pygame.font.Font("American Captain.ttf", 50)
    title_text = font.render("Undead Siege", True, (255, 255, 255))
    classic_text = option_font.render("Classic Mode", True, (255, 255, 255))
    time_rush_text = option_font.render("Time Rush Mode", True, (255, 255, 255))
    endless_text = option_font.render("Endless Horde Mode", True, (255, 255, 255))
    exit_text = option_font.render("Exit", True, (255, 255, 255))

    classic_rect = classic_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    time_rush_rect = time_rush_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    endless_rect = endless_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 200))
    exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 300))

    menu_bg = pygame.transform.scale(pygame.image.load('./img/MenuBG.png'), (1920, 1080))
    pygame.mixer.music.load("./sound/Menu soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    hover_sound = pygame.mixer.Sound("./sound/Button hover.ogg")
    click_sound = pygame.mixer.Sound("./sound/Button click.mp3")
    hovered = None

    while True:
        screen.blit(menu_bg, (0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 2 - 200))

        for rect, text in [(classic_rect, classic_text), (time_rush_rect, time_rush_text), (endless_rect, endless_text), (exit_rect, exit_text)]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                if hovered != rect:
                    hover_sound.play()
                    hovered = rect
                pygame.draw.rect(screen, (255, 215, 0), rect.inflate(30, 15))
            else:
                pygame.draw.rect(screen, (139, 69, 19), rect.inflate(30, 15))
            screen.blit(text, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if classic_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()  # Add unload here
                    loading_screen(screen)
                    return  # Start Classic Mode
                elif time_rush_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()  # Add unload here
                    loading_screen(screen)
                    time_rush_mode(screen)  # Call the time rush mode
                    # Restart menu music after returning from time rush mode
                    pygame.mixer.music.load("./sound/Menu soundtrack.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                elif endless_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.mixer.music.stop()
                    endless_horde_mode(screen)
                elif exit_rect.collidepoint(event.pos):
                    click_sound.play()
                    pygame.quit()
                    exit()

        pygame.display.flip()

def pause_menu(screen):
    '''Displays the pause menu with options to resume or go back to the main menu.'''
    font = pygame.font.Font("American Captain.ttf", 100)  # Use American Captain font
    option_font = pygame.font.Font("American Captain.ttf", 50)  # Use American Captain font
    pause_text = font.render("Paused", True, (255, 255, 255))
    resume_text = option_font.render("Resume", True, (255, 255, 255))
    menu_text = option_font.render("Main Menu", True, (255, 255, 255))
    resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    menu_rect = menu_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    # Load hover and click sounds
    hover_sound = pygame.mixer.Sound("./sound//Button hover.ogg")
    click_sound = pygame.mixer.Sound("./sound//Button click.mp3")
    hovered_resume = False  # Track hover state for Resume button
    hovered_menu = False  # Track hover state for Main Menu button

    while True:
        screen.fill((0, 0, 0))
        screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - 150))

        # Check for hover effect on Resume button
        if resume_rect.collidepoint(pygame.mouse.get_pos()):
            if not hovered_resume:
                hover_sound.play()  # Play hover sound only once
                hovered_resume = True
            pygame.draw.rect(screen, (255, 215, 0), resume_rect.inflate(30, 15))  # Toggle button style
        else:
            hovered_resume = False
            pygame.draw.rect(screen, (139, 69, 19), resume_rect.inflate(30, 15))  # Default button style

        screen.blit(resume_text, resume_rect)

        # Check for hover effect on Main Menu button
        if menu_rect.collidepoint(pygame.mouse.get_pos()):
            if not hovered_menu:
                hover_sound.play()  # Play hover sound only once
                hovered_menu = True
            pygame.draw.rect(screen, (255, 215, 0), menu_rect.inflate(30, 15))  # Toggle button style
        else:
            hovered_menu = False
            pygame.draw.rect(screen, (139, 69, 19), menu_rect.inflate(30, 15))  # Default button style

        screen.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    return  # Resume the game
                elif menu_rect.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    main_menu(screen)  # Go back to the main menu
                    return

        pygame.display.flip()

def time_rush_mode(screen, time_limit=300):
    '''Time Rush Mode: Survive until the timer runs out.'''
    while True:  # Add outer loop for retrying
        # Initialize game elements
        background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
        background = background.convert()
        
        # Music setup
        pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        fire = pygame.mixer.Sound("./sound/bullet1.ogg")
        fire.set_volume(0.5)

        # Initialize player
        player = sprite_module.Player(screen)
        player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)

        # Timeraand nd sc
        timer_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 50), str(time_limit), "Time Left: %s", 255)
        score_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 90), "0", "Score: %s", 255)
        score = 0

        # Health and armor setup
        player_status = [[350, 350], [200, 200], 3]
        health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 350, 350, 0, None)
        armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 200, 200, 0, None)
        health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
        armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)

        # Zombie setup
        z_img = [pygame.image.load('./enemy/' + file) for file in os.listdir('enemy/')]
        z_info = [[6, 10, 50, 50, 10]]
        zombieGroup = pygame.sprite.Group()

        # Add bullet image loading
        bullet_images = []
        for file in os.listdir('bullets/'):
            bullet_images.append(pygame.image.load('./bullets/' + file))

        # Bullet and powerup groups
        bullet_img = pygame.sprite.Group()
        bullet_hitbox = pygame.sprite.Group()
        powerupGroup = pygame.sprite.Group()

        # Gold text setup
        gold_text = sprite_module.Text(30, (255, 215, 0), (screen.get_width() // 2, 130), "0", "Gold: %s", 255)

        # Sprite groups
        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, 
                                                health, armour, health_text, armour_text, timer_text, score_text, gold_text)

        # Game loop setup
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        keepGoing = True
        spawn_timer = 0

        while keepGoing:
            clock.tick(40)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) // 1000
            remaining_time = time_limit - elapsed_time
            timer_text.set_variable(0, str(remaining_time))
            
            # Spawn zombies periodically
            spawn_timer += 1
            if spawn_timer >= 40:
                spawn_timer = 0
                zombie = sprite_module.Zombie(screen, *z_info[0], z_img[0], 0, player.rect.center)
                zombieGroup.add(zombie)
                allSprites.add(zombie)

            # Handle input
            keystate = pygame.key.get_pressed()
            if keystate[pygame.locals.K_w]: player.go_up(screen)
            if keystate[pygame.locals.K_s]: player.go_down(screen)
            if keystate[pygame.locals.K_a]: player.go_left(screen)
            if keystate[pygame.locals.K_d]: player.go_right(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_menu(screen)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    bullet1 = sprite_module.Bullet(bullet_images[0], player.get_angle(), 
                                                 player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                    bullet2 = sprite_module.Bullet(None, None, player.rect.center, 
                                                 pygame.mouse.get_pos(), 12, 10, False)
                    bullet_img.add(bullet1)
                    bullet_hitbox.add(bullet2)
                    allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, 
                                                            zombieGroup, powerupGroup, health, armour, 
                                                            health_text, armour_text, timer_text, score_text, gold_text)
                    fire.play()

            # Update player rotation
            player.rotate(pygame.mouse.get_pos())

            # Check collisions
            # Player-Zombie collision
            if pygame.sprite.spritecollide(player, zombieGroup, False):
                # Handle armor and health damage
                if player_status[1][0] > 0:  # If there's armor
                    player_status[1][0] -= 5  # Damage armor first
                    if player_status[1][0] < 0:  # If armor breaks
                        player_status[0][0] += player_status[1][0]  # Transfer excess damage to health
                        player_status[1][0] = 0  # Set armor to 0
                else:  # No armor, damage health directly
                    player_status[0][0] -= 5

                # Update armor display
                armour.set_status(player_status[1][0])
                armour_text.set_variable(0, str(player_status[1][0]))
                armour_text.set_variable(1, str(player_status[1][1]))

                if player_status[0][0] <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    if game_over_screen(screen):  # If retry is chosen
                        break  # Break inner loop to restart time rush mode
                    else:
                        return  # Return to main menu

            # Bullet-Zombie collision
            hits = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, True)
            for hit in hits:
                score += 10

            # Update score and gold
            score_text.set_variable(0, str(score))
            player.add_gold(2)  # Add 2 gold per zombie kill
            gold_text.set_variable(0, str(player.get_gold()))

            # Update health display
            health.set_status(player_status[0][0])
            health_text.set_variable(0, str(player_status[0][0]))

            # Check win condition
            if remaining_time <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                # Add victory screen here if desired
                return  # Return to main menu

            # Update zombies
            for zombie in zombieGroup:
                zombie.rotate(player.rect.center)
                zombie.set_step_amount(player.rect.center)

            # Draw everything
            screen.blit(background, (0, 0))
            allSprites.update()
            allSprites.draw(screen)
            pygame.display.flip()

def endless_horde_mode(screen):
    '''Endless Horde Mode: Survive as long as possible with continuously increasing difficulty.'''
    # Initialize game elements
    background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
    background = background.convert()
    
    # Music setup
    pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    fire = pygame.mixer.Sound("./sound/bullet1.ogg")
    fire.set_volume(0.5)

    # Initialize player and status
    player = sprite_module.Player(screen)
    player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    player_status = [[350, 350], [200, 200], 3]

    # Status bars and text
    health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 350, 350, 0, None)
    armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 200, 200, 0, None)
    health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
    armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)
    score_text = sprite_module.Text(30, (255, 255, 255), (screen.get_width() // 2, 50), "0", "Score: %s", 255)
    gold_text = sprite_module.Text(30, (255, 215, 0), (screen.get_width() // 2, 90), "0", "Gold: %s", 255)

    # Load images
    bullet_images = [pygame.image.load('./bullets/' + file) for file in os.listdir('bullets/')]
    z_img = [pygame.image.load('./enemy/' + file) for file in os.listdir('enemy/')]

    # Sprite groups
    zombieGroup = pygame.sprite.Group()
    bullet_img = pygame.sprite.Group()
    bullet_hitbox = pygame.sprite.Group()
    powerupGroup = pygame.sprite.Group()

    # Initialize sprite groups
    allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                            powerupGroup, health, armour, health_text, 
                                            armour_text, score_text, gold_text)

    # Game variables
    clock = pygame.time.Clock()
    spawn_timer = 0
    score = 0
    difficulty_multiplier = 1.0
    keepGoing = True

    while keepGoing:
        clock.tick(40)
        spawn_timer += 1

        # Spawn zombies with increasing difficulty based on score
        if spawn_timer >= max(5, 30 - score//500):  # Spawn rate increases with score
            spawn_timer = 0
            zombie_type = random.randint(0, min(len(z_img)-1, score//1000))  # More zombie types as score increases
            zombie_stats = [
                3 + score//1000,  # Speed increases with score
                5 + score//500,   # Damage increases with score
                50 + score//100,  # Health increases with score
                50,              # Attack speed
                10 + score//200  # Score value increases with difficulty
            ]
            zombie = sprite_module.Zombie(screen, *zombie_stats, z_img[zombie_type], 0, player.rect.center)
            zombieGroup.add(zombie)
            allSprites.add(zombie)

        # Handle input
        keystate = pygame.key.get_pressed()
        if keystate[pygame.locals.K_w]: player.go_up(screen)
        if keystate[pygame.locals.K_s]: player.go_down(screen)
        if keystate[pygame.locals.K_a]: player.go_left(screen)
        if keystate[pygame.locals.K_d]: player.go_right(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Shooting mechanism
                bullet1 = sprite_module.Bullet(bullet_images[0], player.get_angle(), 
                                            player.rect.center, pygame.mouse.get_pos(), 12, 10, False)
                bullet2 = sprite_module.Bullet(None, None, player.rect.center, 
                                            pygame.mouse.get_pos(), 12, 10, False)
                bullet_img.add(bullet1)
                bullet_hitbox.add(bullet2)
                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, 
                                                        zombieGroup, powerupGroup, health, armour,
                                                        health_text, armour_text, score_text, gold_text)
                fire.play()

        # Update player rotation
        player.rotate(pygame.mouse.get_pos())

        # Handle collisions
        if pygame.sprite.spritecollide(player, zombieGroup, False):
            if player_status[1][0] > 0:  # If there's armor
                player_status[1][0] -= 5  # Damage armor first
                if player_status[1][0] < 0:
                    player_status[0][0] += player_status[1][0]
                    player_status[1][0] = 0
            else:  # No armor, damage health directly
                player_status[0][0] -= 5

            # Update displays
            armour.set_status(player_status[1][0])
            armour_text.set_variable(0, str(player_status[1][0]))

            if player_status[0][0] <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                if game_over_screen(screen):
                    return
                break

        # Handle zombie kills and scoring
        hits = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, True)
        for hit in hits:
            score += 10
            player.add_gold(2)  # Add 2 gold per zombie kill
            gold_text.set_variable(0, str(player.get_gold()))
            difficulty_multiplier = 1.0 + (score / 1000)  # Increase difficulty with score

        # Update displays
        score_text.set_variable(0, str(score))
        health.set_status(player_status[0][0])
        health_text.set_variable(0, str(player_status[0][0]))

        # Update zombies
        for zombie in zombieGroup:
            zombie.rotate(player.rect.center)
            zombie.set_step_amount(player.rect.center)

        # Draw everything
        screen.blit(background, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

def main():
    '''This function defines the 'mainline logic' for our game.'''
    while True:
        main_menu(screen)

        pygame.display.set_caption("")
     
        background = pygame.transform.scale(pygame.image.load('./img/bg.jpg'), (1920, 1080))
        background = background.convert()
        screen.blit(background, (0, 0))
    
        pygame.mixer.music.load("./sound/InGame soundtrack.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        fire = pygame.mixer.Sound("./sound/bullet1.ogg")
        fire.set_volume(0.5)
        no = pygame.mixer.Sound("./sound/no.ogg")
        no.set_volume(0.8)
    
        player = sprite_module.Player(screen)
        player.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    
        # Classic mode - 10 enemies per wave, evenly distributed
        wave = [6, 1, 1, 1, 1, 0, 0]  # Total 10 enemies per wave (6 basic + 4 special)
    
        z_img = []
        for file in os.listdir('enemy/'):
            z_img.append(pygame.image.load('./enemy/' + file))
            
        z_info = [[3, 5, 10, 100, 2], [3, 5, 20, 100, 4], [3, 5, 20, 100, 6], [3, 5, 20, 100, 8], [3, 5, 20, 100, 10], [3, 5, 20, 100, 12], [15, 20, 100, 100, 40]]
    
        # Initialize first wave zombies
        zombies = []
        zombie_types = [0] * 6 + [1, 2, 3, 4]  # 6 basic zombies + 4 special (total 10)
        random.shuffle(zombie_types)  # Randomize spawn order
        
        for zombie_type in zombie_types:
            zombies.append(sprite_module.Zombie(screen, 
                                             z_info[zombie_type][0], 
                                             z_info[zombie_type][1], 
                                             z_info[zombie_type][2], 
                                             z_info[zombie_type][3], 
                                             z_info[zombie_type][4], 
                                             z_img[zombie_type], 
                                             zombie_type, 
                                             player.rect.center))
            wave[zombie_type] -= 1
    
        ammo = [[20, 30], [40, 20], [15, 10], [100, 10], [30, 30]]
        ammo_capacity = [20, 40, 15, 100, 30]
        temp_string = ''
    
        for index in range(len(ammo)):
            temp_string += str(ammo[index][0]) + ',' + str(ammo[index][1]) + ','
    
        ammo_text = sprite_module.Text(20, (255, 255, 255), (800, 80), temp_string.strip(','), '%s/%s          %s/%s          %s/%s          %s/%s          %s/%s', 255)  
    
        player_status = [[350, 350], [200, 200], 3]   
    
        health = sprite_module.StatusBar((10, 10), (255, 0, 0), (0, 0, 0), (250, 30), 200, 350, 0, None)
        armour = sprite_module.StatusBar((10, 50), (238, 233, 233), (139, 137, 137), (250, 30), 100, 200, 0, None)
    
    
        health_text = sprite_module.Text(25, (255, 255, 255), (135, 25), '350,350', '%s/%s', 255)
        armour_text = sprite_module.Text(25, (0, 0, 0), (135, 65), '200,200', '%s/%s', 255)
        wave_text = sprite_module.Text(30, (255, 255, 255), (450, 40), '0,1,' + str(sum(wave)), 'Score:%s Wave:%s Zombies Left:%s', 255)
        gold_text = sprite_module.Text(30, (255, 215, 0), (450, 80), '0', 'Gold: %s', 255)  # Gold color (255,215,0)
    
        powerupGroup = pygame.sprite.Group()
        zombieGroup = pygame.sprite.Group(zombies)
        bullet_img = pygame.sprite.Group()
        bullet_hitbox = pygame.sprite.Group()
        reloading = pygame.sprite.Group()
    
        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, reloading, health, armour, health_text, armour_text, wave_text, gold_text, ammo_text)
     
        clock = pygame.time.Clock()
        keepGoing = True

        speed_timer = 0
        damage_timer = 0
        invincible_timer = 0
    
        powerup_status = False     
        speed_status = False       
        double_status = False
        invincible_status = False
    
        boss_spawn = False
    
        powerup_images = []
        for file in os.listdir('powerups/'):
            powerup_images.append(pygame.image.load('./powerups/' + file))
            
        bullet_images = []
        for file in os.listdir('bullets/'):
            bullet_images.append(pygame.image.load('./bullets/' + file))
    
        powerup_chance = 0
    
        wave_num = 1
    
        wave_value = [10, 1, 1, 1, 1, 1, 0]
    
        active_zombies = 10
    
        score = 0
    
        weapon = [True, True, True, True, True]
    
        current_weapon = 0
    
        reload_time = [1.5, 2, 1, 0.5, 1.5]
        reload_status = False
    
        machine_gun_fire = False
        machine_gun_delay = 0
    
        while keepGoing:
            clock.tick(40)
        
            keystate = pygame.key.get_pressed()
            if keystate[pygame.locals.K_w]:
                player.go_up(screen) 
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))
                
            if keystate[pygame.locals.K_a]:
                player.go_left(screen)
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))          
        
            if keystate[pygame.locals.K_s]:
                player.go_down(screen)
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))  
                
            if keystate[pygame.locals.K_d]:
                player.go_right(screen)         
                if reload_status:
                    reload.set_position((player.rect.center[0] - 40, player.rect.center[1] - 60))

            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu(screen)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if current_weapon == 0 and ammo[0][0]:
                        ammo[0][0] -= 1
                        # Create visual bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[0], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 12, 2, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 12, 2, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup,
                                                              powerupGroup, reloading, health, armour,
                                                              health_text, armour_text, wave_text, gold_text, ammo_text)
                        fire.play()
                
                    elif current_weapon == 1 and ammo[1][0]:
                        ammo[1][0] -= 1
                        # Create visual bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[1], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 16, 5, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 16, 5, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                              powerupGroup, reloading, health, armour, 
                                                              health_text, armour_text, wave_text, gold_text, ammo_text)
                        fire.play()
                
                    elif current_weapon == 2 and ammo[2][0]:
                        ammo[2][0] -= 1
                        # Create visual bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[2], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 8, 0, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 8, 0, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                              powerupGroup, reloading, health, armour, 
                                                              health_text, armour_text, wave_text, gold_text, ammo_text)
                
                    elif current_weapon == 3 and ammo[3][0]:
                        machine_gun_fire = True
                    
                    elif current_weapon == 4 and ammo[4][0]:
                        ammo[4][0] -= 1
                        # Create railgun visual and hitbox
                        bullet_visual = sprite_module.RailGun(screen, player.rect.center, pygame.mouse.get_pos())
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 20, 20, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                             powerupGroup, reloading, health, armour, 
                                                             health_text, armour_text, wave_text, gold_text, ammo_text)
                    
                    else:
                        if reload_status != True and ammo[current_weapon][1]:
                            reload = sprite_module.StatusBar((player.rect.center[0] - 40, player.rect.center[1] - 60), (0, 255, 0), (0, 0, 0), (70, 7), 0, 100, 1, reload_time[current_weapon])
                            reloading.add(reload)
                            allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, reloading, health, armour, health_text, armour_text, wave_text, gold_text, ammo_text)
                        reload_status = True
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if current_weapon == 3:
                        machine_gun_fire = False
            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and weapon[0] and reload_status == False:
                        current_weapon = 0
                        player.change_image(0)
                        machine_gun_fire = False
                    
                    elif event.key == pygame.K_2 and weapon[1] and reload_status == False:
                        current_weapon = 1
                        player.change_image(1)
                        machine_gun_fire = False
                    
                    elif event.key == pygame.K_3 and weapon[2] and reload_status == False:
                        current_weapon = 2
                        player.change_image(2)
                        machine_gun_fire = False
                    
                    elif event.key == pygame.K_4 and weapon[3] and reload_status == False:
                        current_weapon = 3
                    
                    elif event.key == pygame.K_5 and weapon[4] and reload_status == False:
                        current_weapon = 4
                        player.change_image(4)
                        machine_gun_fire = False
                    
                    elif event.key == pygame.K_r:  # Reload key
                        if not reload_status and ammo[current_weapon][1] > 0:  # If not already reloading and has ammo clips
                            reload = sprite_module.StatusBar(
                                (player.rect.center[0] - 40, player.rect.center[1] - 60),
                                (0, 255, 0), (0, 0, 0), (70, 7), 0, 100, 1, 
                                reload_time[current_weapon]
                            )
                            reloading.add(reload)
                            allSprites = pygame.sprite.OrderedUpdates(
                                bullet_img, bullet_hitbox, player, zombieGroup,
                                powerupGroup, reloading, health, armour,
                                health_text, armour_text, wave_text, gold_text, ammo_text
                            )
                            reload_status = True

                    elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5:
                        no.play()
                    
            x = pygame.sprite.spritecollide(player, zombieGroup, False)
            if x:
                for zombie in x:
                    zombie.move(False)
                
                    if not(invincible_status):
                        if zombie.get_attack():
                            if player_status[1][0] > 0:
                                player_status[1][0] = player_status[1][0] - zombie.get_damage()
                                if player_status[1][0] < 0:
                                    player_status[0][0] = player_status[0][0] + player_status[1][0]
                                    player_status[1][0] = 0
                            else:
                                player_status[0][0] = player_status[0][0] - zombie.get_damage()
                                if player_status[0][0] <= 0:
                                    keepGoing = False
            else:
                for zombie in zombieGroup:
                    zombie.move(True)
                    zombie.reset_attack()
                    
            c = pygame.sprite.groupcollide(bullet_hitbox, zombieGroup, True, False)
            v = pygame.sprite.groupcollide(bullet_img, zombieGroup, True, False)
            if c:
                for bullet in c.keys():
                    if bullet.get_damage() == 0:
                        c[bullet][0].slow()
                    
                    else:
                        if not(c[bullet][0].damage_hp(bullet.get_damage())):
                            wave[c[bullet][0].get_zombie_type()] = wave[c[bullet][0].get_zombie_type()] - 1
                            powerup_chance = random.randint(0, 100)
                            if powerup_chance == 0:
                                powerup_status = True
                                power = sprite_module.Powerup(c[bullet][0].rect.center, 5, powerup_images[5])
                            
                            elif powerup_chance == 1 or powerup_chance == 2:
                                powerup_status = True
                                power = sprite_module.Powerup(c[bullet][0].rect.center, 0, powerup_images[0])
                        
                            elif powerup_chance == 3 or powerup_chance == 4:
                                powerup_status = True
                                power = sprite_module.Powerup(c[bullet][0].rect.center, 1, powerup_images[1])
                            
                            elif powerup_chance == 5 or powerup_chance == 6:
                                powerup_status = True
                                power = sprite_module.Powerup(c[bullet][0].rect.center, 2, powerup_images[2])
                        
                            elif powerup_chance == 7 or powerup_chance == 8:
                                powerup_status = True
                                power = sprite_module.Powerup(c[bullet][0].rect.center, 3, powerup_images[3])
                            
                            elif powerup_chance == 9 or powerup_chance == 10 or powerup_chance == 11 or powerup_chance == 12:
                                powerup_status = True
                                power = sprite_module.Powerup(c[bullet][0].rect.center, 4, powerup_images[4])

                            if powerup_status:
                                powerupGroup.add(power)
                                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, powerupGroup, reloading, health, armour, health_text, armour_text, wave_text, gold_text, ammo_text)
                        
                            score += c[bullet][0].get_value()
                            player.add_gold(2)  # Add 2 gold per kill
                            gold_text.set_variable(0, str(player.get_gold()))  # Update gold display
                            c[bullet][0].kill()
                
            y = pygame.sprite.spritecollide(player, powerupGroup, False)
            if y:
                for buff in y:
                    powerup_type = buff.get_type()
                    if powerup_type == 0:
                        speed_timer = 0
                        speed_status = True
                        player.increase_speed()
                    
                    elif powerup_type == 1:
                        double_status = True
                        damage_timer = 0
                    
                    elif powerup_type == 2:
                        player_status[0][0] = player_status[0][0] + 100
                        if player_status[0][0] > player_status[0][1]:
                            player_status[0][0] = player_status[0][1]
                        
                    elif powerup_type == 3:
                        player_status[1][0] = player_status[1][0] + 100
                        if player_status[1][0] > player_status[1][1]:
                            player_status[1][0] = player_status[1][1]
                        
                    elif powerup_type == 4:
                        ammo_type = random.randint(0, len(ammo) - 1)
                        ammo[ammo_type][0] = ammo_capacity[ammo_type]
                        ammo[ammo_type][1] = ammo[ammo_type][1] + 2
                    
                    elif powerup_type == 5:
                        invincible_status = True
                        invincible_timer = 0
                
                    buff.kill()
                
            player.rotate(pygame.mouse.get_pos())
        
            if machine_gun_fire:
                machine_gun_delay += 1
                if machine_gun_delay % 3 == 0:
                    if ammo[3][0] > 0:  # Only fire if we have ammo
                        ammo[3][0] -= 1
                        # Create machine gun bullet and hitbox with same speed and damage
                        bullet_visual = sprite_module.Bullet(bullet_images[0], player.get_angle(), 
                                                        player.rect.center, pygame.mouse.get_pos(), 14, 6, double_status)
                        bullet_hit = sprite_module.Bullet(None, None, player.rect.center, 
                                                     pygame.mouse.get_pos(), 14, 6, double_status)
                        bullet_img.add(bullet_visual)
                        bullet_hitbox.add(bullet_hit)
                        allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                             powerupGroup, reloading, health, armour, 
                                                             health_text, armour_text, wave_text, gold_text, ammo_text)
                        fire.play()
                
            if ammo[3][0] == 0:
                machine_gun_fire = False
        
            if reload_status:
                if reload.get_reload():
                    ammo[current_weapon][0] = ammo_capacity[current_weapon]
                    ammo[current_weapon][1] = ammo[current_weapon][1] - 1
                    reload_status = False
        
        
            if speed_status: 
                speed_timer += 1
            if double_status:         
                damage_timer += 1
            if invincible_status:         
                invincible_timer += 1
        
            if speed_timer == 450:
                player.reset_speed()
            if damage_timer == 450:
                double_status = False
            if invincible_timer == 450:
                invincible_status = False
    
            # Update score, wave number, and remaining zombies display
            wave_text.set_variable(0, str(score))
            wave_text.set_variable(1, str(wave_num))
            wave_text.set_variable(2, str(len(zombieGroup)))
        
            health.set_status(player_status[0][0])
            armour.set_status(player_status[1][0])
        
            health_text.set_variable(0, str(player_status[0][0]))
            armour_text.set_variable(0, str(player_status[1][0]))
        
        
            index = 0
            for i in range(5):
                for n in range(2):
                    ammo_text.set_variable(index, str(ammo[i][n]))
                    index += 1
        
            for zombie in zombieGroup:
                zombie.rotate(player.rect.center)
                zombie.set_step_amount(player.rect.center)
        
            # Boss wave (every 5th wave)
            if wave_num % 5 == 0 and boss_spawn != True:
                boss_spawn = True
                # For boss waves: 1 boss + 9 regular zombies = 10 total
                wave = [9, 0, 0, 0, 0, 0, 1]  # Reset wave composition for boss wave
                
                # Spawn boss first
                zombie = sprite_module.Zombie(screen, z_info[6][0], z_info[6][1], z_info[6][2], 
                                           z_info[6][3], z_info[6][4], z_img[6], 6, player.rect.center)
                zombieGroup.add(zombie)
                
                # Spawn 9 regular zombies
                for _ in range(9):
                    zombie = sprite_module.Zombie(screen, z_info[0][0], z_info[0][1], z_info[0][2],
                                               z_info[0][3], z_info[0][4], z_img[0], 0, player.rect.center)
                    zombieGroup.add(zombie)
                
                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup, 
                                                        powerupGroup, reloading, health, armour, 
                                                        health_text, armour_text, wave_text, gold_text, ammo_text)
            elif wave_num % 5 > 0:
                boss_spawn = False
            
            # Check if all zombies are defeated
            if len(zombieGroup) == 0:
                # Show "Get ready for next wave" dialog
                font = pygame.font.Font("American Captain.ttf", 50)
                ready_text = font.render("Get Ready For The Next Wave!", True, (255, 255, 255))
                ready_rect = ready_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                
                # Create semi-transparent background
                overlay = pygame.Surface((screen.get_width(), screen.get_height()))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
                
                # Draw dialog
                screen.blit(overlay, (0, 0))
                screen.blit(ready_text, ready_rect)
                pygame.display.flip()
                
                # Wait for 3 seconds
                pygame.time.delay(3000)
                
                wave_num += 1
                # Calculate new enemy count (base 10 + 5 per wave)
                enemy_count = 10 + (wave_num - 1) * 5
                
                if wave_num % 5 == 0:  # Boss wave
                    # Spawn boss first
                    boss = sprite_module.Zombie(screen, z_info[6][0], z_info[6][1], z_info[6][2], 
                                           z_info[6][3], z_info[6][4], z_img[6], 6, player.rect.center)
                    zombieGroup.add(boss)
                    
                    # Spawn remaining enemies as basic zombies
                    for _ in range(enemy_count - 1):
                        zombie = sprite_module.Zombie(screen, z_info[0][0], z_info[0][1], z_info[0][2],
                                               z_info[0][3], z_info[0][4], z_img[0], 0, player.rect.center)
                        zombieGroup.add(zombie)
                else:
                    # Regular wave: 60% basic, 40% special zombies
                    basic_count = int(enemy_count * 0.6)
                    special_count = enemy_count - basic_count
                    special_per_type = special_count // 4
                    
                    # Spawn basic zombies
                    for _ in range(basic_count):
                        zombie = sprite_module.Zombie(screen, z_info[0][0], z_info[0][1], z_info[0][2],
                                               z_info[0][3], z_info[0][4], z_img[0], 0, player.rect.center)
                        zombieGroup.add(zombie)
                    
                    # Spawn special zombies
                    for type in range(1, 5):  # Special zombie types 1-4
                        for _ in range(special_per_type):
                            zombie = sprite_module.Zombie(screen, z_info[type][0], z_info[type][1], z_info[type][2],
                                                   z_info[type][3], z_info[type][4], z_img[type], type, player.rect.center)
                            zombieGroup.add(zombie)
                
                # Update sprite ordering
                allSprites = pygame.sprite.OrderedUpdates(bullet_img, bullet_hitbox, player, zombieGroup,
                                                        powerupGroup, reloading, health, armour,
                                                        health_text, armour_text, wave_text, gold_text, ammo_text)

                
            # Wave progression is handled in the previous block
        
            if player_status[0][0] <= 0:
                print("Game Over triggered!")
                pygame.mixer.music.stop()
                game_over_screen(screen)
                print("Returned from Game Over Screen") 

            screen.blit(background, (0, 0))
            allSprites.update()
            allSprites.draw(screen)
         
            pygame.display.flip()
     
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
     
    pygame.quit()    
     
         
main()
