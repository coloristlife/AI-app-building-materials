#!/bin/bash

# ==========================================
# 1. 配置参数
# ==========================================
MODEL_TYPE="ollama"
MODEL_NAME="qwen3:4b-instruct-2507-q4_K_M"
GENERATIONS=1
TIMEOUT_PER_PROBE="20m"  # ⏳ 每个 Probe 最多运行 20 分钟，超时自动杀掉
OUTPUT_DIR="$PWD/resilient_scan_results"
TRACKING_FILE="${OUTPUT_DIR}/completed_probes.txt"
TIMEOUT_FILE="${OUTPUT_DIR}/timeout_probes.txt" # 记录超时的探针

# ==========================================
# 2. 初始化
# ==========================================
mkdir -p "$OUTPUT_DIR"
touch "$TRACKING_FILE"
touch "$TIMEOUT_FILE"

# The complete list of specific probes (filtered from your list)
PROBES=(
# ==========================================
# 1. 核心提示词注入与系统劫持 (Prompt Injection)
# ==========================================w
"sysprompt_extraction.SystemPromptExtraction"  # 尝试窃取模型的 System Prompt
"promptinject.HijackKillHumans"                # 恶意指令覆盖
"promptinject.HijackLongPrompt"                # 长文本注入
"goodside.ThreatenJSON"                        # JSON格式化逃逸
"goodside.WhoIsRiley"                          # 身份劫持
"goodside.Tag"                                 # 标签闭合注入
"agent_breaker.AgentBreaker"                   # AI Agent 边界突破

# ==========================================
# 2. 越狱攻击 (Jailbreaks - 筛选了最高效的)
# ==========================================
"dan.AutoDAN"                                  # 自动化变异越狱
"dan.DAN_Jailbreak"                            # 经典 Do Anything Now
"dan.Dan_11_0"                                 # 高级 DAN 变体
"dan.ChatGPT_Developer_Mode_v2"                # 开发者模式越狱
"dan.STAN"                                     # STAN 越狱
"dan.DUDE"                                     # DUDE 越狱
"tap.TAP"                                      # Tree of Attacks 越狱
"tap.PAIR"                                     # PAIR 自动化越狱
"suffix.GCG"                                   # 贪婪坐标梯度对抗后缀攻击
"suffix.BEAST"                                 # 快速对抗后缀攻击
"goat.GOATAttack"                              # 动态越狱生成
"doctor.Bypass"                                # 伪装成医生绕过限制
"doctor.Puppetry"                              # 身份操控
"donotanswer.InformationHazard"                # 强制输出危险信息
"donotanswer.MaliciousUses"                    # 强制输出恶意用途信息

# ==========================================
# 3. 信息泄露与隐私窃取 (Data Leakage & PII)
# ==========================================
"apikey.CompleteKey"                           # 诱导模型输出真实 API Key
"apikey.GetKey"                                
"propile.PIILeakQuadruplet"                    # 个人身份信息 (PII) 泄露测试
"propile.PIILeakUnstructured"                  
"dra.DRA"                                      # 数据提取攻击 (Data Replay)
"dra.DRAAdvanced"                              
"leakreplay.NYTComplete"                       # 训练集数据提取 (纽约时报)
"leakreplay.GuardianComplete"                  # 训练集数据提取 (卫报)

# ==========================================
# 4. 恶意代码生成与网络攻击 (Malware & Exploitation)
# ==========================================
"malwaregen.Evasion"                           # 生成免杀恶意代码
"malwaregen.Payload"                           # 生成攻击载荷
"malwaregen.SubFunctions"                      # 生成黑客工具子模块
"malwaregen.TopLevel"                          # 完整木马生成
"exploitation.SQLInjectionEcho"                # 诱导 AI 生成或执行 SQL 注入
"exploitation.SQLInjectionSystem"              
"exploitation.JinjaTemplatePythonInjection"    # SSTI 模板注入
"av_spam_scanning.EICAR"                       # 诱导生成 EICAR 标准病毒特征码
"av_spam_scanning.GTUBE"                       # 诱导生成垃圾邮件特征码
"av_spam_scanning.GTphish"                     # 诱导生成钓鱼邮件
"packagehallucination.Python"                  # 供应链投毒攻击测试 (生成假 Python 库)
"packagehallucination.JavaScript"              # 供应链投毒攻击测试 (生成假 NPM 库)

# ==========================================
# 5. 终端安全、XSS 与数据外带 (Web/Terminal & Exfiltration)
# ==========================================
"web_injection.MarkdownXSS"                    # 诱导输出含 XSS 跨站脚本的 Markdown
"web_injection.TaskXSS"                        
"web_injection.StringAssemblyDataExfil"        # 数据拼装外带
"web_injection.MarkdownImageExfil"             # 利用图片标签外带敏感数据
"ansiescape.AnsiEscaped"                       # 终端 ANSI 转义符注入 (导致控制台被黑)
"ansiescape.AnsiRaw"                           

# ==========================================
# 6. 隐蔽注入与编码绕过 (Obfuscation & Smuggling)
# ==========================================
"latentinjection.LatentJailbreak"              # 隐性越狱 (潜伏在正常文本中)
"latentinjection.LatentWhoisSnippet"           
"smuggling.FunctionMasking"                    # 函数掩蔽攻击
"smuggling.HomoglyphObfuscation"               # 形近字混淆绕过防御
"smuggling.HypotheticalResponse"               # 假设性回应逃逸
"badchars.BadCharacters"                       # 坏字符/不可见字符注入
"encoding.InjectBase64"                        # Base64 绕过
"encoding.InjectHex"                           # 16进制 绕过
"encoding.InjectLeet"                          # 火星文/黑客语 (L33t) 绕过
"encoding.InjectROT13"                         # 凯撒密码绕过
)


echo "🚀 开始扫描，当前每个探针限时: $TIMEOUT_PER_PROBE"

# ==========================================
# 3. 循环执行
# ==========================================
for PROBE in "${PROBES[@]}"; do
    # 跳过已完成的
    if grep -q "^${PROBE}$" "$TRACKING_FILE"; then
        continue
    fi

    echo "▶️  正在运行: $PROBE ..."
    REPORT_PREFIX="${OUTPUT_DIR}/${PROBE}"
    
    # 核心改进：使用 timeout 命令
    # --kill-after=30s 表示如果 SIGTERM 杀不掉，30秒后强制 SIGKILL
    timeout --kill-after=30s $TIMEOUT_PER_PROBE python3 -m garak -m "$MODEL_TYPE" -n "$MODEL_NAME" \
        --probes "$PROBE" \
        --generations "$GENERATIONS" \
        --report_prefix "$REPORT_PREFIX" > "${OUTPUT_DIR}/${PROBE}.log" 2>&1
    
    EXIT_CODE=$?

    # ==========================================
    # 4. 状态判定
    # ==========================================
    if [ $EXIT_CODE -eq 124 ]; then
        # 124 是 timeout 命令的特有返回码，表示超时
        echo "⏰ [超时] $PROBE 运行超过 $TIMEOUT_PER_PROBE，已跳过。"
        echo "$PROBE" >> "$TIMEOUT_FILE"
        # 即使超时，我们也把它记录为“处理过”，或者不记录以便以后重试
        # 建议记录到专用文件，不要记入 completed_probes
        
    elif ls ${REPORT_PREFIX}*.report.jsonl 1> /dev/null 2>&1; then
        echo "✅ [完成] $PROBE"
        echo "$PROBE" >> "$TRACKING_FILE"
        
    else
        echo "❌ [失败] $PROBE 发生非超时错误 (Exit Code: $EXIT_CODE)"
        # 这种情况下可以根据需要决定是 exit 1 (停止整个脚本) 还是继续
        # 建议继续，让脚本尽可能多跑一些
        echo "$PROBE (Error $EXIT_CODE)" >> "${OUTPUT_DIR}/failed_probes.txt"
    fi
done

echo "🎉 所有探针尝试完毕！"
echo "检查 $TRACKING_FILE 查看成功项，检查 $TIMEOUT_FILE 查看超时项。"