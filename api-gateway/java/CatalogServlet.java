package com.example.gateway;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/index")
public class CatalogServlet extends HttpServlet {

    private static final String INVENTORY_PRODUCTS_URL =
            "http://localhost:5002/api/inventory/products";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(INVENTORY_PRODUCTS_URL))
                .GET()
                .build();

        try {
            HttpResponse<String> resp =
                    client.send(req, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("productsJson", resp.body());

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            request.setAttribute(
                "productsJson",
                "{\"success\":false,\"products\":[]}"
            );
        }

        request.getRequestDispatcher("/index.jsp")
               .forward(request, response);
    }
}
