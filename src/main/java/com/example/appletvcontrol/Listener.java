package com.example.appletvcontrol;

import java.util.HashMap;
import java.util.Map;

public class Listener implements UpdateListener {
    AppleTv atv;

    public Listener(AppleTv atv) {
        this.atv = atv;
    }

    @Override
    public void notify(Map<String, Object> value) {
        value.forEach((s, o) -> {
            System.out.println("PRINT JAVA:::: " + s + ": " + o);
            this.atv.data.put(s,o);
        });

    }
}
