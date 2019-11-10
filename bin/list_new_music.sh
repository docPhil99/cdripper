#!/bin/bash
find /home/phil/storage/music/flac/ -type d -printf '%T+ %p\n'  | sort -r | head -n 40
