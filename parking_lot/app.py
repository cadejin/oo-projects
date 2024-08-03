class Vehicle:
    def __init__(self, license_plate, size):
        self._license_plate = license_plate
        self._size = size
    
    def get_size(self):
        return self._size

    def get_license_plate(self):
        return self._license_plate


class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, 1)


class Limo(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, 2)


class SemiTruck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, 3)

class Driver:
    def __init__(self, vehicle, balance):
        self._vehicle = vehicle
        self._balance = balance
        self._ticket = None
    
    def get_vehicle(self):
        return self._vehicle
    
    def get_balance(self):
        return self._balance

    def get_parking_spot(self):
        return self._parking_spot
    
    def park(self, parking_lot, check_in):
        vehicle = self.get_vehicle()
        ticket = parking_lot.assign(vehicle, check_in)
        if ticket:
            level, begin_spot, end_spot, check_in = ticket.get_level(), ticket.get_begin_spot(), ticket.get_end_spot(), ticket.get_check_in()
            self._ticket = ticket
            print(f"Your assigned parking spot is on level {level}, spots {begin_spot} to {end_spot}.")
            print(f"Your checkin time is {check_in}")
        else:
            print(f"Sorry, there are no spots available.")
    
    def check_out(self, parking_lot, check_out):
        vehicle = self.get_vehicle()
        price = parking_lot.get_rate() * (check_out - self._ticket.get_check_in())
        print(f"You must pay {price} dollars.")
        self._balance -= price
        print(f"You now have {self._balance} dollars remaining.")
        parking_lot.empty_spots(self._ticket)

        
class ParkingTicket:
    def __init__(self, level, begin_spot, end_spot, check_in):
        self._level = level
        self._begin_spot = begin_spot
        self._end_spot = end_spot
        self._check_in = check_in

    def get_level(self):
        return self._level

    def get_begin_spot(self):
        return self._begin_spot
    
    def get_end_spot(self):
        return self._end_spot
    
    def get_check_in(self):
        return self._check_in

    def set_level(self, level):
        self._level = level

    def print(self):
        print(f"Your assigned level is {self.get_level()} from spots {self.get_begin_spot()} to {self.get_end_spot}")
        print(f"You checked in at {self._check_in}.\n")

class ParkingFloor:
    def __init__(self, spots):
        self._spots = [None] * spots
    
    def assign(self, vehicle, check_in):
        vehicle_size = vehicle.get_size()
        for i in range(len(self._spots) - vehicle_size + 1):
            for j in range(i, i + vehicle_size):
                if self._spots[j] is not None:
                    break
                if j == i + vehicle_size - 1:
                    for k in range(i, i + vehicle_size):
                        self._spots[k] = vehicle
                    return ParkingTicket(None, i, j, check_in)

    def empty_spots(self, begin_spot, end_spot):
        for spot in range(begin_spot, end_spot + 1):
            self._spots[spot] = None
    
    def print_floor(self):
        res = ""
        for i, vehicle in enumerate(self._spots):
            if vehicle:
                res = res + f"{i}: {vehicle.get_license_plate()} "
            else:
                res = res + f"{i}: Empty "
        print(res)


class ParkingLot:
    def __init__(self, levels, spots, rate):
        self._levels = [ParkingFloor(spots) for _ in range(levels)]
        self._rate = rate
        self._vehicles = {}
    
    def get_rate(self):
        return self._rate

    def get_vehicles(self):
        return self._vehicles

    def add_vehicle(self, vehicle):
        self._vehicle[vehicle] = []
    
    def assign(self, vehicle, check_in):
        for level, floor in enumerate(self._levels):
            ticket = floor.assign(vehicle, check_in)
            if ticket:
                ticket.set_level(level)
                return ticket

    def empty_spots(self, ticket):
        level = ticket.get_level()
        begin_spot = ticket.get_begin_spot()
        end_spot = ticket.get_end_spot()
        self._levels[level].empty_spots(begin_spot, end_spot)
    
    def print_lot(self):
        for level in self._levels:
            level.print_floor()
        print("")



parking_lot = ParkingLot(1, 2, 10)

suv = Car("HI5")
cade = Driver(suv, 100)

limo = Limo("FAKER8")
faker = Driver(limo, 50)

cade.park(parking_lot, 3)
faker.park(parking_lot, 4)
parking_lot.print_lot()

cade.check_out(parking_lot, 5)
faker.park(parking_lot, 6)
parking_lot.print_lot()