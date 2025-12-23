package com.ecommerce.servlet;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;

@WebServlet("/orderHistory")
public class OrderHistoryServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest historyRequest = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5001/api/orders?customer_id=" + customerId))
                .GET()
                .build();

        try {
            HttpResponse<String> historyResponse =
                    client.send(historyRequest, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("orders", historyResponse.body());
            request.getRequestDispatcher("history.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}
