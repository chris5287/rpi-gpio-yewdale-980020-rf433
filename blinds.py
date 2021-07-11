import time
import sys
import RPi.GPIO as GPIO

# Modulation delays.
DELAY_SHORT = 0.000284
DELAY_LONG = 0.000592
DELAY_EXTENDED = 0.005

# GPIO data pin that is connected to transmitter's data pin.
GPIO_DATA_PIN_TRANSMIT = 24

# Helper function to convert hex into binary string representation.
def hex2binary(hexadecimal):
    end_length = len(hexadecimal) * 4

    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)

    return padded_binary

# Main method.
if __name__ == '__main__':

    # Capture target blind and action to perform.
    blind = sys.argv[1]
    action = sys.argv[2]
    open_percentage = sys.argv[3] 

    # Set codes to execute.
    if blind == 'livingroom_left':
        if action == 'up_step':
            codes = ["5CC7C7ADFEFFF431", "5CC7C7ADFEFFDB18"]
        elif action == 'up':
            codes = ["5CC7C7ADFEFFF431", "5CC7C7ADFEFFF431", "5CC7C7ADFEFF74B1", "5CC7C7ADFEFFF431", "5CC7C7ADFEFFF431", "5CC7C7ADFEFF74B1"]
        elif action == 'stop':
            codes = ["5CC7C7ADFEFFDC19"]
        elif action == 'down_step':
            codes = ["5CC7C7ADFEFFBCF9", "5CC7C7ADFEFFDB18"]
        elif action == 'down':
            codes = ["5CC7C7ADFEFFBCF9", "5CC7C7ADFEFFBCF9", "5CC7C7ADFEFF3C79", "5CC7C7ADFEFFBCF9", "5CC7C7ADFEFFBCF9", "5CC7C7ADFEFF3C79"]
        else:
            sys.exit("Unknown action: " + action)

    elif blind == 'livingroom_right':
        if action == 'up_step':
            codes = ["5CC7C7A6FEFFF42A", "5CC7C7A6FEFFDB11"]
        elif action == 'up':
            codes = ["5CC7C7A6FEFFF42A", "5CC7C7A6FEFFF42A", "5CC7C7A6FEFF74AA", "5CC7C7A6FEFFF42A", "5CC7C7A6FEFFF42A", "5CC7C7A6FEFF74AA"]
        elif action == 'stop':
            codes = ["5CC7C7A6FEFFDC12"]
        elif action == 'down_step':
            codes = ["5CC7C7A6FEFFBCF2", "5CC7C7A6FEFFDB11"]
        elif action == 'down':
            codes = ["5CC7C7A6FEFFBCF2", "5CC7C7A6FEFFBCF2", "5CC7C7A6FEFF3C72", "5CC7C7A6FEFFBCF2", "5CC7C7A6FEFFBCF2", "5CC7C7A6FEFF3C72"]
        else:
            sys.exit("Unknown action: " + action)

    else:
        sys.exit("Unknown blind: " + blind)

    # Setup GPIO pin to transmit.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_DATA_PIN_TRANSMIT, GPIO.OUT)

    # Process each code required.
    for code in codes:

        # Convert to binary string.
        code = hex2binary(code)

        # Wait before starting.
        time.sleep(DELAY_EXTENDED)

        # Transmit preamble (remote transmits 6 times).
        for i in range(6):

            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 1)
            time.sleep(DELAY_SHORT)
            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 0)
            time.sleep(DELAY_LONG)

        # Transmit main code (remote transmits 6 times).
        for t in range(6):

            # Transmit starting bits.
            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 1)
            time.sleep(DELAY_EXTENDED)
            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 0)
            time.sleep(DELAY_LONG)

            # Transmit each bit.
            for i in code:
                if i == '1':
                    GPIO.output(GPIO_DATA_PIN_TRANSMIT, 1)
                    time.sleep(DELAY_SHORT)
                    GPIO.output(GPIO_DATA_PIN_TRANSMIT, 0)
                    time.sleep(DELAY_LONG)
                elif i == '0':
                    GPIO.output(GPIO_DATA_PIN_TRANSMIT, 1)
                    time.sleep(DELAY_LONG)
                    GPIO.output(GPIO_DATA_PIN_TRANSMIT, 0)
                    time.sleep(DELAY_SHORT)
                else:
                    continue

            # Transmit ending bits.
            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 1)
            time.sleep(DELAY_LONG)

            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 0)
            time.sleep(DELAY_SHORT)

            GPIO.output(GPIO_DATA_PIN_TRANSMIT, 0)
            time.sleep(DELAY_EXTENDED)

    # Cleanup GPIO for next usage.
    GPIO.cleanup()

    # Print open percentage for Homebridge integration.
    print(open_percentage)
