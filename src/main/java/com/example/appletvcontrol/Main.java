package com.example.appletvcontrol;

import jep.Jep;
import jep.JepException;
import jep.Interpreter;
import jep.SharedInterpreter;

public class Main {

    public void test(Interpreter interp){
        AppleTv atv = new AppleTv();
        Listener listener = new Listener();
        Publisher publisher = new Publisher(interp);
        publisher.scan_network();
        publisher.setListener(listener);
        publisher.connect();
        publisher.play_pause();
        publisher.play_pause();
        publisher.run_forever();
    }

    public static void main(String[] args) throws JepException {
        Main main = new Main();
        try (Interpreter interp = new SharedInterpreter();) {
            main.test(interp);
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
}
