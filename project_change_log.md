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

### README 英文化与扩展

1. 将仓库 README 重写为英文版本。
2. 扩充 README 中的项目定位、核心模式、内容策略、开发阶段、运行方式和后续计划说明。
3. 保留本地制作指导文件的引用，确保 README 与本地实施规则保持一致。

### Stage 2 作文打字主流程

1. 新建 `content/essay_generator.py`，用于从邮件、学术讨论、校园生活等主题池中动态生成作文练习文本。
2. 新建 `services/typing_analysis.py`，用于计算输入文本与目标文本的基础准确率、typo 数量和 WPM。
3. 新建 `ui/essay_practice.py`，用于提供作文打字练习界面、提示展示、实时统计和提交结果。
4. 重写 `ui/main_window.py`，让主界面能够在作文打字、词汇拼写和计时挑战之间切换，并默认展示作文打字模式。
5. 扩展 `models.py`，加入作文提示和文本比对结果等核心数据结构。
6. 使用 `python -m compileall src` 验证新增代码可正常编译，确认 Stage 2 主链路已跑通。
### Stage 3 璇嶆眹妯″紡鍩虹灞?
1. 鎵╁睍 `models.py` 锛屽姞鍏ユ爣鍑嗙殑璇嶆眹棰樼洰鍜屾祴璇曠粨鏋勩€?
2. 鏂板缓 `content/vocabulary_bank.py` 锛屼负璇嶆眹鎷煎啓妯″紡鎻愪緵涓婚鍖栥€佸彲杞崲鐨勯搴撱€?
3. 鏂板缓 `services/vocabulary_scoring.py` 锛屼负鑷姩鍒ゆ柇鍜岃緭鍏ュ綊涓€鍖栨彁渚涘熀纭€閫昏緫銆?

### Stage 3 璇嶆眹妯″紡 UI 鍜屼富娴?
1. 鏂板缓 `ui/vocabulary_practice.py` 锛屾彁渚涜瘝姹囨嫾鍐欑殑棰樺共銆佽緭鍏ャ€佸垽棰樸€佹璇弽棣堝拰涓嬩竴棰樹氦浜掋€?
2. 閲嶅啓 `ui/main_window.py` 锛岃涓荤晫闈㈠彲浠ヤ粠浣滄枃鎵撳瓧鍒囨崲鍒拌瘝姹囨嫾鍐欐ā寮忋€?
3. 浣跨敤 `python -m compileall src` 楠岃瘉 Stage 3 鐨勬柊澧炰唬鐮佸彲鐢ㄣ€?
