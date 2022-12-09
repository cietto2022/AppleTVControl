import asyncio

from pyatv import Protocol

from apple_tv import AppleTvEntry, AppleTvManager, AppleTvPlayer
from scenario_apple_tv import ScenarioAppleTV

AIRPLAY_CREDENTIAL = '6f955f6ee74b2ed83377e60060ba3db9bacd64326cf93a9ab923f3bb9134775f' \
                     ':523d4f77349f21cb057e1c3f2385e9339b0fc2ee2863e8cdabbc0365c730a01d' \
                     ':32303134463939422d304141362d344633442d413432332d334644444635433936324130' \
                     ':33653032383039382d346138662d343962332d396364302d336639623163626234313430'

COMPANION_CREDENTIAL = '6f955f6ee74b2ed83377e60060ba3db9bacd64326cf93a9ab923f3bb9134775f' \
                       ':09c42c97d65a1bd6b19206a24cbfc685161f31bc60ee6a20855b4a6e2ac2def1' \
                       ':32303134463939422d304141362d344633442d413432332d334644444635433936324130' \
                       ':61616564323932322d636234632d346137372d393464352d323665393133393631636364'

RAOP_CREDENTIAL = ":32e27a36c320128e0cc5da245aabcba2987aed5d074e1be89822d363531a02e0::cafc6ed88b69d97a"

HOST_IP = '192.168.11.38'

MAIN_LOOP = asyncio.new_event_loop()


async def test_tv():
    creds = {
        Protocol.AirPlay.value: AIRPLAY_CREDENTIAL,
        Protocol.Companion.value: COMPANION_CREDENTIAL,
        Protocol.RAOP.value: RAOP_CREDENTIAL
    }
    entry = AppleTvEntry(HOST_IP, creds, MAIN_LOOP)

    my_atv = ScenarioAppleTV(entry)

    await my_atv.connect_once(True)
    if not my_atv.atv:
        print("deu ruim")
    else:
        await my_atv.initialize()
        await asyncio.sleep(2)

    while True:
        try:
            await asyncio.sleep(2)
            # await my_atv.atv.remote_control.right()
            # await asyncio.sleep(2)
            # await my_atv.atv.remote_control.up()
            # await asyncio.sleep(2)
            # await my_atv.atv.remote_control.down()
            # await asyncio.sleep(2)
            # await my_atv.atv.remote_control.left()
        except (Exception,):
            pass


MAIN_LOOP.run_until_complete(test_tv())


