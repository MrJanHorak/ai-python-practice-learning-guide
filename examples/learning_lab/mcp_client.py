"""Launch the local stdio server and list or call its tools without any model."""
import argparse
import asyncio
import json
import os
import sys
from datetime import timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def exchange(tool=None, arguments=None):
    # MCP inherits only a safe base environment by default; pass our demo settings explicitly.
    settings = {key: value for key, value in os.environ.items() if key.startswith('LEARNING_REVIEW_')}
    parameters = StdioServerParameters(command=sys.executable, args=['-m', 'examples.learning_lab.mcp_server'], env=settings)
    async with stdio_client(parameters) as (reader, writer):
        async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=15)) as session:
            await session.initialize()
            if tool is None:
                return (await session.list_tools()).model_dump(mode='json')
            return (await session.call_tool(tool, arguments=arguments or {})).model_dump(mode='json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['list', 'call'])
    parser.add_argument('--tool')
    parser.add_argument('--arguments', default='{}', help='JSON object; see lesson for PowerShell examples')
    parser.add_argument('--arguments-file', help='Read JSON arguments from a file instead')
    args = parser.parse_args()
    if args.operation == 'call' and not args.tool:
        parser.error('--tool is required for call')
    if args.arguments_file:
        from pathlib import Path
        arguments = json.loads(Path(args.arguments_file).read_text(encoding='utf-8-sig'))
    else:
        arguments = json.loads(args.arguments)
    if not isinstance(arguments, dict):
        parser.error('Arguments must be a JSON object')
    print(json.dumps(asyncio.run(exchange(args.tool if args.operation == 'call' else None, arguments)), indent=2))


if __name__ == '__main__':
    main()
