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
    data_series['cpu'] = list(group_series['cpu'] * 100 / 4)
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


def plot_series_new(data_series, title, filepath=''):
    fig, ax = plt.subplots()
    l1 = ax.plot(data_series['seconds'], data_series['cpu'], label='CPU', color='red')
    ax.set_ylabel("CPU [%]", color='red')
    ax.set_xlabel('Time [s]')
    ax2 = ax.twinx()
    l2 = ax2.plot(data_series['seconds'], data_series['memory'], label='memory', color='blue')
    ax2.set_ylabel("Memory [Mb]", color="blue")


    lns = l1+l2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.set_title(title)
    plt.show()
    if filepath != '':
        fig.savefig(filepath)

def plot_multiple_series(files, title, resource_type='cpu', type='plain'):
    data_series = [get_data_series_new(f) for f in files]

    fig, ax = plt.subplots()
    # secs = data_series[0]['seconds']
    for i, d in enumerate(data_series):
        reres = re.match(r'.*\.(i\d\d)\..*', files[i])
        interval = reres.group(1)
        if 'deployment' in files[i]:
            label = 'Depl.-{}'.format(interval)
        else:
            label = 'Ingr.-{}'.format(interval)


        ax.plot(d['seconds'], d[resource_type], label=label)

    if type == 'plain':
        plt.axvline(x=1*60, c='grey')
        plt.axvline(x=8*60, c='grey')
    else:
        plt.axvline(x=7.5*60, c='grey')

    ax.legend(loc='best')

    ax.set_ylabel('CPU [%]' if resource_type == 'cpu' else 'Memory [MB]')
    ax.set_xlabel('Time [s]')
    ax.set_title(title)

    # plt.show()
    plt.savefig('results/{}_{}.png'.format(resource_type, type))

if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     filepath = sys.argv[1]
    # else:
    #     raise Exception("No source")

    # data_series = get_data_series_new(filepath)

    # plot_series_new(data_series, 'MTD Ingress (interval 60s, with requests load)', filepath.replace('json', 'png'))
    # plot_series(data_series, 'nginx', 'info', filepath.replace('json', '{}.png'.format('nginx')))

    files_no_req = [
        'results/mtd-deployment/resource-metrics.mtd-deployment.i15.no-req.0-mtd-0.2021.05.26.15.07.23.json',
        'results/mtd-deployment/resource-metrics.mtd-deployment.i30.no-req.0-mtd-0.2021.05.26.14.00.46.json',
        'results/mtd-deployment/resource-metrics.mtd-deployment.i60.no-req.0-mtd-0.2021.05.26.14.23.00.json',
        'results/mtd-ingress/resource-metrics.mtd-ingress.i15.no-req.0-mtd-0.2021.05.31.21.29.57.json',
        'results/mtd-ingress/resource-metrics.mtd-ingress.i30.no-req.0-mtd-0.2021.05.31.21.14.08.json',
        'results/mtd-ingress/resource-metrics.mtd-ingress.i60.no-req.0-mtd-0.2021.05.31.20.57.29.json',
    ]

    files_with_req = [
        'results/mtd-deployment/resource-metrics.mtd-deployment.i15.with-req.mtd.2021.05.26.18.06.59.json',
        'results/mtd-deployment/resource-metrics.mtd-deployment.i30.with-req.mtd.2021.05.26.16.19.17.json',
        'results/mtd-deployment/resource-metrics.mtd-deployment.i60.with-req.mtd.2021.05.26.15.42.17.json',
        'results/mtd-ingress/resource-metrics.mtd-ingress.i15.with-req.mtd.2021.05.31.22.35.19.json',
        'results/mtd-ingress/resource-metrics.mtd-ingress.i30.with-req.mtd.2021.05.31.22.08.24.json',
        'results/mtd-ingress/resource-metrics.mtd-ingress.i60.with-req.mtd.2021.05.31.21.50.32.json'
    ]
    # plot_multiple_series(files_no_req, '', resource_type='memory')
    plot_multiple_series(files_with_req, 'CPU usage for MTDs with load tests', resource_type='cpu', type='load')
    plot_multiple_series(files_with_req, 'Memory usage for MTDs with load tests', resource_type='memory', type='load')

    plot_multiple_series(files_no_req, 'CPU usage for plain MTDs', resource_type='cpu', type='plain')
    plot_multiple_series(files_no_req, 'Memory usage for plain MTDs', resource_type='memory', type='plain')



