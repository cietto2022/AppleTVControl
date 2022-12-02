package com.example.appletvcontrol;

public class AppleTVCommands {

    public String createAppleTV(){
        return "apple_tv = ScenarioAppleTV('192.168.10.246')";
    }

    public String scan_network(){
        return "apple_tv._loop.run_until_complete(apple_tv.scan_network())";
    }

    public String connect(){
        return "apple_tv._loop.run_until_complete(apple_tv.connect())";
    }

    //public void setListener(Listener listener){
    //    interp.set("java_listener", listener);
    //    interp.exec("apple_tv._java_listener = java_listener");
    //}

    public String run_forever(){
        return "apple_tv._loop.run_forever()";
    }

    public String channel_down(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.channel_down())";
    }

    public String channel_up(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.channel_up())";
    }

    public String down(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.down())";
    }

    public String home(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.home())";
    }

    public String home_hold(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.home_hold())";
    }

    public String left(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.left())";
    }

    public String menu(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.menu())";
    }

    public String next(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.next())";
    }

    public String play(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.play())";
    }

    public String pause(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.pause())";
    }

    public String play_pause(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.play_pause())";
    }

    public String right(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.right())";
    }

    public String select(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.select())";
    }

    public String set_position(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_position())";
    }

    public String set_repeat(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_repeat())";
    }

    public String set_shuffle(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.set_shuffle())";
    }

    public String skip_backward(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.skip_backward())";
    }

    public String skip_forward(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.skip_forward())";
    }

    public String stop(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.stop())";
    }

    public String suspend(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.suspend())";
    }

    public String top_menu(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.top_menu())";
    }

    public String up(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.up())";
    }

    public String volume_down(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.volume_down())";
    }

    public String volume_up(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.volume_up())";
    }

    public String wakeup(){
        return "apple_tv._loop.run_until_complete(apple_tv._client.remote_control.wakeup())";
    }

}
