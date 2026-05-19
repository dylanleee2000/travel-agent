## 🚀 快速开始

### 环境要求
- Python 3.10+
- 8GB+ RAM (推荐16GB)
- 稳定的网络连接

### 1. 克隆项目
```bash
git clone https://github.com/your-username/travel-agent.git
cd travel-agent
```

### 2. 安装依赖
```bash
# 安装后端依赖
pip install -r backend/requirements.txt

# 安装前端依赖
pip install -r frontend/requirements.txt
```

### 3. 配置环境变量
```bash
# 创建环境变量文件
cd backend
cp env.example .env

# 编辑环境变量
vim .env
```

必需的环境变量：
```bash
OPENAI_API_KEY=your_openai_style_api_key
OPENAI_BASE_URL=https://api.deepseek.com/v1  # 可按需调整
OPENAI_MODEL=deepseek-chat                  # 可按需调整
```

可选服务（用于MCP天气服务器）：
```bash
QWEATHER_API_KEY=your_qweather_api_key
QWEATHER_API_BASE=https://api.qweather.com
```

### 4. 启动服务

#### 方法1: 使用启动脚本
```bash
# 启动脚本添加执行权限
chmod +x start_*.sh
# 启动后端服务
./start_backend.sh

# 启动前端服务
./start_frontend.sh
```

#### 方法2: 手动启动
```bash
# 启动后端
cd backend
python api_server.py

# 启动前端 (新终端)
cd frontend
streamlit run streamlit_app.py
```

### 5. 访问应用
- **前端界面**: http://localhost:8501
- **后端API**: http://localhost:8080
- **API文档**: http://localhost:8080/docs
- **健康检查**: http://localhost:8080/health

## 📋 使用说明

### 1. 填写旅行需求
在左侧表单中输入：
- 🎯 目的地城市
- 📅 出发和返回日期
- 👥 团队人数
- 💰 预算范围
- 🏨 住宿偏好
- 🚗 交通偏好
- 🎨 兴趣爱好

### 2. 开始AI规划
点击"🚀 开始规划"按钮，系统将：
- 创建规划任务
- 启动多智能体协作
- 实时显示处理进度
- 生成个性化旅行计划

### 3. 查看结果
- 📊 实时进度监控
- 🤖 各智能体专业建议
- 📄 详细规划报告
- �� 多种格式下载

## 🔧 故障排除

### 常见问题

#### 1. Docker构建时SSL证书验证失败
**症状**: `pip install` 报 `[SSL: CERTIFICATE_VERIFY_FAILED]`
**原因**: 企业代理/防火墙使用自签名证书
**解决方案**: Dockerfile 中已添加 `--trusted-host` 参数和环境变量 `CURL_CA_BUNDLE=""`

#### 2. LLM API连接失败
**症状**: 规划任务返回"未知错误"，后端日志 `APIConnectionError`
**原因**: Docker容器内SSL证书验证失败或模型名错误
**解决方案**:
- 确认 `.env` 中模型名大小写正确（如 `mimo-v2.5-pro` 而非 `MiMo-V2.5-Pro`）
- 检查 `CURL_CA_BUNDLE=""` 环境变量是否已设置

#### 3. 请求超时问题
**症状**: 前端显示"任务执行中..."
**原因**: 网络延迟或后端处理时间较长
**解决方案**: 
- 等待几分钟后刷新页面
- 使用手动查询功能
- 检查网络连接

#### 4. 后端连接失败
**症状**: "后端服务连接失败"
**解决方案**:
```bash
# 检查后端服务状态
curl http://localhost:8080/health

# 重启后端服务
./start_backend.sh
```

#### 5. API密钥错误
**症状**: "API认证失败"
**解决方案**:
- 检查环境变量设置
- 验证API密钥有效性
- 确认API配额充足

## 🚀 部署选项

### Docker部署（推荐使用 Compose）
```bash
# 1. 配置环境
cp backend/env.example backend/.env
# 编辑.env文件

# 2. 一键启动（Docker方式）
docker-compose up -d

# 3. 访问Web界面
# http://localhost:8501
```

## 📊 系统监控

### 日志文件
- **后端日志**: `backend/logs/backend.log`

### 健康检查
```bash
# 检查服务状态
curl http://localhost:8080/health

# 查看任务状态
curl http://localhost:8080/status/{task_id}
```

## 📁 项目结构

```
travel-agent/
├── backend/                    # 后端服务
│   ├── agents/                 # 智能体模块
│   │   ├── langgraph_agents.py # LangGraph多智能体系统
│   │   └── simple_travel_agent.py  # 简化版智能体
│   ├── config/                 # 配置模块
│   │   └── langgraph_config.py # LLM和搜索配置
│   ├── tools/                  # 工具模块
│   │   ├── travel_tools.py     # 旅行搜索工具
│   │   ├── weather_client_mcp.py   # MCP天气客户端
│   │   └── weather_server_mcp.py   # MCP天气服务器
│   ├── api_server.py           # FastAPI服务入口
│   ├── Dockerfile              # 后端Docker镜像
│   └── requirements.txt        # Python依赖
├── frontend/                   # 前端服务
│   ├── streamlit_app.py        # Streamlit应用
│   ├── Dockerfile              # 前端Docker镜像
│   └── requirements.txt        # Python依赖
├── docs/                       # 文档
│   └── img/                    # 架构图
├── docker-compose.yml          # Docker Compose配置
└── README.md                   # 项目说明
```

## 📄 许可证

MIT License


**注意**: 本系统需要稳定的网络连接和有效的API密钥才能正常工作。首次使用请确保完成所有配置步骤。