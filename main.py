import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
GRAY = (128, 128, 128)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (135, 206, 250)

# Game settings
FPS = 60
INITIAL_VEHICLE_SPEED = 0.08
INITIAL_LOG_SPEED = 0.06

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_x = x
        self.grid_y = y
        self.moving = False
        self.move_progress = 0
        self.target_x = x
        self.target_y = y
        self.alive = True
        self.on_log = False
        self.current_log = None
        self.idle_timer = 0  # Track how long player has been idle
        self.max_idle_time = 300  # 5 seconds at 60 FPS
        
    def move(self, dx, dy, lanes):
        if self.moving:
            return
        
        # Prevent backward movement (can't move down/south)
        if dy < 0:
            return
        
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Check boundaries
        if new_x < 0 or new_x >= GRID_WIDTH:
            return
        
        # Check for static obstacles
        if dy != 0 or dx != 0:  # Only check if moving
            lane_index = new_y
            if lane_index < len(lanes):
                lane = lanes[lane_index]
                # Check if there's a tree/obstacle at the target position
                if lane.type == "grass" and lane.has_obstacle_at(int(round(new_x))):
                    return
        
        # If moving forward (dy > 0), clear log riding
        if dy > 0:
            self.on_log = False
            self.current_log = None
        
        # Reset idle timer when player moves
        self.idle_timer = 0
        
        self.target_x = new_x
        self.target_y = new_y
        self.moving = True
        self.move_progress = 0
    
    def update(self):
        if self.moving:
            self.move_progress += 0.2
            if self.move_progress >= 1.0:
                self.grid_x = self.target_x
                self.grid_y = self.target_y
                self.x = self.grid_x
                self.y = self.grid_y
                self.moving = False
                self.move_progress = 0
            else:
                self.x = self.grid_x + (self.target_x - self.grid_x) * self.move_progress
                self.y = self.grid_y + (self.target_y - self.grid_y) * self.move_progress
    
    def draw(self, screen, camera_y):
        # Invert Y coordinate - higher grid_y should be higher on screen
        screen_y = (camera_y + GRID_HEIGHT - 1 - self.y) * TILE_SIZE
        screen_x = self.x * TILE_SIZE
        
        # Draw chicken body (yellow circle)
        center_x = int(screen_x + TILE_SIZE // 2)
        center_y = int(screen_y + TILE_SIZE // 2)
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), TILE_SIZE // 3)
        
        # Draw beak (small orange triangle)
        pygame.draw.polygon(screen, (255, 140, 0), [
            (center_x + TILE_SIZE // 4, center_y),
            (center_x + TILE_SIZE // 3 + 5, center_y - 3),
            (center_x + TILE_SIZE // 3 + 5, center_y + 3)
        ])
        
        # Draw eyes
        pygame.draw.circle(screen, BLACK, (center_x - 5, center_y - 5), 2)
        pygame.draw.circle(screen, BLACK, (center_x + 5, center_y - 5), 2)


class Vehicle:
    def __init__(self, x, y, speed, direction, vehicle_type="car"):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # 1 for right, -1 for left
        self.type = vehicle_type
        self.width = 2 if vehicle_type == "truck" else 1.5
        
    def update(self):
        self.x += self.speed * self.direction
        
        # Wrap around
        if self.direction > 0 and self.x > GRID_WIDTH + 2:
            self.x = -2
        elif self.direction < 0 and self.x < -2:
            self.x = GRID_WIDTH + 2
    
    def draw(self, screen, camera_y):
        # Invert Y coordinate
        screen_y = (camera_y + GRID_HEIGHT - 1 - self.y) * TILE_SIZE
        screen_x = self.x * TILE_SIZE
        
        width = int(self.width * TILE_SIZE)
        height = int(TILE_SIZE * 0.7)
        
        color = RED if self.type == "car" else GRAY
        pygame.draw.rect(screen, color, (int(screen_x), int(screen_y + TILE_SIZE * 0.15), width, height))
        
        # Windows
        window_color = LIGHT_BLUE
        pygame.draw.rect(screen, window_color, 
                        (int(screen_x + width * 0.2), int(screen_y + TILE_SIZE * 0.25), 
                         int(width * 0.3), int(height * 0.4)))
    
    def collides_with(self, player):
        # Check if player overlaps with vehicle
        px = player.grid_x
        py = player.grid_y
        
        if abs(py - self.y) < 0.5:
            if self.x <= px <= self.x + self.width:
                return True
        return False


class Log:
    def __init__(self, x, y, speed, direction, length=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.length = length
        
    def update(self):
        self.x += self.speed * self.direction
        
        # Wrap around
        if self.direction > 0 and self.x > GRID_WIDTH + self.length:
            self.x = -self.length
        elif self.direction < 0 and self.x < -self.length:
            self.x = GRID_WIDTH + self.length
    
    def draw(self, screen, camera_y):
        # Invert Y coordinate
        screen_y = (camera_y + GRID_HEIGHT - 1 - self.y) * TILE_SIZE
        screen_x = self.x * TILE_SIZE
        
        width = int(self.length * TILE_SIZE)
        height = int(TILE_SIZE * 0.6)
        
        pygame.draw.rect(screen, BROWN, 
                        (int(screen_x), int(screen_y + TILE_SIZE * 0.2), width, height))
        
        # Log texture lines
        for i in range(int(self.length)):
            line_x = int(screen_x + i * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.line(screen, (100, 50, 0), 
                           (line_x, int(screen_y + TILE_SIZE * 0.2)), 
                           (line_x, int(screen_y + TILE_SIZE * 0.8)), 2)
    
    def is_player_on(self, player):
        px = player.grid_x
        py = player.grid_y
        
        if abs(py - self.y) < 0.5:
            if self.x <= px < self.x + self.length:
                return True
        return False


class Train:
    def __init__(self, y, direction):
        self.y = y
        self.direction = direction
        self.active = False
        self.x = -10 if direction > 0 else GRID_WIDTH + 10
        self.warning_timer = 0
        self.warning_duration = 120  # 2 seconds at 60 FPS
        self.speed = 0.5
        self.length = 5
        
    def trigger_warning(self):
        if not self.active:
            self.warning_timer = self.warning_duration
    
    def update(self):
        if self.warning_timer > 0:
            self.warning_timer -= 1
            if self.warning_timer == 0:
                self.active = True
                self.x = -self.length if self.direction > 0 else GRID_WIDTH + self.length
        
        if self.active:
            self.x += self.speed * self.direction
            
            # Deactivate when off screen
            if (self.direction > 0 and self.x > GRID_WIDTH + 5) or \
               (self.direction < 0 and self.x < -5):
                self.active = False
    
    def draw(self, screen, camera_y):
        # Invert Y coordinate
        screen_y = (camera_y + GRID_HEIGHT - 1 - self.y) * TILE_SIZE
        
        if self.warning_timer > 0:
            # Flash warning
            if self.warning_timer % 20 < 10:
                pygame.draw.rect(screen, RED, (0, int(screen_y), SCREEN_WIDTH, TILE_SIZE), 3)
        
        if self.active:
            screen_x = self.x * TILE_SIZE
            width = int(self.length * TILE_SIZE)
            height = int(TILE_SIZE * 0.8)
            
            pygame.draw.rect(screen, DARK_GREEN, 
                           (int(screen_x), int(screen_y + TILE_SIZE * 0.1), width, height))
            
            # Train windows
            for i in range(self.length):
                window_x = int(screen_x + i * TILE_SIZE + 10)
                pygame.draw.rect(screen, YELLOW, 
                               (window_x, int(screen_y + TILE_SIZE * 0.3), 20, 15))
    
    def collides_with(self, player):
        if not self.active:
            return False
        
        px = player.grid_x
        py = player.grid_y
        
        if abs(py - self.y) < 0.5:
            if self.x <= px < self.x + self.length:
                return True
        return False


class Lane:
    def __init__(self, y, lane_type, direction=1, speed=1.5):
        self.y = y
        self.type = lane_type
        self.direction = direction
        self.speed = speed
        self.vehicles = []
        self.logs = []
        self.train = None
        self.obstacles = []
        
        if lane_type == "road":
            self.spawn_vehicles()
        elif lane_type == "river":
            self.spawn_logs()
        elif lane_type == "train":
            self.train = Train(y, direction)
        elif lane_type == "grass":
            self.spawn_obstacles()
    
    def spawn_vehicles(self):
        num_vehicles = random.randint(2, 4)
        spacing = GRID_WIDTH / num_vehicles
        
        for i in range(num_vehicles):
            x = i * spacing + random.uniform(-spacing * 0.3, spacing * 0.3)
            vehicle_type = random.choice(["car", "car", "truck"])
            self.vehicles.append(Vehicle(x, self.y, self.speed, self.direction, vehicle_type))
    
    def spawn_logs(self):
        num_logs = random.randint(2, 3)
        spacing = GRID_WIDTH / num_logs
        
        for i in range(num_logs):
            x = i * spacing + random.uniform(-spacing * 0.3, spacing * 0.3)
            length = random.randint(2, 3)
            self.logs.append(Log(x, self.y, self.speed, self.direction, length))
    
    def spawn_obstacles(self):
        # Randomly place trees/rocks
        num_obstacles = random.randint(0, 3)
        for _ in range(num_obstacles):
            x = random.randint(0, GRID_WIDTH - 1)
            self.obstacles.append(x)
    
    def has_obstacle_at(self, x):
        return x in self.obstacles
    
    def update(self):
        for vehicle in self.vehicles:
            vehicle.update()
        for log in self.logs:
            log.update()
        if self.train:
            self.train.update()
    
    def draw(self, screen, camera_y):
        # Invert Y coordinate
        screen_y = (camera_y + GRID_HEIGHT - 1 - self.y) * TILE_SIZE
        
        # Draw lane background
        if self.type == "grass":
            color = GREEN
        elif self.type == "road":
            color = GRAY
        elif self.type == "river":
            color = BLUE
        elif self.type == "train":
            color = BROWN
        else:
            color = GREEN
        
        pygame.draw.rect(screen, color, (0, int(screen_y), SCREEN_WIDTH, TILE_SIZE))
        
        # Draw lane decorations
        if self.type == "road":
            # Draw road lines
            dash_width = 20
            dash_spacing = 40
            for x in range(0, SCREEN_WIDTH, dash_width + dash_spacing):
                pygame.draw.rect(screen, WHITE, (x, int(screen_y + TILE_SIZE // 2 - 2), dash_width, 4))
        
        if self.type == "grass":
            # Draw obstacles (trees)
            for obs_x in self.obstacles:
                obs_screen_x = obs_x * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, DARK_GREEN, 
                                 (int(obs_screen_x), int(screen_y + TILE_SIZE // 2)), 
                                 TILE_SIZE // 3)
        
        # Draw entities
        for vehicle in self.vehicles:
            vehicle.draw(screen, camera_y)
        for log in self.logs:
            log.draw(screen, camera_y)
        if self.train:
            self.train.draw(screen, camera_y)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Crossy Road")
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        self.player = Player(GRID_WIDTH // 2, 0)
        self.camera_y = 0
        self.camera_target_y = 0
        self.score = 0
        self.max_progress = 0
        self.game_over = False
        self.game_started = False  # Track if player has moved yet
        self.lanes = []
        
        # Generate initial lanes
        self.generate_initial_lanes()
    
    def generate_initial_lanes(self):
        lane_types = ["grass", "road", "river", "train", "grass"]
        
        for i in range(GRID_HEIGHT + 20):
            if i < 2:
                lane_type = "grass"
            else:
                lane_type = random.choice(lane_types)
                
                # Don't put hazards right next to each other too often
                if len(self.lanes) > 0 and self.lanes[-1].type in ["river", "train"]:
                    if random.random() < 0.6:
                        lane_type = "grass"
            
            direction = random.choice([1, -1])
            base_speed = INITIAL_VEHICLE_SPEED if lane_type == "road" else INITIAL_LOG_SPEED
            speed = base_speed * random.uniform(0.7, 1.3)
            
            self.lanes.append(Lane(i, lane_type, direction, speed))
    
    def update(self):
        if self.game_over:
            return
        
        # Update player
        self.player.update()
        
        # Camera tracks player smoothly - player starts at Y=0 (bottom) and moves up
        self.camera_target_y = max(0, self.player.grid_y - 2)
        
        # Camera constantly moves forward slowly to pressure the player - but only after first move
        if self.game_started:
            camera_forward_speed = 0.008  # Slow constant forward pressure
            self.camera_target_y += camera_forward_speed
        
        # Smooth camera interpolation - consistent throughout the game
        camera_speed = 0.2  # Smooth following that works well at all distances
        self.camera_y += (self.camera_target_y - self.camera_y) * camera_speed
        
        # Check if player gets caught by bottom of screen (only after game has started)
        if self.game_started:
            # Bottom of screen is at camera_y + GRID_HEIGHT - 1
            player_screen_y = self.camera_y + GRID_HEIGHT - 1 - self.player.grid_y
            if player_screen_y >= GRID_HEIGHT - 0.5:  # Player is at or below bottom edge
                self.player.alive = False
                self.game_over = True
                return
        
        # Update score (based on forward progress)
        if self.player.grid_y > self.max_progress:
            self.score += self.player.grid_y - self.max_progress
            self.max_progress = self.player.grid_y
            # Mark game as started once player moves forward
            if not self.game_started:
                self.game_started = True
        
        # Check for eagle attack (idle too long) - only after game has started
        if self.game_started and not self.player.moving:
            self.player.idle_timer += 1
            if self.player.idle_timer >= self.player.max_idle_time:
                # Eagle attack! Game over
                self.player.alive = False
                self.game_over = True
                return
        
        # Generate new lanes ahead
        while len(self.lanes) < self.camera_y + GRID_HEIGHT + 10:
            lane_types = ["grass", "road", "river", "train", "grass"]
            lane_type = random.choice(lane_types)
            
            if len(self.lanes) > 0 and self.lanes[-1].type in ["river", "train"]:
                if random.random() < 0.6:
                    lane_type = "grass"
            
            direction = random.choice([1, -1])
            
            # Progressive difficulty
            difficulty_multiplier = 1 + (self.score / 200) * 0.2
            base_speed = INITIAL_VEHICLE_SPEED if lane_type == "road" else INITIAL_LOG_SPEED
            speed = base_speed * random.uniform(0.7, 1.3) * difficulty_multiplier
            
            new_y = len(self.lanes)
            self.lanes.append(Lane(new_y, lane_type, direction, speed))
        
        # Update lanes
        for lane in self.lanes:
            lane.update()
        
        # Trigger train warnings randomly
        for lane in self.lanes:
            if lane.type == "train" and lane.train and not lane.train.active:
                if random.random() < 0.01:  # 1% chance per frame
                    lane.train.trigger_warning()
        
        # Check collisions
        self.check_collisions()
    
    def check_collisions(self):
        if not self.player.alive:
            return
        
        # Only check most collisions after player has finished moving and landed
        if self.player.moving:
            return
        
        player_lane_index = self.player.grid_y
        if player_lane_index >= len(self.lanes):
            return
            
        lane = self.lanes[player_lane_index]
        
        # Check vehicle collisions - only after landing
        if lane.type == "road":
            for vehicle in lane.vehicles:
                if vehicle.collides_with(self.player):
                    self.player.alive = False
                    self.game_over = True
                    return
        
        # Check water collisions - only after landing
        if lane.type == "river":
            on_log = False
            for log in lane.logs:
                if log.is_player_on(self.player):
                    on_log = True
                    self.player.on_log = True
                    self.player.current_log = log
                    break
            
            # Only die from water if player has landed and not on a log
            if not on_log:
                self.player.alive = False
                self.game_over = True
                return
        
        # If player is on a log, move with it
        if self.player.on_log and self.player.current_log:
            # Move player with log continuously
            self.player.x += self.player.current_log.speed * self.player.current_log.direction
            self.player.grid_x = self.player.x
            self.player.target_x = self.player.x  # Keep target synced
            
            # Only die if player gets carried completely off screen
            if self.player.grid_x < -0.5 or self.player.grid_x >= GRID_WIDTH + 0.5:
                self.player.alive = False
                self.game_over = True
                return
        
        # Check train collisions - only after landing
        if lane.type == "train" and lane.train:
            if lane.train.collides_with(self.player):
                self.player.alive = False
                self.game_over = True
                return
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw lanes
        for lane in self.lanes:
            # Check if lane is visible on screen
            lane_screen_y = self.camera_y + GRID_HEIGHT - 1 - lane.y
            if -2 <= lane_screen_y <= GRID_HEIGHT + 2:
                lane.draw(self.screen, self.camera_y)
        
        # Draw player
        self.player.draw(self.screen, self.camera_y)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw eagle warning if idle for too long (after game started)
        if self.game_started and not self.player.moving:
            time_left = self.player.max_idle_time - self.player.idle_timer
            # Show warning in last 2 seconds (120 frames)
            if time_left < 120:
                warning_alpha = min(255, (120 - time_left) * 4)
                # Draw darkening shadow effect
                shadow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                shadow.set_alpha(warning_alpha // 3)
                shadow.fill(BLACK)
                self.screen.blit(shadow, (0, 0))
                
                # Draw warning text
                if time_left < 60:  # Flash warning in last second
                    if time_left % 20 < 10:
                        warning_font = pygame.font.Font(None, 48)
                        warning_text = warning_font.render("EAGLE INCOMING!", True, RED)
                        self.screen.blit(warning_text, 
                                       (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, 100))
        
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            restart_text = font.render("Press SPACE to Restart", True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:
                    # UP arrow moves forward (north/increases Y)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.move(0, 1, self.lanes)
                    # No backward movement allowed
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move(-1, 0, self.lanes)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move(1, 0, self.lanes)
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()