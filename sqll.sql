-- 创建数据库
CREATE DATABASE IF NOT EXISTS health_app DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE health_app;

-- 运动记录表
CREATE TABLE IF NOT EXISTS exercise (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    steps INT NOT NULL,
    stride_length FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    intensity VARCHAR(20),
    exercise_types VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 睡眠记录表
CREATE TABLE IF NOT EXISTS sleep (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    sleep_time TIME NOT NULL,
    wake_time TIME NOT NULL,
    quality VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 经期记录表
CREATE TABLE IF NOT EXISTS period (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE,
    flow VARCHAR(20) NOT NULL,
    symptoms VARCHAR(200),
    mood VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 体重记录表
CREATE TABLE IF NOT EXISTS weight (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    current_weight FLOAT NOT NULL,
    target_weight FLOAT,
    body_fat_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BMI 记录表
CREATE TABLE IF NOT EXISTS bmi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    bmi_value FLOAT,  -- 可选：前端可根据公式 weight/(height/100)^2 计算后保存
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 饮水记录表
CREATE TABLE IF NOT EXISTS drink (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    water_intake FLOAT NOT NULL,  -- 单位：升
    target FLOAT,                 -- 目标饮水量（升）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 心率记录表
CREATE TABLE IF NOT EXISTS heart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    average_rate INT NOT NULL,  -- 平均心率值
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);