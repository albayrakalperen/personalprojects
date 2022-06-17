#Create turtle. Turtle can only move up.
#Create cars randomly along the y-axis. They go from right side to left side. Increment the spped each level.
#If turtle is at upper side of the screen, level up.
#If turtle hits a car. Game stops. Print game over.

import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move, "w")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.create_car()
    car_manager.move_car()

    if player.position() == (0, 280):
        player.refresh_position()
        scoreboard.level_increase()
        car_manager.increment_speed()

    for car in car_manager.all_cars:
        if player.distance(car) < 38:
            game_is_on = False
            scoreboard.game_over()

screen.exitonclick()
