# TVWSDataScraper

A repo for a directed study project. Used to navigate the 'GWS5000' TVWS radio's WebUI and gather data.

As the project evolves, ill link data + documentation to explain the project more.

If there is a paper, it will speek to a higher level of knowledge.
I will try to keep the readme file in as close to layman's terms so everyone can enjoy!

## TVWS?: 
[TV-WhiteSpace](https://www.rfwel.com/us/index.php/tvws)(TVWS) is the name for the newly (2010) re-classified TV spectrum.
What does that mean?

Communications 101: In grade-school they taught about the electromagnetic spectrum, everything from UV, microwaves, radio and
visable light was on it. The main difference between each of these is how fast the frequency is. Radio waves
are on the lower end, and gamma waves are on the higher end. Generally, The LOWER the frequency is, the FURTHER it can 
travel and the DEEPER it can penetrate. LOW frequency and HIGH wavelength creates signals that travel further.

Keep with me im going to drop some numbers:
- 2.4/5 GHz is the most common frequency of WI-FI.
- 54-698 MHz is the frequency of TVWS.

Just paying attention to the units, GHz to MHz is quite a large change.
This can be seen by how far each is able to broadcast. It varies but WI-FI usually tops out at 100ft. TVWS on the other
hand can be beamed over 10Km.

This is the primary reason that it was used to broadcast TV. TV was first broadcast with an analog signal however,
it was then swapped to a digital signal. Analog can be thought of as continuous, or 0,0.1,0.2,...0.8,0.9,1. Digital can
be through of as 0/1. As you can see by my example, digital is much more space efficient. As digital broadcasting
replaced analog, gaps of unused space began to appear. This brings us back to the FCC in the 2010 passing legislation to
re-categorize the un-used space into what is now TVWS.

## What is our goal?
As we have shown, TVWS broadcasts further than other categories of radio. This git project exists to pull data from
a TVWS antenna webgui. We are going to bury the receiver and see how different depths changes the measured characteristics.

See the Documentation folder for more.



## Features
Input: Uses Selenium to navigate through webgui, toggles through settings and records data.

Output: Currently only .csv files supported, DB can be implemented if school has somewhere to store data.

# SETUP:
1) Make sure to get required dependencies:
'''
pip install -r requirements.txt
'''
2) Config + Secret files are built on first run. Run and you will be prompted to fill out config.

If chrome driver is out of version have to dl latest:
I DON'T KNOW RIGHT NOW HOW TO VERIFY THAT THE CORRECT DRIVER IS INSTALLED AUTOMATICALY.
Newest driver has to be dropped in system path "C:\Windows"

https://googlechromelabs.github.io/chrome-for-testing/#stable

If project turns into something more maybe ill write bash script to handle that if needed.