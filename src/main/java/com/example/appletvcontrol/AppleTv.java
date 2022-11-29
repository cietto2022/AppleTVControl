package com.example.appletvcontrol;

import java.util.HashMap;
import java.util.Map;

public class AppleTv {

    ATVData atvData;

    Map<String, Object> data = new HashMap<>();


    String media_type = "media_type";
    String device_state = "device_state";
    String title = "title";
    String artist = "artist";
    String album = "album";
    String genre = "genre";
    String total_time = "total_time";
    String position = "position";
    String shuffle = "shuffle";
    String repeat = "repeat";
    String hash = "hash";
    String series_name = "series_name";
    String season_number = "season_number";
    String episode_number = "episode_number";
    String content_identifier = "content_identifier";

    public AppleTv() {
        atvData = new ATVData();
        data.put("media_type", " ");
        data.put("media_type", " ");
        data.put("media_type", " ");
    }

    public int getVolume() {
        return atvData.vol;
    }

    public void setVolume(int volume) {
        atvData.vol = volume;
    }
}
