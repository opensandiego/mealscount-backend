package org.opensandiego.mealcount.app;

import com.google.inject.Guice;
import com.google.inject.servlet.GuiceFilter;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;

import javax.servlet.DispatcherType;
import java.util.EnumSet;

/**
 * Simple jetty application
 */
public class Application {

    public static void main(String[] args) throws Exception {
        Guice.createInjector(new InfoModule());

        int port = 8080;
        Server server = new Server(port);

        ServletContextHandler servletContextHandler = new ServletContextHandler(server, "/", ServletContextHandler.SESSIONS);
        servletContextHandler.addFilter(GuiceFilter.class, "/*", EnumSet.allOf(DispatcherType.class));

        // You MUST add DefaultServlet or your server will always return 404s
        servletContextHandler.addServlet(DefaultServlet.class, "/*");

        try {
            // Start the server
            server.start();

            // Wait until the server exits
            server.join();

        } finally {
            server.destroy();
        }
    }
}
