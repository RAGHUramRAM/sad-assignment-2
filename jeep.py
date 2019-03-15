class Director:
    __builder = None
   
    def setBuilder(self, builder):
        self.__builder = builder
   
    def getCar(self):
        car = Car()
      
        # First goes the body
        body = self.__builder.getBody()
        car.setBody(body)
      
        # Then engine
        engine = self.__builder.getEngine()
        car.setEngine(engine)
      
        # And four wheels
        i = 0
        while i < 4:
            wheel = self.__builder.getWheel()
            car.attachWheel(wheel)
            i += 1
        return car

# The whole product
class Car:
    def __init__(self):
        self.__wheels = list()
        self.__engine = None
        self.__body = None

    def setBody(self, body):
        self.__body = body

    def attachWheel(self, wheel):
        self.__wheels.append(wheel)

    def setEngine(self, engine):
        self.__engine = engine

    def specification(self):
        print ("body: %s" % self.__body.shape)
        print ("engine horsepower: %d" % self.__engine.horsepower)
        print ("tire size: %d\'" % self.__wheels[0].size)

class Builder:
        def getWheel(self): pass
        def getEngine(self): pass
        def getBody(self): pass

class JeepBuilder(Builder):
   
    def getWheel(self):
        wheel = Wheel()
        wheel.size = 22
        return wheel
   
    def getEngine(self):
        engine = Engine()
        engine.horsepower = 400
        return engine
   
    def getBody(self):
        body = Body()
        body.shape = "SUV"
        return body

# Car parts
class Wheel:
    size = None

class Engine:
    horsepower = None

class Body:
    shape = None

class _IgnitionSystem(object):
    @staticmethod
    def produce_spark():
        return True
class _Engine(object):
    def __init__(self):
        self.revs_per_minute = 0
    def turnon(self):
        self.revs_per_minute = 2000
    def turnoff(self):
        self.revs_per_minute = 0
class _FuelTank(object):
    def __init__(self, level=30):
        self._level = level
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        self._level = level
class _DashBoardLight(object):

    def __init__(self, is_on=False):
        self._is_on = is_on

    def __str__(self):
        return self.__class__.__name__

    @property
    def is_on(self):
        return self._is_on
   
    @is_on.setter
    def is_on(self, status):
        self._is_on = status
    def status_check(self):
        if self._is_on:
            print("{}: ON".format(str(self)))
        else:
            print("{}: OFF".format(str(self)))

class _HandBrakeLight(_DashBoardLight):
    pass

class _FogLampLight(_DashBoardLight):
    pass

class _Dashboard(object):
   
   def __init__(self):
        self.lights = {"handbreak": _HandBrakeLight(), "fog": _FogLampLight()}
   
   def show(self):
        for light in self.lights.values():
            light.status_check()

# Facade
class Jeep(object):
   
    def __init__(self):
        self.ignition_system = _IgnitionSystem()
        self.engine = _Engine()
        self.fuel_tank = _FuelTank()
        self.dashboard = _Dashboard()
   
    @property
    def km_per_litre(self):
        return 17.0
   
    def consume_fuel(self, km):
        litres = min(self.fuel_tank.level, km / self.km_per_litre)
        self.fuel_tank.level -= litres
   
    def start(self):
        print("\nStarting...")
        self.dashboard.show()
        if self.ignition_system.produce_spark():
            self.engine.turnon()
        else:
            print("Can't start. Faulty ignition system")
   
    def has_enough_fuel(self, km, km_per_litre):
        litres_needed = km / km_per_litre
        if self.fuel_tank.level > litres_needed:
            return True
        else:
            return False
        
    def drive(self, km = 100):
        print("\n")
        if self.engine.revs_per_minute > 0:
            while self.has_enough_fuel(km, self.km_per_litre):
                self.consume_fuel(km)
                print("Drove {}km".format(km))
                print("{:.2f}l of fuel still left".format(self.fuel_tank.level))
        else:
            print("Can't drive. The Engine is turned off!")
         
    def park(self):
        print("\nParking...")
        self.dashboard.lights["handbreak"].is_on = True
        self.dashboard.show()
        self.engine.turnoff()
         
    def switch_fog_lights(self, status):
        print("\nSwitching {} fog lights...".format(status))
        boolean = True if status == "ON" else False
        self.dashboard.lights["fog"].is_on = boolean
        self.dashboard.show()
         
    def fill_up_tank(self):
        print("\nFuel tank filled up!")
        self.fuel_tank.level = 100

class Fuel:
        def __init__(self, name):
                self._observers = []
                self._name = name
                self._fill_up_tank= 0
 
        def attach(self, observer):
                if observer not in self._observers:
                        self._observers.append(observer)
        def detach(self, observer):
                try:
                        self._observers.remove(observer)
                except ValueError:
                        print("Observer is already not in the list of observers.")
        def notify(self):
                for observer in self._observers:
                        observer.update(self)
                 
        @property
        def fill_up_tank(self):
            print("\nFuel tank filled up!")
            return self.fuel_tank.level
 
        @fill_up_tank.setter
        def fill_up_tank(self, fill_up_tank):
                self._fill_up_tank = fill_up_tank
                self.notify()
                 
class TankMonitorCore:
        def update(self, subject):
                if subject._fill_up_tank < 10:
                    print("TankMonitorCore says: {} has fuel {:.2f}l. Code Red!!! fill up the tank".format(subject._name, subject._fill_up_tank))
                else:
                    print("TankMonitorCore says: {} has fuel {:.2f}l. fuel is sufficient.".format(subject._name, subject._fill_up_tank))
 
# Create a subject to be monitored
case = Fuel("Fuel Tank")
 
# Create observers
tankMonitorCase = TankMonitorCore()
 
# Attach the observers to the subject
case.attach(tankMonitorCase)
         
def main():
    jeepBuilder = JeepBuilder() # initializing the class
   
    director = Director()
   
    # Build Jeep
    print ("Jeep")
    director.setBuilder(jeepBuilder)
    jeep = director.getCar()
    jeep.specification()
    print ("")
    
    car = Jeep()
    car.start()
    car.drive()
    car.switch_fog_lights("ON")
    car.switch_fog_lights("OFF")
    car.park()
    car.fill_up_tank()
    car.drive()
    car.start()
    car.drive()
    case.fill_up_tank = car.fuel_tank.level

if __name__ == "__main__":
    main()

