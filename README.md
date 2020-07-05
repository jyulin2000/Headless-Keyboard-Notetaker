# Headless-Keyboard-Notetaker
Small project to turn a Raspberry Pi and USB keyboard into a dedicated headless notetaking tool.

Manifesto:

So about a decade before he wrote Paradise Lost, John Milton lost sight in both eyes, entirely and permanently. And so the way he kept writing was by dictating his passages to his friends and family members, who would write them down for him, day in, and day out. 

Not for coding or anything like that, of course, but for things like taking down thoughts and writing out sentences or passages, I found myself wishing there was some kind of way I could pick up nothing but a keyboard, type out whatever it is I wanted to type with no visual reference to the output, and have it recorded so I could look back at it later. I wasn't sure if it would be useful or productive, necessarily, but I got really excited about the idea of writing without having any way to see the words I was typing. This project was so I could do that. And to my friend who helpfully suggested that I just close my eyes and type into a Google Doc instead of wasting my time on this, IT'S NOT THE SAME (even though it kind of is), and besides, it was pretty fun to make. Now that I've got it working, I'm really happy with the outcome; I've written a couple thousand words on it already and it feels super cool to use.

Some technical details:

I wrote this in Python to quickly get something that works, but it takes up so few resources already that I didn't see the need to rewrite it in a faster/compilable language.

The Caps Lock light on the keyboard serves as a status indicator - on means recording, blinking means recording title/filename, and off means, well, yeah, not recording.

For keyboard capture, I used the keyboard module written by boppreh (https://github.com/boppreh/keyboard), which abstracted away all the low-level OS stuff made my life a thousand times easier.

Note 1: Any keystrokes inputted while this program runs also get buffered by the OS, and once it exits all of that input gets spewed onto the command line. Since this includes enter keys, this basically ends up in nonsensical calls in the command line until the buffer empties. It's weird and messy, but doesn't really affect anything, but there *is* a *possibility*, although statistically slight, that a valid command could be entered in this way and cause bad stuff to happen. I took care of this in the bash script I have that runs this on startup by flushing the input, but I'm looking for a better way to handle/prevent this.

Note 2: The *only* hardware I have tested this on is my own small setup: a Raspberry Pi 3 B+ running a minimal installation of Buster (4.19), and a cheapo wireless USB keyboard (Brand: Macally, Model: RFCOMPACTKEY) I had lying around. I have no idea how much of this would break on a different setup, but I'm pretty (kind-of maybe) sure it wouldn't be too hard to port this, although I'm sure there'd be some necessary adjustments (the way I used the Caps Lock light in particular was pretty hacky and could very well be device-specific). What would ostensibly be the main culprit for anti-cross-compatibility, which is the direct keyboard capture, I actually think would work fine since the keyboard module I mentioned takes care of OS-specific worries (the description even says it works on both Linux and Windows OSes, although I haven't tried this).
