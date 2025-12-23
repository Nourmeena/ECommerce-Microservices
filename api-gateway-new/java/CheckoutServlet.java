package com.ecommerce.servlet;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/checkout")
public class CheckoutServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");
        String[] productIds = request.getParameterValues("product_id");
        String[] quantities = request.getParameterValues("quantity");

        JSONArray products = new JSONArray();

        for (int i = 0; i < productIds.length; i++) {
            JSONObject item = new JSONObject();
            item.put("product_id", Integer.parseInt(productIds[i]));
            item.put("quantity", Integer.parseInt(quantities[i]));
            products.put(item);
        }

        JSONObject payload = new JSONObject();
        payload.put("products", products);

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest pricingRequest = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5003/api/pricing/calculate"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(payload.toString()))
                .build();

        try {
            HttpResponse<String> pricingResponse =
                    client.send(pricingRequest, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("pricing", pricingResponse.body());
            request.setAttribute("products", products.toString());
            request.setAttribute("customer_id", customerId);

            request.getRequestDispatcher("checkout.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        }
    }
}
