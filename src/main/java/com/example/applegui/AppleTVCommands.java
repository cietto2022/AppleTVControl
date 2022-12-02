package com.example.applegui;

public class AppleTVCommands {
    public static String createAppleTV(String ip){
        return "apple_tv = ScenarioAppleTV('"+ ip + "')";
    }

    public static String scan_network(){
        return "apple_tv._loop.run_until_complete(apple_tv.scan_network())";
    }

    public static String connect(){
        return "apple_tv._loop.run_until_complete(apple_tv.connect())";
    }

    public static String run_forever(){
        return "apple_tv._loop.run_forever()";
    }

    public static String channel_down(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.channel_down())";
    }

    public static String channel_up(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.channel_up())";
    }

    public static String down(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.down())";
    }

    public static String home(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.home())";
    }

    public static String home_hold(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.home_hold())";
    }

    public static String left(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.left())";
    }

    public static String menu(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.menu())";
    }

    public static String next(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.next())";
    }

    public static String play(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.play())";
    }

    public static String pause(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.pause())";
    }

    public static String play_pause(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.play_pause())";
    }

    public static String right(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.right())";
    }

    public static String select(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.select())";
    }

    public static String set_position(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_position())";
    }

    public static String set_repeat(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_repeat())";
    }

    public static String set_shuffle(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_shuffle())";
    }

    public static String skip_backward(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.skip_backward())";
    }

    public static String skip_forward(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.skip_forward())";
    }

    public static String stop(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.stop())";
    }

    public static String suspend(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.suspend())";
    }

    public static String top_menu(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.top_menu())";
    }

    public static String up(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.up())";
    }

    public static String volume_down(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.volume_down())";
    }

    public static String volume_up(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.volume_up())";
    }

    public static String wakeup(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.wakeup())";
    }

    public static String launch_app(String appId){
        return "apple_tv._loop.run_until_complete(apple_tv._client.apps.launch_app('"+ appId+"'))";
    }
}
