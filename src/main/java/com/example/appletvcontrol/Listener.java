package com.example.appletvcontrol;

import java.util.Map;

public class Listener implements UpdateListener {
    //UpdateListener java_listener;

    public Listener() {
        //this.java_listener = value -> value.forEach((s, o) -> System.out.println("PRINT JAVA:::: " + s + ": " + o));
    }

    @Override
    public void notify(Map<String, Object> value) {
        value.forEach((s, o) -> System.out.println("PRINT JAVA:::: " + s + ": " + o));

    }
}