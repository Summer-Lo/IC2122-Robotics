import time

labSim_button = 0
labSim_close_button = 0
task1_button = 0
task1_close_button = 0
task1c_button = 0
task1c_close_button = 0
task2_button = 0
task2_close_button = 0
task2c_button = 0
task2c_close_button = 0
task3_button = 0
task3_close_button = 0
task4a_button = 0
task4a_close_button = 0
task4b_button = 0
task4b_close_button = 0
task4c_button = 0
task4c_close_button = 0
ursim_button = 0
ursim_close_button = 0

def disableButton():
    labSim_button.disable()
    task1_button.disable()
    task1c_button.disable()
    task2_button.disable()
    task2c_button.disable()
    task3_button.disable()
    task4a_button.disable()
    task4b_button.disable()
    task4c_button.disable()
    ursim_button.disable()

def enableButton():
    labSim_button.enable()
    task1_button.enable()
    task1c_button.enable()
    task2_button.enable()
    task2c_button.enable()
    task3_button.enable()
    task4a_button.enable()
    task4b_button.enable()
    task4c_button.enable()
    ursim_button.enable()

def disableCloseButton():
    labSim_close_button.disable()
    task1_close_button.disable()
    task1c_close_button.disable()
    task2_close_button.disable()
    task2c_close_button.disable()
    task3_close_button.disable()
    task4a_close_button.disable()
    task4b_close_button.disable()
    task4c_close_button.disable()
    ursim_close_button.disable()

def enableCloseButton(order):
    time.sleep(5)
    if(order == 1):
        labSim_close_button.enable()
    elif(order == 2):
        task1_close_button.enable()
    elif(order == 3):
        task1c_close_button.enable()
    elif(order == 4):
        task2_close_button.enable()
    elif(order == 5):
        task2c_close_button.enable()
    elif(order == 6):
        task3_close_button.enable()
    elif(order == 7):
        task4a_close_button.enable()
    elif(order == 8):
        task4b_close_button.enable()
    elif(order == 9):
        task4c_close_button.enable()
    elif(order == 10):
        ursim_close_button.enable()
