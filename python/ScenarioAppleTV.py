import asyncio
from abc import ABC

from pyatv import connect, scan, const, Protocol
from java.lang import System
from pyatv.interface import PowerListener, PushListener, Playing, DeviceListener

# EXPERIMENTAL CREDENTIALS - TO BE DELETED
COMPANION_CREDENTIAL = '6f955f6ee74b2ed83377e60060ba3db9bacd64326cf93a9ab923f3bb9134775f' \
                       ':09c42c97d65a1bd6b19206a24cbfc685161f31bc60ee6a20855b4a6e2ac2def1' \
                       ':32303134463939422d304141362d344633442d413432332d334644444635433936324130' \
                       ':61616564323932322d636234632d346137372d393464352d323665393133393631636364'

RAOP_CREDENTIAL = ":32e27a36c320128e0cc5da245aabcba2987aed5d074e1be89822d363531a02e0::cafc6ed88b69d97a"

AIRPLAY_CREDENTIAL = '6f955f6ee74b2ed83377e60060ba3db9bacd64326cf93a9ab923f3bb9134775f' \
                     ':523d4f77349f21cb057e1c3f2385e9339b0fc2ee2863e8cdabbc0365c730a01d' \
                     ':32303134463939422d304141362d344633442d413432332d334644444635433936324130' \
                     ':33653032383039382d346138662d343962332d396364302d336639623163626234313430'


class ScenarioAppleTV:
    def __init__(self, host):
        self._host = host
        self._atv = None
        self._client = None
        self._loop = asyncio.new_event_loop()
        self._listener = AppleTVListeners()
        self._media_last_position = 0

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

        conf = self._atv
        conf.set_credentials(Protocol.Companion, COMPANION_CREDENTIAL)
        conf.set_credentials(Protocol.RAOP, RAOP_CREDENTIAL)
        conf.set_credentials(Protocol.AirPlay, AIRPLAY_CREDENTIAL)

        self._client = await connect(conf, self._loop, Protocol.Companion)
        self._client.power.listener = self._listener
        self._client.listener = self._listener
        self._client.push_updater.listener = self._listener
        self._client.push_updater.start()

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
                self._client.close()
                await self.connection_lost(asyncio.TimeoutError)
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
