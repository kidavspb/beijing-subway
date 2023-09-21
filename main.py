import random
from matplotlib import pyplot as plt
import numpy as np


def hat_graph(ax, xlabels, values, group_labels):
    def label_bars(heights, rects):
        """Attach a text label on top of each bar."""
        for height, rect in zip(heights, rects):
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),  # 4 points vertical offset.
                        textcoords='offset points',
                        ha='center', va='bottom')

    values = np.asarray(values)
    x = np.arange(values.shape[1])
    ax.set_xticks(x, labels=xlabels)
    spacing = 0.3  # spacing between hat groups
    width = (1 - spacing) / values.shape[0]
    heights0 = values[0]
    for i, (heights, group_label) in enumerate(zip(values, group_labels)):
        style = {'fill': False} if i == 0 else {'edgecolor': 'black'}
        rects = ax.bar(x - spacing / 2 + i * width, heights - heights0,
                       width, bottom=heights0, label=group_label, **style)
        label_bars(heights, rects)

def draw(num_of_stations, enters, exits):
    fig, ax = plt.subplots()
    hat_graph(ax, [i for i in range(0, num_of_stations)], [enters, exits], ['Enter', 'Exit'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Поездки')
    ax.set_ylabel('Станции')
    ax.set_ylim(0, num_of_stations)
    ax.set_title('Симуляция поездок в пекинском метро')
    ax.legend()

    fig.tight_layout()
    plt.show()

def find_optimal(i, enters, exits, take_from):
    found_min_length = abs(exits[i] - enters[i])  # по умолчанию минимальное расстояние - свое
    found_min_index = i

    for j in range(len(enters)):
        current_length = abs(exits[i] - enters[j])  # ищем, у кого был ближайший вход
        if current_length < found_min_length and j not in take_from:
            found_min_length = current_length
            found_min_index = j
    return found_min_index

def check(take_from):
    for i in range(len(take_from)):
        if take_from[i] == -1:
            return False
        if i not in take_from:
            return False
    return True


if __name__ == '__main__':
    x = num_of_stations = 10

    enters = []
    exits = []

    for i in range(x):
        enter_station = exit_station = 0
        while enter_station == exit_station:
            enter_station = random.randint(0, num_of_stations)
            exit_station = random.randint(0, num_of_stations)
        enters.append(enter_station)
        exits.append(exit_station)

    draw(num_of_stations, enters, exits)

    take_from = [-1 for _ in range(len(enters))]
    while -1 in take_from:
        i = take_from.index(-1)
        found_index = find_optimal(i, enters, exits, take_from)
        if found_index in take_from:
            repeat_index = take_from.index(found_index)
            take_from[repeat_index] = -1

        take_from[i] = found_index

    print("Suitable exits:")
    for i in range(len(take_from)):
        print(f"{i} - {take_from[i]}")

    print("Is it correct? - " + ("✅" if check(take_from) else "❌"))