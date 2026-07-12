

#### 🛠️ Skill 2: `scene_sequel_rhythm_analyzer` (场景与续场节拍器 / GCD-RDD校验)
*   **理论基底**：德怀特·斯温《畅销书写作技巧》（Scene: Goal-Conflict-Disaster vs. Sequel: Reaction-Dilemma-Decision）
*   **核心职责**：控制文武之道（Action vs. Processing），防止连续高压导致读者疲劳，或连续思考导致剧情停滞。
*   **AI 诊断逻辑**：
    1.  **分类判定**：AI 扫描当前片段，判断它是 **Scene（动作场：目标-冲突-灾难）** 还是 **Sequel（文戏场/续场：反应-两难-决定）**。
    2.  **完整性校验**：
        *   如果是 Scene，结尾是不是 **Disaster（灾难/意外）**？如果结尾是“平淡结束”，报错。
        *   如果是 Sequel，主角在消化完上一场灾难的情绪后，有没有做出下一个 **Decision（决定）**？如果没有，报错：“主角陷入无意义的内耗，缺乏推动下一步动作的决定”。
    3.  **宏观节奏图谱**：AI 检查多个连续场景。如果全是 Scene（打打打，没有喘息），或全是 Sequel（哭哭哭，没有行动），给出节奏警告。
*   **输入**：连续 3-5 个场景的情节串联板
*   **输出**：`{"rhythm_pattern": ["Scene", "Sequel", "Scene..."], "missing_elements": "如：第2场缺乏Decision", "pacing_verdict": "节奏紧凑 / 令人疲劳 / 拖沓水字数"}`