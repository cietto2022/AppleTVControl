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
            this.atv.metadata.put(s,o);
        });
    }
    @Override
    public void notifyUser(String s) {
        System.out.println(s);
    }

    // receives exception message
    public void notifyError(String s){
        // send to Log?
        notifyUser("Erro!");
    }
}
