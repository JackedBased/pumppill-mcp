# Example client configs

| File | Client | Where it goes |
|---|---|---|
| `claude-code.sh` | Claude Code | Run it once; it is the one-line `claude mcp add` command. |
| `cursor-mcp.json` | Cursor, Windsurf, Cline | `~/.cursor/mcp.json` (or the client's MCP settings file). |
| `cursor-mcp-member.json` | Cursor, for members | Same place. Replace `<claim>` with the sign-in token from your premium page. Never commit the real value. |
| `cursor-mcp-agent.json` | Cursor, for agentic trading | Same place. Replace `ppa_your_key` with the agent key from the trade bot (Settings, AI agent). Never commit the real value. |
| `vscode-mcp.json` | VS Code | `.vscode/mcp.json` in your workspace. |
| `claude_desktop_config.json` | Claude Desktop over stdio | `claude_desktop_config.json`. Only needed if you are not using Settings → Connectors → Add custom connector. Requires Node.js for `npx`. |

If you already have other servers configured, merge the `pumppill` entry into your existing
file rather than replacing it.
