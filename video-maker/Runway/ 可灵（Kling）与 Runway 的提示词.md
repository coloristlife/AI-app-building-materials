在“图生视频（Image-to-Video, I2V）”的工作流中，由于**Midjourney 生成的起幅图已经决定了画面的人物、构图、色彩、光影和艺术风格**，因此无论是可灵还是 Runway，两者的提示词（Prompt）核心任务都是**只描述“动态”（动作、镜头运动、环境变化）**，而不需要重复描述画面里已经有什么。

尽管核心逻辑一致，但在**提示词的结构偏好、语义理解和书写格式上，可灵和 Runway 存在明显的区别**。

---

### 一、 可灵 与 Runway 提示词的核心区别

| 维度 | 可灵 (Kling) | Runway (Gen-3/Gen-4) |
| :--- | :--- | :--- |
| **核心逻辑** | **主体 + 动作（Subject + Movement）** | **运镜前缀 : 场景动态（Camera + Scene Motion）** |
| **语言理解** | 中英文双语极强，擅长理解**日常自然语言和因果逻辑** | 英文理解极佳，更偏好**工业化电影拍摄术语（CGI/Filmmaking terms）** |
| **书写结构** | 像写小说的动作描写，描述“谁做了什么，然后发生了什么” | 像写电影剧本的分镜脚本，高度结构化，通常用冒号或括号拆分 |
| **物理规律** | 极其精准地响应复杂物体的运动轨迹（如：手部抓取、奔跑） | 极其精准地响应运镜控制和粒子特效（如：镜头推进、闪电爆炸） |

---

### 二、 针对您脚本的实战提示词（Prompt）对比

以您剧本中的两个典型镜头为例，展示两者的书写差异：

#### 示例 A：镜头 2（山谷行走，停下感受，镜头上移呈俯视）
*   **可灵 (Kling) 的提示词写法（偏向物理连贯性与动作因果）**：
    > **中文**：一个年轻男子慢慢走上山坡，随后他停下脚步。他闭上眼睛，微微扬起头静静感受阳光。背景风吹过草地，镜头平稳地向上升起，逐渐切换为俯视角度。  
    > **英文**：A young man slowly walks up the slope, then he stops walking. He closes his eyes and slightly tilts his head up to feel the sunlight. The camera smoothly glides upward, transitioning to a top-down overhead angle.
    >
    > *💡 **可灵要点**：使用连贯的连词（如“随后”、“然后”、“随后停下”）描述顺序动作，可灵能精准执行“走-停-仰头”的动作链。*

*   **Runway 的提示词写法（偏向运镜控制与氛围特效）**：
    > **英文**：A slow crane shot tilting up to a top-down overhead view: The man walking on the slope stops completely and tilts his face up toward the sun. Volumetric cinematic sunlight beams hitting him, cinematic slow motion.
    >
    > *💡 **Runway 要点**：以“运镜方式 + 冒号”作为开头（如 `A slow crane shot...:`），直接用专业电影术语指挥相机，再描述场景中的光影和空气质感。*

#### 示例 B：镜头 4（父亲看报纸，小孩拿着玩具跑来跑去）
*   **可灵 (Kling) 的提示词写法（强调多主体交互与物理避让）**：
    > **中文**：客厅里，父亲安静地坐在沙发上看报纸。一个小男孩手里拿着玩具，快乐地围绕着沙发跑来跑去。镜头缓慢地向后拉远。  
    > **英文**：In the living room, a father sits quietly on the sofa reading a newspaper. A little boy, holding a toy, happily runs around the sofa. The camera slowly dollies back to zoom out.

*   **Runway 的提示词写法（强调画面整体稳定与镜头语言）**：
    > **英文**：A slow dolly-out camera movement: The little child is running around holding a toy, while the father sits still reading a newspaper. Steady camera tracking, photorealistic movement, cinematic pacing.

---

### 三、 事实来源（Source of Truth）

以上对比和书写规律，均来自两家官方发布的权威指南和技术文档：

1.  **可灵官方技术指引 (Kling AI Official Prompting Guide)**：
    *   **核心公式**：官方明确指出，图生视频的黄金公式为 **`Prompt = Subject + Movement, Background + Movement`（主体 + 运动方式，背景 + 运动方式）**。
    *   **物理语义**：官方文档强调可灵模型对“动作轨迹（Motion Trajectories）”的语义理解能力，指导用户使用强动词和因果连词，避免使用概念性虚词。
2.  **Runway 官方提示词指南 (Runway Gen-3 / Gen-4 Prompting Guide)**：
    *   **避免冗余**：官方文档中明确指出：*“You do not need to describe your input image in a text prompt.”*（使用输入图像时，无需在文本提示词中重复描述图像内容）。
    *   **结构与运镜**：官方强烈建议使用明确的**摄像机控制术语（如 Zoom, Pan, Tilt, Dolly）**，并使用简洁直白、具象化的非指令性词汇。例如：不要写“一个人黑入系统”，而要写“一个人在键盘上飞快地敲击”。