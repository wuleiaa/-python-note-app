<template>
	<view class="container">
		<view class="note-list">
			<view class="note-item" v-for="(item, index) in noteList" :key="item.id" @click="goToDetail(item)">
				<view class="item-header">
					<text class="item-title">{{ item.title }}</text>
					<text class="item-time">{{ formatTime(item.create_time) }}</text>
				</view>
				<text class="item-content">{{ item.content || '暂无内容' }}</text>
				<view class="item-footer">
					<text class="item-category">{{ item.category || '默认' }}</text>
				</view>
			</view>
		</view>

		<view class="empty-state" v-if="noteList.length === 0">
			<text class="empty-text">还没有笔记，快去创建一条吧~</text>
		</view>

		<view class="fab-btn" @click="goToAdd">
			<text class="fab-icon">+</text>
		</view>
	</view>
</template>

<script>
	import request from '@/utils/request.js';

	export default {
		data() {
			return {
				noteList: [] // 存储笔记数据
			}
		},
		// ✅ 核心：每次页面显示时（包括从详情页返回），都会触发
		onShow() {
			this.getNoteList();
		},
		// ✅ 下拉刷新触发
		onPullDownRefresh() {
			this.getNoteList();
		},
		methods: {
			// 获取笔记列表
			async getNoteList() {
				try {
					const res = await request({
						url: '/api/note/list',
						method: 'GET'
					});
					if (res.code === 200) {
						this.noteList = res.data;
					}
				} catch (e) {
					console.error(e);
				} finally {
					// 无论成功失败，都要停止下拉刷新动画
					uni.stopPullDownRefresh();
				}
			},
			// 跳转到添加页
			goToAdd() {
				uni.navigateTo({ url: '/pages/note/note' });
			},
			// 跳转到详情页 (编辑页)
			goToDetail(note) {
				// 1. 把当前点击的笔记数据，存到手机本地缓存里，方便下个页面取用
				    uni.setStorageSync('current_edit_note', note);
				    
				    // 2. 跳转，带上 id 只是为了标记是编辑模式
				    uni.navigateTo({ url: '/pages/note/note?id=' + note.id });

			},
			// 简单的日期格式化，截取一下让显示更短
			formatTime(timeStr) {
				if (!timeStr) return '';
				// 后端返回的是 2023-11-20 10:00:00，我们截取月日显示
				return timeStr.substring(5, 16); 
			}
		}
	}
</script>

<style>
	.container {
		padding: 30rpx;
		padding-bottom: 150rpx; /* 防止内容被底部按钮遮挡 */
	}

	/* 笔记卡片样式 */
	.note-item {
		background-color: #fff;
		border-radius: 16rpx;
		padding: 30rpx;
		margin-bottom: 24rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	.item-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16rpx;
	}
	.item-title {
		font-size: 34rpx;
		font-weight: bold;
		color: #333;
		flex: 1;
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis; /* 标题太长显示省略号 */
	}
	.item-time {
		font-size: 24rpx;
		color: #999;
		margin-left: 20rpx;
	}
	.item-content {
		font-size: 28rpx;
		color: #666;
		line-height: 1.5;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2; /* 最多显示2行 */
		overflow: hidden;
		margin-bottom: 20rpx;
	}
	.item-category {
		display: inline-block;
		background-color: #EBF5FF;
		color: #007AFF;
		font-size: 22rpx;
		padding: 4rpx 16rpx;
		border-radius: 8rpx;
	}

	/* 空状态 */
	.empty-state {
		margin-top: 200rpx;
		text-align: center;
	}
	.empty-text {
		color: #999;
		font-size: 28rpx;
	}

	/* 悬浮按钮 (Floating Action Button) */
	.fab-btn {
		position: fixed;
		right: 40rpx;
		bottom: 60rpx;
		width: 110rpx;
		height: 110rpx;
		background-color: #007AFF;
		border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 8rpx 20rpx rgba(0, 122, 255, 0.4);
		z-index: 99;
	}
	.fab-icon {
		color: #fff;
		font-size: 60rpx;
		margin-top: -8rpx; /* 微调位置 */
	}
</style>