// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 创建飘落花瓣
    createPetals();
    
    // 启动打字机效果
    typeWriter();
    
    // 绑定按钮事件
    bindButtonEvents();
    
    // 绑定卡片事件
    bindCardEvents();
    
    // 绑定弹窗事件
    bindModalEvents();
});

// 创建飘落花瓣
function createPetals() {
    const petalsContainer = document.getElementById('petals');
    const petalCount = 30;
    
    for (let i = 0; i < petalCount; i++) {
        const petal = document.createElement('div');
        petal.className = 'petal';
        
        // 随机位置
        petal.style.left = Math.random() * 100 + '%';
        
        // 随机大小
        const size = Math.random() * 15 + 10;
        petal.style.width = size + 'px';
        petal.style.height = size + 'px';
        
        // 随机动画时长
        const duration = Math.random() * 5 + 5;
        petal.style.animationDuration = duration + 's';
        
        // 随机动画延迟
        const delay = Math.random() * 5;
        petal.style.animationDelay = delay + 's';
        
        // 随机颜色
        const colors = ['#ffb6c1', '#ffc0cb', '#ff69b4', '#ff1493', '#db7093'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        petal.style.background = `linear-gradient(45deg, ${color}, #ffc0cb)`;
        
        petalsContainer.appendChild(petal);
    }
}

// 打字机效果
function typeWriter() {
    const text = '在这个特别的日子里，愿每一位女性都能绽放属于自己的光芒，勇敢追梦，活出精彩人生！';
    const element = document.getElementById('typingText');
    let index = 0;
    
    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, 100);
        }
    }
    
    // 延迟开始打字效果
    setTimeout(type, 1000);
}

// 祝福语数组
const wishes = [
    '愿你眼里总有光芒，手里总有鲜花，愿你成为自己的太阳！',
    '愿你的生活常温暖，日子总是温柔又闪光！',
    '愿你无惧时光，优雅到老，深情地美下去！',
    '愿你拥有好运气，一生努力，一生被爱！',
    '愿你所有的情深意重，都能换来岁月温柔！',
    '愿你成为自己的女王，不卑不亢，不慌不忙！'
];

// 绑定按钮事件
function bindButtonEvents() {
    const wishBtn = document.getElementById('wishBtn');
    
    wishBtn.addEventListener('click', function(e) {
        // 创建爱心粒子效果
        createHeartParticles(e.clientX, e.clientY);
        
        // 显示弹窗
        showModal();
    });
    
    // 鼠标悬停效果
    wishBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.05)';
    });
    
    wishBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
}

// 创建爱心粒子效果
function createHeartParticles(x, y) {
    const hearts = ['💖', '💕', '💗', '💓', '💝'];
    const particleCount = 8;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.textContent = hearts[Math.floor(Math.random() * hearts.length)];
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.fontSize = (Math.random() * 20 + 20) + 'px';
        
        // 随机方向
        const angle = (Math.PI * 2 * i) / particleCount;
        const distance = Math.random() * 100 + 50;
        const tx = Math.cos(angle) * distance;
        const ty = Math.sin(angle) * distance;
        
        particle.style.setProperty('--tx', tx + 'px');
        particle.style.setProperty('--ty', ty + 'px');
        
        document.body.appendChild(particle);
        
        // 动画结束后移除
        setTimeout(() => {
            particle.remove();
        }, 1000);
    }
}

// 绑定卡片事件
function bindCardEvents() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            // 添加光晕效果
            this.style.filter = 'brightness(1.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.filter = 'brightness(1)';
        });
        
        // 点击卡片翻转
        card.addEventListener('click', function() {
            const inner = this.querySelector('.card-inner');
            inner.style.transform = inner.style.transform === 'rotateY(180deg)' 
                ? 'rotateY(0deg)' 
                : 'rotateY(180deg)';
        });
    });
}

// 显示弹窗
function showModal() {
    const modal = document.getElementById('modal');
    const modalText = document.getElementById('modalText');
    
    // 随机选择祝福语
    const randomWish = wishes[Math.floor(Math.random() * wishes.length)];
    modalText.textContent = randomWish;
    
    modal.classList.add('active');
    
    // 创建庆祝效果
    createCelebration();
}

// 创建庆祝效果
function createCelebration() {
    const colors = ['#ff6b9d', '#c44569', '#f8b500', '#ffb6c1', '#ff69b4'];
    const celebrationCount = 20;
    
    for (let i = 0; i < celebrationCount; i++) {
        setTimeout(() => {
            const x = Math.random() * window.innerWidth;
            const y = window.innerHeight / 2;
            createHeartParticles(x, y);
        }, i * 100);
    }
}

// 绑定弹窗事件
function bindModalEvents() {
    const modal = document.getElementById('modal');
    const closeBtn = document.getElementById('closeBtn');
    const modalBtn = document.getElementById('modalBtn');
    
    // 关闭按钮
    closeBtn.addEventListener('click', hideModal);
    
    // 确认按钮
    modalBtn.addEventListener('click', hideModal);
    
    // 点击背景关闭
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            hideModal();
        }
    });
    
    // ESC 键关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            hideModal();
        }
    });
}

// 隐藏弹窗
function hideModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('active');
}

// 页面滚动视差效果
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.flowers');
    const speed = 0.5;
    
    if (parallax) {
        parallax.style.transform = `translateY(${scrolled * speed}px)`;
    }
});

// 鼠标跟随效果
document.addEventListener('mousemove', function(e) {
    const flowers = document.querySelectorAll('.flower');
    const mouseX = e.clientX / window.innerWidth - 0.5;
    const mouseY = e.clientY / window.innerHeight - 0.5;
    
    flowers.forEach((flower, index) => {
        const speed = (index + 1) * 10;
        const x = mouseX * speed;
        const y = mouseY * speed;
        
        flower.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// 添加页面加载动画
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});
