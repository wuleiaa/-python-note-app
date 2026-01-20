<template>
	<view class="container">
		<view class="note-card">
			<view class="form-item">
				<text class="label">标题</text>
				<input class="input" type="text" v-model="title" placeholder="给笔记起个标题吧" />
			</view>
			
			<view class="form-item">
				<text class="label">分类</text>
				<picker mode="selector" :range="categories" @change="onCategoryChange">
					<view class="picker-box">
						<text>{{ category }}</text>
						<text class="picker-arrow">▼</text>
					</view>
				</picker>
			</view>

			<view class="form-item no-border">
				<textarea class="textarea" v-model="content" placeholder="在此输入笔记内容..." maxlength="-1"></textarea>
			</view>
		</view>

		<view class="btn-group">
			<button class="btn-save" @click="saveNote">保 存</button>
			
			<button class="btn-delete" v-if="id" @click="deleteNote">删 除</button>
		</view>
	</view>
</template>

<script>
	import request from '@/utils/request.js';

	export default {
		data() {
			return {
				id: null,
				title: '',
				content: '',
				category: '默认',
				categories: ['默认', '生活', '工作', '学习', '心情'] 
			}
		},
		onLoad(options) {
			if (options.id) {
				this.id = options.id;
				uni.setNavigationBarTitle({ title: '编辑笔记' });
				
				// ✅ 编辑回显：从缓存里取出刚才点击的那条笔记
				const note = uni.getStorageSync('current_note');
				if (note) {
					this.title = note.title;
					this.content = note.content;
					this.category = note.category;
				}
			} else {
				uni.setNavigationBarTitle({ title: '新建笔记' });
			}
		},
		methods: {
			onCategoryChange(e) {
				this.category = this.categories[e.detail.value];
			},
			
			// 保存逻辑
			async saveNote() {
				if (!this.title) {
					uni.showToast({ title: '标题不能为空', icon: 'none' });
					return;
				}
				const url = this.id ? '/api/note/edit' : '/api/note/add';
				const data = { title: this.title, content: this.content, category: this.category };
				if (this.id) data.id = this.id;

				try {
					const res = await request({ url: url, method: 'POST', data: data });
					if (res.code === 200) {
						uni.showToast({ title: '保存成功' });
						setTimeout(() => uni.navigateBack(), 1000);
					}
				} catch (e) { console.error(e); }
			},

			// 删除逻辑
			deleteNote() {
				uni.showModal({
					title: '提示',
					content: '确定要删除这条笔记吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								const apiRes = await request({
									url: '/api/note/delete',
									method: 'POST',
									data: { id: this.id }
								});
								if (apiRes.code === 200) {
									uni.showToast({ title: '删除成功' });
									setTimeout(() => uni.navigateBack(), 1000);
								}
							} catch (e) { console.error(e); }
						}
					}
				});
			}
		}
	}
</script>

<style>
	.container {
		min-height: 100vh;
		padding: 30rpx;
		background-color: #E8F5E9; 
		
		/* ✅ 这里已经改成了 bg.png */
		background-image: url('/static/bg.png');
		
		background-size: cover;
		background-position: center center;
		background-attachment: fixed;
	}

	.note-card {
		background-color: rgba(255, 255, 255, 0.85);
		border-radius: 20rpx;
		padding: 30rpx;
		backdrop-filter: blur(10px);
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.1);
	}

	.form-item { border-bottom: 1rpx solid #eee; padding: 20rpx 0; margin-bottom: 20rpx; }
	.no-border { border-bottom: none; }
	.label { font-size: 28rpx; color: #666; margin-bottom: 10rpx; display: block; }
	.input { font-size: 34rpx; height: 60rpx; color: #333; font-weight: bold; }
	.textarea { width: 100%; height: 400rpx; font-size: 30rpx; color: #333; line-height: 1.6; }
	.picker-box { font-size: 30rpx; color: #333; display: flex; justify-content: space-between; align-items: center; }
	.picker-arrow { color: #999; font-size: 24rpx; }

	.btn-group {
		margin-top: 50rpx;
		display: flex;
		gap: 30rpx;
	}

	.btn-save {
		flex: 1;
		background-color: #4CAF50;
		color: #fff;
		border-radius: 50rpx;
		box-shadow: 0 10rpx 20rpx rgba(76, 175, 80, 0.3);
		font-weight: bold;
	}

	.btn-delete {
		width: 200rpx;
		background-color: #FF5252;
		color: #fff;
		border-radius: 50rpx;
		box-shadow: 0 10rpx 20rpx rgba(255, 82, 82, 0.3);
		font-weight: bold;
	}
	
	button:active { transform: scale(0.98); }
</style>