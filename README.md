# CapStone_Robotics
## TAFE Robotics Capstone Project.

### - Why has the Repo been created Midway through part B?
Part A had no need for Github in my opinion, prepping the VM, collecting evidence and other things were perfectly do-able without github.
When i did start writing my code, i wrote it within my VM initially before swapping over to VSCode, unfortunately at that point i had long forgotten about it.
I am able to produce photo evidence of document creation on my onedrive for the note taking.
It was only until now that I was reading back after i took a photo of my tests working without any hardware,
THEN i had read the repo statement, meaning all i can really do is upload my work now as is,
I just wanted to at least create the repo with an initial commit before going ahead.
SORRY

# Temp BareBones Readme

# xarm_toolkit

A Python package for controlling a Hiwonder xArm using modifiable target sources.

## Features

- ArmController wrapper for xarm.Controller
- Servo movement and position reading
- Battery voltage-monitoring
- Abstract TargetSource interface
- Pygame mouse-click target source
- Future ARI tracking integration

## Installation

Install the package with its optional dependencies:

    pip install -e ".[mock,dev]"

## E.G

    from xarm_toolkit import ArmController

    with ArmController() as arm:
        arm.point_at(400, 300)

## Test it!

Run the automated tests:

    pytest -v

