import axios from 'axios';
const BASE_URL = 'localhost:666';

export default () => {
	return axios.create({
		baseURL: BASE_URL
	});
};
