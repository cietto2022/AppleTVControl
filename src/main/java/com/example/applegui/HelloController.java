package com.example.applegui;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import jep.Interpreter;
import jep.SharedInterpreter;

public class HelloController {
    @FXML
    private final Interpreter interpreter = new SharedInterpreter();

    @FXML
    protected void onUpButtonClick() {
        interpreter.eval(AppleTVCommands.up());
    }
    @FXML
    protected void onDownButtonClick() {
        interpreter.eval(AppleTVCommands.down());
    }
    @FXML
    protected void onLeftButtonClick() {
        interpreter.eval(AppleTVCommands.left());
    }

    @FXML
    protected void onRightButtonClick() {
        interpreter.eval(AppleTVCommands.right());
    }

    @FXML
    protected void onSelectButtonClick() {
        interpreter.eval(AppleTVCommands.select());
    }

    @FXML
    protected void onMenuButtonClick() {
        interpreter.eval(AppleTVCommands.menu());
    }

    @FXML
    protected void onNetflixButtonClick() {
        interpreter.eval(AppleTVCommands.launch_app("com.netflix.Netflix"));
    }

    @FXML
    protected void onYoutubeButtonClick() {
        interpreter.eval(AppleTVCommands.launch_app("com.google.ios.youtube"));
    }

    @FXML
    protected void onConnectButtonClick() {
        String pythonScriptFullPath = "ScenarioAppleTV.py";
        interpreter.runScript(pythonScriptFullPath);

        interpreter.eval("apple_tv = ScenarioAppleTV('192.168.11.38')");
        interpreter.eval("apple_tv._loop.run_until_complete(apple_tv.connect())");
    }
}