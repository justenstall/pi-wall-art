package main

import (
	"image"
	"image/color"
	"image/draw"
	"os"

	rgbmatrix "github.com/mcuadros/go-rpi-rgb-led-matrix"
)

func main() {
	os.Setenv("MATRIX_EMULATOR", "1")
	setAllWhite()
}

func setAllWhite() {
	// create a new Matrix instance with the DefaultConfig
	m, _ := rgbmatrix.NewRGBLedMatrix(&rgbmatrix.DefaultConfig)

	// create the Canvas, implements the image.Image interface
	c := rgbmatrix.NewCanvas(m)
	defer c.Close() // don't forgot close the Matrix, if not your leds will remain on

	// using the standard draw.Draw function we copy a white image onto the Canvas
	draw.Draw(c, c.Bounds(), &image.Uniform{color.White}, image.ZP, draw.Src)

	// don't forget call Render to display the new led status
	c.Render()
}
