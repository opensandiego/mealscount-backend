package org.opensandiego.mealcount.app;

import com.google.inject.Singleton;
import com.google.inject.servlet.ServletModule;
import com.sun.jersey.guice.spi.container.servlet.GuiceContainer;
import org.opensandiego.mealcount.app.controllers.InfoController;

/**
 * Module for {@link InfoController}
 * Created by rishavdas on 3/20/18.
 */
public class InfoModule extends ServletModule {
    @Override
    protected void configureServlets() {
        serve("/*").with(GuiceContainer.class);
        bind(InfoController.class).in(Singleton.class);
    }
}