package com.ecommerce.servlet;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;

@WebServlet("/profile")
public class CustomerProfileServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest profileRequest = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5004/api/customers/" + customerId))
                .GET()
                .build();

        try {
            HttpResponse<String> profileResponse =
                    client.send(profileRequest, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("customer", profileResponse.body());
            request.getRequestDispatcher("profile.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}
