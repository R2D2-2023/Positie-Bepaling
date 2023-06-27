import matplotlib.pyplot as plt
import numpy as np

waardes = {
    100: {'meetafstand': 100, 'lidar meting': 100},
    200: {'meetafstand': 200, 'lidar meting': 200},
    300: {'meetafstand': 300, 'lidar meting': 303},
    400: {'meetafstand': 400, 'lidar meting': 407}
}

x = []
y_meting = []
y_afwijking = []

for afstand in waardes:
    x.append(afstand)
    y_meting.append(waardes[afstand]['meetafstand'])
    y_afwijking.append(waardes[afstand]['lidar meting'])

bar_width = 0.4

bar_positions = np.arange(len(x))

plt.bar(bar_positions, y_meting, label='Meetafstand', color='b', width=bar_width, alpha=0.7)
plt.bar(bar_positions + bar_width, y_afwijking, label='lidar meting', color='r', width=bar_width, alpha=0.7)
plt.xticks(bar_positions + bar_width/2, x)
plt.xlabel('Meetafstand (cm)')
plt.ylabel('Waarde (cm)')
plt.title('Lidar metingen (in cm)')
plt.legend()

for i, (xpos, ypos) in enumerate(zip(bar_positions, y_meting)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')

for i, (xpos, ypos) in enumerate(zip(bar_positions + bar_width, y_afwijking)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')

plt.show()
