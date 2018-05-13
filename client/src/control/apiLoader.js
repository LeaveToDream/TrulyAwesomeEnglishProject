import axios from 'axios';

const HOSTNAME = 'omachi.moe';
const HOSTPORT = 9876;

const API_URL = `http://${HOSTNAME}:${HOSTPORT}/api/`;

export default () => {
	return axios.create({
		baseURL: API_URL
	});
};
