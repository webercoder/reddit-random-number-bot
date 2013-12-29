#!/bin/bash
until "./bot.py"; do
    echo "Server 'reddit-random-number-bot' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done