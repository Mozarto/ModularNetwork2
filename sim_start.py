import pygame
from classes_sim.Body import Body
from classes_sim.Walls import Walls
from classes_sim.CollisionManager import CollisionManager
from classes_sim.Food import Food


def sim(ind, view, neuron_manager, screen_size, screen_size_surfaces, screen_border, time, zoom, map_size, food_timer, food_density):
    pygame.init()

    screen_main = pygame.display.set_mode(screen_size)
    screen_main.fill("white")
    clock = pygame.time.Clock()
    running = True
    framerate = 15

    surface_world = pygame.Surface(screen_size_surfaces)

    body = Body(screen_size_surfaces, zoom)
    walls = Walls(screen_size_surfaces, zoom, map_size)

    food = Food(walls, zoom, food_timer, food_density)
    body.position(walls, food)
    cm = CollisionManager(body, walls, food)

    surface_view = pygame.Surface(screen_size_surfaces)

    timer = 0

    neurons_size_surface = (screen_size[0] / 4 * 3 - (screen_border * 2), screen_size[1] - (screen_border * 2))
    surface_neurons = pygame.Surface(neurons_size_surface)

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Network input
        ind.depolarize_effectors()
        ind.activate_first_neurons()
        ind.manage_activated_neurons(body, ind.effectors)
        ind.depolarize_neurons()


        # print("over")

        # Movement
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     body.up()
        # if keys[pygame.K_s]:
        #     body.down()
        # if keys[pygame.K_a]:
        #     body.left()
        # if keys[pygame.K_d]:
        #     body.right()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
             running = False

        neuron_manager.move()

        walls.move([body.speed_vector[0], body.speed_vector[1]])
        food.move([body.speed_vector[0], body.speed_vector[1]])
        body.move_manager()

        # Processing
        cm.body_walls(cm.walls)
        cm.body_walls(cm.trees)
        cm.body_food()
        food.create_foods_timer()

        view.check((food.get_foods(), walls.lines, food.trees, [body]),
                   (food.trees[0].FOOD_COLOR, walls.COLOR, food.COLOR, body.COLOR))

        # fill the surface_world with a color to wipe away anything from last frame
        surface_world.fill("black")

        surface_view.fill("black")

        surface_neurons.fill("gray")

        # RENDER YOUR GAME HERE
        walls.draw(surface_world)
        body.draw(surface_world)
        food.draw(surface_world, walls)

        view.draw(surface_view)
        counter = 0
        for i in ind.first_neurons:
            if ind.first_neurons[i].is_activated:
                counter += 1
        #print(counter)
        neuron_manager.draw(surface_neurons)

        screen_main.blit(surface_world,
                         (screen_border, screen_size[1] / 2 + screen_border))
        screen_main.blit(surface_view, (screen_border, screen_size[1] / 4 * 3 + screen_border))

        screen_main.blit(surface_neurons, (screen_size[0] / 4 + screen_border, screen_border))

        # flip() the display to put your work on surface_world
        pygame.display.flip()

        timer += 1
        if timer == time:
            running = False

        clock.tick(framerate)  # limits FPS

    # saving

    pygame.quit()

    return (body.score, body.calculate_distance_travelled())
