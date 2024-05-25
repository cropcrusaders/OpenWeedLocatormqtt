import time
import platform

# check if the system is being tested on a Windows or Linux x86 64 bit machine
if platform.system() == "Windows":
    testing = True
else:
    if '64' in platform.machine():
        testing = True
    else:
        from gpiozero import Button, LED
        testing = False

class BasicController:
    def __init__(self, detection_state, stop_flag, board_pin='BOARD37', bounce_time=1.0):
        self.switch = Button(board_pin, bounce_time=bounce_time)

        self.detection_state = detection_state
        self.stop_flag = stop_flag

        self.switch.when_pressed = self.toggle_detection

    def toggle_detection(self):
        with self.detection_state.get_lock():
            self.detection_state.value = not self.detection_state.value

    def run(self):
        while not self.stop_flag.value:
            time.sleep(0.1)  # sleep to reduce CPU usage

    def stop(self):
        with self.stop_flag.get_lock():
            self.stop_flag.value = True


class SensitivitySelector:
    def __init__(self, switchDict: dict):
        self.switchDict = switchDict
        self.buttonList = []

        for sensitivityList, GPIOpin in self.switchDict.items():
            button = Button(f"BOARD{GPIOpin}")
            self.buttonList.append([button, sensitivityList])

    def sensitivity_selector(self):
        pass

# used with a physical dial to select the algorithm during initial validation.
# No longer used in the main greenonbrown.py file
class Selector:
    def __init__(self, switchDict: dict):
        self.switchDict = switchDict
        self.buttonList = []

        for algorithm, GPIOpin in self.switchDict.items():
            button = Button(f"BOARD{GPIOpin}")
            self.buttonList.append([button, algorithm])

    def algorithm_selector(self, algorithm):
        for button in self.buttonList:
            if button[0].is_pressed:
                if algorithm == button[1]:
                    return button[1], False

                return button[1], True

        return 'exg', False

# video recording button
class Recorder:
    def __init__(self, recordGPIO: int):
        self.record_button = Button(f"BOARD{recordGPIO}")
        self.record = False
        self.save_recording = False
        self.running = True
        self.led = LED(pin='BOARD38')

        self.record_button.when_pressed = self.start_recording
        self.record_button.when_released = self.stop_recording

    def button_check(self):
        while self.running:
            self.record_button.when_pressed = self.start_recording
            self.record_button.when_released = self.stop_recording
            time.sleep(1)

    def start_recording(self):
        self.record = True
        self.save_recording = False
        self.led.on()

    def stop_recording(self):
        self.save_recording = True
        self.record = False
        self.led.off()


