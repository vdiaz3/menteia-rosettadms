#!/bin/bash
# Runs by cron: keeps /opt/rosettadms in sync with GitHub main; nginx serves its site/ folder.
set -e
REPO=https://github.com/vdiaz3/menteia-rosettadms
DIR=/opt/rosettadms
[ -d $DIR/.git ] || git clone -q --depth 1 $REPO $DIR
cd $DIR && git fetch -q --depth 1 origin main && git reset -q --hard origin/main
