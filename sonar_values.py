import matplotlib.pyplot as plt
import numpy as np

# Gegeven waardes
waardes = {
    10: {'meetafstand': 10, 'sonar meting': 13},
    20: {'meetafstand': 20, 'sonar meting': 23},
    30: {'meetafstand': 30, 'sonar meting': 33},
    40: {'meetafstand': 40, 'sonar meting': 43},
    50: {'meetafstand': 50, 'sonar meting': 56},
    100: {'meetafstand': 100, 'sonar meting': 115},
    150: {'meetafstand': 150, 'sonar meting': 175},
    200: {'meetafstand': 200, 'sonar meting': 218},
    375: {'meetafstand': 375, 'sonar meting': 443},
    400: {'meetafstand': 400, 'sonar meting': 477},
}

# X- en Y-coördinaten voor de plot
x = []
y_meting = []
y_afwijking = []

# Verzamel de gegevens voor de plot
for afstand in waardes:
    x.append(afstand)
    y_meting.append(waardes[afstand]['meetafstand'])
    y_afwijking.append(waardes[afstand]['sonar meting'])

# Breedte van de balken
bar_width = 0.4
bar_positions = np.arange(len(x))

# Maak de plot
plt.bar(bar_positions, y_meting, label='meetafstand', color='b', width=bar_width, alpha=0.7)
plt.bar(bar_positions+ bar_width, y_afwijking, label='sonar meting', color='r', width=bar_width, alpha=0.7)
plt.xlabel('Meetafstand (cm)')
plt.ylabel('Waarde (cm)')
plt.title('Sonar resultaten')
plt.xticks(bar_positions + bar_width/2, x)
plt.legend()

# Dikkere balken
for rect in plt.gca().patches:
    rect.set_linewidth(1.5)

for i, (xpos, ypos) in enumerate(zip(bar_positions, y_meting)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')

for i, (xpos, ypos) in enumerate(zip(bar_positions + bar_width, y_afwijking)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')

# Display the plot
plt.show()
