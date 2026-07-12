#!/bin/bash
echo "🔄 开始合并 Garak 扫描结果..."

OUTPUT_DIR="resilient_scan_results"
MERGED_JSONL="final_merged_scan.report.jsonl"
MERGED_HITLOG="final_merged_scan.hitlog.jsonl"

# 1. 合并高危命中记录 (Hitlogs)
echo "📂 合并所有 hitlog 记录..."
cat ${OUTPUT_DIR}/*.hitlog.jsonl > ${MERGED_HITLOG} 2>/dev/null
echo "✅ 高危日志合并完成 -> ${MERGED_HITLOG}"

# 2. 合并所有测试数据 (Report JSONL)
echo "📂 合并所有 JSONL 报告..."
python3 -m garak.analyze.aggregate_reports ${OUTPUT_DIR}/*.report.jsonl > ${MERGED_JSONL}

# 3. 重新生成总 HTML 报告
echo "📊 生成综合 HTML 报告..."
# 适配最新和老版本 garak 的生成命令
if python3 -m garak.report ${MERGED_JSONL}; then
    echo "✅ 全局 HTML 报告生成完毕！"
else
    python3 -m garak.analyze.report_html ${MERGED_JSONL}
    echo "✅ 全局 HTML 报告生成完毕！"
fi

echo "============================================="
echo "🎉 所有的结果已整理完毕！"
echo "你可以使用 python3 -m http.server 8080 在浏览器中查看 HTML 报告。"