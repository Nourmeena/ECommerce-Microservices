package com.ecommerce.servlet;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/home")
public class HomeServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest invRequest = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5002/api/inventory/products"))
                .GET()
                .build();

        try {
            HttpResponse<String> invResponse =
                    client.send(invRequest, HttpResponse.BodyHandlers.ofString());

            JSONObject json = new JSONObject(invResponse.body());
            JSONArray products = json.getJSONArray("products");

            request.setAttribute("products", products);
            request.getRequestDispatcher("index.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}
