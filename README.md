# Headless-Keyboard-Notetaker
Small project to turn a Raspberry Pi and USB keyboard into a dedicated headless notetaking tool.

## Interface:
- Press Enter to begin a new note, and Alt+E to close out and save it. Notes will also save automatically every 30 seconds during recording.
- To title your note, press Alt+T at any point while recording, type your title, then press Enter to return to recording.
- If you want automatic syncing with Google Keep, include a file called '.auth' in the google_auth folder with your Google login in the first line in the form <username>,<password> (obviously, this ***not*** a secure practice, do this at your own risk).

The current status is indicated by the Caps Lock light - on means recording, blinking means recording title/filename, and off means not recording. I have disabled the actual function of Caps Lock in my OS to avoid interfering with the light indication.

## Background:

One of the readings for an English class I took last semester was *Paradise Lost*, by John Milton. During class one day I learned that Milton was blind when he wrote it, having lost his sight more than a decade before. He wrote the entire ten-book epic by dictating it to various friends and assistants who wrote it down for him, never able to see for himself a single word of it. I got really interested in trying out a much less extreme version of this - some kind of way I could pick up nothing but a keyboard, type out my thoughts with no visual reference to the output, and automatically record it all (yeah, you could just close your eyes while typing into a Google doc, but it's just not the same). This project was so I could do that. Now that I've got it working, I'm really happy with the outcome; I've written a couple thousand words on it already and it feels super natural to use! (You have to know how to touch type, of course.)

## Some technical details:

For keyboard capture, I used the keyboard module written by boppreh (https://github.com/boppreh/keyboard), which abstracted away all of the low-level OS stuff and made my life a hundred times easier.

To reproduce this project, just clone this repo to your own device, and have Main.py run on startup (sudo privileges required). ***However***, keep in mind that the *only* hardware I have tested this on is my own small setup: a Raspberry Pi 3 B+ running a minimal installation of Buster (4.19), and a cheap wireless USB keyboard (Brand: Macally, Model: RFCOMPACTKEY). I have no idea how much of this would break on a different setup, but I'm pretty (kind-of maybe) sure it wouldn't be too hard to port this, although there could very well be some necessary adjustments (the way I used the Caps Lock light in particular was pretty hacky, involving some ioctl calls that might not work with other keyboards).
