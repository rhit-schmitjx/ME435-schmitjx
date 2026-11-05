import plateloader

<<<<<<< HEAD

def main():
    print("serial Menu")
    loader = plateloader.PlateLoader("/dev/ttyACM0")
    loader.connect()
    print("0: Exit")
    print("1: RESET")
    print("2: X-AXIS")
    print("3: GRIPPER")
    print("4: Z-AXIS")
    print("5: MOVE")
    print("6: Status")
=======
def main():
    print("Serial Menu")
    # loader = plateloader.PlateLoader("/dev/ttyUSB0")
    loader = plateloader.PlateLoader()
    loader.connect()
    print("0. Exit")
    print("1. RESET")
    print("2. X-AXIS")
    print("3. GRIPPER")
    print("4. Z-AXIS")
    print("5. MOVE")
    print("6. Status")
>>>>>>> 0426b797c97eb552faa2757e78295d23553a309d
    while True:
        selection = int(input("Selection: "))
        if selection == 0:
            break
        elif selection == 1:
<<<<<<< HEAD
            loader.send_command("RESET")

    loader.disconnect()
    print("Goodbye")

    
=======
            response = loader.send_command("RESET")
            print(response)
    
    loader.disconnect()
    print("Goodbye")




>>>>>>> 0426b797c97eb552faa2757e78295d23553a309d

main()