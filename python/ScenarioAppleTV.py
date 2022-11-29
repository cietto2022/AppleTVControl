import asyncio
from abc import ABC

from pyatv import connect, scan, const
from java.lang import System
from pyatv.interface import PowerListener, PushListener, Playing, DeviceListener


class ScenarioAppleTV:
    def __init__(self, host):
        self._host = host
        self._atv = None
        self._client = None
        self._loop = asyncio.new_event_loop()
        self._listener = AppleTVListeners()

    async def scan_network(self):
        atv = await scan(self._loop, hosts=[self._host], timeout=5)
        await asyncio.sleep(3)

        if not atv:
            System.out.println("No devices found...")
            return False

        for a in atv:
            System.out.println(f"Name: {a.name}, Address: {a.address}")

        self._atv = atv[0]

        return True

    async def connect(self):
        await self.scan_network()
        self._client = await connect(self._atv, self._loop)
        self._client.power.listener = self._listener
        self._client.listener = self._listener
        self._client.push_updater.listener = self._listener
        self._client.push_updater.start()

    async def play_pause(self):
        await self._client.remote_control.play_pause()

    async def up(self):
        await self._client.remote_control.up()

    async def down(self):
        await self._client.remote_control.down()

    async def left(self):
        await self._client.remote_control.left()

    async def right(self):
        await self._client.remote_control.right()

    async def select(self):
        await self._client.remote_control.select()

    async def menu(self):
        await self._client.remote_control.menu()

    async def set_position(self, position):
        await self._client.remote_control.set_position(position)

    async def close(self):
        result = await self._client.close()
        return result

    async def check_if_alive(self):
        while True:
            await asyncio.sleep(2)
            try:
                is_playing = await asyncio.wait_for(self._client.metadata.playing(), 10)
            except asyncio.TimeoutError:
                System.out.println("Nada...")
                # self._client.close()
                self._listener.connection_lost(asyncio.TimeoutError)
            else:
                System.out.println(" ")
                System.out.println(str(is_playing))

    async def connection_lost(self, exception: Exception) -> None:
        """Device was unexpectedly disconnected."""
        System.out.println("Connection lost...")
        new_connection = ScenarioAppleTV('192.168.10.246')

        while not new_connection._client:
            try:
                await asyncio.wait_for(new_connection.connect(), 10)
            except asyncio.TimeoutError:
                System.out.println("Connection failed... trying again")
            else:
                self._client = new_connection._client


class AppleTVListeners(PowerListener, PushListener, DeviceListener, ABC):
    # PowerListener methods
    def powerstate_update(
            self, old_state: const.PowerState, new_state: const.PowerState
    ):
        System.out.println(str(new_state))

    # PushListener methods
    def playstatus_update(self, updater, playstatus: Playing) -> None:
        if not playstatus:
            self.connection_lost()
        else:
            System.out.println(" ")
            System.out.println(" ")
            System.out.println(str(playstatus))

    def playstatus_error(self, updater, exception: Exception) -> None:
        System.out.println(str(exception))

    # DeviceListener methods
    def connection_lost(self, exception: Exception) -> None:
        """Device was unexpectedly disconnected."""
        System.out.println("Connection lost...")

    def connection_closed(self) -> None:
        """Device connection was (intentionally) closed."""
        System.out.println("Connection closed...")
