package com.example.appletvcontrol;

public class ScenATV {

    Publisher publisher;
    ATVData atvData;

    public ScenATV(Publisher pub) {
        this.publisher = pub;
        atvData = new ATVData();
    }

    //public void volume_up(){
        //publisher.volume_up();
    //}

    public int getVolume() {
        return atvData.vol;
    }

    public void setVolume(int volume) {
        atvData.vol = volume;
    }
}
