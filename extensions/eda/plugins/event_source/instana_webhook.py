"""An ansible-rulebook event source module for receiving events via a Instana.

Arguments:
---------
    host: The hostname to listen to. Set to 0.0.0.0 to listen on all
          interfaces. Defaults to 127.0.0.1
    port: The TCP port to listen to.  Defaults to 5000
    - name: Listen for events on a webhook
  hosts: all
  ## Define our source for events
  sources:
   - ibm.instana.instana_webhook:
       host: 0.0.0.0
       port: 5000
 ## Define the conditions we are looking for
  rules:
   - name: Test
     condition: event.payload.message == "Node failed"
     action:
        run_playbook:
          name: test..yml
   - name: Event
     condition: event.payload.problem.problemText == "Erroneous call rate is too high"
     action:
        run_playbook:
          name: remediate.yml
"""

import asyncio
import logging
from typing import Any

from aiohttp import web

routes = web.RouteTableDef()
@routes.post("/{instana}")
async def instana_webhook(request: web.Request) -> web.Response:
    """Do parsing of Instana event data from the request.

    Arguments:
    ---------
    request (web.Request): Request from Instana.

    Returns:
    -------
    response(web.Response): Create response with results.
    """
    payload = await request.json()
    endpoint = request.match_info["instana"]
    data = {
        "payload": payload,
        "meta": {"endpoint": endpoint, "headers": dict(request.headers)},
    }
    await request.app["queue"].put(data)
    return web.Response(text=endpoint)


async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    """Start server on port 5000 listening for Instana events.

    Arguments:
    ---------
    queue (Queue): Order incoming request from Instana.
    args (dict): Use server configurations.
    """
    app = web.Application()
    app["queue"] = queue

    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, args.get("host") or "localhost",
        args.get("port") or 5000,
       )
    await site.start()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
       logging.info("Plugin Task Cancelled")
    finally:
        await runner.cleanup()

"""Begin main method."""
if __name__ == "__main__":
    class MockQueue:
        """Start Queue for incoming request.

        Arguments:
        ---------
        event: Event used stored in queue.
        """

        async def put(self: instana_webhook, event: web.Event) -> None:
            """Log the incoming event from Instana."""
            logging.info(event)

    asyncio.run(main(MockQueue(), {}))
