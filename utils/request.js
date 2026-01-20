// 🏠 如果是真机调试，建议把 'http://127.0.0.1:5000' 换成你电脑的局域网 IP
const BASE_URL = 'http://127.0.0.1:5000'; 

const request = (options) => {
	return new Promise((resolve, reject) => {
		
		// 显示加载中
		uni.showLoading({
			title: '加载中...',
			mask: true
		});

		// 获取 Token
		const token = uni.getStorageSync('token');

		uni.request({
			url: BASE_URL + options.url,
			method: options.method || 'GET',
			data: options.data || {},
			header: {
				'Authorization': token ? `Bearer ${token}` : '' 
			},
			success: (res) => {
				uni.hideLoading();
				if (res.statusCode === 200) {
					resolve(res.data);
				} else if (res.statusCode === 401) {
					uni.showToast({ title: '请先登录', icon: 'none' });
					uni.reLaunch({ url: '/pages/login/login' });
					reject(res);
				} else {
					uni.showToast({ title: res.data.msg || '请求失败', icon: 'none' });
					reject(res);
				}
			},
			fail: (err) => {
				uni.hideLoading();
				uni.showToast({ title: '网络连接失败', icon: 'none' });
				reject(err);
			}
		});
	});
}

export default request;