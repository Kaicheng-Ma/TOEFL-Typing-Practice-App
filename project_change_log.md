# 项目变更日志

## 2026-06-21

### 初始化阶段

1. 创建 TOEFL Typing Practice App 的本地 git 仓库。
2. 绑定 GitHub 远程仓库 `https://github.com/Kaicheng-Ma/TOEFL-Typing-Practice-App.git`。
3. 新建本地专用制作指导文件 `LOCAL_IMPLEMENTATION_GUIDE.md`，用于后续全部实现工作的统一依据。
4. 新建根目录变更日志 `project_change_log.md`，用于持续记录项目层级的关键修改。
5. 新建 `.gitignore`，排除 Python 常见构建产物，并排除本地专用指导文件，避免其进入对外仓库。

### 设计概念

1. 明确项目主目标为 TOEFL 输入训练，而非单纯打字练习。
2. 确认核心功能包含作文打字、词汇拼写、计时挑战三条主线。
3. 确认素材来源以邮件、学术讨论、TOEFL 高频词汇与高频表达为主。
4. 确认内容生成采用“受约束随机 + 去重 + 错误回流”的方式，避免固定练习文本。

### 分阶段制作

1. 将后续开发拆分为 Stage 0 到 Stage 6。
2. 将项目骨架、作文打字、词汇拼写、计时挑战、个性化回流、统计体验分别拆成独立阶段。
3. 明确每个 stage 都需要对应的目标、产出和完成标准，避免一次性展开过多内容。

### README 编写

1. 新建并完善仓库对外 README。
2. 在 README 中说明项目定位、核心模式、内容来源和当前状态。
3. 在 README 中保留本地制作指导文件的引用，方便后续按同一套规则推进实现。

### Stage 1 骨架落地

1. 新建 `pyproject.toml` 作为 Python 项目入口配置。
2. 新建 `src/toefl_typing_practice_app/` 包结构。
3. 新建应用配置、数据模型、路径工具、主窗口与启动入口。
4. 使用 `python -m compileall src` 进行了基础语法验证，确认模块可被正常编译。
