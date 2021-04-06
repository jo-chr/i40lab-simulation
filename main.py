import simpy
import simpy.rt
import configparser
import util

config = configparser.ConfigParser()
config.read('config.ini')

state_data = [[],[],[],[]] #-->[["warehouse1"],["cell1"],["cell2"],["warehouse2"]]
event_data = {}

class Warehouse(object):
    def __init__(self, env, out_store):
        self.env = env
        self.out_store = out_store
        self.broken = False
        self.process = env.process(self.working())
        env.process(self.break_machine())

    def working(self):
        i = 0
        while True:
            try:
                state_data[0].append((env.now, "working"))
                event_data.update({f'token_{i}':{'WH1_prepareMaterialStart':env.now}})
                print('time ' + str(env.now) + '\t|\t Warehouse 1 \t|\t prepareMaterial')
                util.write_event_data_json(event_data)
                yield self.env.timeout(config.getint('ASSETS', 'warehouse1'))
                event_data[f'token_{i}']['WH1_prepareMaterialEnd'] = env.now
                state_data[0].append((env.now, "idle"))
                with mobile_robot.request() as req:
                    event_data[f'token_{i}']['AGV_transportToTrackStart'] = env.now
                    print('time ' + str(env.now) + '\t|\t AGV \t\t|\t transportToTrack')
                    util.write_event_data_json(event_data)
                    yield req
                    yield env.timeout(config.getint('ASSETS', 'AGV'))
                    event_data[f'token_{i}']['AGV_transportToTrackEnd'] = env.now
                    yield self.out_store.put(f'token_{i}')
                i += 1

            except simpy.Interrupt:
                        self.broken = True
                        state_data[0].append((env.now, "failed"))
                        event_data[f'token_{i}']['WH1_failure'] = env.now
                        print('time ' + str(env.now) + '\t|\t Warehouse 1 \t|\t broken')
                        yield self.out_store.put(f'token_{i}') #optional
                        yield self.env.timeout(config.getint('REPAIR', 'warehouse1'))
                        event_data[f'token_{i}']['WH1_repaired'] = env.now
                        print('time ' + str(env.now) + '\t|\t Warehouse 1 \t|\t repaired')
                        self.broken = False
                        i += 1
    
    def break_machine(self):
        while True:
            yield self.env.timeout(config.getint('BREAK', 'warehouse1'))
            if not self.broken:
                self.process.interrupt()
                

class Cell1(object):
    def __init__(self, env, in_store, out_store):
        self.env = env
        self.in_store = in_store
        self.out_store = out_store
        self.process = env.process(self.working())

    def working(self):
        processed_tokens = []
        while True:
            token = yield self.in_store.get(lambda item: item not in processed_tokens)
            with magnetic_track_discs.request() as req:
                event_data[token]['TRACK_transportToCell1Start'] = env.now
                print('time ' + str(env.now) + '\t|\t Track \t\t|\t transportToCell1')
                util.write_event_data_json(event_data)
                yield req
                yield env.timeout(config.getint('ASSETS', 'track'))
                event_data[token]['TRACK_transportToCell1End'] = env.now
            event_data[token]['CELL1_assemblyStart'] = env.now
            state_data[1].append((env.now, "working"))
            print('time ' + str(env.now) + '\t|\t Cell 1 \t|\t assembly')
            util.write_event_data_json(event_data)
            processed_tokens.append(token)
            yield self.env.timeout(config.getint('ASSETS', 'cell1'))
            event_data[token]['CELL1_assemblyEnd'] = env.now
            state_data[1].append((env.now, "idle"))
            yield self.out_store.put(token)


class Cell2(object):
    def __init__(self, env, in_store, out_store):
        self.env = env
        self.in_store = in_store
        self.out_store = out_store
        self.process = env.process(self.working())

    def working(self):
        processed_tokens = []
        while True:
            token = yield self.in_store.get(lambda item: item not in processed_tokens)
            with magnetic_track_discs.request() as req:
                event_data[token]['TRACK_transportToCell2Start'] = env.now
                print('time ' + str(env.now) + '\t|\t Track \t\t|\t transportToCell2')
                util.write_event_data_json(event_data)
                yield req
                yield env.timeout(config.getint('ASSETS', 'track'))
                event_data[token]['TRACK_transportToCell2End'] = env.now
            event_data[token]['CELL2_assemblyStart'] = env.now
            state_data[2].append((env.now, "working"))
            print('time ' + str(env.now) + '\t|\t Cell 2 \t|\t assembly')
            util.write_event_data_json(event_data)
            processed_tokens.append(token)
            yield self.env.timeout(config.getint('ASSETS', 'cell2'))
            event_data[token]['CELL2_assemblyEnd'] = env.now
            state_data[2].append((env.now, "idle"))
            yield self.out_store.put(token)

class Warehouse2(object):
    def __init__(self, env, in_store, out_store):
        self.env = env
        self.in_store = in_store
        self.out_store = out_store
        self.process = env.process(self.working())

    def working(self):
        processed_tokens = []
        while True:
            item = yield self.in_store.get(lambda item: item not in processed_tokens)
            state_data[3].append((env.now, "working"))
            event_data[item]['WH2_storeProductStart'] = env.now
            print('time ' + str(env.now) + '\t|\t Warehouse 2 \t|\t storeProduct')
            util.write_event_data_json(event_data)
            processed_tokens.append(item)
            yield self.env.timeout(config.getint('ASSETS', 'warehouse2'))
            event_data[item]['WH2_storeProductEnd'] = env.now
            state_data[3].append((env.now, "idle"))
            yield self.out_store.put(item)

if config.getboolean('SIMULATION', 'realtime'):
    env = simpy.rt.RealtimeEnvironment()
else: env = simpy.Environment()

token_wh_out = simpy.FilterStore(env)
token_cell1_out = simpy.FilterStore(env)
token_cell2_out = simpy.FilterStore(env)
token_wh2_out = simpy.FilterStore(env)

warehouse = Warehouse(env, out_store = token_wh_out)
cell1 = Cell1(env, in_store = token_wh_out, out_store = token_cell1_out)
cell2 = Cell2(env, in_store = token_cell1_out, out_store = token_cell2_out)
warehouse2 = Warehouse2(env, in_store = token_cell2_out, out_store = token_wh2_out)

mobile_robot = simpy.Resource(env, capacity=1)
magnetic_track_discs = simpy.Resource(env, capacity=3)

print(f'STARTING SIMULATION')
print(f'----------------------------------')

env.run(until = config.getint('SIMULATION', 'until'))

util.format_and_write_state_data(state_data)
util.format_and_write_event_data(event_data)
