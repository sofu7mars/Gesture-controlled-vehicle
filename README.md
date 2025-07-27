
#  Gesture-Controlled Vehicle

Description

This project demonstrates a real-time gesture-controlled vehicle using computer vision and wireless communication. Hand gestures captured via a webcam are processed on a PC using Python and OpenCV, and control signals are sent wirelessly to a mobile platform.
Features

    Real-time gesture recognition with OpenCV

    Two modes of control: gesture or joystick

    Serial communication between PC and Arduino Nano

    Wireless RF communication between Arduino Nano and Arduino Uno

    Controls a mobile vehicle remotely

Hardware Used

    PC with webcam

    Arduino Nano (connected to PC)

    Arduino Uno (on the vehicle)

    RF Module (433 MHz or similar)

    Motors and driver for the vehicle

Software Used

    Python (for gesture recognition and control logic)

    OpenCV (for image processing)

    Arduino IDE

Communication Flow

    PC ↔ Arduino Nano:

        Via USB Serial Port

        Sends gesture/joystick commands

    Arduino Nano ↔ Arduino Uno:

        Via RF Module

        Transmits control signals wirelessly to the vehicle

    Arduino Uno → Vehicle:

        Receives commands and drives the motors accordingly

How It Works

    The user performs hand gestures in front of the webcam.

    The PC processes the video feed using OpenCV and identifies the gesture.

    The command is sent over the serial port to the Arduino Nano.

    The Nano transmits it wirelessly using an RF module to the Arduino Uno.

    The Uno interprets the command and moves the vehicle.

Project Goals

    Create a flexible and responsive gesture-based control system.

    Minimize latency in communication between devices.

    Focus on the software side of gesture recognition and transmission.

