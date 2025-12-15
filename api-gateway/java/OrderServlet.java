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

@WebServlet("/submitOrder")
public class OrderServlet extends HttpServlet {

    private static final String ORDER_SERVICE_URL =
            "http://localhost:5001/api/orders/create";

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");
        String productId  = request.getParameter("product_id");
        String quantity   = request.getParameter("quantity");

        String jsonPayload = String.format(
            "{\"customer_id\":%s,\"product_id\":%s,\"quantity\":%s}",
            customerId, productId, quantity
        );

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(ORDER_SERVICE_URL))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .build();

        try {
            HttpResponse<String> resp =
                    client.send(req, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("orderResponse", resp.body());

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            request.setAttribute(
                "orderResponse",
                "{\"error\":\"Order service unavailable\"}"
            );
        }

        request.getRequestDispatcher("/confirmation.jsp")
               .forward(request, response);
    }
}
