	

# Run this in the zone class to draw funky equidistant radial lines out from center of sprite!!!

def enemy_view_test(self):
angle = 0
line_count = 12
for x in range(360//line_count):
	angle += line_count
	start_point = self.grunt.rect.center - self.rendered_sprites.offset
	end_point = self.grunt.rect.centerx, self.grunt.rect.centery - 8
	pygame.draw.line(self.game.screen, WHITE, (pygame.math.Vector2(start_point)), (pygame.math.Vector2(end_point).rotate(angle)))