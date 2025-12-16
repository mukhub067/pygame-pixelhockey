import pygame
import sys
import random
import math

# --- Constants & Configuration ---
WIDTH, HEIGHT = 1200, 600
FPS = 60

# Dimensions
PADDLE_RADIUS = 40
PUCK_RADIUS = 15

# Goal Size: 3 times the size (diameter) of the player
GOAL_HEIGHT = (PADDLE_RADIUS * 2) * 3 

# Speeds
PADDLE_SPEED = 8
BASE_PUCK_SPEED = 7
MAX_PUCK_SPEED = 20

# Neon Colors
BLACK = (10, 10, 18)
NEON_BLUE = (0, 255, 255)      # Left Player
NEON_PINK = (255, 20, 147)     # Right Player
NEON_GREEN = (57, 255, 20)     # UI / Puck
WHITE = (255, 255, 255)
WALL_COLOR = (50, 50, 80)
GOAL_LINE_COLOR = (255, 50, 50) # Red line for goal

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PIXEL HOCKEY: GAP GOAL EDITION")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont("consolas", 60, bold=True)
font_medium = pygame.font.SysFont("consolas", 30)

# --- Classes ---

class Paddle:
    def __init__(self, x, y, color, is_left):
        self.x = x
        self.y = y
        self.radius = PADDLE_RADIUS
        self.color = color
        self.is_left = is_left
        self.vel_x = 0
        self.vel_y = 0
        self.score = 0

    def move(self, keys):
        self.vel_x = 0
        self.vel_y = 0

        # Input
        if self.is_left:
            if keys[pygame.K_w]: self.vel_y = -PADDLE_SPEED
            if keys[pygame.K_s]: self.vel_y = PADDLE_SPEED
            if keys[pygame.K_a]: self.vel_x = -PADDLE_SPEED
            if keys[pygame.K_d]: self.vel_x = PADDLE_SPEED
        else:
            if keys[pygame.K_UP]: self.vel_y = -PADDLE_SPEED
            if keys[pygame.K_DOWN]: self.vel_y = PADDLE_SPEED
            if keys[pygame.K_LEFT]: self.vel_x = -PADDLE_SPEED
            if keys[pygame.K_RIGHT]: self.vel_x = PADDLE_SPEED

        # Apply movement
        self.x += self.vel_x
        self.y += self.vel_y

        # Boundary Checks (Keep paddle inside walls)
        if self.y - self.radius < 0: self.y = self.radius
        if self.y + self.radius > HEIGHT: self.y = HEIGHT - self.radius
        
        # Side checks
        if self.is_left:
            if self.x - self.radius < 0: self.x = self.radius
            if self.x + self.radius > WIDTH // 2: self.x = WIDTH // 2 - self.radius
        else:
            if self.x - self.radius < WIDTH // 2: self.x = WIDTH // 2 + self.radius
            if self.x + self.radius > WIDTH: self.x = WIDTH - self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius - 5, 2)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 5)

class Puck:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = PUCK_RADIUS
        self.dx = 0
        self.dy = 0
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        direction = random.choice([-1, 1])
        angle = random.uniform(-0.5, 0.5)
        self.dx = direction * BASE_PUCK_SPEED
        self.dy = BASE_PUCK_SPEED * angle

    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Calculate Goal Y-Range
        goal_top = (HEIGHT // 2) - (GOAL_HEIGHT // 2)
        goal_bottom = (HEIGHT // 2) + (GOAL_HEIGHT // 2)

        # --- Wall Collisions ---
        
        # Top Wall
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy *= -1
            
        # Bottom Wall
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy *= -1
            
        # Left Wall (Check for Goal Gap)
        if self.x - self.radius <= 0:
            # If we are NOT in the goal gap, BOUNCE
            if self.y < goal_top or self.y > goal_bottom:
                self.x = self.radius # Push out
                self.dx *= -1
            # Else: We are in the gap, let it pass (Game loop handles score)

        # Right Wall (Check for Goal Gap)
        elif self.x + self.radius >= WIDTH:
            # If we are NOT in the goal gap, BOUNCE
            if self.y < goal_top or self.y > goal_bottom:
                self.x = WIDTH - self.radius # Push out
                self.dx *= -1
            # Else: Let it pass

    def draw(self, surface):
        pygame.draw.circle(surface, NEON_GREEN, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)

# --- Helper Functions ---

def draw_text_centered(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, rect)
    return rect

def draw_button(text, font, text_color, rect_color, rect):
    pygame.draw.rect(screen, rect_color, rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_field():
    screen.fill(BLACK)
    
    # Calculate Goal Coords
    cy = HEIGHT // 2
    gh_half = GOAL_HEIGHT // 2
    
    # 1. Center Line
    pygame.draw.line(screen, (30, 30, 30), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)
    pygame.draw.circle(screen, (30, 30, 30), (WIDTH//2, HEIGHT//2), 100, 5)
    
    # 2. Side Walls (Left)
    # Top Left Wall Segment
    pygame.draw.line(screen, WALL_COLOR, (0, 0), (0, cy - gh_half), 10)
    # Bottom Left Wall Segment
    pygame.draw.line(screen, WALL_COLOR, (0, cy + gh_half), (0, HEIGHT), 10)
    
    # 3. Side Walls (Right)
    # Top Right Wall Segment
    pygame.draw.line(screen, WALL_COLOR, (WIDTH, 0), (WIDTH, cy - gh_half), 10)
    # Bottom Right Wall Segment
    pygame.draw.line(screen, WALL_COLOR, (WIDTH, cy + gh_half), (WIDTH, HEIGHT), 10)
    
    # 4. Goal Lines (Visual Indicator for the gap)
    pygame.draw.line(screen, GOAL_LINE_COLOR, (0, cy - gh_half), (0, cy + gh_half), 2)
    pygame.draw.line(screen, GOAL_LINE_COLOR, (WIDTH-2, cy - gh_half), (WIDTH-2, cy + gh_half), 2)


# --- Game Logic ---

def score_menu():
    max_score = 5
    running = True
    
    while running:
        screen.fill(BLACK)
        draw_text_centered("SET MAX SCORE", font_medium, NEON_GREEN, -100)
        draw_text_centered(str(max_score), font_large, WHITE, 0)
        
        minus_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 50, 50)
        plus_rect = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 - 25, 50, 50)
        play_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 + 100, 150, 50)
        
        draw_button("-", font_medium, NEON_BLUE, NEON_BLUE, minus_rect)
        draw_button("+", font_medium, NEON_PINK, NEON_PINK, plus_rect)
        draw_button("START", font_medium, NEON_GREEN, NEON_GREEN, play_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if minus_rect.collidepoint(pos) and max_score > 1: max_score -= 1
                if plus_rect.collidepoint(pos) and max_score < 20: max_score += 1
                if play_rect.collidepoint(pos): return max_score
        
        pygame.display.flip()
        clock.tick(FPS)

def game_loop(max_score):
    left_paddle = Paddle(100, HEIGHT//2, NEON_BLUE, True)
    right_paddle = Paddle(WIDTH - 100, HEIGHT//2, NEON_PINK, False)
    puck = Puck()
    running = True
    winner = None

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return

        # Movement
        left_paddle.move(keys)
        right_paddle.move(keys)
        puck.move()

        # Physics: Circle-Circle Collision
        for paddle in [left_paddle, right_paddle]:
            dx = puck.x - paddle.x
            dy = puck.y - paddle.y
            distance = math.hypot(dx, dy)

            if distance < (paddle.radius + puck.radius):
                overlap = (paddle.radius + puck.radius) - distance
                if distance == 0: distance = 0.1
                nx = dx / distance
                ny = dy / distance
                
                puck.x += nx * overlap
                puck.y += ny * overlap
                
                paddle_effect_x = paddle.vel_x * 0.5
                paddle_effect_y = paddle.vel_y * 0.5
                
                speed = math.hypot(puck.dx, puck.dy)
                if speed < BASE_PUCK_SPEED: speed = BASE_PUCK_SPEED
                
                puck.dx = (nx * speed) + paddle_effect_x
                puck.dy = (ny * speed) + paddle_effect_y
                
                # Cap max speed
                total_speed = math.hypot(puck.dx, puck.dy)
                if total_speed > MAX_PUCK_SPEED:
                    scale = MAX_PUCK_SPEED / total_speed
                    puck.dx *= scale
                    puck.dy *= scale

        # Goal Detection (Only triggers if puck actually passed the gap check in move())
        if puck.x < 0:
            right_paddle.score += 1
            puck.reset()
        if puck.x > WIDTH:
            left_paddle.score += 1
            puck.reset()

        # Win Condition
        if left_paddle.score >= max_score:
            winner = "LEFT PLAYER WINS!"
            running = False
        if right_paddle.score >= max_score:
            winner = "RIGHT PLAYER WINS!"
            running = False

        # Drawing
        draw_field()
        
        left_score_surf = font_large.render(str(left_paddle.score), True, NEON_BLUE)
        right_score_surf = font_large.render(str(right_paddle.score), True, NEON_PINK)
        screen.blit(left_score_surf, (WIDTH//4, 20))
        screen.blit(right_score_surf, (WIDTH*3//4, 20))

        left_paddle.draw(screen)
        right_paddle.draw(screen)
        puck.draw(screen)
        
        pygame.display.flip()

    return winner

def main_menu():
    while True:
        screen.fill(BLACK)
        title = font_large.render("PIXEL HOCKEY", True, NEON_GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        start_rect = pygame.Rect(WIDTH//2 - 100, 300, 200, 50)
        quit_rect = pygame.Rect(WIDTH//2 - 100, 400, 200, 50)
        
        draw_button("START", font_medium, NEON_BLUE, NEON_BLUE, start_rect)
        draw_button("QUIT", font_medium, NEON_PINK, NEON_PINK, quit_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(pos):
                    max_score = score_menu()
                    result = game_loop(max_score)
                    if result:
                        screen.fill(BLACK)
                        draw_text_centered(result, font_large, NEON_GREEN)
                        pygame.display.flip()
                        pygame.time.delay(3000)
                if quit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()