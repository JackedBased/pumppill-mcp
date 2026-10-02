<p align="center">
  <img src="assets/logo-400.png" alt="PumpPill" width="120" height="120">
</p>

# PumpPill MCP server

Read-only token intelligence for **Robinhood Chain** (chainId 4663) and **Solana**, served as a
hosted [Model Context Protocol](https://modelcontextprotocol.io) server.

```
https://api.pumppill.org/mcp
```

Streamable HTTP. No key, no account, nothing to install. Registry name:
`org.pumppill/token-safety` (v1.2.2). How-to page: <https://www.pumppill.org/for-agents>

This repository holds the connection instructions, example client configs and the registry
manifest. The server itself is hosted by PumpPill; its source is not published here.

## What it answers

The questions that cost people money: can this contract be sold, which contract is the real one
behind a ticker, what has this deployer launched before, which wallets hold enough to move a
pool, and what happened to the tokens PumpPill logged, with the losers counted.

Every result carries a `cite` string and a timestamp for when the read was taken. A token
PumpPill has not read comes back as `found: false`, which means "not in the index", never "safe".
Nothing here predicts a price or recommends a trade.

## Tools

### Public (17 tools, read-only, no key)

| Tool | What it returns |
|---|---|
| `rh_token_safety` | The stored safety read for one Robinhood Chain token: sellability, launch flags with evidence, where the launch money went, and the move since PumpPill first logged it. Never triggers a scan. |
| `rh_ticker_resolve` | The one Robinhood Chain contract worth naming for a ticker: alive, $10K+ in its pool, not flagged HIGH or CRITICAL. Other contracts using the name come back as a count. |
| `rh_deployer_record` | What one Robinhood Chain wallet has launched and how those went: tokens, liveness, liquidity, which crossed $100K. |
| `rh_flagged_recent` | Tokens whose latest scan in the last 30 days found HIGH or CRITICAL structural risk, with the findings named. |
| `rh_stock_pairs` | Memecoins quoted in tokenized stocks (NVDA, SPY, TSLA) on Robinhood Chain, with liquidity and latest scan risk. |
| `rh_chain_stats` | How Robinhood Chain measures from PumpPill's index, recomputed hourly with the method in the payload. |
| `rh_whale_wallets` | Wallets holding 10+ ETH or $50K+ in tokens, read as on-chain balances, tiered by dollars held. Measures who *can* move a pool, not who is right. |
| `rh_wallet_record` | One Robinhood Chain wallet's holdings and trades off the chain's own feed. Sell sizes are floors, never profit. |
| `rh_early_wallets` | Robinhood Chain wallets whose first buy landed early on tokens that later crossed $100K, with the base rate beside every rate. |
| `sol_early_wallets` | Solana wallets recorded among a token's first buyers on tokens that later reached 5x, with the base rate beside every rate. |
| `sol_token_detail` | Any Solana token by mint: holders, bundled-launch read, what the deployer still holds, socials, and a one-sentence verdict. |
| `outcomes_measured` | Forward-measured outcomes across both chains: the share of logged tokens that doubled, reached 5x, 10x, or never moved. Losers are in the denominator. |
| `exit_check` | Can this token be sold, and what can the deployer still do to it: mint and freeze authority, dev share of supply, the liquidity position. Both chains. |
| `fomo_gathering` | Tokens several different FOMO app traders bought inside a window (default 3 traders in 60 minutes), on both chains, with the market cap of the latest buy. Counts FOMO users, not all buyers; no trade sizes. |
| `search` | Find PumpPill's read for a Robinhood Chain address, a Solana mint, or a ticker. Returns ids for `fetch`. Built for ChatGPT connectors and deep research. |
| `fetch` | Fetch one result by the id `search` returned. Returns the stored read as text with its citation and as-of time. |
| `membership_status` | Whether this connection carries an active PumpPill membership, its tier, and when it renews. An unauthenticated call answers `signed_in: false`, not an error. |

### Member tools (4 tools)

These answer a PumpPill member. They are listed for everyone; called without a membership they
answer with what sits behind them and a link. Three of them can also be bought one call at a
time with x402 (see [Pay per call](#pay-per-call-x402)).

21 tools in all: 17 public, 4 for members, 3 of those payable per call.

| Tool | What it returns |
|---|---|
| `rh_scan_now` | Reads one Robinhood Chain contract fresh, when the stored read is missing or stale. **Spends:** capped per member and per day (resets 00:00 UTC). Annotated not read-only and not idempotent, so a well-behaved client asks before calling it. |
| `premium_calls_recent` | The premium call table: Solana tokens PumpPill logged for members, newest first, with the market cap at logging and the move since. |
| `my_watched_wallets` | The Robinhood Chain wallets this member follows: what each holds, its record beside the chain's base rate, recent activity. |
| `x_chatter` | What X has been saying about one contract: posts naming it, distinct accounts, combined reach, and each poster's record on earlier calls. **Spends:** may use an hourly live-read budget. Annotated not read-only and not idempotent. |

### Resource and prompts

- `pumppill://facts` — the quotable fact sheet: what the index covers, headline figures, how to
  cite them and what they do not mean.
- `check_before_buying(address)` — the full read on one contract, with the limits stated.
- `real_contract_for_ticker(symbol)` — which of the contracts using a name is the one that matters.

## Connect

### Claude Code

```bash
claude mcp add --transport http pumppill https://api.pumppill.org/mcp
```

### Claude on the web or desktop (Pro, Max, Team, Enterprise)

Settings → Connectors → **Add custom connector**. Name it PumpPill, paste
`https://api.pumppill.org/mcp`, and leave the OAuth fields empty. The public tools then work in
any chat. The member tools need a header that claude.ai cannot send, so use an editor client for
those.

A Claude Desktop build without custom connectors can bridge over stdio instead; see
[`examples/claude_desktop_config.json`](examples/claude_desktop_config.json).

### Cursor

One click: [Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=pumppill&config=eyJ1cmwiOiJodHRwczovL2FwaS5wdW1wcGlsbC5vcmcvbWNwIn0=)
(GitHub may not open `cursor://` links; the same link is on
[/for-agents](https://www.pumppill.org/for-agents)). Or by hand, in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "pumppill": { "url": "https://api.pumppill.org/mcp" }
  }
}
```

The same block works in Windsurf, Cline and other clients that take a remote MCP server.

### VS Code

One click: [Add to VS Code](vscode:mcp/install?%7B%22name%22%3A%22pumppill%22%2C%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A//api.pumppill.org/mcp%22%7D)
· [VS Code Insiders](vscode-insiders:mcp/install?%7B%22name%22%3A%22pumppill%22%2C%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A//api.pumppill.org/mcp%22%7D).
Or by hand, in `.vscode/mcp.json` (VS Code names the transport):

```json
{
  "servers": {
    "pumppill": { "type": "http", "url": "https://api.pumppill.org/mcp" }
  }
}
```

### ChatGPT

Add it as a connector with the same URL. `search` and `fetch` are the tools ChatGPT calls.

### Stdio-only clients

```bash
npx -y mcp-remote https://api.pumppill.org/mcp
```

### Member tools

A member sends their sign-in token as a header:

```
Authorization: Bearer <claim>
```

The whole connect line can be copied from the member's page at
<https://www.pumppill.org/premium>. In Cursor that is a `"headers"` object beside the URL; see
[`examples/cursor-mcp-member.json`](examples/cursor-mcp-member.json). Treat the claim like a
password: keep it in a header, never in a URL, and never commit it.

### Check the connection

```bash
curl -sX POST https://api.pumppill.org/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'
```

## Pay per call (x402)

No membership? An agent with a wallet can buy a single answer from three of the member tools,
paid in USDC on Base through [x402](https://www.x402.org):

| Tool | Price per call |
|---|---|
| `rh_scan_now` | $0.05 |
| `x_chatter` | $0.05 |
| `premium_calls_recent` | $0.10 |

1. Call the tool. Without a membership or a payment, it answers with an x402 payment request:
   the price, the network (Base), the asset (USDC) and where to pay.
2. An x402 client signs a USDC authorization and repeats the same call with the payment in
   `_meta["x402/payment"]`.
3. The answer carries the settlement receipt in `_meta["x402/payment-response"]`.

A payment is collected only when the tool returns a real answer: a miss, an error or a refused
read costs nothing. One payment buys one call of one tool. `my_watched_wallets` stays members
only. Clients without x402 support (Claude and ChatGPT today) show the request as an error that
names both ways in.

## Limits

- **Public tools spend nothing.** They answer from stored reads and never trigger a live scan.
  A token PumpPill has not read yet is queued for reading, and is usually available a few
  minutes later.
- **Two tools spend**, and only for a member or a caller who paid for that call: `rh_scan_now`
  and `x_chatter`. Both are annotated as not read-only and not idempotent so a client asks
  before calling them.
- **Rate limits:** 240 requests a minute per address and 60 a minute per client, then HTTP 429.
- **Coverage:** answers cover what PumpPill has scanned, not every contract on either chain.

## How to read the answers

- Quote `cite` and the as-of timestamp. Figures are recomputed continuously, and a number without
  its time goes stale within the hour.
- A flag is a finding with evidence, not a verdict. It says what is structurally true about a
  contract, not what the price will do.
- An outcome figure is a count, not a success rate for anyone who bought. Entry is the market cap
  at the moment PumpPill logged the token, which is not a price anyone was offered.
- `found: false` is an honest miss. Say so rather than filling the gap.

## Privacy

The server records one line per tool call: the tool name, whether it succeeded, how long it
took, whether a membership header was present (yes or no), and the name the client declares
for itself. It does not record the membership token or who is asking. A paid call also keeps
the payment record needed to settle it (tool, price, and the paying wallet named in the signed
authorization). Member tools send the
token to PumpPill only to check the membership. Full policy: <https://www.pumppill.org/privacy>

## Terms

Research, not advice. Nothing returned by this server is financial advice, an offer, or a
recommendation to buy or sell anything, and a clean read is evidence, not an endorsement. Quote
it with attribution and a link to the page the result cites. Terms of use:
<https://www.pumppill.org/terms> · citation terms: <https://www.pumppill.org/for-agents#terms>

## Links

- Website: <https://www.pumppill.org>
- For agents: <https://www.pumppill.org/for-agents>
- The MCP server, explained: <https://www.pumppill.org/blog/pumppill-mcp-server-token-safety-for-ai-assistants>
- Contact: pumppillai@gmail.com

## License

The contents of this repository (documentation, example configs, manifest) are MIT licensed; see
[LICENSE](LICENSE). The hosted service and the PumpPill name and logo are not covered by it.
