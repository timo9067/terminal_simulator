## Terminal simulator

This program simulates the requests sent by terminal vehicles.

## How to run the program

Module terminal_simulator.py can be run on local computer and is controlled by GET queries:
- `http://127.0.0.1:5000/?command=start&filename=<PATH_TO_THE_FILE>&url=<URL_FOR_SENDING_REQUESTS>` - to START process
- `http://127.0.0.1:5000/?command=stop` - to STOP process

## System requirements
Python 3.10.12
Flask 3.0.0
