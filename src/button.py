import gpiozero

button = gpiozero.MCP3008(channel=0)

while True:
	print(button.value)