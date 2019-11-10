#!/bin/bash
echo -e "rescanprogress\nexit\n" | nc localhost 9090 | urldecode.py
