<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="org.json.JSONObject, org.json.JSONArray" %>

<html>
<head>
    <title>Order Details</title>
</head>
<body>

<h2>Order Details</h2>

<%
    JSONObject order = new JSONObject((String) request.getAttribute("order"));
    JSONArray products = order.getJSONArray("products");
%>

Order ID: <%= order.getString("order_id") %><br>
Total: <%= order.getDouble("total_amount") %><br>
Status: <%= order.getString("status") %><br>
<hr>

<h3>Products</h3>

<%
    for (int i = 0; i < products.length(); i++) {
        JSONObject p = products.getJSONObject(i);
%>

    Product ID: <%= p.getInt("product_id") %>
    Quantity: <%= p.getInt("quantity") %><br>

<%
    }
%>

</body>
</html>
