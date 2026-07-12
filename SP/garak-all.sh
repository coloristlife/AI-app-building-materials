#!/bin/bash

# ==========================================
# 1. 配置参数
# ==========================================
MODEL_TYPE="ollama"
MODEL_NAME="qwen3:4b-instruct-2507-q4_K_M"
GENERATIONS=1
TIMEOUT_PER_PROBE="40m"  # ⏳ 每个 Probe 最多运行 20 分钟，超时自动杀掉
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

# The complete list of specific probes (filtered from your list)
PROBES=(
"agent_breaker.AgentBreaker" "ansiescape.AnsiEscaped" "ansiescape.AnsiRaw" 
"ansiescape.AnsiRawTokenizerHF" "apikey.CompleteKey" "apikey.GetKey" "atkgen.Tox" 
"audio.AudioAchillesHeel" "av_spam_scanning.EICAR" "av_spam_scanning.GTUBE" 
"av_spam_scanning.GTphish" "badchars.BadCharacters" "continuation.ContinueSlursReclaimedSlurs" 
"continuation.ContinueSlursReclaimedSlursFull" "dan.Ablation_Dan_11_0" "dan.AntiDAN" 
"dan.AutoDAN" "dan.AutoDANCached" "dan.ChatGPT_Developer_Mode_RANTI" "dan.ChatGPT_Developer_Mode_v2" 
"dan.ChatGPT_Image_Markdown" "dan.DAN_Jailbreak" "dan.DUDE" "dan.DanInTheWild" 
"dan.DanInTheWildFull" "dan.Dan_10_0" "dan.Dan_11_0" "dan.Dan_6_0" "dan.Dan_6_2" 
"dan.Dan_7_0" "dan.Dan_8_0" "dan.Dan_9_0" "dan.STAN" "divergence.Repeat" 
"divergence.RepeatExtended" "divergence.RepeatedToken" "doctor.Bypass" 
"doctor.BypassLeet" "doctor.Puppetry" "donotanswer.DiscriminationExclusionToxicityHatefulOffensive" 
"donotanswer.HumanChatbox" "donotanswer.InformationHazard" "donotanswer.MaliciousUses" 
"donotanswer.MisinformationHarms" "dra.DRA" "dra.DRAAdvanced" "encoding.InjectAscii85" 
"encoding.InjectAtbash" "encoding.InjectBase16" "encoding.InjectBase2048" 
"encoding.InjectBase32" "encoding.InjectBase64" "encoding.InjectBraille" 
"encoding.InjectEcoji" "encoding.InjectHex" "encoding.InjectLeet" "encoding.InjectMime" 
"encoding.InjectMorse" "encoding.InjectNato" "encoding.InjectQP" "encoding.InjectROT13" 
"encoding.InjectSneakyBits" "encoding.InjectUU" "encoding.InjectUnicodeTagChars" 
"encoding.InjectUnicodeVariantSelectors" "encoding.InjectZalgo" "exploitation.JinjaTemplatePythonInjection" 
"exploitation.SQLInjectionEcho" "exploitation.SQLInjectionSystem" "fileformats.HF_Files" 
"fitd.FITD" "glitch.Glitch" "glitch.GlitchFull" "goat.GOATAttack" "goodside.Davidjl" 
"goodside.Tag" "goodside.ThreatenJSON" "goodside.WhoIsRiley" "grandma.Slurs" 
"grandma.Substances" "grandma.Win10" "grandma.Win11" "latentinjection.LatentInjectionFactSnippetEiffel" 
"latentinjection.LatentInjectionFactSnippetEiffelFull" "latentinjection.LatentInjectionFactSnippetLegal" 
"latentinjection.LatentInjectionFactSnippetLegalFull" "latentinjection.LatentInjectionReport" 
"latentinjection.LatentInjectionReportFull" "latentinjection.LatentInjectionResume" 
"latentinjection.LatentInjectionResumeFull" "latentinjection.LatentInjectionTranslationEnFr" 
"latentinjection.LatentInjectionTranslationEnFrFull" "latentinjection.LatentInjectionTranslationEnZh" 
"latentinjection.LatentInjectionTranslationEnZhFull" "latentinjection.LatentJailbreak" 
"latentinjection.LatentJailbreakFull" "latentinjection.LatentWhois" "latentinjection.LatentWhoisSnippet" 
"latentinjection.LatentWhoisSnippetFull" "leakreplay.GuardianCloze" "leakreplay.GuardianClozeFull" 
"leakreplay.GuardianComplete" "leakreplay.GuardianCompleteFull" "leakreplay.LiteratureCloze" 
"leakreplay.LiteratureClozeFull" "leakreplay.LiteratureComplete" "leakreplay.LiteratureCompleteFull" 
"leakreplay.NYTCloze" "leakreplay.NYTClozeFull" "leakreplay.NYTComplete" 
"leakreplay.NYTCompleteFull" "leakreplay.PotterCloze" "leakreplay.PotterClozeFull" 
"leakreplay.PotterComplete" "leakreplay.PotterCompleteFull" "lmrc.Anthropomorphisation" 
"lmrc.Bullying" "lmrc.Deadnaming" "lmrc.Profanity" "lmrc.QuackMedicine" 
"lmrc.SexualContent" "lmrc.Sexualisation" "lmrc.SlurUsage" "malwaregen.Evasion" 
"malwaregen.Payload" "malwaregen.SubFunctions" "malwaregen.TopLevel" "misleading.FalseAssertion" 
"packagehallucination.Dart" "packagehallucination.JavaScript" "packagehallucination.Perl" 
"packagehallucination.Python" "packagehallucination.RakuLand" "packagehallucination.Ruby" 
"packagehallucination.Rust" "phraising.FutureTense" "phrasing.FutureTenseFull" 
"phrasing.PastTense" "phrasing.PastTenseFull" "promptinject.HijackHateHumans" 
"promptinject.HijackHateHumansFull" "promptinject.HijackKillHumans" "promptinject.HijackKillHumansFull" 
"promptinject.HijackLongPrompt" "promptinject.HijackLongPromptFull" "propile.PIILeakQuadruplet" 
"propile.PIILeakTriplet" "propile.PIILeakTwin" "propile.PIILeakUnstructured" 
"realtoxicityprompts.RTPBlank" "realtoxicityprompts.RTPFlirtation" "realtoxicityprompts.RTPIdentity_Attack" 
"realtoxicityprompts.RTPInsult" "realtoxicityprompts.RTPProfanity" "realtoxicityprompts.RTPSevere_Toxicity" 
"realtoxicityprompts.RTPSexually_Explicit" "realtoxicityprompts.RTPThreat" "sata.MLM" 
"smuggling.FunctionMasking" "smuggling.HomoglyphObfuscation" "smuggling.HypotheticalResponse" 
"snowball.GraphConnectivity" "snowball.GraphConnectivityFull" "snowball.Primes" 
"snowball.PrimesFull" "snowball.Senators" "snowball.SenatorsFull" "suffix.BEAST" 
"suffix.GCG" "suffix.GCGCached" "sysprompt_extraction.SystemPromptExtraction" 
"tap.PAIR" "tap.TAP" "tap.TAPCached" "test.Blank" "test.Test" "topic.WordnetAllowedWords" 
"topic.WordnetBlockedWords" "topic.WordnetControversial" "visual_jailbreak.FigStep" 
"visual_jailbreak.FigStepFull" "web_injection.ColabAIDataLeakage" "web_injection.MarkdownImageExfil" 
"web_injection.MarkdownURIImageExfilExtended" "web_injection.MarkdownURINonImageExfilExtended" 
"web_injection.MarkdownXSS" "web_injection.PlaygroundMarkdownExfil" "web_injection.StringAssemblyDataExfil" 
"web_injection.TaskXSS"
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