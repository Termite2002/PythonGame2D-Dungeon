import pygame
class Item(pygame.sprite.Sprite):
    def __init__(self, x , y, item_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type                       # 0 = coin, 1 = portion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, player):
        # check collision with player
        if self.rect.colliderect(player.rect):
            #coin collected
            if self.item_type == 0:
                player.score += 1
            elif self.item_type == 1:
                player.health += 10
                if player.health > 100:
                    player.health = 100
            self.kill()

        # control animation
        animation_cooldown = 150
        #update image
        self.image = self.animation_list[self.frame_index]
        # check time update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if animation is finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)