# README.md

CSC 251 Final Project by **Max Mason**
Port Scanner Program 
-----------------------------------------

List of all files:
* port_scanner.py -- the main file.

Usage guide:
* Before you do anything, install `scapy` and some form of `pcap`.
* Running `python port_scanner.py` with no/missing arguments shows you the following:
    ```
    Usage: python port_scanner.py [TARGET IPv4 ADDR] [SCAN MODE]
    Scan mode options: CONNECT, STEALTH, FIN (case-insensitive)
    ```
* `[TARGET IPv4 ADDR]` argument takes in a string: IPv4 address. 
    * Example: `24.156.99.202`
    * If resolving the hostname fails, program will exit.
* `[SCAN MODE]` argument takes in a string: preferred port scanning method.
    * Examples: `CONNECT` or `Stealth` or `fin`
    * Failing to provide **valid** scan mode will cause the program to exit.

Example output (removed my IP for obvious reasons):
```
maxma@max-PC MINGW64 ~/Desktop/CSC 251 Final
$ python port_scanner.py [###MY IP###] connect

* Start port scan at 2021-05-21 01:50:36.098284
* Notable open ports on [###MY IP###]...
-------------------------------------------------------
|      PORT       |      STATE      |     SERVICE     |
-------------------------------------------------------
|       53        |      OPEN       |     domain      |
|       80        |      OPEN       |      http       |
|       443       |      OPEN       |      https      |
|      3389       |      OPEN       |  ms-wbt-server  |
-------------------------------------------------------
* Elapsed time: 0:04:29.041411
* Not shown: 65521 closed ports. The rest do not have a service associated.
```

Port scan will show you open ports **with services** only, time elapsed, and number of closed ports on host. 

## For class purposes:
* The biggest problem I really only had was deciding a method for sending packets to a host on a specific port, 
and that was a bit intimidating considering I was previously unfamiliar with `scapy` and only had experience with
`socket` in the past.
* For this project, I spent a few hours learning how to use `scapy` (mostly through trial and error) which was really fun! 
It was a pain at first because I didn't have `Npcap` (I'm on Windows 10 w/ mingw) installed so I was really running into a wall for a good amount of the time I was working on this project. 
