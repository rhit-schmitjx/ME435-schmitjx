import plateloader


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
    while True:
        selection = int(input("Selection: "))
        if selection == 0:
            break
        elif selection == 1:
            loader.send_command("RESET")

    loader.disconnect()
    print("Goodbye")

    

main()