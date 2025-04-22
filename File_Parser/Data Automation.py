import pandas as pd
import matplotlib.pyplot as plt
import moviepy
from tabulate import tabulate
import csv

file_name = str(input('Input the filename: '))
file = pd.read_csv(file_name, sep = '\t', skiprows = [1,2])

s = 'Input the Offset for ' + file_name + ' in seconds: '
offset = int(input(s))
file_offset = offset * 500
print('Offset: ',round(offset,2))
print('File Offset: ', round(file_offset,3))

time_lst = []
for i in range(len(file)):
    time_lst.append((i / 500) - offset)
file['Time'] = time_lst


new_file = file[file_offset:]

x = new_file['Time']
longitudinal_force = new_file['LR_Fx']
lateral_force = new_file['LR_Fy']
vertical_force = new_file['LR_Fz']
camber_moment = new_file['LR_Mx']
wheel_torque = new_file['LR_My']
steer_torque = new_file['LR_Mz']
wheel_speed = new_file['LR_Wheel Speed']
wheel_position = new_file['LR_Position']
longitudinal_acceleration = new_file['LR_Ax']
vertical_acceleration = new_file['LR_Az']


# Extract the indices of the maximum values
index_Fx = longitudinal_force.idxmax()
index_Fy = lateral_force.idxmax()
index_Fz = vertical_force.idxmax()
index_Mx = camber_moment.idxmax()
index_My = wheel_torque.idxmax()
index_Mz = steer_torque.idxmax()
index_Ax = longitudinal_acceleration.idxmax()
index_Az = vertical_acceleration.idxmax()
index_Ws = wheel_speed.idxmax()

max_indices = [index_Fx, index_Fy, index_Fz, index_Mx, index_My, index_Mz, index_Ax, index_Az, index_Ws]
final_data = []
row_headers = ["Fx", "Fy", "Fz", "Mx", "My", "Mz", "Ax", "Az", "Ws"]
count = 0


for i in max_indices:
    max_rows= [row_headers[count],
               new_file['Time'][i],
               round(new_file['LR_Fx'][i]),
               round(new_file['LR_Fy'][i]),
               round(new_file['LR_Fz'][i]),
               round(new_file['LR_Mx'][i]),
               round(new_file['LR_My'][i]),
               round(new_file['LR_Mz'][i]),
               round(new_file['LR_Ax'][i]),
               round(new_file['LR_Az'][i]),
               round(new_file['LR_Wheel Speed'][i]),
               round(new_file['LR_Position'][i])
               ]
    final_data.append(max_rows)
    count += 1


headers = ["Time", "Fx", "Fy", "Fz", "Mx", "My", "Mz", "Ax", "Az", "Ws", "Wp"]

formatted_table = tabulate(final_data, headers=headers, tablefmt="plain")

lines = formatted_table.split("\n")
dash_row = "-" * len(lines[0])
lines.insert(1, dash_row)

print("\n".join(lines))


final_data.insert(0, ["Maximum Loads","Timestamp (sec)", "Fx", "Fy", "Fz", "Mx", "My", "Mz", "Ax", "Az", "Ws", "Wp"])


#output to an excel sheet test 1

# Specify the file name
output_filename = 'output.csv'

# Writing to csv file
with open(output_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

print(f"Data has been written to {output_filename}")





"""
choice = str(input('How would you like to view the data? \n A) Separate graphs for each data set. \n B) One graph with all the data. \n Q) Quit. \n'))
while choice != 'q' and choice != 'Q':

    if choice == 'a' or choice == 'A':

        plt.figure(figsize = (10,10))
        plt.suptitle(file_name)
        plt.subplot(5,2,1)
        plt.title('Longitudinal Force')
        plt.plot(x, longitudinal_force, 'red', label = 'Longitudinal Force')
        plt.grid(True)
        plt.subplot(5,2,2)
        plt.title('Lateral Force')
        plt.plot(x, lateral_force, 'orange',  label = 'Lateral Force')
        plt.grid(True)
        plt.subplot(5,2,3)
        plt.title('Vertical Force')
        plt.plot(x, vertical_force, 'gray', label = 'Vertical Force')
        plt.grid(True)
        plt.subplot(5,2,4)
        plt.title('Camber Moment')
        plt.plot(x, camber_moment, 'green', label = 'Camber Moment')
        plt.grid(True)
        plt.subplot(5,2,5)
        plt.title('Wheel Torque')
        plt.plot(x, wheel_torque, 'blue', label = 'Wheel Torque')
        plt.grid(True)
        plt.subplot(5,2,6)
        plt.title('Steer Torque')
        plt.plot(x, steer_torque, 'purple', label = 'Steer Torque')
        plt.grid(True)
        plt.subplot(5,2,7)
        plt.title('Wheel Speed')
        plt.plot(x, wheel_speed, 'black', label = "Wheel Speed")
        plt.grid(True)
        plt.subplot(5,2,8)
        plt.title('Wheel Position')
        plt.plot(x, wheel_position, 'pink', label = 'Wheel Position')
        plt.grid(True)
        plt.subplot(5,2,9)
        plt.title("Longitudinal Acceleration")
        plt.plot(x, longitudinal_acceleration, 'cyan', label = 'Longitudinal Acceleration')
        plt.grid(True)
        plt.subplot(5,2,10)
        plt.title("Vertical Acceleration")
        plt.plot(x, vertical_acceleration, 'brown', label = 'Vertical Acceleration')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    elif choice == 'b' or choice == 'B':
        plt.figure(figsize = (10, 10))
        plt.title(file_name)
        plt.plot(x, longitudinal_force, 'red', label = 'Longitudinal Force')
        plt.plot(x, lateral_force, 'orange',  label = 'Lateral Force')
        plt.plot(x, vertical_force, 'gray', label = 'Vertical Force')
        plt.plot(x, camber_moment, 'green', label = 'Camber Moment')
        plt.plot(x, wheel_torque, 'blue', label = 'Wheel Torque')
        plt.plot(x, steer_torque, 'purple', label = 'Steer Torque')
        plt.plot(x, wheel_speed, 'black', label = "Wheel Speed")
        plt.plot(x, wheel_position, 'pink', label = 'Wheel Position')
        plt.plot(x, longitudinal_acceleration, 'cyan', label = 'Longitudinal Acceleration')
        plt.plot(x, vertical_acceleration, 'brown', label = 'Vertical Acceleration')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    choice = input('How would you like to view the data? \n A) Subplot full of graphs for each data set. \n B) One graph with all the data overlapped. \n Q) Quit. \n')
"""