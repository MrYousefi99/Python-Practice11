import arcade
import random

 
class Player(arcade.Sprite):
    
    def __init__(self):
        super().__init__()
        self.color=arcade.color.BLUE
        self.width = 15
        self.height=80
        self.score=0
    
    def reset(self, x, y):
        self.center_x = x
        self.center_y = y
        
    def range(self):
        if self.top > 560 and self.change_y == 1: self.change_y = 0
        if self.bottom < 0 and self.change_y == -1: self.change_y = 0
        
    def update(self):
        self.range()
        self.center_y += (5 * self.change_y)

    def draw (self):
         arcade.draw_rectangle_filled(self.center_x,self.center_y,self.width,self.height,self.color) 
    

class Ball(arcade.Sprite):
    
    def __init__(self):
        super().__init__()
        self.color=arcade.color.CHERRY
        self.r=13
        self.width=23
        self.height=23
        self.screen_height=490
        self.hitter=1
        self.first_time=True

    def reset(self):
        self.center_x = (490)
        self.center_y = (280)
        self.change_x = random.choice([-1, 1])
        self.change_y = random.choice([-1, 1])

    def check_collisions(self, player_list):
        if self.left <= 0 or self.right >= 980:
            self.change_x = 0
            self.change_y = 0
        
        if self.top > 560: self.change_y = -1
        if self.bottom < 0: self.change_y = 1
        
        vis = self.collides_with_list(player_list)
        
        if vis:
            if self.center_x <490 and self.change_x == -1: self.change_x = 1
            elif self.center_x > 490 and self.change_x == 1: self.change_x = -1

    def update(self, player_list):
        self.center_x += (5 * self.change_x)
        self.center_y += (5 * self.change_y)
        self.check_collisions(player_list)
        
    def draw(self):
        arcade.draw_circle_filled(self.center_x,self.center_y,self.r,self.color)


class PongGame(arcade.Window):
    
    def __init__(self):
        super().__init__(980, 560, "Pong Game")
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.LIGHT_YELLOW)
        self.ball = Ball()
        self.ball.reset()
        self.players = arcade.SpriteList()
        self.player_1 = Player()
        self.player_1.reset(self.player_1.width, 280)
        self.players.append(self.player_1)
        self.player_2 = Player()
        self.player_2.reset(980 - self.player_2.width, 280)
        self.players.append(self.player_2)
        self.hit_upper_wall=False
        self.hit_lower_wall=False
        self.down_press=True
        self.up_press=True

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()
        self.player_1.draw()
        self.player_2.draw()
        score_text = f"{self.player_1.score} : {self.player_2.score}"
        arcade.draw_text(score_text,((self.width/2)-40),self.height-40,arcade.color.AMERICAN_ROSE,30)

    def on_update(self, delta_time):
        if (self.ball.center_x > 980): 
            self.player_1.score += 1
            self.ball.reset()
        if( self.ball.center_x-20 < 0): 
            self.player_2.score += 1
            self.ball.reset()
        self.player_1.update()
        self.P2_Move()
        self.player_2.update()
        self.ball.update(self.players)

    def P2_Move(self):
        if self.ball.center_y != self.player_2.center_y: self.player_2.change_y = self.ball.change_y
        else: self.player_2.change_y = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP : self.player_1.change_y=1
        elif key == arcade.key.DOWN : self.player_1.change_y=-1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP: self.player_1.change_y=0
        elif key == arcade.key.DOWN : self.player_1.change_y=0

PongGame()
arcade.run()        