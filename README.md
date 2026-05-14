# 🌍 AI旅行规划智能体 (AI Trip Planner Agent)

一个基于LangGraph多智能体协作的智能旅行规划系统，由 OpenAI 兼容大模型（ChatOpenAI）与 DuckDuckGo 搜索驱动。

## 🏗️ 系统架构

### 整体架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   LangGraph     │
│   前端界面      │◄──►│   后端API       │◄──►│   多智能体系统  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 技术栈
- **前端**: Streamlit (Python Web框架)
- **后端**: FastAPI (高性能异步API框架)
- **AI引擎**: LangGraph (多智能体协作框架)
- **大语言模型**: ChatOpenAI（OpenAI 兼容接口，可接入 DeepSeek、通义千问等）
- **搜索服务**: DuckDuckGo实时搜索
- **数据存储**: JSON文件存储 + 内存缓存
- **部署**: Docker容器化 + 可选的Kubernetes

## 🤖 AI智能体团队

### 核心智能体
1. **🎯 协调员智能体** - 工作流编排与决策综合
2. **✈️ 旅行顾问** - 目的地专业知识与实时搜索
3. **💰 预算优化师** - 成本分析与实时定价
4. **🌤️ 天气分析师** - 天气情报与当前数据
5. **🏠 当地专家** - 内部知识与实时本地信息
6. **📅 行程规划师** - 日程优化与物流安排

### 智能体协作流程

#### 简化流程
```
用户请求 → 协调员 → 并行执行各专业智能体 → 结果整合 → 生成报告
```

#### 详细工作流程图

```mermaid
graph TB
    Start([用户发起旅行规划请求]) --> Init[初始化TravelPlanState<br/>设置目的地、预算、兴趣等]
    Init --> Coordinator[协调员智能体<br/>_coordinator_agent]
    
    Coordinator --> CoordRouter{协调员路由器<br/>_coordinator_router<br/>决定下一步}
    
    CoordRouter -->|需要旅行建议| TravelAdvisor[旅行顾问智能体<br/>_travel_advisor_agent<br/>提供景点、文化洞察]
    CoordRouter -->|需要天气分析| WeatherAnalyst[天气分析师智能体<br/>_weather_analyst_agent<br/>分析天气、活动规划]
    CoordRouter -->|需要预算优化| BudgetOptimizer[预算优化师智能体<br/>_budget_optimizer_agent<br/>成本分析、省钱策略]
    CoordRouter -->|需要本地知识| LocalExpert[当地专家智能体<br/>_local_expert_agent<br/>小众景点、文化贴士]
    CoordRouter -->|需要行程安排| ItineraryPlanner[行程规划师智能体<br/>_itinerary_planner_agent<br/>日程优化、物流安排]
    CoordRouter -->|需要搜索信息| Tools[工具执行节点<br/>_tool_executor_node]
    CoordRouter -->|所有智能体完成| Compile[编译最终计划<br/>_compile_final_plan]
    
    TravelAdvisor --> AgentRouter1{智能体路由器<br/>_agent_router}
    WeatherAnalyst --> AgentRouter2{智能体路由器<br/>_agent_router}
    BudgetOptimizer --> AgentRouter3{智能体路由器<br/>_agent_router}
    LocalExpert --> AgentRouter4{智能体路由器<br/>_agent_router}
    ItineraryPlanner --> AgentRouter5{智能体路由器<br/>_agent_router}
    
    AgentRouter1 -->|需要搜索| Tools
    AgentRouter2 -->|需要搜索| Tools
    AgentRouter3 -->|需要搜索| Tools
    AgentRouter4 -->|需要搜索| Tools
    AgentRouter5 -->|需要搜索| Tools
    
    AgentRouter1 -->|完成任务| Coordinator
    AgentRouter2 -->|完成任务| Coordinator
    AgentRouter3 -->|完成任务| Coordinator
    AgentRouter4 -->|完成任务| Coordinator
    AgentRouter5 -->|完成任务| Coordinator
    
    Tools --> ToolDecision{智能工具选择}
    ToolDecision -->|天气查询| SearchWeather[search_weather_info<br/>获取天气预报]
    ToolDecision -->|景点查询| SearchAttractions[search_attractions<br/>搜索景点活动]
    ToolDecision -->|预算查询| SearchBudget[search_budget_info<br/>查询费用信息]
    ToolDecision -->|住宿查询| SearchHotels[search_hotels<br/>搜索酒店]
    ToolDecision -->|餐饮查询| SearchRestaurants[search_restaurants<br/>搜索餐厅]
    ToolDecision -->|本地贴士| SearchLocalTips[search_local_tips<br/>获取本地信息]
    ToolDecision -->|通用查询| SearchDestination[search_destination_info<br/>目的地信息]
    
    SearchWeather --> ToolReturn[返回搜索结果到消息历史]
    SearchAttractions --> ToolReturn
    SearchBudget --> ToolReturn
    SearchHotels --> ToolReturn
    SearchRestaurants --> ToolReturn
    SearchLocalTips --> ToolReturn
    SearchDestination --> ToolReturn
    
    ToolReturn --> Coordinator
    
    Compile --> Result{检查智能体输出}
    Result -->|整合所有建议| FinalPlan[生成最终旅行计划<br/>包含各智能体贡献]
    
    FinalPlan --> End([返回完整旅行计划])
```

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
# 使用 Docker Compose 启动（自动构建前后端镜像）
docker compose up --build

# 后台启动
docker compose up -d --build

# 查看日志
docker compose logs -f backend
docker compose logs -f frontend

# 停止服务
docker compose down
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

## 🙏 致谢

- OpenAI / ChatOpenAI 团队及各大 OpenAI 兼容模型服务商
- DuckDuckGo提供的实时搜索服务
- LangGraph团队的多智能体框架
- Streamlit和FastAPI的优秀框架支持

---

**注意**: 本系统需要稳定的网络连接和有效的API密钥才能正常工作。首次使用请确保完成所有配置步骤。
