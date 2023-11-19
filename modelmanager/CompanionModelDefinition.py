import math
import os
import random
import time


class CompanionModelDefinition:
    MIN_SCREEN_STEP = 0.00005
    MAX_SCREEN_STEP = 0.00015

    def __init__(self, location: str, manifest: dict):
        self.name = manifest['name']
        self.scale = manifest['scale']
        self.aabb = manifest['aabb'] if 'aabb' in manifest else {
            'x': 0, 'y': 0,
            'width': manifest['sprite']['meta']['size']['w'],
            'height': manifest['sprite']['meta']['size']['h']
        }
        self.is_inverted = manifest['inverted']
        self.language = manifest['language']
        self.frames_count = manifest['sprite']['frameCount'] if 'frameCount' in manifest['sprite'] \
            else 1
        self.sprite_count = manifest['sprite']['spriteCount']
        self.image_size = manifest['sprite']['meta']['size']
        self.frame_size = {
            'w': self.image_size['w'] / self.sprite_count['w'],
            'h': self.image_size['h'] / self.sprite_count['h']
        }
        self.current_animation_frame = 0
        self.image = os.path.join(location, manifest['sprite']['meta']['image'])
        self.can_fly = manifest['canFly'] if 'canFly' in manifest else False

        self.target = (-1, -1)
        self.speed = (0, 0)
        self.pos = [0, 0]

        self.want_to_walk = True
        self.last_state_change_time = time.time()
        self.state_change_time = 1
        self.last_animation_frame_change_time = time.time_ns()

        self.should_validate_pos = False

    def update_position(self, pos: tuple[int, int]):
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.should_validate_pos = True

    def get_next_pos(self, screen_bounds: tuple[int, int, int, int],
                     companion_size: tuple[int, int, int, int],
                     pos: tuple[int, int]) -> tuple[int, int]:
        if self.should_validate_pos:
            self.should_validate_pos = False
            x, y = self.fix_position(screen_bounds, companion_size, (self.pos[0], self.pos[1]))
            self.pos[0] = x
            self.pos[1] = y
            self.find_new_target(screen_bounds, companion_size, pos)
            return self.pos[0], self.pos[1]
        if not self.can_fly:
            if self.last_state_change_time + self.state_change_time <= time.time():
                self.want_to_walk = not self.want_to_walk
                self.last_state_change_time = time.time()
                self.state_change_time = random.random() * 8 + 2
                if self.want_to_walk:
                    self.find_new_target(screen_bounds, companion_size, pos)
            if not self.want_to_walk:
                return pos
        has_reached_x = pos[0] >= self.target[0] if self.speed[0] > 0 else pos[0] <= self.target[0]
        has_reached_y = pos[1] >= self.target[1] if self.speed[1] > 0 else pos[1] <= self.target[1]
        init = self.target[0] == -1
        if self.target[0] == -1 or (has_reached_x and has_reached_y):
            self.find_new_target(screen_bounds, companion_size, pos)
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if init:
            self.pos[0] = self.target[0]
            self.pos[1] = self.target[1]
            return self.target
        return self.pos[0], self.pos[1]

    def find_new_target(self, screen_bounds: tuple[int, int, int, int],
                        companion_size: tuple[int, int, int, int],
                        pos: tuple[int, int]):
        x = random.randint(screen_bounds[0] - companion_size[0],
                           screen_bounds[2] - companion_size[2])
        if self.can_fly:
            y = random.randint(screen_bounds[1] - companion_size[1],
                               screen_bounds[3] - companion_size[3])
        else:
            y = screen_bounds[3] - companion_size[3]
        delta = x - pos[0], y - pos[1]
        distance = math.sqrt(delta[0] ** 2 + delta[1] ** 2)
        if distance == 0:
            self.find_new_target(screen_bounds, companion_size, pos)
            return
        step = self.get_pixels_per_second(screen_bounds)
        self.speed = step * delta[0] / distance, step * delta[1] / distance
        self.target = x, y

    def get_pixels_per_second(self, screen_bounds: tuple[int, int, int, int]):
        max_step = self.MAX_SCREEN_STEP
        if self.can_fly:
            max_step *= 2
        screen_diagonal = math.sqrt(screen_bounds[2] ** 2 + screen_bounds[3] ** 2)
        screen_step = random.random() * (max_step - self.MIN_SCREEN_STEP) + self.MAX_SCREEN_STEP
        return screen_step * screen_diagonal

    def fix_position(self, screen_bounds: tuple[int, int, int, int],
                     companion_size: tuple[int, int, int, int],
                     pos: tuple[int, int]) -> tuple[int, int]:
        x = min(max(screen_bounds[0] - companion_size[0], pos[0]), screen_bounds[2])
        if self.can_fly:
            y = min(max(screen_bounds[1] - companion_size[1], pos[1]), screen_bounds[3])
        else:
            y = screen_bounds[3] - companion_size[3]
        return x, y

    def apply_scale(self, scale):
        for i in 'w', 'h':
            self.frame_size[i] *= scale
            self.image_size[i] *= scale

    def get_next_frame_bounds(self) -> tuple[int, int, int, int]:
        if self.sprite_count['w'] == 1 and self.sprite_count['h'] == 1:
            return 0, 0, self.image_size['w'], self.image_size['h']
        if self.last_animation_frame_change_time + 25 * 10**6 < time.time_ns():
            self.last_animation_frame_change_time = time.time_ns()
            self.current_animation_frame += 1
            if self.current_animation_frame >= self.frames_count:
                self.current_animation_frame = 0
        return (
            self.frame_size['w'] * (self.current_animation_frame % self.sprite_count['w']),
            self.frame_size['h'] * (self.current_animation_frame // self.sprite_count['w']),
            self.frame_size['w'], self.frame_size['h']
        )
