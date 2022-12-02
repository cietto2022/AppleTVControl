import asyncio
from abc import ABC
from pyatv import connect, scan, const
from java.lang import System
from pyatv.interface import PushListener, Playing, DeviceListener, PowerListener


class ScenarioAppleTV(DeviceListener, PushListener, PowerListener, ABC):

    def __init__(self, host):
        self._host = host
        self._atv = None
        self._client = None
        self._loop = asyncio.new_event_loop()
        self._java_listener = None

    async def scan_network(self):
        atv = await scan(self._loop, hosts=[self._host], timeout=5)

        if not atv:
            System.out.println("No devices found...")
            return False

        for a in atv:
            System.out.println(f"Name: {a.name}, Address: {a.address}")

        self._atv = atv[0]
        return True

    async def connect(self):
        self._client = await connect(self._atv, self._loop)
        System.out.println("connected apple tv")
        self._client.power.listener = self
        self._client.push_updater.listener = self
        self._client.push_updater.start()

    def playstatus_update(self, updater, playstatus: Playing) -> None:
        System.out.println("-")
        System.out.println("-")
        System.out.println(str(playstatus))
        self._java_listener.notify({"playstatus": playstatus})

    def playstatus_error(self, updater, exception: Exception) -> None:
        System.out.println(str(exception))

    def connection_lost(self, exception: Exception) -> None:
        System.out.println(str(exception))
        message = "connection suddenly lost"
        self._java_listener.notify({"problem": message})
        System.out.println("Apple TV lost connection")

    def connection_closed(self) -> None:
        message = "Apple TV closed connection"
        self._java_listener.notify({"problem": message})
        System.out.println("Apple TV closed connection")

    def powerstate_update(self, old_state: const.PowerState, new_state: const.PowerState):
        System.out.println(str(old_state))
        System.out.println(str(new_state))


