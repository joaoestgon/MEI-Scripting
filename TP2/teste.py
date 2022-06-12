import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered 
# and plotted counter-clockwise:
labels = 'A', 'B', 'C', 'D', 'E', 'F'
sizes = [15, 20, 10, 17, 1, 37]

# Illustration 1
distance = 0.2
separate = (distance, distance, distance, distance, distance, distance)
plt.figure()
plt.pie(sizes, labels=labels, explode=separate, autopct='%1.1f%%')
# Equal aspect ratio ensures that 
# pie is drawn as a circle.
plt.axis('equal')  
plt.title('saperation diatance = 0.4')
plt.show()