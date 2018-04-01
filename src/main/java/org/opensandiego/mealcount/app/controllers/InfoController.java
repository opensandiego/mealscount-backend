package org.opensandiego.mealcount.app.controllers;

import com.google.inject.Singleton;

import javax.ws.rs.GET;
import javax.ws.rs.Path;

/**
 * Resource to get information about server
 * Created by rishavdas on 3/20/18.
 */
@Path("mealscount")
@Singleton
public class InfoController {

    @GET
    @Path("info")
    public String getString() {
        return "{\"project\":\"meals-count\"}";
    }
}
