import time
import RPi.GPIO as GPIO

# GPIO pin identifiers
PIN_R = 17
PIN_B = 27
PIN_G = 22
PINS = [PIN_R, PIN_B, PIN_G]
LED_R = 13
LED_B = 19
LED_G = 26
LEDS = [LED_R, LED_B, LED_G]
START_TIME = time.time()
LAST_PUSH = {LED_R:START_TIME, LED_B:START_TIME, LED_G:START_TIME}



# Setting up GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # gets rid of stupid channel in use warnings
# Setting up button pins as inputs
for x in PINS:
    GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Associate LED pins as outputs
for x in LEDS:
    GPIO.setup(x, GPIO.OUT)
# Add event listeners
for x in PINS:
    GPIO.add_event_detect(x,GPIO.FALLING)

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

# Checks stuff
def isMatch(progress, complete):
    for x in range(len(progress)):
        if progress[x] != complete[x]:
            return False
    return True
# Input phase
def Player(match):
    pushed = []
    while len(pushed) < len(match) and isMatch(pushed, match):
#        print(time.time()-LAST_PUSH[LED_R])
        if time.time()-LAST_PUSH[LED_R] > 0.25 and lightUpPress(PIN_R, LED_R):
            pushed.append('R') #print("RED")
        if time.time()-LAST_PUSH[LED_B] > 0.25 and lightUpPress(PIN_B, LED_B):
            pushed.append('B') #print("BLUE")
        if time.time()-LAST_PUSH[LED_G] > 0.25 and lightUpPress(PIN_G, LED_G):
            pushed.append('G') #print("GREEN")
        for x in LEDS:
            GPIO.output(x,GPIO.LOW)
    return pushed

# Simon's turn
def Simon(hist):
    choices = ['R','B','G']
    mappy = {'R':LEDS[0],'B':LEDS[1],'G':LEDS[2]}
    temp = hist
    randomNum = (int)((time.time()%1)*3)
    temp.append(choices[randomNum])
    for x in temp:
        GPIO.output(mappy[x],GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(mappy[x],GPIO.LOW)
        time.sleep(0.5)
    return temp

def game():
    simonSays = []
    player = []
    while isMatch(player,simonSays):
        simonSays = Simon(simonSays)
        player = Player(simonSays)
        time.sleep(1)
    print("GAME OVER")

def main():
    game()

main()
