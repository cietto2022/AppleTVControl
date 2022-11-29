package com.example.appletvcontrol;

import jep.Jep;
import jep.JepException;
import jep.Interpreter;
import jep.SharedInterpreter;

public class Main {



    public static void main(String[] args) throws JepException {

            try (Interpreter interp = new SharedInterpreter();) {

                String pyAppleTVPath = "./python/ScenarioAppleTV.py";
                interp.runScript(pyAppleTVPath);
                AppleTv atv = new AppleTv();
                Listener listener = new Listener();
                Publisher publisher = new Publisher(interp);
                publisher.scan_network();
                publisher.setListener(listener);
                publisher.connect();
                publisher.play_pause();
                publisher.run_forever();

            } catch (Throwable e) {
                e.printStackTrace();
            }
    }
}
