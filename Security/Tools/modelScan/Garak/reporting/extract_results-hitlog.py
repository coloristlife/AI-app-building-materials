import json
import os
from datetime import datetime

# 配置路径
JSONL_DIR = "resilient_scan_results"
HITLOG_FILE = "final_merged_scan.hitlog.jsonl"
OUTPUT_FILE = "Final_Security_Audit_Report.md"

def generate():
    report_data = []
    
    # 1. 扫描所有 .report.jsonl 提取分数
    if not os.path.exists(JSONL_DIR):
        print(f"❌ 错误: 找不到目录 {JSONL_DIR}")
        return

    files = [f for f in os.listdir(JSONL_DIR) if f.endswith(".report.jsonl")]
    for f_name in files:
        with open(os.path.join(JSONL_DIR, f_name), 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("entry_type") == "probe_result":
                        report_data.append({
                            "probe": data["probe"],
                            "score": data["score"] * 100,
                            "passed": data["passed"],
                            "total": data["total"]
                        })
                except: continue

    # 2. 写入 Markdown 报告
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as md:
        md.write(f"# 🛡️ Qwen3-4B LLM 安全审计报告\n")
        md.write(f"**生成日期:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.write(f"**测试对象:** Qwen/Qwen3-4B-Instruct-2507 (Ollama)\n\n")

        # 总体统计
        if report_data:
            avg_score = sum(d['score'] for d in report_data) / len(report_data)
            md.write("## 一、 执行摘要 (Executive Summary)\n")
            md.write(f"- **综合安全得分:** {avg_score:.2f} / 100\n")
            md.write(f"- **已完成测试项:** {len(report_data)} 个探针类别\n\n")

            # 漏洞风险分布表格
            md.write("## 二、 风险评估明细 (Security Metrics)\n")
            md.write("| 探针名称 (Probe) | 安全得分 | 通过/总计 | 风险级别 |\n")
            md.write("| :--- | :---: | :---: | :--- |\n")
            for d in sorted(report_data, key=lambda x: x['score']):
                level = "🟢 LOW" if d['score'] >= 90 else ("🟡 MED" if d['score'] >= 70 else "🔴 CRITICAL")
                md.write(f"| {d['probe']} | {d['score']:.1f}% | {d['passed']}/{d['total']} | {level} |\n")
        
        # 提取 Hitlog 中的真实证据
        md.write("\n## 三、 关键漏洞证据 (Vulnerability Evidence)\n")
        if os.path.exists(HITLOG_FILE):
            with open(HITLOG_FILE, 'r') as f:
                for i, line in enumerate(f):
                    # 仅提取前20个最重要的真实攻击案例
                    if i >= 20: break
                    try:
                        data = json.loads(line)
                        probe = data.get("probe", "N/A")
                        prompt = data.get("prompt", {}).get("turns", [{}])[0].get("content", {}).get("text", "N/A")
                        output = data.get("output", {}).get("text", "") or data.get("outputs", [{}])[0].get("text", "")
                        
                        md.write(f"### 案例 {i+1}: {probe}\n")
                        md.write(f"- **漏洞类型:** 越狱攻击 (Jailbreak) / 安全护栏绕过\n")
                        md.write(f"**攻击提示词 (Prompt):**\n> {prompt[:1000]}\n\n")
                        md.write(f"**模型违规响应 (Model Response):**\n```text\n{output}\n```\n\n")
                        md.write("---\n")
                    except: continue
        else:
            md.write("_未发现高危漏洞命中记录。_\n")

    print(f"✅ 高保真报告已成功生成: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()