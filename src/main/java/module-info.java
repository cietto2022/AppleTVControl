module com.example.applegui {
    requires javafx.controls;
    requires javafx.fxml;
    requires jep;


    opens com.example.applegui to javafx.fxml;
    exports com.example.applegui;
}