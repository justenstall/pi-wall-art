#!/bin/bash

for FONT in fonts/*; do
	python ~/pillow-scripts/Scripts/pilfont.py "$FONT"
done