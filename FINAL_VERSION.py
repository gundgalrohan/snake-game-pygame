import pygame as pg
import random
import time

pg.init()

# Highscore list
high_scores = [0, 0, 0, 0, 0]

def generate_stone_strips(num_strips, extra_stones=3):
    stone_positions = []
    while len(stone_positions) < num_strips * 4:  # Each strip has 4 stones
        direction = random.choice(['vertical', 'horizontal'])
        block = []

        # Ensure stones spawn away from the boundaries
        boundary_offset = 50  # Minimum distance from boundary

        if direction == 'vertical':
            start_x = random.randint(boundary_offset, 550 - boundary_offset)  # Ensure x is away from the edges
            start_y = random.randint(boundary_offset, 450 - boundary_offset)  # Ensure y is away from the edges
            for i in range(4):
                block.append((start_x, start_y + i * 20))  # 20 pixels apart vertically
        else:
            start_x = random.randint(boundary_offset, 550 - boundary_offset)  # Ensure x is away from the edges
            start_y = random.randint(boundary_offset, 450 - boundary_offset)  # Ensure y is away from the edges
            for i in range(4):
                block.append((start_x + i * 20, start_y))  # 20 pixels apart horizontally

        # Check if the new block is at least 20 pixels away from existing stones
        if all(abs(a[0] - b[0]) >= 20 and abs(a[1] - b[1]) >= 20 for a in block for b in stone_positions):
            stone_positions.extend(block)

    # Generate additional stones
    while len(stone_positions) < num_strips * 4 + extra_stones:  # Ensure total stones include extra
        new_stone = (random.randint(50, 550), random.randint(50, 450))  # Random position
        
        # Check if the new stone is at least 20 pixels away from existing stones
        if all(abs(new_stone[0] - pos[0]) >= 20 and abs(new_stone[1] - pos[1]) >= 20 for pos in stone_positions):
            stone_positions.append(new_stone)

    return stone_positions

def game_loop():
    x = 250
    y = 250
    xf = random.randint(50, 450)
    yf = random.randint(50, 450)

    growth = 20
    velo = 3
    fps = 120
    vel_x = 0
    vel_y = 0
    points = 0
    game_started = False
    start_time = None
    game_paused = False  # For pause functionality

    screen = pg.display.set_mode((600, 500))  # Increased width to 600 for the score bar
    pg.display.set_caption('SNAKE GAME')  # Set the window title to SNAKE GAME

    quitg = False
    s_list = [[250, 250]]
    s_length = 1

    # Generate 4 strips of stones and 3 additional stones
    stone_positions = generate_stone_strips(4, extra_stones=3)

    def plot(s_list):
        for i, (x, y) in enumerate(s_list):
            if i == len(s_list) - 1:
                # Draw head with a gradient effect
                pg.draw.circle(screen, (0, 255, 0), (x, y), 14)  # Head larger, brighter green
                # Draw eyes
                pg.draw.circle(screen, (255, 255, 255), (x - 4, y - 4), 3)  # Left eye
                pg.draw.circle(screen, (255, 255, 255), (x + 4, y - 4), 3)  # Right eye
                # Draw pupils
                pg.draw.circle(screen, (0, 0, 0), (x - 4, y - 4), 1)  # Left pupil
                pg.draw.circle(screen, (0, 0, 0), (x + 4, y - 4), 1)  # Right pupil
                # Draw tongue
                pg.draw.line(screen, (255, 0, 0), (x, y), (x, y + 10), 3)
            else:
                # Draw body as a circle
                pg.draw.circle(screen, (34, 139, 34), (x, y), 10)  # Body

    def show_high_scores():
        font = pg.font.SysFont(None, 25)
        screen.blit(font.render('Leaderboard', True, (173, 216, 230)), [490, 10])  # Light Blue
        for i, score in enumerate(high_scores):
            screen.blit(font.render(f"{i + 1}. {score}", True, (173, 216, 230)), [550, 40 + i * 20])

    def update_high_scores(score):
        high_scores.append(score)
        high_scores.sort(reverse=True)
        if len(high_scores) > 5:
            high_scores.pop()

    def spawn_apple():
        while True:
            new_xf = random.randint(50, 450)
            new_yf = random.randint(50, 450)
            # Ensure apple does not spawn on stones or too close to the snake
            if all(abs(new_xf - stone[0]) >= 20 and abs(new_yf - stone[1]) >= 20 for stone in stone_positions) and \
               all(abs(new_xf - sx) >= 20 and abs(new_yf - sy) >= 20 for sx, sy in s_list):
                return new_xf, new_yf

    xf, yf = spawn_apple()  # Spawn initial apple

    while not quitg:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitg = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    game_loop()
                if event.key == pg.K_r:  # Restart key
                    game_loop()
                if event.key == pg.K_ESCAPE:  # Pause key with ESC
                    game_paused = not game_paused

        if game_paused:
            # Display pause message
            font = pg.font.SysFont(None, 50)
            screen.blit(font.render('PAUSED', True, 'white'), [200, 200])
            pg.display.update()
            continue

        if start_time:
            elapsed_time = int(time.time() - start_time)
        else:
            elapsed_time = 0

        # Check for collision with stones
        for stone in stone_positions:
            if abs(x - stone[0]) < 15 and abs(y - stone[1]) < 15:
                update_high_scores(points)  # Update the high score list when the player dies
                font = pg.font.SysFont(None, 100)
                screen.blit(font.render('GAME OVER', True, 'red'), [90, 210])
                small_font = pg.font.SysFont(None, 30)
                screen.blit(small_font.render('Press R to Restart', True, 'white'), [200, 280])
                pg.display.update()
                time.sleep(2)  # Delay before restart
                game_loop()

        # Boundary or self-collision check
        if x >= 600 or x <= 0 or y <= 0 or y >= 500 or s_list[0] in s_list[1:len(s_list)]:
            update_high_scores(points)
            font = pg.font.SysFont(None, 100)
            screen.blit(font.render('GAME OVER', True, 'red'), [90, 210])
            small_font = pg.font.SysFont(None, 30)
            screen.blit(small_font.render('Press R to Restart', True, 'white'), [200, 280])
            pg.display.update()
            time.sleep(2)
            game_loop()

        pg.time.Clock().tick(fps)
        kevent = pg.key.get_pressed()

        if kevent[pg.K_a] or kevent[pg.K_LEFT]:
            vel_x = -velo
            vel_y = 0
        elif kevent[pg.K_d] or kevent[pg.K_RIGHT]:
            vel_x = velo
            vel_y = 0
        elif kevent[pg.K_w] or kevent[pg.K_UP]:
            vel_y = -velo
            vel_x = 0
        elif kevent[pg.K_s] or kevent[pg.K_DOWN]:
            vel_y = velo
            vel_x = 0 

        if vel_x != 0 or vel_y != 0:
            if not game_started:
                start_time = time.time()
                game_started = True

            x += vel_x
            y += vel_y

            # Check for apple collision
            if abs(x - xf) < 20 and abs(y - yf) < 20:
                points += 1
                xf, yf = spawn_apple()  # Spawn a new apple far away
                s_length += 1

            head = [x, y]
            s_list.append(head)

            if len(s_list) > s_length:
                del s_list[0]

        screen.fill((0, 0, 0))

        # Display points instead of time
        screen.blit(pg.font.SysFont(None, 50).render(f'Score: {points}', True, 'yellow'), [10, 10])

        # Draw apple with a stem
        pg.draw.circle(screen, (225, 0, 0), (xf, yf), 10)  # Draw apple
        pg.draw.rect(screen, (139, 69, 19), (xf - 2, yf - 12, 4, 8))  # Draw stem

        # Draw stone strips with smooth edges
        for stone in stone_positions:
            # Draw a rectangle with rounded edges
            pg.draw.rect(screen, (169, 169, 169), (stone[0] - 10, stone[1] - 10, 20, 20), border_radius=5)

        plot(s_list)
        show_high_scores()  # Show high scores
        pg.display.update()

    pg.quit()

game_loop()
