#!/bin/bash

for FONT in fonts/*.bdf; do
	python ~/pillow-scripts/Scripts/pilfont.py "$FONT"
done