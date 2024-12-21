<template>
  <div class="achievement-card" :class="{ 'locked': locked, 'completed': isCompleted }">
    <div class="achievement-icon">
      <span class="icon-emoji">{{ icon }}</span>
    </div>
    <div class="achievement-content">
      <div class="achievement-header">
        <h3 class="achievement-title">{{ title }}</h3>
        <span class="achievement-progress">{{ current }}/{{ total }}</span>
      </div>
      <p class="achievement-description">{{ description }}</p>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AchievementCard',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    current: {
      type: Number,
      default: 0
    },
    total: {
      type: Number,
      required: true
    },
    locked: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    progressPercentage() {
      return Math.min((this.current / this.total) * 100, 100)
    },
    isCompleted() {
      return this.current >= this.total
    }
  }
}
</script>

<style scoped>
.achievement-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  /* 添加边框 */
}

.achievement-icon {
  width: 48px;
  height: 48px;
  background: #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-emoji {
  font-size: 28px;
  line-height: 1;
}

.achievement-card.completed .icon-emoji {
  filter: none;
}

.achievement-content {
  flex: 1;
}

.achievement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.achievement-title {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.achievement-progress {
  font-size: 14px;
  color: #666;
}

.achievement-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #666;
}

.progress-bar {
  height: 6px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4CAF50;
  transition: width 0.3s ease;
}

/* 锁定状态样式 */
.achievement-card.completed {
  background: #f8fff8;
  /* 淡绿色背景 */
  border-color: #4CAF50;
  /* 绿色边框 */
}

/* 移除之前的渐变背景和文字颜色变化 */
.achievement-card.completed .achievement-title {
  color: #333;
}

.achievement-card.completed .achievement-progress,
.achievement-card.completed .achievement-description {
  color: #666;
}

.achievement-card.completed .achievement-icon {
  background: #e8f5e9;
  /* 淡绿色图标背景 */
}

.achievement-card.completed .progress-fill {
  background: #4CAF50;
  /* 保持进度条为绿色 */
}

/* 锁定状态样式 */
.achievement-card.locked {
  opacity: 0.6;
  filter: grayscale(100%);
}

/* 悬停效果 */
.achievement-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
