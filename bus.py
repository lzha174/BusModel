
import math

import pandas
import simpy
import collections
import random
fly_seg = collections.namedtuple('flyseg', 'bus segId')
busStopDict = {1: 'Oruamo Domain', 2: 'Roberts Road', 3: 'Coronation Road', 4: 'McDowell Crescent',
               5:'Coroglen Avenue', 6:'Pupuke Road', 7:'Waratah Street', 8:'Birkenhead Avenue', 9:'Aorangi Place',
               10:'Park Avenue', 11:'Onewa Road', 12:'St Mary Catholic Church', 13:'Northcote Primary School', 14:'Bruce Street',15:'Fanshawe Street'}
busNameToId = {value: key for key, value in busStopDict.items()}
flyTime = {}

class Busstation:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __hash__(self):
        return self.id
    def __str__(self):
        return f'{self.name}'
    def __repr__(self):
        return self.__str__()

class Route:

    def __init__(self, id, flySequence: list[int]):
        self.id = id
        self.busStopSequence = flySequence

    def __str__(self):
        return f'route  {self.id}  {[busStopDict[i] for i in self.busStopSequence]}'
    def __repr__(self):
        return self.__str__()

class Bus:
    def __init__(self, id, route: Route, startTime: int):
        self.id = id
        self.route = route
        self.startTime = startTime
    def __str__(self):
        return f'airplne {self.id} fly {self.route}'
    def __repr__(self):
        return self.__str__()
    def get_depart_time(self):
        return self.startTime

class Passanger:
    def __init__(self, id, busId, departBusStop, arriveBusStop, timeAtStop):
        self.id = id
        self.busId = busId
        self.departBusStop = departBusStop
        self.arriveBusStop = arriveBusStop
        self.timeAtStop = timeAtStop
        self.on_bus = 0
        self.leave_bus = 0
        self.busId = 0
    def __str__(self):
        return f'passange {self.id} fly from  {busStopDict[self.departBusStop]} to {busStopDict[self.arriveBusStop]}'
    def __repr__(self):
        return self.__str__()

    def set_on_bus(self, onBusTime:int, butId: int):
        self.on_bus = onBusTime
        self.busId = butId

    def set_leave_bus(self, leaveBusTime:int):
        self.leave_bus = leaveBusTime

    def get_on_bus(self):
        return self.on_bus

class BusTime:
    def __init__(self, departureId, arriveId, departTime, duration):
        self.departureId = departureId
        self.arriveId = arriveId
        self.duration = duration
        self.departureTime = departTime


def travel_time(start, finish):
    # uniform travel time
    sorted_start = min(start, finish)
    sorted_finish = max(start, finish)
    travel_dict = {(1,2): 4, (1,3): 3, (2,3): 5, (1,4): 9, (2,4): 3, (3,4): 2}
    isPeak = random.choices([True, False], weights=[0.25, 0.75], k=1)[0]
    isPeak = True
    if isPeak:
        # 5min -> 5s -> 500 ms
        return 500 * (finish - start)
        return int(travel_dict[sorted_start, sorted_finish] * (1+ random.uniform(0,1)))
    else:
        # 5min -> 5s -> 5000 ms
        return 500* (finish - start)
        return travel_dict[sorted_start, sorted_finish]




def get_next_arrive_time():
    # time is in sec unit, covert to millonsec
    rate_per_sec = 10
    while True:
        x = random.expovariate(rate_per_sec) * 4000
        yield math.ceil(x)

def generatePassangers():
    passangers: list[Passanger] = []
    gen = get_next_arrive_time()

    for stop in list(busStopDict.keys()):
        if stop == 15: continue
        start = 0
        for i in range(120):
            startStop = stop
            endStop = random.randint(startStop + 1, 15)
            print(f'start stop {startStop} end stop {endStop}')
            x = next(gen)
            start += x
            print(f'next arrival at time {start} millionsec')
            p = Passanger(id=len(passangers), busId=0, departBusStop=startStop, arriveBusStop=endStop, timeAtStop=start)
            passangers.append(p)
    return passangers

def define_bus_table(bus: Bus):
    flyTime[bus.id] = []
    totalDurationBeforeThisStop = 0
    for idx, stationId in enumerate(bus.route.busStopSequence):
        if (idx == len(bus.route.busStopSequence) - 1):
            break
        travelTime = travel_time(stationId, bus.route.busStopSequence[idx + 1])

        departTime = bus.get_depart_time()
        if idx > 0:
            departTime += totalDurationBeforeThisStop

        flyTime[bus.id].append(
            BusTime(departureId=stationId, arriveId=bus.route.busStopSequence[idx + 1], departTime=departTime,
                    duration=travelTime))
        totalDurationBeforeThisStop += travelTime


def generateBuses():
    # run bus every 10 mins- > 10s -> 10000 millonsec
    step = 5000
    start = 0
    buses: list[Bus] = []
    stops = sorted(busStopDict.keys())
    for i in range(10):
        bus = Bus(id=len(buses), route=Route(len(buses), stops), startTime=start)
        define_bus_table(bus)
        start += step
        buses.append(bus)
    return buses

passangers = generatePassangers()
buses = generateBuses()


class BusSimulation:
    def __init__(self, buses: list[Bus], passangers:list[Passanger]):
        self.env  = simpy.Environment()
        self.buses: list[Bus] = buses
        self.passangers: list[Passanger] = passangers
        self.busReadyAtDepartureEvent = {}
        self.busDepartureEvent: dict[(int, int), simpy.Event] = {}
        self.busLandEvent = {}
        for busIdx, bus in enumerate(self.buses):
            for idx, busStopId in enumerate(bus.route.busStopSequence):
                if idx < len(bus.route.busStopSequence) - 1:
                    self.busDepartureEvent[bus.id, busStopId] = self.env.event()
                if idx > 0:
                    self.busLandEvent[bus.id, busStopId] = self.env.event()
            self.env.process(self.busRunSim(busIdx))

        for idx, passanger in enumerate(self.passangers):
            self.env.process(self.passangerSim(idx))


    def runAirSim(self):
        self.env.run()

    def passangerSim(self, idx):
        yield self.env.timeout(self.passangers[idx].timeAtStop)

        # passanger can wait for any plane he can catch

        successOnBus = False
        busLeft = []
        busTaken: Bus = None
        leaveAngry = self.env.timeout(100 * 1000, value='leave')
        while not successOnBus:

            waitForBuses = []

            for bus in self.buses:
                # this bus already left the waiting stop, wait for next bus
                if bus in busLeft: continue
                try:
                    departIndx =  bus.route.busStopSequence.index(self.passangers[idx].departBusStop)
                    arriveIdx = bus.route.busStopSequence.index(self.passangers[idx].arriveBusStop)
                    if departIndx < arriveIdx:
                        waitForBuses.append(self.busDepartureEvent[bus.id, self.passangers[idx].departBusStop])
                except ValueError:
                    continue
            if len(waitForBuses) == 0:
                print(f'no bus for me {idx}')
                return
            result = yield self.env.any_of(waitForBuses) | leaveAngry
            if leaveAngry in result:
                print(f'passanger {idx} leave angry')
                return
            print(f' time is {self.env.now}')
            for key, value in result.items():
                flyInfo: fly_seg = value
                bus = flyInfo.bus
                segInfo : BusTime = flyTime[bus.id][flyInfo.segId]
                departTime = segInfo.departureTime
                if departTime < self.env.now:
                    print(f'bus {bus.id} already left')
                    busLeft.append(bus)
                else:
                    successOnBus = True
                    busTaken = bus
                    break
            if successOnBus:
                break

        #yield self.airplaneDepartureEvent[airplaneId, self.passangers[idx].departAir]
        print(f'passanger {idx} ready to on borad of bus {busTaken.id} at {self.env.now} at {busStopDict[self.passangers[idx].departBusStop]}')
        self.passangers[idx].set_on_bus(self.env.now, busTaken.id)
        yield  self.busLandEvent[busTaken.id, self.passangers[idx].arriveBusStop]
        print(f'passanger {idx} ready to leave of bus {busTaken.id} at {self.env.now} at {busStopDict[self.passangers[idx].arriveBusStop]}')
        self.passangers[idx].set_leave_bus(self.env.now)

    def busRunSim(self, busIdx):
        bus = self.buses[busIdx]
        yield self.env.timeout(bus.get_depart_time())
        busStopSequence = self.buses[busIdx].route.busStopSequence
        for idx, location in enumerate(busStopSequence):

            if idx < len(busStopSequence) - 1:
                flyTimeData = flyTime[busIdx][idx]

                if self.busDepartureEvent.get(bus.id, location) is not None:
                    self.busDepartureEvent[bus.id, location].succeed(fly_seg(bus=bus, segId=idx))

                print(f'bus {busIdx} time to fly at {self.env.now} at {busStopDict[flyTimeData.departureId]}')
                yield self.env.timeout(flyTimeData.duration)
                print(f'bus {busIdx} arrive at {busStopDict[flyTimeData.arriveId]} at time {self.env.now}')

                if self.busLandEvent.get(bus.id, flyTimeData.arriveId) is not None:
                    self.busLandEvent[bus.id, flyTimeData.arriveId].succeed()


sim = BusSimulation(buses=buses, passangers=passangers)
sim.runAirSim()



for id, busTimes in flyTime.items():
    for busSegTime in busTimes:
        busSegTime: BusTime = busSegTime
        print(f'bus {id} leave from {busStopDict[busSegTime.departureId]} '
              f'at {busSegTime.departureTime} to {busStopDict[busSegTime.arriveId]} with {busSegTime.duration} seconds')
pData = []
for p in passangers:
    print(f'{p.id} on bus {p.busId} at time {p.get_on_bus()} from stop {busStopDict[p.departBusStop]} '
          f' wait at {p.timeAtStop} to {busStopDict[p.arriveBusStop]} arrive at time {p.leave_bus} ')
    pData.append([p.id, busStopDict[p.departBusStop], busStopDict[p.arriveBusStop], p.timeAtStop, p.get_on_bus()])

pLog = pandas.DataFrame(pData, columns = ['id', 'start', 'dest', 'show time', 'on bus'])
pLog.to_csv('passangers.csv', index=False)

import matplotlib.pyplot as plt
def plot_bus_table(buses: list[Bus], passengers:list[Passanger] = []):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    stops = list(busStopDict.values())
    #print(stops)
    yLabelPosition = [s * 10 for s in range(len(stops))]
    #print(yLabelPosition)
    xLabelPosition = [i for i in range(20)]
    #print(xLabelPosition)

    for bus in buses:
        x = []
        y = []
        for idx, busSegTime in enumerate(flyTime[bus.id]):
            busSegTime: BusTime = busSegTime
            #print(f'bus {bus.id} leave from {busStopDict[busSegTime.departureId]} '
            #      f'at {busSegTime.departureTime} to {busStopDict[busSegTime.arriveId]} with {busSegTime.duration} seconds')
            x.append(busSegTime.departureTime)
            #x.append(busSegTime.departureTime + busSegTime.duration)
            y.append(yLabelPosition[(busSegTime.departureId - 1)])
            #y.append(yLabelPosition[(busSegTime.arriveId - 1)])
            if idx == len(flyTime[bus.id]) - 1:
                x.append(busSegTime.departureTime + busSegTime.duration)
                y.append(yLabelPosition[(busSegTime.arriveId - 1)])

            #print(x,y)
        ax.plot(x, y, marker='o', label=f'bus {bus.id}')
    plt.xticks(xLabelPosition)
    plt.xlabel('Time')

    ax.set_yticks(yLabelPosition)
    ax.set_yticklabels(stops)

    if False:
        no_of_colors = 5
        colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
                 for j in range(no_of_colors)]

        for passanger in passengers:
            x = []
            y = []
            x.append(passanger.timeAtStop)
            y.append(yLabelPosition[passanger.departBusStop - 1])
            ax.plot(x, y, marker='o', color=colors[passanger.id], label=f'passanger {passanger.id}')

    plt.legend()
    plt.show()

#plot_bus_table(buses, passangers)