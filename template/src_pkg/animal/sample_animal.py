from .horse import Horse

my_horse = Horse('jack', weight=200, speed=48.5)
print(my_horse)
print(f'{my_horse.name} can go 100 km in {my_horse.time_to_go(100):.2f} hours.')