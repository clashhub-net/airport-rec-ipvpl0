# 机场推荐与代理工具导航完全指南

> 📡 本仓库整理优质机场推荐、代理协议深度解析、Clash 分流规则与订阅转换工具，帮助用户找到高速稳定、低延迟、抗封锁的科学上网方案。
>
> **关键词**：机场推荐、代理协议对比、VLESS、VMess、Trojan、Hysteria2、Clash规则、订阅转换、流媒体解锁、科学上网

---

## 📖 目录

- [机场 vs 自建 VPS](#-机场-vs-自建-vps)
- [代理协议深度解析](#-代理协议深度解析)
- [优质机场推荐标准](#-优质机场推荐标准)
- [工具箱](#-工具箱)
- [分流规则使用指南](#-分流规则使用指南)
- [订阅转换教程](#-订阅转换教程)
- [常见问题](#-常见问题)

---

## 🌐 机场 vs 自建 VPS

| 对比项 | 机场 | 自建 VPS |
|--------|------|----------|
| **价格** | ¥15-50/月 | $3-10/月 |
| **上手难度** | 零配置，订阅即用 | 需要选购、安装、维护 |
| **稳定性** | 依赖机场商诚信 | 完全自主可控 |
| **速度** | 多节点负载均衡 | 取决于线路质量 |
| **抗封锁** | 中等（机场负责） | 较高（可随时换IP） |
| **适用场景** | 日常浏览、视频、游戏 | 高性能需求、建站 |

**结论**：
- 日常使用 → 选优质机场（省心省力）
- 技术能力较强 / 需要更高自由度 → 自建 VPS
- 两者结合（机场做备用）→ 最佳方案

---

## 🔐 代理协议深度解析

### 主流协议对比表

| 协议 | 速度 | 稳定性 | 抗封锁 | 配置难度 | 推荐场景 |
|------|------|--------|--------|----------|----------|
| **VLESS + XTLS/TLS** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中等 | 主流推荐 |
| **Trojan** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中等 | 深度伪装 |
| **Hysteria2 (Hy2)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 较复杂 | 高带宽需求 |
| **VMess** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 中等 | 通用场景 |
| **Shadowsocks (SS)** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 简单 | 备选/轻度使用 |

### 各协议详细说明

#### VLESS + XTLS/TLS（⭐⭐⭐⭐⭐ 推荐）

**优势**：
- 基于 TLS 1.3，流量与正常 HTTPS 网站几乎无法区分
- 抗封锁能力极强
- 支持 WebSocket 传输，可套 CDN（Cloudflare）
- 无需同步时间（解决了 VMess 的时钟漂移问题）

**推荐配置（Clash）**：
```yaml
proxies:
  - name: "VLESS-TLS"
    type: vless
    server: your-server.com
    port: 443
    uuid: <your-uuid>
    network: ws
    tls: true
    servername: your-server.com
    ws-opts:
      path: /vless
      headers:
        Host: your-server.com
```

#### Hysteria2（⭐⭐⭐⭐⭐ 高带宽推荐）

**优势**：
- 基于 QUIC 协议，峰值速度可达带宽上限
- 抗丢包能力强（中国网络环境优势明显）
- 配置简单，支持 ACME 自动申请证书

**适用场景**：大文件下载、4K 视频、直播推流

#### Trojan（⭐⭐⭐⭐ 经典方案）

**优势**：
- 模拟真实 HTTPS 流量，反向代理思维
- 成熟稳定，社区生态完善
- 配合 Nginx/V2Ray 使用效果最佳

---

## ⭐ 优质机场推荐标准

### 选购机场的 7 个核心指标

| 指标 | 说明 | 权重 |
|------|------|------|
| **线路类型** | IPLC/IEPL 专线 > 入口优化 > 普通线路 | 30% |
| **节点数量** | 至少 10+ 节点，覆盖主要地区 | 15% |
| **月流量** | 最低 300GB/月，建议 500GB+ | 20% |
| **协议支持** | 必须支持 VLESS/Trojan，Hy2 加分 | 15% |
| **退款政策** | 至少 24-48 小时退款保证 | 10% |
| **口碑历史** | 运营 1 年以上，无跑路记录 | 10% |

### 警惕！这类机场不要买

❌ 月付价格低于 ¥10 且自称"高速"的
❌ 只支持 SS/SSR 协议的（已被深度识别）
❌ 无退款政策、运营不到半年的
❌ 限制同时在线设备数的（体验极差）
❌ 节点 IP 段被大量封禁的

---

## 🛠️ 工具箱

### 文件说明

| 文件 | 说明 | 适用场景 |
|------|------|----------|
| `sub-convert.py` | 订阅链接解析、过滤、格式转换 | 节点筛选、格式转换 |
| `rules.yaml` | Clash 分流规则（广告屏蔽/国内直连/流媒体） | 全局规则管理 |
| `adblock.txt` | 广告+追踪器域名黑名单 | 广告屏蔽 |
| `direct.txt` | 国内直连域名列表 | 优化国内网站访问 |

### sub-convert.py 使用方法

```bash
# 解析订阅并输出为 Clash 格式
python3 sub-convert.py --url "你的订阅链接" --format clash

# 关键词过滤（如只保留美国节点）
python3 sub-convert.py --url "你的订阅链接" --keyword "US" --format clash
```

---

## 📋 分流规则使用指南

### 分流原理

Clash 的分流规则通过 `rules.yaml` 定义，匹配逻辑为从上到下逐一匹配，**第一个命中的规则决定走哪个出口**。

### 推荐分流策略

```
全球加速 → 国内直连 → 广告屏蔽 → 流媒体专属 → 默认代理
```

### 常用规则类型

| 规则类型 | 说明 | 示例 |
|----------|------|------|
| `DOMAIN-SUFFIX` | 域名后缀匹配 | `DOMAIN-SUFFIX,netflix.com` |
| `DOMAIN-KEYWORD` | 域名关键词匹配 | `DOMAIN-KEYWORD,google` |
| `IP-CIDR` | IP 段匹配 | `IP-CIDR,10.0.0.0/8` |
| `GEOIP` | 国家 IP 库匹配 | `GEOIP,CN`（中国 IP 直连） |
| `PROCESS-NAME` | 进程名匹配 | `PROCESS-NAME,Telegram` |

### 推荐规则顺序

```yaml
rules:
  # 1. 广告拦截（最先匹配，节省流量）
  - DOMAIN-SUFFIX,doubleclick.net,REJECT

  # 2. 国内直连（节省代理流量）
  - DOMAIN-SUFFIX,cn,DIRECT
  - DOMAIN-SUFFIX,baidu.com,DIRECT
  - IP-CIDR,10.0.0.0/8,DIRECT
  - IP-CIDR,172.16.0.0/12,DIRECT
  - GEOIP,CN,DIRECT

  # 3. 特定应用走代理（即使域名看起来是国内）
  - PROCESS-NAME,Telegram,Proxy

  # 4. 流媒体优先匹配
  - DOMAIN-SUFFIX,netflix.com,Netflix
  - DOMAIN-SUFFIX,youtube.com,YouTube

  # 5. 默认代理
  - MATCH,Proxy
```

---

## 🔄 订阅转换教程

### 什么是订阅转换？

订阅转换（Sub Convert）是指将机场提供的原始订阅链接，转换为兼容 Clash/V2Ray 等客户端的格式，同时支持过滤、筛选、节点排序等操作。

### 常用订阅转换服务

| 服务 | 特点 | 链接 |
|------|------|------|
| **Subconverter** | 开源自建，支持所有格式 | https://sub.v1.mk |
| **ACL4SSR** | 社区维护，规则齐全 | https://acl4ssr-sub.github.io |

### 使用示例（Subconverter）

```
https://sub.v1.mk/sub?target=clash&url=<你的订阅链接>&insert=true&exclude=广告&sort=true
```

参数说明：
- `target`: 输出格式（clash/v2ray/trojan）
- `url`: 你的机场订阅链接（需 URL 编码）
- `insert`: 是否插入自己的节点
- `exclude`: 排除关键词（多个用 `&` 分隔）
- `sort`: 是否按节点名排序

---

## ❓ 常见问题

### Q1：节点延迟低但速度慢是怎么回事？

延迟（ping）≠ 带宽（speed）。可能是：
- 机场入口带宽小
- 晚高峰多人使用
- 机场限速策略

**建议**：同时测试多个节点的带宽表现，不要只看延迟。

### Q2：如何判断机场是否跑路前兆？

🚨 以下情况需警惕：
- 突然无法访问官网（可能正在迁移）
- 无法充值，只能消耗存量
- 客服消失，工单无回应
- 节点数量急剧减少
- 价格异常涨价

**建议**：长用机场至少保留一个备用方案。

### Q3：Clash Premium 和 Clash Meta 有什么区别？

| 对比 | Clash Premium | Clash Meta |
|------|--------------|------------|
| 维护者 | Dreamacro | MetaCubeX |
| 规则语法 | 基础 | 扩展（支持脚本） |
| 代理协议 | 较少 | 支持 Hy2/TUIC 等新协议 |
| 社区活跃度 | 一般 | 活跃（推荐） |

**推荐**：新用户直接使用 **Clash Verge** 或 **Stash**（基于 Clash Meta）。

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| 🏠 ClashHub 规则集 | [https://clashhub.net](https://clashhub.net) |
| 📥 Clash for Windows | [https://clash-for-windows.net](https://clash-for-windows.net) |
| 🧭 导航站 | [https://nav.clashvip.net](https://nav.clashvip.net) |
| 🖥️ VPS选购指南 | [https://vpsvip.net](https://vpsvip.net) |
| 💬 ClashHub 论坛 | [https://bbs.clashhub.net](https://bbs.clashhub.net) |

---

*本仓库由 [ClashHub](https://clashhub.net) 维护 · 更新时间：2026-04-17*
*欢迎 ⭐ Star，你的支持是我持续更新的动力！*
