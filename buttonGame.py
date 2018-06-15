import time
import RPi.GPIO as GPIO

# GPIO pin identifiers
PIN_R = 17
PIN_B = 27
PIN_G = 22
LED_R = 13
LED_B = 19
LED_G = 26
START_TIME = time.time()
LAST_PUSH = {LED_R:START_TIME, LED_B:START_TIME, LED_G:START_TIME}



# Setting up GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # gets rid of stupid channel in use warnings
# Setting up button pins as inputs
GPIO.setup(PIN_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_G, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Associate LED pins as outputs
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
# Add event listeners
GPIO.add_event_detect(PIN_R,GPIO.FALLING)
GPIO.add_event_detect(PIN_B,GPIO.FALLING)
GPIO.add_event_detect(PIN_G,GPIO.FALLING)

# Keeps LED on while PIN is pushed down
def lightUpPress (PIN, LED):
    pushed = False
    if GPIO.event_detected(PIN):
	while GPIO.input(PIN) == GPIO.LOW:
            # Pretty much while the button is down set LED to HIGH
            GPIO.output(LED, GPIO.HIGH)
            # Sleep a little bit and wait to check again so LED doesn't flicker a lot
            #time.sleep(0.2)
            pushed = True
        LAST_PUSH[LED] = time.time()
    # Default to LED at LOW
    if time.time()-LAST_PUSH[LED] > 0.1:
        GPIO.output(LED, GPIO.LOW)
    return pushed

# Main 
def main():
    while True:
#        print(time.time()-LAST_PUSH[LED_R])
        if time.time()-LAST_PUSH[LED_R] > 0.25 and lightUpPress(PIN_R, LED_R):
            print("RED")
        if time.time()-LAST_PUSH[LED_B] > 0.25 and lightUpPress(PIN_B, LED_B):
            print("BLUE")
        if time.time()-LAST_PUSH[LED_G] > 0.25 and lightUpPress(PIN_G, LED_G):
            print("GREEN")
        # Quits upon simultaneous 3-button press
        if (GPIO.input(PIN_R)==GPIO.input(PIN_B)==GPIO.input(PIN_G)==GPIO.LOW):
            break
main()
