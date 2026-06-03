#!/usr/bin/env python3
import time
import sys
from rpi_ws281x import PixelStrip, Color

# =========================================================================
# PROGRAM: SEQUENCE TEST 1 (6-Segment Edition)
# =========================================================================
LED_COUNT      = 30      # Total number of LEDs on your strip
LED_PIN        = 18      # Hardware PWM0 Pin (Physical Pin 12)
LED_FREQ_HZ    = 800000  # Strict 800kHz data timing rate
LED_DMA        = 10      # Direct Memory Access channel
LED_BRIGHTNESS = 50      # Safe brightness limit for power bank stability
LED_INVERT     = False   # Direct logic signaling
LED_CHANNEL    = 0       # PWM Channel 0

# Initialize the strip object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

def clear_strip():
    """Turns off all pixels across all segments safely."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def light_single_segment(target_segment):
    """Isolates power and data signaling to exactly one of the 6 targeted segments."""
    # First, force all 30 pixels completely OFF to clear old states
    for i in range(0, 30):
        strip.setPixelColor(i, Color(0, 0, 0))

    # Calculate exact start and end boundaries mathematically (5 LEDs per segment)
    start_index = (target_segment - 1) * 5
    end_index = start_index + 5

    print(f"[+] Isolating Zone {target_segment}: LEDs {start_index} to {end_index - 1} are now GREEN")
    
    # Light up only the targeted 5 LEDs
    for i in range(start_index, end_index):
        strip.setPixelColor(i, Color(0, 255, 0)) # Green
        
    strip.show()

# =========================================================================
# MAIN EXECUTION RUNTIME
# =========================================================================
if __name__ == "__main__":
    try:
        strip.begin()
        print("====================================================")
        print("                SEQUENCE TEST 1                     ")
        print("====================================================")
        print("[*] System Online. 6 Segments mapped (5 LEDs each).")
        print("[*] Idle State: OFF (Waiting for input...)")
        
        # Valid inputs are now strings '1' through '6'
        valid_inputs = [str(x) for x in range(1, 7)]
        
        while True:
            # Force the strip to stay completely dark while waiting for input
            clear_strip()
            
            print("\n----------------------------------------------------")
            print("Command Options:")
            print("  Type '1' through '6' -> Light that specific segment Green")
            print("  Type 'exit'          -> Close execution engine")
            print("----------------------------------------------------")
            
            user_input = input("[?] Enter your sequence choice (1-6): ").strip().lower()
            
            if user_input == 'exit':
                print("[*] Terminating Sequence Test 1...")
                break
                
            elif user_input in valid_inputs:
                # Call the selector function to light up only that segment
                light_single_segment(int(user_input))
                
                # Maintain the isolation state until user interaction triggers reset
                input("\n[*] Segment isolated! Press [ENTER] to turn off the strip and wait for next input...")
                print("[*] Resetting baseline to OFF...")
                
            else:
                print("[X] Entry unverified. Please enter a number from 1 to 6, or exit.")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Emergency termination signal received.")
    finally:
        clear_strip()
        print("[+] Hardware pins cleared. Sequence Test 1 Closed cleanly.")