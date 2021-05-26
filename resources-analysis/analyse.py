import pandas as pd
import numpy as np
import json
import re
import sys
import math
import matplotlib.pyplot as plt

servers = [
    { 'name': 'nginx', 'pod': 'wordpress-nginx' },
    { 'name': 'apache', 'pod': 'wp-apache' }
]

def get_data_series(filepath):
    df = pd.read_json(filepath)
    df['pod'] = df['pod'].apply(lambda x: re.match(r'^(\w+-\w+)-.*', x).groups()[0])
    group_series = df.groupby(['timestamp', 'pod'])['cpu', 'memory'].sum()

    pods = np.array([x[1] for x in group_series.index])

    data_series = {}
    for server in servers:
        ids = np.where(pods == server['pod'])[0]
        data_series[server['name']] = {}
        for type in ['cpu', 'memory']:
            data_series[server['name']][type] = list(group_series[type][ids])

        timestamps = [t[0] for t in group_series['cpu'][ids].index]
        dt = math.floor((timestamps[1] - timestamps[0]).total_seconds())
        data_series[server['name']]['seconds'] = [i * dt for i in range(len(timestamps))]
    return data_series

def get_data_series_new(filepath):
    df = pd.read_json(filepath)
    df['pod'] = df['pod'].apply(lambda x: re.match(r'^(\w+)-.*', x).groups()[0])
    group_series = df.groupby(['timestamp', 'pod'])['cpu', 'memory'].sum()

    pods = np.array([x[1] for x in group_series.index])

    data_series = {}
    data_series['cpu'] = list(group_series['cpu'] * 100)
    data_series['memory'] = list(group_series['memory'])

    timestamps = [t[0] for t in group_series['cpu'].index]
    dt = math.floor((timestamps[1] - timestamps[0]).total_seconds())
    data_series['seconds'] = [i * dt for i in range(len(timestamps))]

    return data_series

def plot_series(data_series, server_name, title_info, filepath=''):
    fig, ax = plt.subplots()
    l1 = ax.plot(data_series[server_name]['seconds'], data_series[server_name]['cpu'], label='CPU', color='red')
    ax.set_ylabel("CPU []", color='red')
    ax.set_xlabel('Time [s]')
    ax2 = ax.twinx()
    l2 = ax2.plot(data_series[server_name]['seconds'], data_series[server_name]['memory'], label='memory', color='blue')
    ax2.set_ylabel("Memory [Mb]", color="blue")


    lns = l1+l2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.set_title('Server: {} - {}'.format(server_name, title_info))
    # plt.show()
    if filepath != '':
        fig.savefig(filepath)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        raise Exception("No source")

    data_series = get_data_series(filepath)

    for server in servers:
        plot_series(data_series, server['name'], 'info', filepath.replace('json', '{}.png'.format(server['name'])))
    # plot_series(data_series, 'nginx', 'info', filepath.replace('json', '{}.png'.format('nginx')))



