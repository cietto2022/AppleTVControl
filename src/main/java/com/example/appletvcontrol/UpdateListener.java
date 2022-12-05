package com.example.appletvcontrol;

import java.util.Map;

public interface UpdateListener {

    void notify(Map<String, Object> value);
    void notifyUser(String s);

    public void notifyError(String s);

}
