from easygopigo3 import EasyGoPiGo3
import time

gpg = EasyGoPiGo3()
gpg.reset_encoders()
gpg.set_speed(100)
battery = gpg.volt()
# Display Battery Level
print(f"{battery} volts")
max_dist = 25
count = 0
run = True
# Error Var to account for length of robot, and Var for
dist_from_wheel_to_sensor = 10  # 10 cm for each side reading
cm_per_wheel_turn = 22

my_sensor1 = gpg.init_ultrasonic_sensor('AD1')
my_sensor2 = gpg.init_ultrasonic_sensor('AD2')

while run:
    sensor1_dist = my_sensor1.read()
    sensor2_dist = my_sensor2.read()
    if sensor1_dist >= max_dist and sensor2_dist >= max_dist:
        if count == 0:
            while sensor2_dist >= max_dist:
                sensor2_dist = my_sensor2.read()
                gpg.forward()
            gpg.stop()
        if count == 1:
            while sensor1_dist >= max_dist:
                sensor1_dist = my_sensor1.read()
                gpg.forward()
            gpg.stop()
    sensor1_dist = my_sensor1.read()
    sensor2_dist = my_sensor2.read()
    if sensor1_dist < max_dist and sensor2_dist < max_dist:
        print("Entering if statement that reads the box size")
        gpg.reset_encoders()
        if count == 0:
            print("Reading side 1...")
            while sensor1_dist < max_dist and sensor2_dist < max_dist:
                sensor1_dist = my_sensor1.read()
                sensor2_dist = my_sensor2.read()
                gpg.forward()
            gpg.stop()
            side1 = list(gpg.read_encoders())
        if count == 1:
            print("Reading side 2...")
            while sensor1_dist < max_dist and sensor2_dist < max_dist:
                sensor1_dist = my_sensor1.read()
                sensor2_dist = my_sensor2.read()
                gpg.forward()
            gpg.stop()
            side2 = list(gpg.read_encoders())
    sensor1_dist = my_sensor1.read()
    sensor2_dist = my_sensor2.read()
    if sensor1_dist < max_dist and sensor2_dist >= max_dist:
        while sensor1_dist < max_dist and sensor2_dist >= max_dist:
            sensor1_dist = my_sensor1.read()
            sensor2_dist = my_sensor2.read()
            gpg.forward()
        gpg.stop()
    sensor1_dist = my_sensor1.read()
    sensor2_dist = my_sensor2.read()
    if sensor1_dist >= max_dist and sensor2_dist < max_dist:
        print("Entering turning if statement")
        while sensor2_dist < max_dist:
            sensor2_dist = my_sensor2.read()
            gpg.forward()
        gpg.drive_cm(5)
        gpg.turn_degrees(-90)
        count += 1
    if count >= 2:
        print("done")
        run = False

side1_degrees = sum(side1) / 2
side2_degrees = sum(side2) / 2
print(f"side 1 degrees {side1_degrees}")
print(f"side 2 degrees {side2_degrees}")

side1_length = (side1_degrees / 360) * cm_per_wheel_turn + dist_from_wheel_to_sensor
side2_length = (side2_degrees / 360) * cm_per_wheel_turn + dist_from_wheel_to_sensor
print(f"Side 1 is {side1_length}cm")
print(f"Side 2 is {side2_length}cm")

box_perimeter = (2 * side1_length) + (2 * side2_length)
print(f"Perimeter of box is {box_perimeter}")

box_square_cm = side1_length * side2_length
print(f"Square centimers of box is {box_square_cm}cm squared")

combined_dist = side1_length + side2_length
print(f"Width and length have a combined distance of {combined_dist}cm")
