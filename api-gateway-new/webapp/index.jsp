<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="org.json.JSONArray, org.json.JSONObject" %>

<html>
<head>
    <title>Home - Product Catalog</title>
</head>
<body>

<h2>Product Catalog</h2>

<form action="checkout" method="post">

    <!-- Customer Selection -->
    <label>Select Customer:</label>
    <select name="customer_id" required>
        <option value="1">Ahmed Hassan</option>
        <option value="2">Sara Mohamed</option>
        <option value="3">Omar Ali</option>
    </select>

    <br><br>

    <%
        JSONArray products = (JSONArray) request.getAttribute("products");
        for (int i = 0; i < products.length(); i++) {
            JSONObject p = products.getJSONObject(i);
    %>

        <input type="checkbox" name="product_id" value="<%= p.getInt("product_id") %>">
        <strong><%= p.getString("product_name") %></strong>
        - Price: <%= p.getDouble("unit_price") %>
        - Available: <%= p.getInt("quantity_available") %>

        Quantity:
        <input type="number"
               name="quantity"
               min="1"
               max="<%= p.getInt("quantity_available") %>">

        <br><br>

    <%
        }
    %>

    <button type="submit">Proceed to Checkout</button>

</form>

</body>
</html>
