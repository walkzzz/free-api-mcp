# Free API MCP Server 扩展计划

## 🎯 新增API服务规划

### 🎮 娱乐类API
1. **随机猫咪图片** - TheCatAPI
2. **随机狗狗图片** - TheDogAPI  
3. **随机表情包** - Meme API
4. **随机事实** - Useless Facts API
5. **今日历史** - Today in History API

### 🔧 实用工具API
6. **二维码生成** - QR Code API
7. **短链接生成** - TinyURL API
8. **颜色信息** - Color API
9. **随机密码生成** - Password Generator
10. **UUID生成器** - UUID API

### 🌍 地理位置API
11. **国家信息** - REST Countries API
12. **时区查询** - WorldTimeAPI
13. **ISS位置** - ISS Location API
14. **地震信息** - Earthquake API

### 📚 知识类API
15. **随机诗词** - Poetry API
16. **英语单词** - Dictionary API
17. **数学计算** - Math API
18. **随机名言** - Quotable (已有，可扩展)

### 🎨 创意类API
19. **随机头像** - Avatars API
20. **占位图片** - Placeholder Images
21. **渐变色** - Gradient API
22. **随机用户** - Random User API

### 🔍 查询类API
23. **域名信息** - Domain Info API
24. **GitHub用户** - GitHub API
25. **网站截图** - Screenshot API
26. **URL预览** - Link Preview API

## 🏗️ 实现策略

### 阶段1: 娱乐和实用工具 (优先)
- 随机图片类API (猫、狗、表情包)
- 二维码和短链接生成
- 随机事实和历史

### 阶段2: 地理和知识类
- 国家信息和时区
- 诗词和词典API
- ISS和地震信息

### 阶段3: 创意和查询类
- 头像和占位图片
- 域名和GitHub查询
- 网站相关API

## 📁 文件结构扩展

```
src/services/
├── entertainment_service.py  # 娱乐类API
├── utility_service.py       # 实用工具API
├── geography_service.py     # 地理位置API
├── knowledge_service.py     # 知识类API
├── creative_service.py      # 创意类API
└── query_service.py         # 查询类API
```

## 🎯 目标

- 从15个工具扩展到40+个工具
- 保持现有的容错和备用机制
- 确保所有新API都是免费的
- 提供有趣和实用的功能组合