import matplotlib.pyplot as plt
import numpy as np

# Gegeven waardes
waardes = {
    90: {'meetafstand': 90, 'rechts': 89, 'links': 88},
    180: {'meetafstand': 180, 'rechts': 177, 'links': 183},
    270: {'meetafstand': 270, 'rechts': 267, 'links': 271}
}

# X- en Y-coördinaten voor de plot
x = []
y_rechts = []
y_links = []

# Verzamel de gegevens voor de plot
for hoek in waardes:
    x.append(hoek)
    y_rechts.append(waardes[hoek]['rechts'])
    y_links.append(waardes[hoek]['links'])

# Breedte en positie van de balken
bar_width = 0.2
bar_positions = np.arange(len(x))

# Maak de plot
plt.bar(bar_positions, y_rechts, width=bar_width, label='Rechtsom gemeten', color='blue')
plt.bar(bar_positions + bar_width, x, width=bar_width, label='Originele waarde', color='green')
plt.bar(bar_positions + bar_width + bar_width, y_links, width=bar_width, label='Linksom gemeten', color='red')
plt.xlabel('Hoek (graden)')
plt.ylabel('Gemeten waarde')
plt.title('Metingen van hoeken (linksom en rechtsom)')
plt.xticks(bar_positions + bar_width/3, x)
plt.legend()

for i, (xpos, ypos) in enumerate(zip(bar_positions, y_rechts)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')
    
for i, (xpos, ypos) in enumerate(zip(bar_positions + bar_width, x)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')

for i, (xpos, ypos) in enumerate(zip(bar_positions + bar_width + bar_width, y_links)):
    plt.text(xpos, ypos, str(ypos), ha='center', va='bottom', color='black')

# Display the plot
plt.show()
