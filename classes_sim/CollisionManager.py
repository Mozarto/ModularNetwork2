
class CollisionManager:
    def __init__(self, body, walls, food):
        self.body = body
        self.walls = walls.lines
        self.map = walls
        self.trees = food.trees
        self.food = food

    def body_walls(self, list_of_objects):

        indices = self.body.collidelistall(list_of_objects)

        if len(indices) > 0:
            i = indices[0]
            if len(indices) > 1:
                most_diagonals = 0
                for wall in indices:
                    body_top_left = [self.body.x, self.body.y]
                    body_top_right = [self.body.x + self.body.size[0], self.body.y]
                    body_bottom_left = [self.body.x, self.body.y + self.body.size[1]]
                    body_bottom_right = [self.body.x + self.body.size[0], self.body.y + self.body.size[1]]

                    diagonals = [body_top_left, body_bottom_left, body_bottom_right, body_top_right]

                    diag_counter = 0

                    for d in diagonals:
                        if list_of_objects[wall].collidepoint(d):
                            diag_counter += 1

                    if diag_counter > most_diagonals:
                        most_diagonals = diag_counter
                        i = wall


            horizontal_contact = False
            vertical_contact = False

            previous_speed_horizontal = (self.body.speed_vector[0] / self.body.INERTIA)
            previous_speed_vertical = (self.body.speed_vector[1] / self.body.INERTIA)

            rect = self.body.copy()

            rect.move_ip([previous_speed_horizontal, 0])

            if not rect.colliderect(list_of_objects[i]):
                horizontal_contact = True

            rect.move_ip([-previous_speed_horizontal, previous_speed_vertical])

            if not rect.colliderect(list_of_objects[i]):
                vertical_contact = True

            rect.move_ip([previous_speed_horizontal, 0])

            if not rect.colliderect(list_of_objects[i]) and not vertical_contact and not horizontal_contact:
                horizontal_contact = True
                vertical_contact = True

            if horizontal_contact and not vertical_contact:
                self.map.move([-previous_speed_horizontal, 0])
                self.food.move([-previous_speed_horizontal, 0])
                self.body.speed_vector[0] *= -1

            if vertical_contact and not horizontal_contact:
                self.map.move([0, -previous_speed_vertical])
                self.food.move([0, -previous_speed_vertical])
                self.body.speed_vector[1] *= -1

            if (vertical_contact and horizontal_contact):
                self.map.move([-previous_speed_horizontal, -previous_speed_vertical])
                self.food.move([-previous_speed_horizontal, -previous_speed_vertical])
                self.body.speed_vector[1] *= -1
                self.body.speed_vector[0] *= -1

            self.body_walls(list_of_objects)

    def body_food(self):
        for tree in self.trees:
            indices = self.body.collidelistall(tree.foods)

            for index in sorted(indices, reverse=True):
                self.body.score += 1
                del tree.foods[index]
