import asyncio
from abc import ABC
from random import randrange

from pyatv import exceptions, scan, connect
from pyatv.const import FeatureState, FeatureName, Protocol, DeviceState, PowerState, MediaType
from pyatv.interface import Playing, AppleTV, PushListener
from pyatv.protocols.mrp.protobuf import RepeatMode

from const import *


class AppleTvEntry:
    def __init__(self, host, credentials: dict[Protocol, str], loop):
        self.host = host
        self.credentials = credentials | {}
        self.loop = loop


class AppleTvManager:
    def __init__(self, entry: AppleTvEntry):
        self.atv = None
        self.entry = entry
        self._connection_attempts = 0
        self._connection_was_lost = False
        self.is_on = True
        self._task = None

    async def initialize(self):
        await self.connect()

    async def connect(self):
        """Connect to device."""
        self.is_on = True
        self._start_connect_loop()

    def _start_connect_loop(self):
        """Start background connect loop to device."""
        if not self._task and self.atv is None and self.is_on:
            self._task = self.entry.loop.call_soon_threadsafe(self._connect_loop)
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
            backoff = min(
                max(
                    BACKOFF_TIME_LOWER_LIMIT,
                    randrange(2 ** self._connection_attempts),
                ),
                BACKOFF_TIME_UPPER_LIMIT,
            )

            print("Reconnecting in %d seconds", backoff)
            await asyncio.sleep(backoff)

        print("Connect loop ended")
        self._task = None

    async def connect_once(self, raise_missing_credentials):
        """Try to connect once."""
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
        self.atv.listener = self

        self._connection_attempts = 0
        if self._connection_was_lost:
            print("Connection was re-established to device")
            self._connection_was_lost = False

    async def disconnect(self):
        """Disconnect from device."""
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


class AppleTvEntity:
    def __init__(self, manager):
        self.atv = None
        self.manager = manager


class AppleTvPlayer(AppleTvEntity, PushListener, ABC):
    def __init__(self, manager: AppleTvManager):
        """Apple TV player representation"""
        super().__init__(manager)
        self._playing = None
        self._app_list = {}
        
    async def initialize(self):
        self.atv = self.manager.atv
        # Listen to push updates
        if self.atv.features.in_state(FeatureState.Available, FeatureName.PushUpdates):
            self.atv.push_updater.listener = self
            self.atv.push_updater.start()

        # Listen to power updates
        self.atv.power.listener = self
        
        if self.atv.features.in_state(FeatureState.Available, FeatureName.AppList):
            self.manager.entry.loop.create_task(self._update_app_list())

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

    def playstatus_update(self, updater, playstatus: Playing) -> None:
        self._playing = playstatus
        print(playstatus)

    def playstatus_error(self, updater, exception: Exception) -> None:
        print("erro")

    @property
    def state(self):
        """Return the state of the device."""
        if self.manager.is_connecting:
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

    # REMOTE CONTROL
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

    async def async_media_play_pause(self) -> None:
        """Pause media on media player."""
        if self._playing:
            await self.atv.remote_control.play_pause()

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

    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""
        if self.atv:
            await self.atv.remote_control.set_position(position)

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

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        if app_id := self._app_list.get(source):
            await self.atv.apps.launch_app(app_id)
