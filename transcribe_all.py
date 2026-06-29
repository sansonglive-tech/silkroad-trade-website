import whisper
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

audio_dir = r"E:\郑州录音"
files = ["1.m4a", "2.m4a", "3.m4a", "4.m4a", "5.m4a", "6.m4a"]

print("正在加载模型...")
model = whisper.load_model('base')
print("模型加载完成！")

for fname in files:
    in_path = os.path.join(audio_dir, fname)
    base = os.path.splitext(fname)[0]
    out_path = os.path.join(audio_dir, base + ".txt")
    
    if os.path.exists(out_path):
        print(f"跳过 {fname}（{base}.txt 已存在）")
        continue
    
    print(f"\n开始转写 {fname} ...")
    try:
        result = model.transcribe(in_path, language='zh')
        text = result['text']
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✅ 已保存：{base}.txt（{len(text)} 字）")
    except Exception as e:
        print(f"❌ 转写失败 {fname}：{e}")

print("\n全部完成！")
