import pygame
import random
import time

pygame.init()

Width, Height = 800, 600
WIN = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Car Game")

FONT = pygame.font.SysFont("garamond", 22)

def draw(time_passed):
    time_passed_text = FONT.render(f"Time: {round(time_passed)}s", 1, "black")
    WIN.blit(time_passed_text, (10, 10))

# colors
gray = (100, 100, 100)
green = (3, 192, 60)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# road marker size
marker_width = 10
marker_height = 50

# road and edge markers
road = (250, 0, 300, Height)
left_edge_marker = (245, 0, marker_width, Height)
right_edge_marker = (545, 0, marker_width, Height)

# coordinates of lanes
right_lane = 300
centre_lane = 400
left_lane = 500
lanes = [right_lane, centre_lane, left_lane]

# lane movement animation
lane_marker_move_y = 0
velocity = 2

# loading screen image
loading_screen_image = pygame.image.load("FireCar.jpeg")
game_over_image = pygame.image.load("Game_over_screen.jpg")

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # scale the image down
        image_scale = 100 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('Vehicle_image/Mini_van.png')
        super().__init__(image, x, y)

# starting coordinates
player_x = 400
player_y = 500

# player car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

#other vehicles
image_filenames = ['Ambulance.png', 'truck.png','Car.png', 'Black_viper.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('Vehicle_image/'+ image_filename)
    vehicle_images.append(image)

#sprite vehicle group
vehicle_group = pygame.sprite.Group()

def loading_screen():
    WIN.fill(gray)
    WIN.blit(loading_screen_image, (Width // 2 - loading_screen_image.get_width() // 2, Height // 2 - loading_screen_image.get_height() // 2))
    font = pygame.font.SysFont(None, 55)
    text = font.render('Loading...', True, (0, 0, 0))
    WIN.blit(text, (Width // 2 - text.get_width() // 2, Height // 2 + loading_screen_image.get_height() // 2))
    pygame.display.update()
    time.sleep(3)  # Display loading screen for 3 seconds

def game_over_screen():
    WIN.fill(white)
    WIN.blit(game_over_image, (Width // 2 - game_over_image.get_width() // 2, Height // 2 - game_over_image.get_height() // 2))
    font = pygame.font.SysFont("garamond", 55)
    text = font.render('Failed! Collision detected', True, red)
    WIN.blit(text, (Width // 2 - text.get_width() // 2, Height // 2 - text.get_height() // 2))
    pygame.display.update()
    time.sleep(5)


# screen function
def screen():
    global lane_marker_move_y
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    time_passed = 0

    # game loop
    while run:
        clock.tick(60)
        time_passed = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move the car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > road[0]:
            player.rect.x -= 10
        if keys[pygame.K_RIGHT] and player.rect.right < road[0] + road[2]:
            player.rect.x += 10

        # draw grass
        WIN.fill(green)

        # draw road
        pygame.draw.rect(WIN, gray, road)

        # draw edge markers
        pygame.draw.rect(WIN, yellow, left_edge_marker)
        pygame.draw.rect(WIN, yellow, right_edge_marker)

        # draw the lane markers
        lane_marker_move_y += velocity * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0

        for y in range(marker_height * -2, Height, marker_height * 2):
            pygame.draw.rect(WIN, white, (centre_lane - 5, y + lane_marker_move_y, marker_width, marker_height))

        player_group.draw(WIN)
        draw(time_passed)

        if len(vehicle_group) < 2:
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height*1.5:
                    add_vehicle = False

            if add_vehicle:
                #choose a random lane
                lane = random.choice(lanes)

                #select a random vehicle
                image = random.choice(vehicle_images)

                #add new vehicle
                new_vehicle = Vehicle(image, lane, -image.get_rect().height)
                vehicle_group.add(new_vehicle)


        #make the cars move
        for vehicle in vehicle_group:
            vehicle.rect.y += velocity

            if vehicle.rect.top >= Height:
                vehicle.kill()
        

        #check for collisions
        if pygame.sprite.spritecollide(player, vehicle_group, False):
            print("Collision detected!")
            game_over_screen()
            run = False

        vehicle_group.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    loading_screen()
    screen()
