#!/usr/bin/env python3

import gpiod
import time
import sys
import os

CHIP_NAME = 'gpiochip1'
LINE_NUMBER = 78

CONSUMER = 'cpu_temp_fan_control'

FAN_ON_TEMP = 51.0
FAN_OFF_TEMP = 50.5

POLLING_INTERVAL = 5

def read_cpu_temp():
    temp_path = '/sys/class/thermal/thermal_zone2/temp'
    
    try:
        with open(temp_path, 'r') as f:
            temp_raw = int(f.read().strip())
            temp_celsius = temp_raw / 1000.0
            return temp_celsius
    except FileNotFoundError:
        print(f"Error: CPU temperature file not found at {temp_path}.", file=sys.stderr)
    except Exception as e:
        print(f"Error: Could not read temp from {temp_path}: {e}", file=sys.stderr)
    
    return None

def main():
    chip = None
    line = None
    fan_is_on = False
    try:
        chip = gpiod.Chip(CHIP_NAME)
        line = chip.get_line(LINE_NUMBER)
        line.request(CONSUMER, gpiod.LINE_REQ_DIR_OUT)
        
        while True:
            temp = read_cpu_temp()
            if temp is None:
                time.sleep(POLLING_INTERVAL)
                continue

            if temp >= FAN_ON_TEMP and not fan_is_on:
                line.set_value(1)
                fan_is_on = True
            elif temp <= FAN_OFF_TEMP and fan_is_on:
                line.set_value(0)
                fan_is_on = False
            
            time.sleep(POLLING_INTERVAL)

    except PermissionError as e:
        print(f"ERROR: Could not access GPIO chip '{CHIP_NAME}' or line '{LINE_NUMBER}'.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        print("Make sure the GPIO line is not in use and run with 'sudo'.", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        pass
    finally:
        if line and line.is_requested():
            line.set_value(0)
            line.release()
        if chip:
            chip.close()

if __name__ == '__main__':
    main()
