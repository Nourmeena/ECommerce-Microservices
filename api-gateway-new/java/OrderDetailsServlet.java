package com.ecommerce.servlet;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;

@WebServlet("/orderDetails")
public class OrderDetailsServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String orderId = request.getParameter("order_id");

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest orderRequest = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5001/api/orders/" + orderId))
                .GET()
                .build();

        try {
            HttpResponse<String> orderResponse =
                    client.send(orderRequest, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("order", orderResponse.body());
            request.getRequestDispatcher("orderDetails.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}
