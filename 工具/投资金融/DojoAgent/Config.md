```
version: 1

llm_provider:
  default: openai
  providers:
    openai:
      author: openai
      model: gpt-4.1
      models:
        - gpt-4.1
        - gpt-4o
      base_url: https://api.openai.com/v1
      api_key_env: OPENAI_API_KEY
      extra_headers:
        X-Tenant-ID: ${OPENAI_TENANT_ID}
        X-Request-Source: dojoagents
      context_window: 128000

agent:
  max_iterations: 100
  max_tool_workers: 4
  lazy_skills: true
  enable_skill_cache: true
  enable_guardrails: true
  enable_think_scrubbing: true
  enable_context_compression: true
  compression_threshold_ratio: 0.8
  default_context_window: 32768
  default_skills:
    - dojo-quant-analyst

tools:
  sandbox:
    allowed_roots:
      - ${PWD}
      - /tmp
    allow_network: false
    allowed_commands: []
    timeout_seconds: 120
  web:
    search_backend: ddgs
    extract_backend: fetch
    # tavily / exa / firecrawl 等付费后端需要配置 api_key 或 api_key_env
    # api_key_env: TAVILY_API_KEY
    max_extract_urls: 5
    max_content_bytes: 2000000

skills:
  dir: ~/.dojo/skills
  generated_skill_dir: ~/.dojo/skills/generated
  external_dirs: []
  disabled: []
  read_claude_skills: false

dashboard:
  host: 127.0.0.1
  port: 8765
  profiler:
    enabled: false
  financial:
    dashboard_data_root: ~/.dojo/dashboard-data
    sdk_cache_dir: ~/.cache/huggingface/hub
    stock_quote_refresh_seconds: 15
    constituent_kline_max_concurrent: 8

gateway:
  enabled: true
  hooks: {}

sessions:
  enabled: true
  provider: dojo_repository
  root: ~/.dojo/agents/strands_sessions
  agent_id: dojo-agent
  persist_openai_history: true
  sync_memory: true
  export_default_dir: ~/Desktop/dojo-chat-export
  
```