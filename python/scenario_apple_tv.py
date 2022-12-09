"""
    This is a Python scrypt for Scenario Apple TV Driver (used with JEP)
    @author: Paulo Cesar de Moraes Filho
"""

# *************** Imports and Constants
import asyncio
from abc import ABC
from random import randrange

from pyatv import exceptions, scan, connect, const, FacadeAppleTV
from pyatv.const import FeatureState, FeatureName, Protocol, PowerState, MediaType, DeviceState, InputAction
from pyatv.interface import Playing, PushListener, DeviceListener, PowerListener

BACKOFF_TIME_LOWER_LIMIT = 5  # seconds
BACKOFF_TIME_UPPER_LIMIT = 300  # Five minutes

MEDIA_TYPE_MUSIC = "Music"
MEDIA_TYPE_TVSHOW = "Tvshow"
MEDIA_TYPE_VIDEO = "Video"

STATE_IDLE = "Idle"
STATE_OFF = "Off"
STATE_PAUSED = "Paused"
STATE_PLAYING = "Playing"
STATE_STANDBY = "Standby"


# *************** Apple TV Classes
class AppleTvEntry:
    def __init__(self, host, credentials: dict[Protocol, str], loop: asyncio.AbstractEventLoop):
        self.host = host
        self.credentials = credentials | {}
        self.loop = loop


class ScenarioAppleTV(DeviceListener, PowerListener, PushListener, ABC):
    def __init__(self, entry: AppleTvEntry):
        """
            Apple TV representation.
            - DeviceListener: connection callbacks
            - PowerListener: Deep Sleep (on/off) callbacks
            - PushListener: State changes callbacks
        """
        self.atv: FacadeAppleTV = None
        self.entry = entry
        self._connection_attempts = 0
        self._connection_was_lost = False
        self.is_on = True
        self._task = None
        self._playing = None
        self._app_list = {}

# *************** Connection handling functions
    async def initialize(self):
        await self.connect()

    def _init_listeners(self):
        # Self listener
        self.atv.listener = self

        # Listen to push updates
        if self.atv.features.in_state(FeatureState.Available, FeatureName.PushUpdates):
            self.atv.push_updater.listener = self
            self.atv.push_updater.start()

        # Listen to power updates
        self.atv.power.listener = self

        if self.atv.features.in_state(FeatureState.Available, FeatureName.AppList):
            self.entry.loop.create_task(self._update_app_list())

    async def connect(self):
        """Connect to device."""
        self.is_on = True
        self._start_connect_loop()

    def _start_connect_loop(self):
        """Starts a connection loop on background."""
        if not self._task and self.atv is None and self.is_on:
            self._task = self.entry.loop.create_task(self._connect_loop())
        else:
            print("Not starting loop")

    async def _connect_loop(self):
        """Connect loop background task function."""
        print("Starting connect loop")

        # Try to find device and connect as long as the user has said that
        # we are allowed to connect and we are not already connected.
        while self.is_on and self.atv is None:
            await self.connect_once(raise_missing_credentials=False)
            if self.atv is not None:
                break
            self._connection_attempts += 1
            # backoff = min(
            #     max(
            #         BACKOFF_TIME_LOWER_LIMIT,
            #         randrange(2 ** self._connection_attempts),
            #     ),
            #     BACKOFF_TIME_UPPER_LIMIT,
            # )
            backoff = BACKOFF_TIME_LOWER_LIMIT

            print("Reconnecting in %d seconds", backoff)
            await asyncio.sleep(backoff)

        print("Connect loop ended")
        self._task = None

    async def connect_once(self, raise_missing_credentials):
        """Try to establish a connection once."""
        try:
            if conf := await self.host_scan():
                await self.host_connect(conf, raise_missing_credentials)
        except exceptions.AuthenticationError:
            # self.config_entry.async_start_reauth(self.hass)
            asyncio.create_task(self.disconnect())
            print("Authentication failed...")
            return
        except asyncio.CancelledError:
            pass
        except (Exception,):  # pylint: disable=broad-except
            print("Failed to connect")
            self.atv = None

    async def host_scan(self):
        """Search for a specific address provided by AppleTVEntry."""
        address = self.entry.host

        protocols = {
            Protocol(int(protocol))
            for protocol in self.entry.credentials
        }

        atv_list = await scan(self.entry.loop, protocol=protocols, hosts=[address])

        if atv_list:
            return atv_list[0]

        print("Device not found")
        return None

    async def host_connect(self, conf, raise_missing_credentials):
        """Setup credentials and protocols then connect to host address."""
        credentials = self.entry.credentials
        missing_protocols = []

        for protocol_int, creds in credentials.items():
            protocol = Protocol(int(protocol_int))
            if conf.get_service(protocol) is not None:
                conf.set_credentials(protocol, creds)
            else:
                missing_protocols.append(protocol.name)

        if missing_protocols:
            missing_protocols_str = ", ".join(missing_protocols)
            if raise_missing_credentials:
                print("missing credentials")
            print(f"missing protocols {missing_protocols_str}")
            return

        print("Connecting...")
        self.atv = await connect(conf, self.entry.loop)
        self._init_listeners()

        self._connection_attempts = 0
        if self._connection_was_lost:
            print("Connection was re-established to device")
            self._connection_was_lost = False

    async def disconnect(self):
        """Disconnect the device."""
        print("Disconnecting from device")
        self.is_on = False
        try:
            if self.atv:
                self.atv.close()
                self.atv = None
            if self._task:
                self._task.cancel()
                self._task = None
        except (Exception,):  # pylint: disable=broad-except
            print("An error occurred while disconnecting")

    def _handle_disconnect(self):
        """Handle with a connection lost."""
        if self.atv:
            self.atv.close()
            self.atv = None
        self._start_connect_loop()

# *************** Callbacks dos Listeners
    def connection_lost(self, _):
        """Device disconnected unintentionally.
        This is a callback function from pyatv.interface.DeviceListener.
        """
        print('Connection lost to Apple TV')
        self._connection_was_lost = True
        self._handle_disconnect()

    def connection_closed(self):
        """Device disconnected intentionally - close().
        This is a callback function from pyatv.interface.DeviceListener.
        """
        # self._handle_disconnect()

    def playstatus_update(self, updater, playstatus: Playing) -> None:
        """Retrieve playing information when state changes.
        This is a callback function from pyatv.interface.PushListener.
        """
        self._playing = playstatus
        print(" ")
        print(playstatus)

    def playstatus_error(self, updater, exception: Exception) -> None:
        """Called when got a playing error.
        This is a callback function from pyatv.interface.PushListener.
        """
        print("erro")

    def powerstate_update(
            self, old_state: const.PowerState, new_state: const.PowerState
    ):
        print(new_state)

# *************** App List Update
    async def _update_app_list(self):
        print("Updating app list")
        try:
            apps = await self.atv.apps.app_list()
        except exceptions.NotSupportedError:
            print("Listing apps is not supported")
        except exceptions.ProtocolError:
            print("Failed to update app list")
        else:
            self._app_list = {
                app.name: app.identifier
                for app in sorted(apps, key=lambda app: app.name.lower())
            }

# *************** Apple TV Properties (GET)
    @property
    def is_connecting(self):
        """Return true if connection is in progress."""
        return self._task is not None

    @property
    def state(self):
        """Return the state of the device."""
        if self.is_connecting:
            return None
        if self.atv is None:
            return STATE_OFF
        if (
                self._is_feature_available(FeatureName.PowerState)
                and self.atv.power.power_state == PowerState.Off
        ):
            return STATE_STANDBY
        if self._playing:
            state = self._playing.device_state
            if state in (DeviceState.Idle, DeviceState.Loading):
                return STATE_IDLE
            if state == DeviceState.Playing:
                return STATE_PLAYING
            if state in (DeviceState.Paused, DeviceState.Seeking, DeviceState.Stopped):
                return STATE_PAUSED
            return STATE_STANDBY  # Bad or unknown state?
        return None

    @property
    def app_id(self):
        """ID of the current running app."""
        if self._is_feature_available(FeatureName.App):
            return self.atv.metadata.app.identifier
        return None

    @property
    def app_name(self):
        """Name of the current running app."""
        if self._is_feature_available(FeatureName.App):
            return self.atv.metadata.app.name
        return None

    @property
    def source_list(self):
        """List of available input sources."""
        return list(self._app_list.keys())

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        if self._playing:
            return {
                MediaType.Video: MEDIA_TYPE_VIDEO,
                MediaType.Music: MEDIA_TYPE_MUSIC,
                MediaType.TV: MEDIA_TYPE_TVSHOW,
            }.get(self._playing.media_type)
        return None

    @property
    def media_content_id(self):
        """Content ID of current playing media."""
        if self._playing:
            return self._playing.content_identifier
        return None

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        if self._is_feature_available(FeatureName.Volume):
            return self.atv.audio.volume / 100.0  # from percent
        return None

    @property
    def media_duration(self):
        """Duration of current playing media in seconds."""
        if self._playing:
            return self._playing.total_time
        return None

    @property
    def media_position(self):
        """Position of current playing media in seconds."""
        if self._playing:
            return self._playing.position
        return None

    @property
    def media_title(self):
        """Title of current playing media."""
        if self._playing:
            return self._playing.title
        return None

    @property
    def media_artist(self):
        """Artist of current playing media, music track only."""
        if self._is_feature_available(FeatureName.Artist):
            return self._playing.artist
        return None

    @property
    def media_album_name(self):
        """Album name of current playing media, music track only."""
        if self._is_feature_available(FeatureName.Album):
            return self._playing.album
        return None

    @property
    def media_series_title(self):
        """Title of series of current playing media, TV show only."""
        if self._is_feature_available(FeatureName.SeriesName):
            return self._playing.series_name
        return None

    @property
    def media_season(self):
        """Season of current playing media, TV show only."""
        if self._is_feature_available(FeatureName.SeasonNumber):
            return str(self._playing.season_number)
        return None

    @property
    def media_episode(self):
        """Episode of current playing media, TV show only."""
        if self._is_feature_available(FeatureName.EpisodeNumber):
            return str(self._playing.episode_number)
        return None

    async def async_get_media_image(self):
        """Fetch media image of current playing image."""
        state = self.state
        if self._playing and state not in [STATE_OFF, STATE_IDLE]:
            artwork = await self.atv.metadata.artwork()
            if artwork:
                return artwork.bytes, artwork.mimetype

        return None, None

    def _is_feature_available(self, feature):
        """Return if a feature is available."""
        if self.atv and self._playing:
            return self.atv.features.in_state(FeatureState.Available, feature)
        return False

# *************** Physical Remote Control functions
    async def async_up(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.up(action)

    async def async_down(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.down(action)

    async def async_left(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.left(action)

    async def async_right(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.right(action)

    async def async_select(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.select(action)

    async def async_menu(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.menu(action)

    async def async_home(self, action: InputAction = InputAction.SingleTap) -> None:
        if self.atv:
            await self.atv.remote_control.home(action)

    async def async_media_play_pause(self) -> None:
        """Pause media on media player."""
        if self._playing:
            await self.atv.remote_control.play_pause()

    async def async_remote_volume_up(self) -> None:
        if self.atv:
            await self.atv.remote_control.volume_up()

    async def async_remote_volume_down(self) -> None:
        if self.atv:
            await self.atv.remote_control.volume_down()

# *************** Audio functions
    async def async_volume_up(self) -> None:
        """Turn volume up for media player."""
        if self.atv:
            await self.atv.audio.volume_up()

    async def async_volume_down(self) -> None:
        """Turn volume down for media player."""
        if self.atv:
            await self.atv.audio.volume_down()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        if self.atv:
            # pyatv expects volume in percent
            await self.atv.audio.set_volume(volume * 100.0)

# *************** Extra functions (logical Remote Control)
    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        if self._is_feature_available(FeatureName.TurnOn):
            await self.atv.power.turn_on()

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        if (self._is_feature_available(FeatureName.TurnOff)) and (
                not self._is_feature_available(FeatureName.PowerState)
                or self.atv.power.power_state == PowerState.On
        ):
            await self.atv.power.turn_off()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        if app_id := self._app_list.get(source):
            await self.atv.apps.launch_app(app_id)

    async def async_media_play(self) -> None:
        """Play media."""
        if self.atv:
            await self.atv.remote_control.play()

    async def async_media_stop(self) -> None:
        """Stop the media player."""
        if self.atv:
            await self.atv.remote_control.stop()

    async def async_media_pause(self) -> None:
        """Pause the media player."""
        if self.atv:
            await self.atv.remote_control.pause()

    async def async_media_next_track(self) -> None:
        """Send next track command."""
        if self.atv:
            await self.atv.remote_control.next()

    async def async_media_previous_track(self) -> None:
        """Send previous track command."""
        if self.atv:
            await self.atv.remote_control.previous()

    async def async_media_seek(self, position: int) -> None:
        """Send seek command."""
        if self.atv:
            await self.atv.remote_control.set_position(position)

    async def async_media_repeat(self) -> None:
        """Set repeat status."""
        if self.atv:
            await self.atv.remote_control.set_repeat()

    async def async_media_shuffle(self) -> None:
        """Set shuffle status."""
        if self.atv:
            await self.atv.remote_control.set_shuffle()

    async def async_media_skip_backward(self) -> None:
        """Send skip_backward command."""
        if self.atv:
            await self.atv.remote_control.skip_backward()

    async def async_media_skip_forward(self) -> None:
        """Send skip_forward command."""
        if self.atv:
            await self.atv.remote_control.skip_forward()

    async def async_channel_up(self) -> None:
        """Send channel up command."""
        if self.atv:
            await self.atv.remote_control.channel_up()

    async def async_channel_down(self) -> None:
        """Send channel down command."""
        if self.atv:
            await self.atv.remote_control.channel_down()

    async def async_top_menu(self) -> None:
        """Back to top menu of Apple TV."""
        if self.atv:
            await self.atv.remote_control.top_menu()
