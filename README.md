# kitty-image-viewer-simplified
This is a python script that makes it easier to display multiple images at once in kitty terminal.
The program works on linux (haven't tested on )

## Screenshots

![Single image usage screenshot](/Screenhots/Screenshot_20200604_190754.png "Single image")
![Multiple images usage screenshot](/Screenhots/Screenshot_20200604_191012.png "Multiple images")
![Multiple images behind text usage screenshot](/Screenhots/Screenshot_20200604_191044.png "Multiple images behind text")
![Single image behind text terminal max usage screenshot](/Screenhots/Screenshot_20200604_192147.png "Single image behind text terminal max")


## Dependencies
- kitty
- python3

## Installation
You can either just run the script like this `python3 kitty-image-viewer.py /path/to/image.jpg`
or move/copy it to /usr/local/bin/ (I called the shortcut img)

    sudo cp kitty-image-viewer.py /usr/local/bin/img
    sudo chmod +x /usr/local/bin/img

## Usage

### Show images
- img /path/to/image.jpg
- img /path/to/image.png /path/to/other/image.jpeg
- img /path/to/images*
### Show image(s) at terminal maximum resolution:
- img -f /path/to/image.jpg
- img --full /path/to/image.jpg
### Show image(s) at maximum resolution:
- img -m /path/to/image.jpg
- img --max /path/to/image.jpg
### Show image(s) underneeth text (z-index=-1)
- img -b /path/to/image.jpg
- img --behind /path/to/image.jpg
- img -m -b /path/to/image.jpg
### Clear images shown on screen:
- img -c
- img --clear
### Help Menu (this page):
- img -h
- img --help


## NOTES
Crappy code, bunch of `if`, `else` uhhh.
It works! and it works like it should (I believe)
