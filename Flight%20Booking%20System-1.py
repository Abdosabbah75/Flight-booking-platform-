def login():
    attempts = 3
    while attempts > 0:
        print("\nLogin")
        username = input("Username: ")
        password = input("Password: ")
        with open("users.txt", "r") as log:
            lines = log.readlines()[1:]
        for line in lines:
            part = line.strip().split(',')
            user = part[0]
            passw = part[1]
            if user == username and passw == password:
                print("Login successfully")
                return username
        attempts -= 1
        print(f"Invalid data. {attempts} attempts remaining")
    print("Attempts exhausted. Return to login menu.")
    return ""

def register():
    print("\nCreate new account")
    username = input("Username: ")
    password = input("Password: ")
    with open("users.txt", "a") as reg:
        reg.write(f"{username},{password}\n")
    print("Account created successfully")
    return username

def flights_(flights):
    for fly in flights:
        duration_minutes = fly.get('duration')
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        print(f"Flight No: {fly.get('id')}, from {fly.get('from')} to {fly.get('to')}, airline: {fly.get('airline')}, date: {fly.get('date')}, duration: {hours} hours and {minutes} minutes, price: {fly.get('price')}$")

def search(flights):
    origin = input("Origin: ").strip().lower()
    destination = input("Destination: ").strip().lower()
    matched = []
    for s in flights:
        if s['from'].lower() == origin and s['to'].lower() == destination:
            matched.append(s)
    if matched:
        print(f"Available flights from {origin} to {destination}:")
        flights_(matched)
    else:
        print("Not available flights")

def book(username , flights):
    flight_NO = input("Enter flight NO: ")
    matched = ""
    for f in flights:
        if f['id'] == flight_NO:
            matched = f
            print("The flight has been found.")
            break
    else:
        print("Flight NO. not found.")
        return
    if matched:
        name = input("Traveler name: ")
        with open("bookings.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                part = line.strip().split(',')
                nam = part[1]
                NO = part[2]
                if nam == name and NO == flight_NO:
                    print("This flight is already booked..")
                    return
        with open("bookings.txt", 'a') as file:
            file.write(f"{username},{name},{flight_NO}\n")
        print("Booked successfully.")

def cancel(username):
    name = input("Traveler name: ")
    flight_id = input("Flight NO: ")

    found = False
    with open("bookings.txt", 'r') as file:
        lines = file.readlines()

    with open("bookings.txt", 'w') as file:
        for line in lines:
            part = line.strip().split(',')
            user = part[0]
            nam = part[1]
            NO = part[2]
            if user == username and nam == name and NO == flight_id:
                found = True
            else:
                file.write(line)

    if found:
        print("Your Reservation has been cancelled.")
    else:
        print("Reservation not found.")
    
def modify(username, flights):
    name = input("Enter traveler name: ")
    flight_NO = input("Enter flight NO: ")
    
    matched = ""
    for f in flights:
        if f['id'] == flight_NO:
            matched = f
            print("The flight has been found.")
            break
    else:
        print("Flight NO. not found.")
        return

    if matched:
        with open("bookings.txt", 'r') as file:
            lines = file.readlines()
            found = False
            found1 = False
            updated = []
            for line in lines:
                part = line.strip().split(',')
                user = part[0]
                nam = part[1]
                NO = part[2]
                if user == username and nam == name and NO == flight_NO:
                    print("Booking found. You can change your booking details.")
                    print("1. Change traveler name\n2. Change flight NO.")
                    choice = int(input("Choose option: "))
                    if choice == 1:
                        new_name = input("Enter new traveler name: ")
                        with open("bookings.txt", 'r') as file_check:
                            check_lines = file_check.readlines()
                            for line_check in check_lines:
                                check_part = line_check.strip().split(',')
                                if check_part[1] == new_name and check_part[2] == NO:
                                    found1 = True
                                    updated.append(line)
                                    break
                            else:
                                found = True
                                updated.append(f"{user},{new_name},{NO}\n")
                    elif choice == 2:
                        new_flight_NO = input("Enter new flight NO: ")
                        valid = False
                        for f in flights:
                            if f['id'] == new_flight_NO:
                                valid = True
                                break
                        if valid:
                            with open("bookings.txt", 'r') as file_check:
                                check_lines = file_check.readlines()
                                for line_check in check_lines:
                                    check_part = line_check.strip().split(',')
                                    if check_part[1] == nam and check_part[2] == new_flight_NO:
                                        found1 = True
                                        updated.append(line)
                                        break
                                else:
                                    found = True
                                    updated.append(f"{user},{nam},{new_flight_NO}\n")
                        else:
                            updated.append(line)
                    else:
                        print("Invalid option.")
                        updated.append(line)
                        return
                else:
                    updated.append(line)

            if found:
                with open("bookings.txt", 'w') as file:
                    file.writelines(updated)
                print("Booking updated successfully.")
            elif found1:
                print("This booking already exists with the new flight number. Keeping the old booking.")
    
            else:
                print("No booking found with the given details. Keeping the old booking.")

def filter_(flights):
    print("Filtered by: ")
    print("1. Date.")
    print("2. Airline.")
    print("3. Destination.")
    print("4. Origin.")
    print("5. Price.")
    choice = int(input("Choose: "))
    filtered = []
    if choice == 1:
        keyword = input("Enter date (yyyy-mm-dd): ").lower()
        for flight in flights:
            if flight['date'].lower() == keyword:
                filtered.append(flight)
    elif choice == 2:
        keyword = input("Enter name of airline: ").lower()
        for flight in flights:
            if flight['airline'].lower() == keyword:
                filtered.append(flight)
    elif choice == 3:
        keyword = input("Enter destination: ").lower()
        for flight in flights:
            if flight['to'].lower() == keyword:
                filtered.append(flight)
    elif choice == 4:
        keyword = input("Enter origin: ").lower()
        for flight in flights:
            if flight['from'].lower() == keyword:
                filtered.append(flight)
    elif choice == 5:
        keyword = input("Enter max price: ")
        if keyword.isdigit():
            keyword = float(keyword)
            for flight in flights:
                if flight['price'] <= keyword:
                    filtered.append(flight)
        else:
            print("Not valid price.")
            return
    if filtered:
        flights_(filtered)
    else:
        print("No results.")

def compare(flights):
    print("Compare flight prices")
    print("Compare between:\n1. Two airlines\n2. Two destinations\n3. Two flights")
    choice = int(input("Choose: "))
    prices1 = []
    prices2 = []
    if choice == 1:
        a1 = input("Name of airline 1: ").strip().lower()
        a2 = input("Name of airline 2: ").strip().lower()
        for f in flights:
            if f['airline'].lower() == a1:
                prices1.append(f['price'])
            elif f['airline'].lower() == a2:
                prices2.append(f['price'])
        if prices1 and prices2:
            avg1 = sum(prices1) / len(prices1)
            avg2 = sum(prices2) / len(prices2)
            print(f"Average prices of airline 1 = {avg1}$")
            print(f"Average prices of airline 2 = {avg2}$")
        else:
            print("Not enough information.")    
    elif choice == 2:
        d1 = input("First destination: ").strip().lower()
        d2 = input("Second destination: ").strip().lower()
        for f in flights:
            if f['to'].lower() == d1:
                prices1.append(f['price'])
            elif f['to'].lower() == d2:
                prices2.append(f['price'])
        if prices1 and prices2:
            avg1 = sum(prices1) / len(prices1)
            avg2 = sum(prices2) / len(prices2)
            print(f"Average prices of first destination = {avg1}$")
            print(f"Average prices of second destination = {avg2}$")
        else:
            print("Not enough information.")   
    elif choice == 3:
        id1 = input("NO. of flight 1: ")
        id2 = input("NO. of flight 2: ")
        for f in flights:
            if f['id'] == id1:
                prices1.append(f['price'])
            elif f['id'] == id2:
                prices2.append(f['price'])
        if prices1 and prices2:
            avg1 = sum(prices1) / len(prices1)
            avg2 = sum(prices2) / len(prices2)
            print(f"First flight price = {avg1}$")
            print(f"Second flight price = {avg2}$")
        else:
            print("Not enough information.")
    else:
        print("Not available choice.")
        return

def ticket(username, flights):
    print("--- Printing ticket ---")
    name = input("Traveler name: ").strip()
    flight_NO = input("Flight NO: ").strip()
    with open("bookings.txt", 'r') as file:
        lines = file.readlines()
    for line in lines:
        part = line.strip().split(',')
        user = part[0]
        nam = part[1]
        NO = part[2]
        if user == username and nam == name and NO == flight_NO:
            for flight in flights:
                if flight['id'] == NO:
                    duration = flight.get('duration')
                    hours = duration // 60
                    minutes = duration % 60
                    ticket = (
                        f"\n==============================\n"
                        f"           🎫 Ticket        \n"
                        f"==============================\n"
                        f"👤 Username: {username}\n"
                        f"👤 Traveler name: {name}\n"
                        f"✈️ Flight NO: {flight['id']}\n"
                        f"🛫 From: {flight['from']}\n"
                        f"🛬 TO: {flight['to']}\n"
                        f"🏢 Airline: {flight['airline']}\n"
                        f"📅 Date: {flight['date']}\n"
                        f"🕓 Duration: {hours} hours {minutes} minutes\n"
                        f"💵 Price: {flight['price']}$\n"
                        f"==============================\n"
                    )
                    with open(f"{username}_ticket.txt", 'w') as tick:
                        tick.write(ticket)
                    wb = Workbook()
                    ws = wb.active
                    ws.append(["Username", "Name", "From", "To", "Airline", "Date", "Duration", "Price", "Flight NO."])
                    ws.append([username, name, flight['from'], flight['to'], flight['airline'], flight['date'], f"{hours}h{minutes}m", f"{flight['price']}$", flight['id']])
                    wb.save(f"{username}_ticket.xlsx")
                    print(f"The ticket has been printed in {username}_ticket.txt and {username}_ticket.xlsx")
                    return
    print("Reservation not found.")

from openpyxl import Workbook
import datetime

username = ""
while username == "":
    print("\nFlight booking system")
    print("1. Login\n2. Register")
    choice = int(input("\nChoose: "))
    if choice == 1:
        username = login()
    elif choice == 2:
        username = register()
flights = []
with open("flights.txt", 'r') as file:
    lines = file.readlines()[1:]
    for line in lines:
        part = line.strip().split(',')
        flights.append({
            'id': part[0],
            'from': part[1],
            'to': part[2],
            'airline': part[3],
            'date': part[4],
            'duration': int(part[5]),
            'price': float(part[6])
        })
while True:
    print("\nMenu\n")
    print("1. Available flights")
    print("2. Search flights by origin and destination")
    print("3. Booking a flight")
    print("4. Cancel booking")
    print("5. Modify booking or traveler information")
    print("6. Filter flights by date, airline, destination")
    print("7. Compare prices between airline, destinations, or flight NO.")
    print("8. Print ticket")
    print("9. Exit")
    choice = int(input("Choose: "))
    match choice:
        case 1:
            flights_(flights)
        case 2:
            search(flights)
        case 3:
            book(username , flights)
        case 4:
            cancel(username)
        case 5:
            modify(username , flights)
        case 6:
            filter_(flights)
        case 7:
            compare(flights)
        case 8:
            ticket(username , flights)
        case 9:
            print("Checked out")
            break
        case _:
            print("Incorrect choice")
