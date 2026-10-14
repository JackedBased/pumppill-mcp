"""Read Robinhood Chain through PumpPill's MCP server with the OpenAI Agents SDK.

pip install openai-agents
"""
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp


async def main() -> None:
    async with MCPServerStreamableHttp(params={"url": "https://api.pumppill.org/mcp"}) as pumppill:
        agent = Agent(
            name="Robinhood Chain reader",
            instructions="Answer from PumpPill's tools and quote each answer's cite line.",
            mcp_servers=[pumppill],
        )
        result = await Runner.run(agent, "What launched on Robinhood Chain in the last 6 hours above a $20K market cap?")
        print(result.final_output)


asyncio.run(main())
