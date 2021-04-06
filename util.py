import pandas as pd
import csv
import json
import itertools
from collections import defaultdict


def format_and_write_state_data(state_data):
    for state_list in state_data:
        prev_tuple = (0, "idle")
        time = 0
        #if current time is not in state_list then add new tuple with current time and last known state (fill up)
        for tuple in state_list:
            if time != tuple[0]:
                state_list.insert(time,(time,prev_tuple[1]))
            else: prev_tuple = tuple
            if time == len(state_list):
                break
            time += 1

    # merge to one list
    state_data = list(itertools.chain.from_iterable(state_data))

    # group by timestamp
    mapp = defaultdict(list)
    for key, val in state_data:
        mapp[key].append(val)
    state_data = [(key, *val) for key, val in mapp.items()]

    with open("data/state_log.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["ts","warehouse","cell1","cell2","warehouse2"])
        for row in state_data:
                wr.writerow(row)

def format_and_write_event_data(event_data):
    event_log = pd.DataFrame(columns = ["timestamp","case", "event","asset"])

    for key in event_data:
        for assetEvent in event_data[key]:
            timestamp = event_data[key][assetEvent]
            asset = assetEvent.split("_")[0]
            event = assetEvent.split("_")[1]
            case = "case_" + key.split("_")[1]
            event_log.loc[len(event_log.index)] = [timestamp, case, event, asset] 
    event_log = event_log.sort_values('timestamp')
    event_log.to_csv("data/event_log.csv")

def write_event_data_json(data):
    with open('data/event_log.json', 'w') as fp:
        json.dump(data, fp)