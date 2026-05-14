FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 禁用SSL证书验证（企业代理/防火墙自签名证书场景）
# 影响范围：pip、curl、Python requests/httpx 等所有HTTPS请求
ENV CURL_CA_BUNDLE=""
ENV REQUESTS_CA_BUNDLE=""
ENV SSL_CERT_FILE=""

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
# 添加 --trusted-host 解决 SSL 证书验证失败问题（公司代理/防火墙场景）
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.python.org \
    -r requirements.txt

# 复制应用代码
COPY . .

# 创建results目录
RUN mkdir -p results

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 启动命令
CMD ["python", "api_server.py"]
