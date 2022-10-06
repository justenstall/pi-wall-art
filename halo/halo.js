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

		const haloapi = {
				baseURL: 'https://cryptum.halodotapi.com/games/hi',
				// timeout: 1000,
				headers: { 
					'Authorization': env.HALO_TOKEN,
					'Content-Type': 'application/json',
				},
				data: {},
			}

		const instance = axios.create(haloapi);

		// make API request
		// Make a request for a user with a given ID
		let gamertag = 'JStall17'
		instance.get(`/appearance/players/${gamertag}`, haloapi)
			.then(response => {
				console.log(response.data);
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



