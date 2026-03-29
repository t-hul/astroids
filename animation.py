import pygame


class Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, parent_shape, width, height, pivot):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.parent = parent_shape
        self.width = width
        self.height = height
        self.pivot = pivot
        self.transparent_color = "black"
        self.time = 0

    def draw(self, screen):
        frame = self.get_frame(self.time, 2)
        # frame = pygame.transform.rotate(frame, -self.parent.rotation - 90)
        # screen.blit(frame, self.parent.position)
        self.blitRotate(
            screen,
            frame,
            self.parent.position,
            (self.width, self.height / 2),
            -self.parent.rotation - 90,
        )

    def update(self, dt):
        self.time += dt

    def get_frame(self, time, scale):
        frame_id = int(time * 5) % 23
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(
            self.sprite_sheet_image,
            (0, 0),
            (frame_id * self.width, 0, self.width, self.height),
        )
        image = pygame.transform.scale(image, (self.width * scale, self.height * scale))
        image.set_colorkey(self.transparent_color)

        return image

    def rotate_and_blit(self, surf, image, pos, originPos, angle):
        # offset from pivot to center
        image_rect = image.get_rect(
            topleft=(pos[0] - originPos[0], pos[1] - originPos[1])
        )
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        # rotate and blit the image
        surf.blit(rotated_image, rotated_image_rect)

        # draw rectangle around the image
        pygame.draw.rect(
            surf,
            (255, 0, 0),
            (*rotated_image_rect.topleft, *rotated_image.get_size()),
            2,
        )
