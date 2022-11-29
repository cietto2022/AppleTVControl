
package com.example.appletvcontrol;

import jep.Jep;
import jep.JepException;
import jep.Interpreter;
import jep.SharedInterpreter;

public class Main {
    public static void main(String[] args) throws JepException {
        test_reconnection();
    }

    private static void test_commands() {
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

    private static void test_reconnection() {
        try (Interpreter interp = new SharedInterpreter();) {
            String pythonScriptFullPath = "./python/ScenarioAppleTV.py";
            interp.runScript(pythonScriptFullPath);

            interp.eval("apple_tv = ScenarioAppleTV('192.168.10.246')");
            interp.eval("apple_tv._loop.run_until_complete(apple_tv.connect())");
//        Thread.sleep(10000);
//        interp.eval("await asyncio.gather(*apple_tv.close())");
            interp.eval("apple_tv._loop.run_until_complete(apple_tv.check_if_alive())");

        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
}