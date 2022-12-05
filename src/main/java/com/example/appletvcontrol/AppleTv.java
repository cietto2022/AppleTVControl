package com.example.appletvcontrol;

import java.util.HashMap;
import java.util.Map;

public class AppleTv {
    AppleTVCommands atvCommands;
    Map<String, Object> metadata = new HashMap<>();
    Map<String, Object> powerdata = new HashMap<>();

    public AppleTv() {
        metadata.put("media_type", null);
        metadata.put("device_state", null);
        metadata.put("title", null);
        metadata.put("artist", null);
        metadata.put("album", null);
        metadata.put("genre", null);
        metadata.put("total_time", null);
        metadata.put("position", null);
        metadata.put("shuffle", null);
        metadata.put("repeat", null);
        metadata.put("hash", null);
        metadata.put("series_name", null);
        metadata.put("season_number", null);
        metadata.put("episode_number", null);
        metadata.put("content_identifier", null);





    }
}
