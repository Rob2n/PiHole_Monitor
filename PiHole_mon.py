import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import requests
import subprocess
from gpiozero import Button

def button_presssed():
  global mode
  if mode==1:
    mode=0
  else:
    mode=1

ButtonGPIO=21

# Configure button connected to GPIO21 (Pin 40) and Ground (Pin 39)
button = Button(ButtonGPIO)
button.when_pressed = button_presssed

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',15)

# Draw Some Text
text = "Hi PiHole ;)"

(idk_var1, idk_var2, font_width, font_height) = font.getbbox(text)
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)

# Display image
oled.image(image)
oled.show()

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = HEIGHT-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load Truetype font from https://www.dafont.com/bitmap.php
# VCR OSD Mono by Riciery Leal
font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',15)
font2 = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',40)

counter = 28
mode = 0
r = ''
while True:
  if mode == 0 and counter>29:
    # Get Pi-Hole data
    r = requests.get("http://localhost/admin/api.php?summary")

    # Scroll from right-hand side (x 128 to 0 in steps of 16)
    for x in range(128,-1,-16):

      # Draw a black filled box to clear image.
      draw.rectangle((0,0,WIDTH,HEIGHT), outline=0, fill=0)

      # Display large Pi-Hole ads blocked percentage
      draw.text((x, top-2),   "%s%%" % r.json()["ads_percentage_today"],  font=font2, fill=255)
      draw.text((x, top+34),   "Ads blocked:", font=font, fill=255)
      draw.text((x, top+48),   "%s" % r.json()["ads_blocked_today"], font=font, fill=255)

      # Display image.
      oled.image(image)
      oled.show()
    counter=0

  if mode==1 and r:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,WIDTH,HEIGHT), outline=0, fill=0)

    # Get system data
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    # Write Pi-Hole data
    draw.text((x, top), "Last 24h",  font=font, fill=255)
    # draw.text((x, top+16), "%%: %s%%" % r.json()["ads_percentage_today"],  font=font, fill=255)
    draw.text((x, top+16), "Blocked: %s" % r.json()["ads_blocked_today"], font=font, fill=255)
    draw.text((x, top+32), "Queries: %s" % r.json()["dns_queries_today"], font=font, fill=255)
    cmd = "vcgencmd measure_temp | awk -F= '{printf \"Temp: %s\", $2}'"
    Temp = subprocess.check_output(cmd, shell = True )
    draw.text((x, top+48),  str(Temp.decode('UTF-8')),font=font, fill=255)

    # Display image.
    oled.image(image)
    oled.show()
    time.sleep(8)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,WIDTH,HEIGHT), outline=0, fill=0)

    # Get system data °
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB\", $3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Dsk: %d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Display system stats
    draw.text((x, top),       "Sys usage",  font=font, fill=255)
    draw.text((x, top+16),    str(CPU.decode('UTF-8')), font=font, fill=255)
    draw.text((x, top+32),    str(MemUsage.decode('UTF-8')), font=font, fill=255)
    draw.text((x, top+48),    str(Disk.decode('UTF-8')),font=font, fill=255)

    # Display image.
    oled.image(image)
    oled.show()
    time.sleep(6)

    mode=0
    counter=29

  counter=counter+1
  time.sleep(1)
