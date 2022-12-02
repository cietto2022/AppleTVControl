package com.example.appletvcontrol;

import jep.Interpreter;

public class Publisher {

    Interpreter interp;

    public Publisher(Interpreter interp) {
        this.interp = interp;
        String pythonScriptFullPath = "./python/oldScenarioAppleTV.py";
        this.interp.runScript(pythonScriptFullPath);
        this.interp.exec("apple_tv = ScenarioAppleTV('192.168.10.246')");
    }

    public void scan_network(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv.scan_network())");
    }

    public void connect(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv.connect())");
    }

    public void setListener(Listener listener){
        interp.set("java_listener", listener);
        interp.exec("apple_tv._java_listener = java_listener");
    }

    public void run_forever(){
        interp.exec("apple_tv._loop.run_forever()");
    }

    public void channel_down(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.channel_down())");
    }

    public void channel_up(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.channel_up())");
    }

    public void down(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.down())");
    }

    public void home(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.home())");
    }

    public void home_hold(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.home_hold())");
    }

    public void left(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.left())");
    }

    public void menu(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.menu())");
    }

    public void next(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.next())");
    }

    public void play(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.play())");
    }

    public void pause(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.pause())");
    }

    public void play_pause(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.play_pause())");
    }

    public void right(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.right())");
    }

    public void select(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.select())");
    }

    public void set_position(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_position())");
    }

    public void set_repeat(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_repeat())");
    }

    public void set_shuffle(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_shuffle())");
    }

    public void skip_backward(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.skip_backward())");
    }

    public void skip_forward(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.skip_forward())");
    }

    public void stop(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.stop())");
    }

    public void suspend(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.suspend())");
    }

    public void top_menu(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.top_menu())");
    }

    public void up(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.up())");
    }

    public void volume_down(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.volume_down())");
    }

    public void volume_up(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.volume_up())");
    }

    public void wakeup(){
        this.interp.exec("apple_tv._loop.run_until_complete(apple_tv._client.remote_control.wakeup())");
    }

}
