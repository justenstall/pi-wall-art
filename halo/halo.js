import { LedMatrix, GpioMapping } from 'rpi-led-matrix';
import path from 'path';
import { env } from 'process';
import axios from 'axios';

(async () => {
	try {
		const matrix = new LedMatrix(
			{
				...LedMatrix.defaultMatrixOptions(),
				rows: 64,
				cols: 64,
				hardwareMapping: GpioMapping.AdafruitHatPwm,
				limitRefreshRateHz: 150,
				pwmDitherBits: 1,
			},
			{
				...LedMatrix.defaultRuntimeOptions(),
				gpioSlowdown: 4,
			}
		);

		matrix.clear().brightness(100);

		const halodotapi = axios.create({
			baseURL: 'https://cryptum.halodotapi.com/',
			timeout: 1000,
			headers: {
				'Authorization': 'Bearer nc0tSzdnESGwGa84RNIL7aK17dLPUl4LjEkBHapZHMXk4rM75SDClGymRcHSIH2b',
				'Content-Type': 'application/json'
			}
		});

		// make API request
		// Make a request for a user with a given ID
		let gamertag = 'JStall17'
		axios.get(`https://cryptum.halodotapi.com/games/hi/appearance/players/${gamertag}`,
			{
				timeout: 1000,
				headers: {
					'Authorization': 'Bearer nc0tSzdnESGwGa84RNIL7aK17dLPUl4LjEkBHapZHMXk4rM75SDClGymRcHSIH2b',
					'Content-Type': 'application/json'
				}
			}
		)
			.then(function (response) {
				// handle success
				console.log(response);
			})
			.catch(function (error) {
				// handle error
				console.log(error);
			})
			.finally(function () {
				// always executed
			});

		const baseBuffer = [...Array(matrix.width() * matrix.height() * 3).keys()];
		const buffer1 = Buffer.of(
			...baseBuffer.map(() => (Math.random() < 0.1 ? 0xff : 0x00))
		);
		const buffer2 = Buffer.of(
			...baseBuffer.map(() => (Math.random() < 0.1 ? 0xff : 0x00))
		);

		let useBuffer1 = true;
		matrix.afterSync(() => {
			useBuffer1 = !useBuffer1;
			matrix.drawBuffer(useBuffer1 ? buffer1 : buffer2);
			setTimeout(() => matrix.sync(), 0);
		});

		matrix.sync();
	} catch (error) {
		console.error(`${path.basename(".")} caught: `, error);
	}
})();



