# Letter Treasure Prototype

一个可运行的最小原型：
- 随机生成一个目标单词（默认从内置词库中选择）
- 玩家在限定次数内猜测单词
- 每次猜测返回逐字反馈：
  - `correct`：字母和位置都正确
  - `present`：字母存在但位置不正确
  - `absent`：字母不存在
- 成功时返回剩余次数，失败时显示答案

## 快速开始

```bash
python -m src.letter_treasure
```

## 运行测试

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## 计划与当前完成度

- [x] Phase 1：搭建核心领域模型（游戏状态、反馈逻辑）
- [x] Phase 2：实现命令行交互式流程
- [x] Phase 3：补充单元测试与文档
- [ ] Phase 4：扩展词库与难度策略（后续）
