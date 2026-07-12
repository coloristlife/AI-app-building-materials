

### Is a Python Virtual Environment Necessary?

**Practically speaking, yes.** 

Technically, you *could* install Python tools globally, but on modern Macs, it is highly discouraged and often blocked. Recent versions of macOS and Homebrew use a security feature (PEP 668) that will give you an `externally-managed-environment` error if you try to use `pip install` globally. 

Using a virtual environment (venv) is the standard best practice. It creates a tiny, isolated sandbox for Garak so its dependencies don't clash with your Mac's system tools or other projects. 

Here is the complete, start-to-finish SOP for setting up and running Garak on a Mac using Ollama.

---

### **Complete SOP: Garak + Ollama on macOS**

#### **Phase 1: Mac App Preparation**
1. **Install Ollama:**
   * Go to [ollama.com](https://ollama.com/) and download the Mac version.
   * Unzip it, drag it to your Applications folder, and open it.
   * You will see a little llama icon in your Mac's top menu bar. This means Ollama is running quietly in the background.

2. **Download Your Model:**
   * Open your Mac's **Terminal** app.
   * Tell Ollama to download the Qwen model. *(Note: Ollama uses the `qwen2.5` family, which includes a 3B and 7B parameter version. We will use the 3B version here as the closest equivalent to your 4B model).*
   * Run this command:
     ```bash
     ollama pull qwen2.5:3b
     ```
   * Wait a minute or two for the download to finish.

#### **Phase 2: Python Virtual Environment Setup**
You only need to create the environment once. 

1. **Create a Folder for Your Scans:**
   ```bash
   mkdir ~/garak_scans
   cd ~/garak_scans
   ```

2. **Create the Virtual Environment:**
   This creates a sandbox folder named `garak_env`.
   ```bash
   python3 -m venv garak_env
   ```

3. **Activate the Virtual Environment:**
   You must run this command every time you open a new terminal window to use Garak. (You'll know it worked because your terminal prompt will start with `(garak_env)`).
   ```bash
   source garak_env/bin/activate
   ```

4. **Install Garak:**
   Now that you are inside the sandbox, install Garak securely.
   ```bash
   pip install garak
   ```

#### **Phase 3: Running Intermittent Scans**
Because you are using Ollama, you can start, stop, and pause whenever you want.

1. **The Quick Sanity Check (1 minute):**
   Run a very fast test to ensure Garak and Ollama are talking to each other.
   ```bash
   garak -m ollama -n qwen2.5:3b --probes lmrc.SlurUsage
   ```

2. **The Security Scan (Start this when you have time):**
   Let's test for jailbreaks and prompt injections.
   ```bash
   garak -m ollama -n qwen2.5:3b --probes jailbreak,promptinject --report_prefix qwen_mac_scan
   ```

3. **How to Pause/Interrupt:**
   * If you need to close your laptop or stop the scan, just press **`Ctrl + C`** in the terminal. Garak will safely abort. 
   * Ollama will notice the model is no longer being used and will automatically clear it from your Mac's memory after 5 minutes.
   * When you are ready to resume, just run a new Garak command.

#### **Phase 4: Viewing the Results**
Every time Garak finishes a scan, it saves the reports in the folder you are currently in (`~/garak_scans`).

1. **View the Dashboard:**
   Garak generates a nice HTML dashboard. To open it directly from the terminal, type:
   ```bash
   open qwen_mac_scan.report.html
   ```
   *(If you didn't use a `--report_prefix`, look for the file named `garak.[timestamp].report.html` and open that).*

2. **Check the Raw Logs:**
   If the HTML report says the model was successfully jailbroken, open the `.hitlog.jsonl` file in any text editor to see exactly what prompts tricked the model.

#### **Phase 5: Closing Down**
When you are completely done for the day and want to leave the virtual environment:
```bash
deactivate
```
Your terminal will return to normal.

**Next time you want to scan:**
Simply open Terminal, go to your folder, activate the environment, and run Garak!
```bash
cd ~/garak_scans
source garak_env/bin/activate
garak -m ollama -n qwen2.5:3b --probes dan
```