# 好莱坞大片风格海报生成

## 任务
用户要求生成一张"好莱坞大片"风格的图片。通过 canvas-design skill 流程完成。

## 过程
1. 读取 canvas-design skill 的 SKILL.md，了解设计哲学 + 视觉表达的双步流程
2. 查看可用字体库（80+ 字体，选用 BigShoulders-Bold、InstrumentSerif-Italic、Outfit）
3. 创建设计哲学文档 "Celestial Spectacle"（史诗电影美学运动）
4. 首选用 canvas 工具渲染 HTML，但缺少可用 node，回退到 Python Pillow 方案
5. 编写 Python 脚本 gen_poster.py，使用 Pillow 逐像素绘制：
   - 径向渐变背景（深红铜金调色）
   - 中心暖色光晕（高斯模糊叠加）
   - 暗角效果（距离渐变）
   - 光射线（多角度半透明射线 + 高斯模糊）
   - 胶片颗粒纹理
   - 破碎同心圆环结构（斗兽场式）
   - 中央锥形支柱
   - 微小剪影人物（尺度对比）
   - 水平光条 + 地面辉光
   - 碎屑粒子散布
   - 标题排版（字母间距手动计算）
   - 副标题/标语/发行日期/演职员表

## 输出
- 文件：`E:\1214\Celestial_Spectacle.png`
- 规格：1080×1440px, 0.5 MB
- 效果：暗调史诗感，好莱坞大片海报风格
