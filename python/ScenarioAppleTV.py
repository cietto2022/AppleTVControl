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

    async def channel_down(self):
        await self._client.remote_control.channel_down()

    async def channel_up(self):
        await self._client.remote_control.channel_up()

    async def down(self):
        await self._client.remote_control.down()

    async def home(self):
        await self._client.remote_control.home()

    async def home_hold(self):
        await self._client.remote_control.home_hold()

    async def left(self):
        await self._client.remote_control.left()

    async def menu(self):
        await self._client.remote_control.menu()

    async def next(self):
        await self._client.remote_control.next()

    async def pause(self):
        await self._client.remote_control.pause()

    async def play(self):
        await self._client.remote_control.play()

    async def play_pause(self):
        await self._client.remote_control.play_pause()

    async def previous(self):
        await self._client.remote_control.previous()

    async def right(self):
        await self._client.remote_control.right()

    async def select(self):
        await self._client.remote_control.select()

    async def set_position(self):
        await self._client.remote_control.set_position()

    async def set_repeat(self):
        await self._client.remote_control.set_repeat()

    async def set_shuffle(self):
        await self._client.remote_control.select()

    async def skip_backward(self):
        await self._client.remote_control.skip_backward()

    async def skip_forward(self):
        await self._client.remote_control.skip_forward()

    async def stop(self):
        await self._client.remote_control.stop()

    async def suspend(self):
        await self._client.remote_control.suspend()

    async def top_menu(self):
        await self._client.remote_control.top_menu()

    async def up(self):
        await self._client.remote_control.up()

    async def volume_down(self):
        await self._client.remote_control.volume_down()

    async def volume_up(self):
        await self._client.remote_control.volume_up()

    async def wakeup(self):
        await self._client.remote_control.wakeup()


