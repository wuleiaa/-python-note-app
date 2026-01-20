<template>
	<div class="container">
		<div class="header">
			<text class="title">轻享笔记</text>
			<text class="sub-title">{{ isRegister ? '创建新账号' : '欢迎回来' }}</text>
		</div>

		<div class="form-area">
			<div class="input-group">
				<input class="input" type="text" v-model="username" placeholder="请输入用户名" />
			</div>
			<div class="input-group">
				<input class="input" type="password" v-model="password" placeholder="请输入密码 (至少6位)" />
			</div>
			
			<button class="btn-primary submit-btn" @click="handleSubmit">
				{{ isRegister ? '立即注册' : '登 录' }}
			</button>

			<div class="toggle-area" @click="toggleMode">
				<text class="toggle-text">
					{{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
				</text>
			</div>
		</div>
	</div>
</template>

<script>
	// 引入我们封装好的请求工具
	import request from '@/utils/request.js';

	export default {
		data() {
			return {
				username: '',
				password: '',
				isRegister: false // false=登录模式，true=注册模式
			}
		},
		methods: {
			// 切换 登录/注册
			toggleMode() {
				this.isRegister = !this.isRegister;
				this.username = '';
				this.password = '';
			},

			// 提交表单
			async handleSubmit() {
				// 1. 本地校验
				if (!this.username || !this.password) {
					uni.showToast({ title: '请输入用户名和密码', icon: 'none' });
					return;
				}
				if (this.password.length < 6) {
					uni.showToast({ title: '密码不能少于6位', icon: 'none' });
					return;
				}

				// 2. 准备参数
				const postData = {
					username: this.username,
					password: this.password
				};

				// 3. 判断是调登录接口，还是注册接口
				const url = this.isRegister ? '/api/user/register' : '/api/user/login';

				try {
					// 发送请求（request.js 会自动显示加载动画）
					const res = await request({
						url: url,
						method: 'POST',
						data: postData
					});

					// 4. 成功后的处理
					if (res.code === 200) {
						uni.showToast({ title: res.msg });
						
						// 核心：把 Token 存到手机本地！
						uni.setStorageSync('token', res.data.token);
						// 把用户信息也存一下，以后展示昵称用
						uni.setStorageSync('user', res.data.user);

						// 延迟跳转到首页 (pages/index/index)
						setTimeout(() => {
							uni.reLaunch({ url: '/pages/index/index' });
						}, 1000);
					}
				} catch (e) {
					// 错误已经在 request.js 里弹窗提示了，这里不用处理
					console.error(e);
				}
			}
		}
	}
</script>

<style>
	/* 页面容器 */
	.container {
		padding: 50rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		height: 100vh; /* 全屏高度 */
		background-color: #fff;
	}

	/* 标题样式 */
	.header {
		margin-bottom: 80rpx;
	}
	.title {
		font-size: 60rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 20rpx;
	}
	.sub-title {
		font-size: 32rpx;
		color: #999;
	}

	/* 输入框样式 */
	.input-group {
		margin-bottom: 40rpx;
		border-bottom: 2rpx solid #eee;
		padding-bottom: 20rpx;
	}
	.input {
		font-size: 32rpx;
		height: 60rpx;
	}

	/* 按钮样式 */
	.submit-btn {
		margin-top: 60rpx;
		border-radius: 50rpx;
		box-shadow: 0 10rpx 20rpx rgba(0, 122, 255, 0.2);
	}

	/* 切换文字样式 */
	.toggle-area {
		margin-top: 40rpx;
		text-align: center;
	}
	.toggle-text {
		color: #007AFF;
		font-size: 28rpx;
	}
</style>