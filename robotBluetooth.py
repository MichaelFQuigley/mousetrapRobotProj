import thread
import serial
from tracker import cart2pol, pol2cart
from numpy import cos, pi, arctan, tan

FULL_POWER = 70
ATAN1 = arctan(1)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BTPeripheral:
    def __init__(self, btDeviceName='/dev/cu.HC-06-DevB', readTimeout=0.01):
        self.btDeviceName = btDeviceName
        self.serPort = None
        self.readTimeout = readTimeout
        if self.connect():
            print "Robot connected"
        else:
            print "Robot could not connect"

    # returns false on failure
    def connect(self):
        baudRate = 9600
        try:
            self.serPort = serial.Serial(self.btDeviceName, baudRate, timeout=self.readTimeout)
        except:
            return False
        return True

    def send(self, text):
        self.serPort.write(str(text))

    def close(self):
        self.serPort.close()

    def startListeningForRead(self, callback):
        thread.start_new_thread(self.readWorker, (callback,))

    # callback takes format callback(string)
    def readWorker(self, callback):
        while True:
            inStr = self.read()
            if len(inStr) > 0:
                callback(inStr)

    def read(self):
        resultStr = ""
        ch = self.serPort.read()
        while len(ch) > 0:
            resultStr += ch
            ch = self.serPort.read()
        return resultStr

    def follow_command(self, location, front, target):
        if location and front:
            bearing = cart2pol(front[0] - location[0], -(front[1] - location[1]))[1]
            while bearing < 0:
                bearing += pi * 2
            target_bearing = cart2pol(target[0] - location[0], -(target[1] - location[1]))[1]
            while target_bearing < 0:
                target_bearing += pi * 2
            angle = target_bearing - bearing
            if angle < -2.0 * pi:
                angle += 2.0 * pi
            if abs(angle) > pi:
                if angle > pi:
                    angle -= 2.0 * pi
                else:
                    angle += 2.0 * pi

            left_wheel, right_wheel = self._control_pivot(angle, FULL_POWER)

            print "bearing: {} rad {} deg".format(bearing, bearing * 180 / pi)
            print "target : {} rad {} deg".format(target_bearing, target_bearing * 180 / pi)
            print "angle  : {} rad {} deg".format(angle, angle * 180 / pi)
            print "sending power left, right  ({}, {})".format(left_wheel, right_wheel)
            self.send("{}, {}\n".format(left_wheel, right_wheel))

    def _control_power_over_circle(self, angle, max_power=FULL_POWER):
        power = max_power
        threshold_rad = pi / 2.0
        if abs(angle) > threshold_rad / 2.0:
            power = max_power * 0.65
        if abs(angle) > threshold_rad:
            return self._control_circular_with_spin(angle, power)
        else:
            return self._control_power(angle, power)

    def _control_power_over_linear(self, angle, max_power=FULL_POWER):
        power = max_power
        threshold_rad = pi / 2.0
        if abs(angle) > threshold_rad / 2.0:
            power = max_power * 0.65
        if abs(angle) > threshold_rad / 2.0:
            return self._control_linear_with_spin(angle, power)
        else:
            return self._control_power_over_circle(angle, power)

    def _control_power_over_pivot(self, angle, max_power=FULL_POWER):
        power = max_power
        threshold_rad = pi / 2.0
        if abs(angle) > threshold_rad / 2.0:
            power = max_power * 0.65
        if abs(angle) > threshold_rad / 2.0:
            return self._control_pivot(angle, power)
        else:
            return self._control_power_over_circle(angle, power)


    @staticmethod
    def _control_power(angle, max_power=FULL_POWER):
        left_wheel = max_power
        right_wheel = max_power
        if angle < 0:
            right_wheel = int(((pi / 2.0 + angle) ** 3) * max_power / (pi / 2.0))
        if angle > 0:
            left_wheel = int(((pi / 2.0 - angle) ** 3) * max_power / (pi / 2.0))
        return left_wheel, right_wheel

    @staticmethod
    def _control_pivot(angle, max_power=FULL_POWER):
        threshold_rad = pi / 14.0
        left_wheel = max_power
        right_wheel = max_power
        if angle > threshold_rad:
            left_wheel = -max_power
        if angle < -threshold_rad:
            right_wheel = -max_power
        return left_wheel, right_wheel

    # logic is wrong
    # @staticmethod
    # def _control_atan_with_spin(angle, max_power=FULL_POWER):
    #     left_wheel = max_power
    #     right_wheel = max_power
    #     if angle < 0:
    #         right_wheel = int((tan((1.0 + 2.0 * angle * ATAN1 / pi) ** 3)) * max_power / (pi / 2.0))
    #     if angle > 0:
    #         left_wheel = int((tan((1.0 - 2.0 * angle * ATAN1 / pi) ** 3)) * max_power / (pi / 2.0))
    #     return left_wheel, right_wheel

    @staticmethod
    def _control_linear_with_spin(angle, max_power=FULL_POWER):
        left_wheel = max_power
        right_wheel = max_power
        if angle < 0:
            right_wheel = int((pi / 2.0 + angle) * max_power / (pi / 2.0))
        if angle > 0:
            left_wheel = int((pi / 2.0 - angle) * max_power / (pi / 2.0))
        return left_wheel, right_wheel

    @staticmethod
    def _control_circular_with_spin(angle, max_power=FULL_POWER):
        left_wheel = max_power
        right_wheel = max_power
        if angle < 0:
            right_wheel = int(cos(-angle) * max_power)
        if angle > 0:
            left_wheel = int(cos(angle) * max_power)
        return left_wheel, right_wheel

    def _control_circular(self, angle, max_power=FULL_POWER):
        left_wheel, right_wheel = self._control_circular_with_spin(angle, max_power)
        return max(left_wheel, 0), max(right_wheel, 0)

    def _control_linear(self, angle, max_power=FULL_POWER):
        left_wheel, right_wheel = self._control_linear_with_spin(angle, max_power)
        return max(left_wheel, 0), max(right_wheel, 0)

    # def _control_atan(self, angle, max_power=FULL_POWER):
    #     left_wheel, right_wheel = self._control_atan_with_spin(angle, max_power)
    #     return max(left_wheel, 0), max(right_wheel, 0)

    def victory_dance(self):
        self.send(str(FULL_POWER) + "," + str(-FULL_POWER) + "\n")

# exampleUsage

# def prinnnt(x):
#     print bcolors.OKGREEN + x + bcolors.ENDC
#
# peripheral = BTPeripheral('/dev/cu.HC-06-DevB')
#
# if peripheral.connect():
#     peripheral.startListeningForRead(prinnnt)
#     try:
#         while True:
#             peripheral.send(str(raw_input("Input to send:\n")) + '\n')
#     finally:
#         peripheral.close()
# else:
#     print "Could not connect"


# import robotBluetooth
# robot = robotBluetooth.BTPeripheral()
# robot.follow_command((0, 0), (-1, 0), (-1, 1))
