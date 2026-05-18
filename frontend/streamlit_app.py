#!/usr/bin/env python3
"""
AI旅行规划智能体 - Streamlit前端

这个模块提供基于Streamlit的Web前端界面，用户可以通过浏览器
与LangGraph多智能体旅行规划系统进行交互。

主要功能：
1. 用户友好的旅行规划表单
2. 实时显示规划进度
3. 展示多智能体协作结果
4. 下载规划报告
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="马小跳 — 智能旅行规划",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
def inject_custom_css():
    """注入自定义CSS样式 — 暖色调编辑风格"""
    st.markdown("""
    <style>
    /* ========== 字体导入 ========== */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

    /* ========== CSS变量 ========== */
    :root {
        --color-bg: #faf8f5;
        --color-surface: #ffffff;
        --color-text: #1a1a1a;
        --color-text-secondary: #6b6560;
        --color-text-muted: #9e9893;
        --color-accent: #c45d3e;
        --color-accent-hover: #a94d32;
        --color-accent-light: rgba(196, 93, 62, 0.08);
        --color-border: #e8e2db;
        --color-border-light: #f0ebe5;
        --color-warm-bg: #f5f0ea;
        --color-olive: #5a6b4a;
        --color-olive-light: rgba(90, 107, 74, 0.08);
        --font-display: 'Noto Serif SC', 'Songti SC', 'SimSun', serif;
        --font-body: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.06);
        --shadow-lg: 0 8px 32px rgba(0,0,0,0.08);
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ========== 全局基础 ========== */
    .stApp {
        background-color: var(--color-bg);
        background-attachment: fixed;
    }

    /* 去掉Streamlit默认的顶部装饰条 */
    header[data-testid="stHeader"] {
        background: transparent;
        height: 0;
    }

    /* 主内容区域 */
    .main .block-container {
        background: var(--color-surface);
        border-radius: var(--radius-lg);
        padding: 2.5rem 3rem;
        box-shadow: var(--shadow-md);
        position: relative;
        z-index: 1;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        max-width: 1200px;
        border: 1px solid var(--color-border-light);
    }

    /* ========== 侧边栏 ========== */
    section[data-testid="stSidebar"] {
        background: var(--color-surface);
        border-right: 1px solid var(--color-border-light);
    }

    /* 侧边栏所有文字 */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--color-text) !important;
        text-shadow: none !important;
    }

    /* Widget标签 — 统一颜色和大小 */
    section[data-testid="stSidebar"] label p {
        color: var(--color-text-secondary) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        font-family: var(--font-body) !important;
    }

    /* 输入框值文字 — 统一字体和大小 */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        background: transparent !important;
        color: var(--color-text) !important;
        border: none !important;
        border-bottom: 1px solid var(--color-border) !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        font-family: var(--font-body) !important;
        font-size: 0.9rem !important;
    }

    section[data-testid="stSidebar"] input:focus,
    section[data-testid="stSidebar"] textarea:focus {
        border-bottom-color: var(--color-accent) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* 下拉选择框 — 底部线风格 + 统一字体 */
    section[data-testid="stSidebar"] [data-baseweb="select"] {
        border: none !important;
        border-bottom: 1px solid var(--color-border) !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
        font-family: var(--font-body) !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"]:hover,
    section[data-testid="stSidebar"] [data-baseweb="select"]:focus-within {
        border-bottom-color: var(--color-accent) !important;
    }

    /* 下拉选项文字 */
    section[data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"],
    section[data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"],
    section[data-testid="stSidebar"] [data-baseweb="select"] [class*="valueContainer"] {
        font-family: var(--font-body) !important;
        font-size: 0.9rem !important;
        color: var(--color-text) !important;
    }

    /* 下拉弹出菜单 */
    section[data-testid="stSidebar"] [data-baseweb="popover"] {
        font-family: var(--font-body) !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="menu"] {
        font-family: var(--font-body) !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--color-border-light) !important;
        box-shadow: var(--shadow-md) !important;
        padding: 0.25rem !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="menu"] li {
        font-family: var(--font-body) !important;
        font-size: 0.85rem !important;
        color: var(--color-text) !important;
        border-radius: 4px !important;
        padding: 0.4rem 0.6rem !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="menu"] li:hover,
    section[data-testid="stSidebar"] [data-baseweb="menu"] li[aria-selected="true"] {
        background: var(--color-accent-light) !important;
        color: var(--color-accent) !important;
    }

    /* 日期选择器 — 底部线风格 */
    section[data-testid="stSidebar"] [data-testid="stDateInput"] > div {
        border: none !important;
        border-bottom: 1px solid var(--color-border) !important;
        border-radius: 0 !important;
        background: transparent !important;
    }

    section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
        background: transparent !important;
        border: none !important;
        font-family: var(--font-body) !important;
        font-size: 0.9rem !important;
    }

    /* 数字输入框 — 底部线风格 */
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] > div {
        border: none !important;
        border-bottom: 1px solid var(--color-border) !important;
        border-radius: 0 !important;
        background: transparent !important;
    }

    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background: transparent !important;
        border: none !important;
        font-family: var(--font-body) !important;
        font-size: 0.9rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 复选框文字 */
    section[data-testid="stSidebar"] .stCheckbox label p {
        color: var(--color-text-secondary) !important;
        font-size: 0.85rem !important;
        font-family: var(--font-body) !important;
    }

    /* 侧边栏分隔线 */
    section[data-testid="stSidebar"] hr {
        border: none;
        border-top: 1px solid var(--color-border-light);
        margin: 0.75rem 0;
    }

    /* 侧边栏按钮 */
    section[data-testid="stSidebar"] .stButton > button {
        background: var(--color-text) !important;
        color: var(--color-surface) !important;
        font-weight: 600;
        font-family: var(--font-body) !important;
        border-radius: var(--radius-sm) !important;
        border: none !important;
        transition: var(--transition);
        width: 100%;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: var(--color-accent) !important;
        transform: translateY(-1px);
        box-shadow: var(--shadow-sm);
    }

    /* 侧边栏列间距 */
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
    }

    /* ========== 标题排版 ========== */
    h1 {
        font-family: var(--font-display) !important;
        color: var(--color-text) !important;
        font-weight: 700 !important;
        text-align: left !important;
        font-size: 2.2rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
        -webkit-text-fill-color: var(--color-text) !important;
    }

    .main h2 {
        color: var(--color-text) !important;
        font-weight: 600 !important;
        font-family: var(--font-display) !important;
        font-size: 1.4rem !important;
        letter-spacing: -0.01em;
    }

    .main h3 {
        color: var(--color-text) !important;
        font-weight: 600 !important;
        font-family: var(--font-body) !important;
        font-size: 1rem !important;
    }

    .main h4 {
        color: var(--color-text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ========== 按钮 ========== */
    .stButton > button {
        background: var(--color-text) !important;
        color: var(--color-surface) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        font-family: var(--font-body) !important;
        transition: var(--transition);
        box-shadow: none !important;
        letter-spacing: 0.02em;
    }

    .stButton > button:hover {
        background: var(--color-accent) !important;
        transform: translateY(-1px);
        box-shadow: var(--shadow-sm) !important;
    }

    /* 主要按钮 */
    .stButton > button[kind="primary"] {
        background: var(--color-accent) !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--color-accent-hover) !important;
    }

    /* 次要按钮 */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--color-text) !important;
        border: 1px solid var(--color-border) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: var(--color-accent) !important;
        color: var(--color-accent) !important;
    }

    /* ========== 卡片 ========== */
    .feature-card {
        background: var(--color-surface);
        border-radius: var(--radius-md);
        padding: 1.75rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
        border: 1px solid var(--color-border-light);
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--color-border);
    }

    /* ========== 画廊 ========== */
    .gallery-item {
        position: relative;
        overflow: hidden;
        border-radius: var(--radius-md);
        height: 220px;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
        cursor: pointer;
    }

    .gallery-item:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }

    .gallery-item:hover img {
        transform: scale(1.04);
    }

    .gallery-item img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .gallery-caption {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(26, 26, 26, 0.85) 0%, transparent 100%);
        color: white;
        padding: 2rem 1.2rem 1.2rem 1.2rem;
        font-weight: 500;
        font-size: 0.9rem;
        font-family: var(--font-body);
        letter-spacing: 0.01em;
    }

    /* ========== 状态消息 — 统一暖色调 ========== */

    /* 通用alert基础 */
    .stAlert {
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.85rem 1.1rem !important;
        font-family: var(--font-body) !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
        box-shadow: none !important;
    }

    .stAlert p {
        font-family: var(--font-body) !important;
        font-size: 0.88rem !important;
    }

    /* 成功 — 橄榄绿调 */
    .stSuccess,
    div[data-testid="stNotification"] .stSuccess {
        background-color: rgba(90, 107, 74, 0.06) !important;
        border-left: 3px solid var(--color-olive) !important;
        color: var(--color-text) !important;
    }

    .stSuccess svg {
        color: var(--color-olive) !important;
    }

    /* 错误 — 赤陶色 */
    .stError,
    div[data-testid="stNotification"] .stError {
        background-color: rgba(196, 93, 62, 0.06) !important;
        border-left: 3px solid var(--color-accent) !important;
        color: var(--color-text) !important;
    }

    .stError svg {
        color: var(--color-accent) !important;
    }

    /* 信息 — 暖灰调 */
    .stInfo,
    div[data-testid="stNotification"] .stInfo {
        background-color: var(--color-warm-bg) !important;
        border-left: 3px solid var(--color-border) !important;
        color: var(--color-text-secondary) !important;
    }

    .stInfo svg {
        color: var(--color-text-muted) !important;
    }

    /* 警告 — 柔和暖调 */
    .stWarning,
    div[data-testid="stNotification"] .stWarning {
        background-color: rgba(196, 93, 62, 0.04) !important;
        border-left: 3px solid rgba(196, 93, 62, 0.3) !important;
        color: var(--color-text-secondary) !important;
    }

    .stWarning svg {
        color: rgba(196, 93, 62, 0.5) !important;
    }

    /* ========== 自定义进度组件 ========== */
    .travel-progress-card {
        background: var(--color-warm-bg);
        border: 1px solid var(--color-border-light);
        border-radius: var(--radius-md);
        padding: 1.5rem 1.75rem;
        margin: 1rem 0;
    }

    .tp-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.25rem;
    }

    .tp-label {
        font-family: var(--font-display);
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--color-text-secondary);
        letter-spacing: 0.08em;
    }

    .tp-percent {
        font-family: var(--font-body);
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--color-accent);
    }

    .tp-track {
        background: var(--color-border-light);
        border-radius: 100px;
        height: 5px;
        overflow: hidden;
        margin-bottom: 1.25rem;
    }

    .tp-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #c45d3e 0%, #d4836e 100%);
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .tp-fill.tp-pulse {
        animation: tp-glow 2s ease-in-out infinite;
    }

    @keyframes tp-glow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    .tp-steps {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.25rem;
        padding: 0 0.25rem;
    }

    .tp-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.4rem;
        position: relative;
        z-index: 1;
    }

    .tp-step-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--color-border);
        transition: var(--transition);
        flex-shrink: 0;
    }

    .tp-step.tp-done .tp-step-dot {
        background: var(--color-olive);
    }

    .tp-step.tp-active .tp-step-dot {
        background: var(--color-accent);
        box-shadow: 0 0 0 3px rgba(196, 93, 62, 0.15);
        animation: tp-dot-pulse 2s ease-in-out infinite;
    }

    @keyframes tp-dot-pulse {
        0%, 100% { box-shadow: 0 0 0 3px rgba(196, 93, 62, 0.15); }
        50% { box-shadow: 0 0 0 6px rgba(196, 93, 62, 0.06); }
    }

    .tp-step-label {
        font-family: var(--font-body);
        font-size: 0.65rem;
        color: var(--color-text-muted);
        white-space: nowrap;
        transition: var(--transition);
    }

    .tp-step.tp-done .tp-step-label {
        color: var(--color-olive);
    }

    .tp-step.tp-active .tp-step-label {
        color: var(--color-accent);
        font-weight: 500;
    }

    .tp-connector {
        flex: 1;
        height: 1px;
        background: var(--color-border);
        margin: 0 -0.25rem;
        margin-bottom: 1.2rem;
        transition: background 0.5s ease;
    }

    .tp-connector.tp-done {
        background: var(--color-olive);
    }

    .tp-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .tp-status-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--color-accent);
        animation: tp-dot-blink 1.5s ease-in-out infinite;
        flex-shrink: 0;
    }

    @keyframes tp-dot-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .tp-status-text {
        font-family: var(--font-body);
        font-size: 0.78rem;
        color: var(--color-text-secondary);
        transition: opacity 0.3s ease;
    }

    .tp-done-check {
        color: var(--color-olive);
        font-size: 0.75rem;
    }

    /* ========== Spinner ========== */
    .stSpinner > div {
        border-color: var(--color-accent) transparent transparent transparent !important;
    }

    /* ========== 输入框 ========== */
    .stTextInput > div > div > input {
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-body) !important;
        transition: var(--transition);
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--color-accent) !important;
        box-shadow: 0 0 0 3px var(--color-accent-light) !important;
    }

    /* ========== Textarea ========== */
    .stTextArea textarea {
        font-size: 1rem !important;
        line-height: 1.7 !important;
        padding: 1rem !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--color-border) !important;
        font-family: var(--font-body) !important;
        transition: var(--transition);
        background: var(--color-bg) !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--color-accent) !important;
        box-shadow: 0 0 0 3px var(--color-accent-light) !important;
    }

    .stTextArea textarea::placeholder {
        color: var(--color-text-muted) !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* ========== 页脚 ========== */
    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        color: var(--color-text-muted);
        font-size: 0.8rem;
        margin-top: 2rem;
        border-top: 1px solid var(--color-border-light);
        font-family: var(--font-body);
        letter-spacing: 0.02em;
    }

    /* ========== Hero区域 ========== */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem 3.5rem 2rem;
        background: var(--color-bg);
        border-radius: var(--radius-lg);
        margin-bottom: 2.5rem;
        border: 1px solid var(--color-border-light);
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(ellipse at 30% 20%, rgba(196, 93, 62, 0.04) 0%, transparent 60%),
                    radial-gradient(ellipse at 70% 80%, rgba(90, 107, 74, 0.04) 0%, transparent 60%);
        pointer-events: none;
    }

    .hero-section > * {
        position: relative;
        z-index: 1;
    }

    .hero-badge {
        display: inline-block;
        background: var(--color-accent-light);
        color: var(--color-accent);
        padding: 0.4rem 1rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        font-family: var(--font-body);
        border: 1px solid rgba(196, 93, 62, 0.12);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--color-text);
        font-family: var(--font-display);
        letter-spacing: -0.03em;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--color-text-secondary);
        margin-bottom: 0;
        line-height: 1.8;
        max-width: 560px;
        margin-left: auto;
        margin-right: auto;
        font-family: var(--font-body);
        font-weight: 400;
    }

    /* ========== 自然语言输入区域 ========== */
    .chat-input-container {
        background: var(--color-bg);
        border-radius: var(--radius-lg);
        padding: 2rem;
        border: 1px solid var(--color-border);
        margin: 2rem 0;
        transition: var(--transition);
    }

    .chat-input-container:hover {
        border-color: var(--color-accent);
    }

    /* ========== 快捷示例 ========== */
    .example-chips {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
        margin: 1.5rem 0 2rem 0;
    }

    .example-chip {
        background: var(--color-surface);
        color: var(--color-text-secondary);
        padding: 0.5rem 1rem;
        border-radius: 100px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: var(--transition);
        border: 1px solid var(--color-border);
        font-family: var(--font-body);
    }

    .example-chip:hover {
        border-color: var(--color-accent);
        color: var(--color-accent);
        background: var(--color-accent-light);
    }

    /* ========== 侧边栏品牌 ========== */
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid var(--color-border-light);
        margin-bottom: 1.5rem;
    }

    .sidebar-brand-title {
        font-family: var(--font-display);
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--color-text);
        margin: 0.5rem 0 0.2rem 0;
        letter-spacing: -0.02em;
    }

    .sidebar-brand-sub {
        font-family: var(--font-body);
        font-size: 0.7rem;
        color: var(--color-text-muted);
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    /* ========== 分隔标题 ========== */
    .section-header {
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--color-border-light);
    }

    .section-header h2 {
        margin: 0 !important;
        font-family: var(--font-display) !important;
    }

    .section-header p {
        color: var(--color-text-muted);
        font-size: 0.85rem;
        margin-top: 0.3rem;
        font-family: var(--font-body);
    }

    /* ========== 步骤指示器 ========== */
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        background: var(--color-accent-light);
        color: var(--color-accent);
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 1rem;
        font-family: var(--font-display);
        border: 1px solid rgba(196, 93, 62, 0.15);
    }

    /* ========== 智能体卡片 ========== */
    .agent-card {
        background: var(--color-bg);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        border: 1px solid var(--color-border-light);
        transition: var(--transition);
        height: 100%;
    }

    .agent-card:hover {
        border-color: var(--color-border);
        box-shadow: var(--shadow-sm);
    }

    .agent-card-icon {
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }

    .agent-card h4 {
        font-family: var(--font-body) !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: var(--color-text) !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        margin-bottom: 0.4rem !important;
    }

    .agent-card p {
        font-size: 0.82rem;
        color: var(--color-text-muted);
        line-height: 1.6;
        margin: 0;
    }

    /* ========== Expander ========== */
    .streamlit-expanderHeader {
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: var(--color-text) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ========== Selectbox ========== */
    .stSelectbox > div > div {
        border-radius: var(--radius-sm) !important;
    }

    /* ========== Metric ========== */
    [data-testid="stMetric"] {
        background: var(--color-bg);
        border: 1px solid var(--color-border-light);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
    }

    [data-testid="stMetric"] label {
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--color-text-muted) !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: var(--color-text) !important;
    }

    /* ========== 收起全部Streamlit默认空白 ========== */
    .block-container {
        padding-top: 1rem !important;
    }

    /* ========== 平滑滚动 ========== */
    html {
        scroll-behavior: smooth;
    }

    /* ========== 下载按钮 ========== */
    .stDownloadButton > button {
        background: var(--color-surface) !important;
        color: var(--color-text) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.85rem !important;
        font-family: var(--font-body) !important;
        transition: var(--transition);
    }

    .stDownloadButton > button:hover {
        border-color: var(--color-accent) !important;
        color: var(--color-accent) !important;
    }

    /* ========== Radio / Checkbox 优化 ========== */
    .stRadio label, .stCheckbox label {
        font-family: var(--font-body) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# API基础URL
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://192.168.172.128:8080")

def check_api_health():
    """检查API服务状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=15)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"API服务返回错误状态: {response.status_code}"}
    except requests.exceptions.Timeout:
        return False, {"error": "API请求超时，后端服务可能正在启动中，请稍等片刻后刷新页面"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "无法连接到API服务器，请确保后端服务已启动 (运行: ./start_backend.sh)"}
    except Exception as e:
        return False, {"error": f"连接错误: {str(e)}"}

def create_travel_plan(travel_data: Dict[str, Any]) -> Optional[str]:
    """创建旅行规划任务"""
    try:
        response = requests.post(f"{API_BASE_URL}/plan", json=travel_data, timeout=60)
        if response.status_code == 200:
            return response.json()["task_id"]
        else:
            st.error(f"创建任务失败: {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("创建任务超时，请稍后重试")
        return None
    except requests.exceptions.ConnectionError:
        st.error("无法连接到API服务器，请确保后端服务已启动")
        return None
    except Exception as e:
        st.error(f"API请求失败: {str(e)}")
        return None

def get_planning_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取规划状态"""
    max_retries = 3
    for retry in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=60)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                st.warning(f"任务 {task_id} 不存在")
                return None
            else:
                if retry < max_retries - 1:
                    time.sleep(3)
                else:
                    st.error(f"获取状态失败: HTTP {response.status_code}")
                    return None
        except requests.exceptions.Timeout:
            if retry < max_retries - 1:
                time.sleep(3)
            else:
                return None
        except requests.exceptions.ConnectionError:
            st.error("无法连接到后端服务，请确保后端服务已启动")
            return None
        except Exception as e:
            if retry < max_retries - 1:
                time.sleep(3)
            else:
                st.error(f"获取状态失败: {str(e)}")
                return None
    return None

def get_planning_result(task_id: str) -> Optional[Dict[str, Any]]:
    """获取规划结果 - 从状态查询中获取结果"""
    try:
        status_info = get_planning_status(task_id)
        if status_info and status_info.get("result"):
            return status_info["result"]
        else:
            st.warning("结果尚未准备好或任务未完成")
            return None
    except Exception as e:
        st.error(f"获取结果失败: {str(e)}")
        return None

def generate_markdown_report(result: Dict[str, Any], task_id: str) -> str:
    """生成Markdown格式的旅行规划报告"""
    if not result:
        return "# 旅行规划报告\n\n无可用数据"

    travel_plan = result.get("travel_plan", {})
    agent_outputs = result.get("agent_outputs", {})

    destination = travel_plan.get("destination", "未知")
    duration = travel_plan.get("duration", 0)
    group_size = travel_plan.get("group_size", 0)
    budget_range = travel_plan.get("budget_range", "未知")
    interests = travel_plan.get("interests", [])
    travel_dates = travel_plan.get("travel_dates", "未知")

    markdown_content = f"""# {destination}旅行规划报告

## 规划概览

| 项目 | 详情 |
|------|------|
| 目的地 | {destination} |
| 旅行时间 | {travel_dates} |
| 行程天数 | {duration}天 |
| 团队人数 | {group_size}人 |
| 预算类型 | {budget_range} |
| 兴趣爱好 | {', '.join(interests) if interests else '无特殊偏好'} |

---

## AI智能体专业建议

"""

    agent_names_cn = {
        'travel_advisor': '旅行顾问',
        'weather_analyst': '天气分析师',
        'budget_optimizer': '预算优化师',
        'local_expert': '当地专家',
        'itinerary_planner': '行程规划师'
    }

    for agent_name, output in agent_outputs.items():
        agent_display_name = agent_names_cn.get(agent_name, agent_name)
        status = output.get('status', '未知')
        response = output.get('response', '无输出')
        timestamp = output.get('timestamp', '')

        markdown_content += f"""### {agent_display_name}

**状态**: {status.upper()}
**完成时间**: {timestamp[:19] if timestamp else '未知'}

{response}

---

"""

    from datetime import datetime
    markdown_content += f"""## 报告信息

- **任务ID**: `{task_id}`
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **生成方式**: LangGraph多智能体AI系统
- **报告格式**: Markdown

---

*本报告由AI旅行规划智能体自动生成*
"""

    return markdown_content


def save_report_to_results(content: str, filename: str) -> str:
    """保存Markdown报告到results目录"""
    import os

    results_dir = "../results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    file_path = os.path.join(results_dir, filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    except Exception as e:
        st.error(f"保存文件失败: {str(e)}")
        return None


def build_travel_progress_html(percent: int, message: str, agent: str = "", done: bool = False):
    """构建暖色调旅行规划进度组件 HTML"""
    steps = [
        {"label": "初始化", "threshold": 10},
        {"label": "启动系统", "threshold": 30},
        {"label": "智能分析", "threshold": 50},
        {"label": "多智能体协作", "threshold": 60},
        {"label": "完成", "threshold": 100},
    ]

    def step_class(threshold):
        if percent >= threshold:
            return "tp-step tp-done"
        if percent >= threshold * 0.5:
            return "tp-step tp-active"
        return "tp-step"

    dots_html = ""
    for i, s in enumerate(steps):
        dots_html += f'<div class="{step_class(s["threshold"])}"><div class="tp-step-dot"></div><span class="tp-step-label">{s["label"]}</span></div>'
        if i < len(steps) - 1:
            conn_class = "tp-connector tp-done" if percent >= steps[i + 1]["threshold"] else "tp-connector"
            dots_html += f'<div class="{conn_class}"></div>'

    if done:
        status_html = '<div class="tp-status"><span class="tp-done-check">&#10003;</span><span class="tp-status-text">规划完成</span></div>'
        fill_class = "tp-fill"
    else:
        status_text = f"{agent}　·　{message}" if agent else message
        status_html = f'<div class="tp-status"><div class="tp-status-dot"></div><span class="tp-status-text">{status_text}</span></div>'
        fill_class = "tp-fill tp-pulse"

    return f"""
    <div class="travel-progress-card">
        <div class="tp-header">
            <span class="tp-label">AI 智能规划中</span>
            <span class="tp-percent">{percent}%</span>
        </div>
        <div class="tp-track"><div class="{fill_class}" style="width: {percent}%"></div></div>
        <div class="tp-steps">{dots_html}</div>
        {status_html}
    </div>
    """


def display_hero_section():
    """显示Hero区域"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">AI Multi-Agent System</div>
        <h1 class="hero-title">马小跳</h1>
        <p class="hero-subtitle">
            六位专业 AI 智能体协同工作，<br/>
            为您量身定制完美旅程
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_chat_interface():
    """显示自然语言交互界面"""
    st.markdown("""
    <div class="section-header">
        <h2>描述你的旅行想法</h2>
        <p>用自然语言告诉马小跳你的需求，AI会自动为你规划</p>
    </div>
    """, unsafe_allow_html=True)

    # 输入框
    user_input = st.text_area(
        "自然语言输入",
        placeholder="例如：我想下周去北京玩3天，预算3000元，喜欢历史文化...\n\n你可以详细描述旅行需求，包括目的地、时间、预算、兴趣偏好等",
        key="chat_input",
        height=200,
        label_visibility="collapsed"
    )

    # 快捷示例按钮
    st.markdown('<div class="example-chips">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    examples = [
        "北京3日游，历史文化",
        "杭州周末游，2人，预算中等",
        "成都美食之旅，5天",
        "上海亲子游，一家三口"
    ]

    clicked_example = None

    with col1:
        if st.button(examples[0], key="ex1", use_container_width=True):
            clicked_example = examples[0]
    with col2:
        if st.button(examples[1], key="ex2", use_container_width=True):
            clicked_example = examples[1]
    with col3:
        if st.button(examples[2], key="ex3", use_container_width=True):
            clicked_example = examples[2]
    with col4:
        if st.button(examples[3], key="ex4", use_container_width=True):
            clicked_example = examples[3]

    st.markdown('</div>', unsafe_allow_html=True)

    # 处理输入
    input_to_process = clicked_example if clicked_example else user_input

    if input_to_process:
        with st.spinner("正在理解你的需求..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={"message": input_to_process},
                    timeout=30
                )

                if response.status_code == 200:
                    chat_response = response.json()

                    st.markdown("#### 马小跳回复")
                    st.info(chat_response["clarification"])

                    if chat_response["can_proceed"] and chat_response.get("task_id"):
                        task_id = chat_response["task_id"]
                        st.success(f"任务已创建　{task_id}")

                        st.session_state.current_task_id = task_id
                        st.session_state.planning_started = True
                        st.rerun()

                    if chat_response["extracted_info"]:
                        with st.expander("已识别的信息"):
                            for key, value in chat_response["extracted_info"].items():
                                st.write(f"**{key}**: {value}")

                    if chat_response["missing_info"]:
                        with st.expander("还需要补充的信息"):
                            for item in chat_response["missing_info"]:
                                st.write(f"- {item}")
                else:
                    st.error(f"请求失败: {response.status_code}")

            except requests.exceptions.Timeout:
                st.info("任务创建中，请稍候...")
            except Exception as e:
                st.error(f"发生错误: {str(e)}")


def display_features_section():
    """显示功能特色区域"""
    st.markdown("""
    <div class="section-header">
        <h2>为什么选择马小跳</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    features = [
        ("多智能体协作", "6 个专业 AI 智能体协同工作，覆盖旅行规划的每一个环节"),
        ("个性化定制", "根据兴趣、预算和偏好，量身定制专属旅行方案"),
        ("快速高效", "几分钟内完成专业旅行规划，不再为做攻略烦恼"),
        ("专业报告", "生成详细的规划报告，支持 Markdown 和 JSON 下载"),
    ]

    for i, (title, desc) in enumerate(features):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="feature-card">
                <h4 style="margin-bottom: 0.5rem;">{title}</h4>
                <p style="color: var(--color-text-muted); font-size: 0.85rem; line-height: 1.7; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)


def display_world_gallery():
    """显示世界各地风光画廊"""
    st.markdown("""
    <div class="section-header">
        <h2>探索世界之美</h2>
        <p>让 AI 带你发现世界各地的精彩</p>
    </div>
    """, unsafe_allow_html=True)

    destinations = [
        {"name": "巴黎", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&h=400&fit=crop"},
        {"name": "富士山", "url": "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=600&h=400&fit=crop"},
        {"name": "圣托里尼", "url": "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=600&h=400&fit=crop"},
        {"name": "阿尔卑斯", "url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=600&h=400&fit=crop"},
        {"name": "马尔代夫", "url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=600&h=400&fit=crop"},
        {"name": "纽约", "url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=600&h=400&fit=crop"},
        {"name": "罗马", "url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=600&h=400&fit=crop"},
        {"name": "巴厘岛", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop"},
    ]

    # 第一行
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.markdown(f"""
            <div class="gallery-item">
                <img src="{destinations[i]['url']}" alt="{destinations[i]['name']}">
                <div class="gallery-caption">{destinations[i]['name']}</div>
            </div>
            """, unsafe_allow_html=True)

    # 第二行
    cols = st.columns(4)
    for i in range(4, 8):
        with cols[i - 4]:
            st.markdown(f"""
            <div class="gallery-item">
                <img src="{destinations[i]['url']}" alt="{destinations[i]['name']}">
                <div class="gallery-caption">{destinations[i]['name']}</div>
            </div>
            """, unsafe_allow_html=True)


def display_footer():
    """显示页脚"""
    st.markdown("""
    <div class="footer">
        <p style="font-size: 0.85rem; color: var(--color-text-secondary); margin-bottom: 0.5rem; font-family: var(--font-display);">
            马小跳
        </p>
        <p>
            LangGraph 多智能体系统驱动 · FastAPI + Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_planning_result(result: Dict[str, Any]):
    """显示规划结果"""
    if not result:
        return

    st.markdown("""
    <div class="section-header">
        <h2>规划结果</h2>
    </div>
    """, unsafe_allow_html=True)

    travel_plan = result.get("travel_plan", {})
    agent_outputs = result.get("agent_outputs", {})

    if travel_plan:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("目的地", travel_plan.get("destination", "未知"))
            st.metric("行程天数", f"{travel_plan.get('duration', 0)}天")
        with col2:
            st.metric("团队人数", f"{travel_plan.get('group_size', 0)}人")
            st.metric("预算类型", travel_plan.get("budget_range", "未知"))
        with col3:
            interests = travel_plan.get("interests", [])
            st.metric("兴趣爱好", f"{len(interests)}项")
            if interests:
                st.write("、".join(interests))

    if agent_outputs:
        st.markdown("#### AI 智能体建议")

        agent_names_cn = {
            'travel_advisor': '旅行顾问',
            'weather_analyst': '天气分析师',
            'budget_optimizer': '预算优化师',
            'local_expert': '当地专家',
            'itinerary_planner': '行程规划师',
            'simple_agent': 'AI规划师',
            'mock_agent': '模拟规划师'
        }

        for agent_name, output in agent_outputs.items():
            agent_display_name = agent_names_cn.get(agent_name, agent_name)
            status = output.get('status', '未知')
            response = output.get('response', '无输出')

            with st.expander(f"{agent_display_name} · {status.upper()}", expanded=True):
                st.text_area("建议内容", value=response, height=200, disabled=True,
                           key=f"agent_{agent_name}", label_visibility="collapsed")


def main():
    """主函数"""
    # 注入自定义CSS样式
    inject_custom_css()

    # 显示Hero区域
    display_hero_section()

    # 显示自然语言交互界面
    display_chat_interface()

    # 侧边栏
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">马小跳</div>
            <div class="sidebar-brand-sub">Travel Smart Agent</div>
        </div>
        """, unsafe_allow_html=True)

        # 基本信息
        destination = st.text_input("目的地", placeholder="例如：北京、上海、成都")

        # 日期选择
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("出发日期", value=date.today() + timedelta(days=1))
        with col2:
            end_date = st.date_input("返回日期", value=date.today() + timedelta(days=8))

        # 团队信息
        group_size = st.number_input("团队人数", min_value=1, max_value=20, value=2)

        st.markdown("<hr/>", unsafe_allow_html=True)

        # 偏好设置
        budget_range = st.selectbox("预算范围", [
            "经济型 (300-800元/天)",
            "舒适型 (800-1500元/天)",
            "中等预算 (1500-3000元/天)",
            "高端旅行 (3000-6000元/天)",
            "奢华体验 (6000元以上/天)"
        ])

        accommodation = st.selectbox("住宿偏好", [
            "经济型酒店/青旅",
            "商务酒店",
            "精品酒店",
            "民宿/客栈",
            "度假村",
            "奢华酒店"
        ])

        transportation = st.selectbox("交通偏好", [
            "公共交通为主",
            "混合交通方式",
            "租车自驾",
            "包车/专车",
            "高铁/飞机"
        ])

        st.markdown("<hr/>", unsafe_allow_html=True)

        # 旅游偏好 — 两列布局，更宽松
        st.markdown('<p style="font-size: 0.85rem; font-weight: 600; color: var(--color-text-secondary); margin: 0 0 0.4rem 0;">旅游偏好</p>', unsafe_allow_html=True)
        interests = []

        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("历史文化"):
                interests.append("历史文化")
            if st.checkbox("美食体验"):
                interests.append("美食体验")
            if st.checkbox("自然风光"):
                interests.append("自然风光")
            if st.checkbox("艺术表演"):
                interests.append("艺术表演")
            if st.checkbox("海滨度假"):
                interests.append("海滨度假")
            if st.checkbox("购物娱乐"):
                interests.append("购物娱乐")
            if st.checkbox("运动健身"):
                interests.append("运动健身")
            if st.checkbox("摄影打卡"):
                interests.append("摄影打卡")

        with col2:
            if st.checkbox("休闲放松"):
                interests.append("休闲放松")
            if st.checkbox("主题乐园"):
                interests.append("主题乐园")
            if st.checkbox("登山徒步"):
                interests.append("登山徒步")
            if st.checkbox("文艺创作"):
                interests.append("文艺创作")
            if st.checkbox("品酒美食"):
                interests.append("品酒美食")
            if st.checkbox("博物馆"):
                interests.append("博物馆")
            if st.checkbox("夜生活"):
                interests.append("夜生活")

        st.markdown("<br/>", unsafe_allow_html=True)

        # 提交按钮
        if st.button("开始规划", type="primary", use_container_width=True):
            if not destination:
                st.error("请输入目的地")
            elif start_date >= end_date:
                st.error("返回日期必须晚于出发日期")
            else:
                travel_data = {
                    "destination": destination,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "group_size": group_size,
                    "budget_range": budget_range,
                    "interests": interests,
                    "accommodation_preference": accommodation,
                    "transportation_preference": transportation,
                    "currency": "CNY"
                }

                st.session_state.travel_data = travel_data
                st.session_state.planning_started = True
                st.rerun()

    # 手动查询结果功能
    with st.expander("手动查询任务结果", expanded=False):
        st.markdown("如果之前的规划任务超时，可以在这里手动查询结果")

        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            manual_task_id = st.text_input("输入任务ID", placeholder="例如: task_20250807_123456")
            if st.button("查询结果", type="secondary", use_container_width=True):
                if manual_task_id:
                    st.session_state.manual_query_task_id = manual_task_id
                    st.session_state.show_manual_result = True
                else:
                    st.warning("请输入任务ID")

    # 在expander外部显示查询结果
    if hasattr(st.session_state, 'show_manual_result') and st.session_state.show_manual_result:
        manual_task_id = st.session_state.manual_query_task_id

        st.markdown("---")

        with st.spinner("正在查询结果..."):
            result = get_planning_result(manual_task_id)
            if result:
                _, result_col, _ = st.columns([0.5, 3, 0.5])
                with result_col:
                    st.success("找到结果")
                    display_planning_result(result)

                    st.markdown("""
                    <div class="section-header">
                        <h2>下载报告</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)

                    with col1:
                        download_url = f"{API_BASE_URL}/download/{manual_task_id}"
                        st.markdown(f"[JSON 格式数据]({download_url})")
                        st.caption("包含完整的 AI 分析数据")

                    with col2:
                        travel_plan = result.get("travel_plan", {})
                        destination = travel_plan.get("destination", "未知目的地").replace("/", "-").replace("\\", "-")
                        group_size = travel_plan.get("group_size", 1)
                        filename_base = f"{destination}-{group_size}人-旅行规划指南"

                        markdown_content = generate_markdown_report(result, manual_task_id)
                        md_filename = f"{filename_base}.md"
                        saved_md_path = save_report_to_results(markdown_content, md_filename)

                        st.download_button(
                            label="下载 Markdown 报告",
                            data=markdown_content,
                            file_name=md_filename,
                            mime="text/markdown"
                        )

                        if saved_md_path:
                            st.success(f"报告已保存到: {saved_md_path}")

                    if st.button("关闭结果", use_container_width=True):
                        st.session_state.show_manual_result = False
                        st.rerun()
            else:
                _, error_col, _ = st.columns([1, 2, 1])
                with error_col:
                    st.error("未找到该任务的结果")
                    if st.button("重新查询", use_container_width=True):
                        st.session_state.show_manual_result = False
                        st.rerun()

    # 主内容区域
    if hasattr(st.session_state, 'planning_started') and st.session_state.planning_started:
        if hasattr(st.session_state, 'current_task_id'):
            task_id = st.session_state.current_task_id
        else:
            travel_data = st.session_state.travel_data

            # 构建出行需求卡片
            fields = [
                ("目的地", travel_data.get("destination", "—")),
                ("出发日期", travel_data.get("start_date", "—")),
                ("返回日期", travel_data.get("end_date", "—")),
                ("出行人数", str(travel_data.get("group_size", "—")) + " 人"),
                ("预算范围", travel_data.get("budget_range", "—")),
            ]

            row_style = 'style="display:flex; justify-content:space-between; padding: 0.55rem 0; border-bottom: 1px solid #f0ebe5;"'
            label_style = 'style="font-size: 0.8rem; color: #9e9893;"'
            value_style = 'style="font-size: 0.8rem; color: #1a1a1a; font-weight: 500;"'
            rows_html = "".join(
                f'<div {row_style}><span {label_style}>{lb}</span><span {value_style}>{vl}</span></div>'
                for lb, vl in fields
            )

            interests = travel_data.get("interests", [])
            if interests:
                if isinstance(interests, str):
                    interests = [interests]
                tag_style = 'style="display:inline-block; background: rgba(196,93,62,0.08); color: #c45d3e; font-size: 0.72rem; padding: 0.15rem 0.55rem; border-radius: 100px; margin: 0.15rem;"'
                tags_html = " ".join(f'<span {tag_style}>{t}</span>' for t in interests)
                rows_html += (
                    f'<div style="padding: 0.55rem 0;">'
                    f'<span style="font-size: 0.8rem; color: #9e9893; display:block; margin-bottom: 0.35rem;">兴趣偏好</span>'
                    f'<div style="display:flex; flex-wrap:wrap; gap: 0.3rem;">{tags_html}</div>'
                    f'</div>'
                )

            card_html = (
                '<div style="background: #f5f0ea; border: 1px solid #f0ebe5; border-radius: 12px; '
                'padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;">'
                '<div style="font-family: \'Noto Serif SC\', serif; font-size: 0.82rem; font-weight: 600; '
                'color: #6b6560; letter-spacing: 0.06em; margin-bottom: 0.75rem;">出行需求</div>'
                f'{rows_html}'
                '</div>'
            )

            st.markdown(card_html, unsafe_allow_html=True)

            with st.spinner("正在创建规划任务..."):
                task_id = create_travel_plan(travel_data)

        if task_id:
            st.markdown(f"""
            <div style="background: var(--color-warm-bg); border: 1px solid var(--color-border-light); border-radius: var(--radius-md); padding: 0.75rem 1rem; margin-bottom: 1rem;">
                <span style="font-size: 0.75rem; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.04em;">任务已创建</span><br/>
                <code style="font-size: 0.82rem; color: var(--color-text); background: none; padding: 0;">{task_id}</code>
            </div>
            """, unsafe_allow_html=True)

            progress_placeholder = st.empty()

            max_attempts = 60
            attempt = 0
            last_progress = 0

            while attempt < max_attempts:
                status_info = get_planning_status(task_id)

                if status_info:
                    status = status_info.get("status", "unknown")
                    progress = status_info.get("progress", 0)
                    message = status_info.get("message", "处理中...")
                    current_agent = status_info.get("current_agent", "")

                    progress_placeholder.markdown(
                        build_travel_progress_html(progress, message, current_agent),
                        unsafe_allow_html=True,
                    )

                    if progress > last_progress:
                        last_progress = progress
                        attempt = 0

                    if status == "completed":
                        progress_placeholder.markdown(
                            build_travel_progress_html(100, "规划完成", done=True),
                            unsafe_allow_html=True,
                        )

                        result = status_info.get("result")
                        if result:
                            display_planning_result(result)

                            st.markdown("""
                            <div class="section-header">
                                <h2>下载报告</h2>
                            </div>
                            """, unsafe_allow_html=True)

                            col1, col2 = st.columns(2)

                            with col1:
                                download_url = f"{API_BASE_URL}/download/{task_id}"
                                st.markdown(f"[JSON 格式数据]({download_url})")
                                st.caption("包含完整的 AI 分析数据")

                            with col2:
                                travel_plan = result.get("travel_plan", {})
                                destination = travel_plan.get("destination", "未知目的地").replace("/", "-").replace("\\", "-")
                                group_size = travel_plan.get("group_size", 1)
                                filename_base = f"{destination}-{group_size}人-旅行规划指南"

                                markdown_content = generate_markdown_report(result, task_id)
                                md_filename = f"{filename_base}.md"
                                saved_md_path = save_report_to_results(markdown_content, md_filename)

                                st.download_button(
                                    label="下载 Markdown 报告",
                                    data=markdown_content,
                                    file_name=md_filename,
                                    mime="text/markdown"
                                )

                                if saved_md_path:
                                    st.success(f"报告已保存到: {saved_md_path}")

                        break

                    elif status == "failed":
                        error_msg = status_info.get("error", "未知错误")
                        progress_placeholder.empty()
                        st.error(f"规划失败: {error_msg}")
                        break

                    elif status in ["processing", "running", "pending"]:
                        time.sleep(5)
                        attempt += 1

                    else:
                        time.sleep(5)
                        attempt += 1
                else:
                    attempt += 1
                    if attempt < max_attempts:
                        progress_placeholder.markdown(
                            build_travel_progress_html(0, f"处理中　·　{attempt}/{max_attempts}"),
                            unsafe_allow_html=True,
                        )
                        time.sleep(5)
                    else:
                        st.error("无法获取任务状态")
                        break

            if attempt >= max_attempts:
                progress_placeholder.empty()
                st.warning("规划超时，后端可能仍在处理中")
                st.info("你可以稍后刷新页面查看结果，或重新提交规划请求")
        else:
            st.error("创建规划任务失败")

    else:
        # 显示功能特色区域
        display_features_section()

        # 智能体团队介绍
        st.markdown("""
        <div class="section-header">
            <h2>AI 智能体团队</h2>
            <p>六位专业智能体协同工作，覆盖旅行规划的每一个细节</p>
        </div>
        """, unsafe_allow_html=True)

        agents = [
            ("travel", "旅行顾问", "目的地概览、景点推荐和旅行建议"),
            ("weather", "天气分析师", "天气状况分析、穿衣指南和最佳出行时间"),
            ("budget", "预算优化师", "合理预算分配，确保每一分钱花得物有所值"),
            ("local", "当地地道专家", "地道餐厅、体验和隐藏景点推荐"),
            ("plan", "行程规划师", "详细日程安排、路线优化"),
            ("coord", "协调员", "统筹各智能体工作，整合最优方案"),
        ]

        cols = st.columns(3)
        for i, (_, name, desc) in enumerate(agents):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="agent-card">
                    <h4>{name}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # 使用指南
        st.markdown("""
        <div class="section-header">
            <h2>三步开启智能旅行规划</h2>
        </div>
        """, unsafe_allow_html=True)

        steps = [
            ("01", "填写需求", "在左侧表单中填写目的地、日期、预算和兴趣偏好"),
            ("02", "AI 智能规划", "点击开始规划，智能体团队将几分钟内生成专属方案"),
            ("03", "下载报告", "获取详细的规划报告，支持 Markdown 和 JSON 格式"),
        ]

        cols = st.columns(3)
        for i, (num, title, desc) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="feature-card" style="text-align: center;">
                    <div class="step-number">{num}</div>
                    <h4 style="margin-bottom: 0.5rem;">{title}</h4>
                    <p style="color: var(--color-text-muted); font-size: 0.85rem; line-height: 1.7; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # 世界风光画廊
        display_world_gallery()

    # 显示页脚
    display_footer()


if __name__ == "__main__":
    main()
