<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
			// 这里可以检查是否已登录
			const token = uni.getStorageSync('token');
			if(!token){
				// 没登录就去登录页 (稍后创建)
				uni.reLaunch({ url: '/pages/login/login' })
			}
		}
	}
</script>

<style>
	/* ✅ 模块5-1：全局样式适配 */
	page {
		background-color: #F5F7FA; /* 浅灰背景，护眼 */
		font-size: 28rpx; /* 使用 rpx 单位，自动适配所有手机屏幕 */
		color: #333;
		line-height: 1.6;
	}
	
	/* 通用按钮样式 */
	.btn-primary {
		background-color: #007AFF;
		color: #fff;
		border-radius: 10rpx;
		text-align: center;
		padding: 20rpx 0;
		font-size: 32rpx;
	}
</style>