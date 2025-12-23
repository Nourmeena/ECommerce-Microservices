<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="org.json.JSONObject, org.json.JSONArray" %>

<html>
<head>
    <title>Checkout</title>
</head>
<body>

<h2>Checkout</h2>

<%
    JSONObject pricing = new JSONObject((String) request.getAttribute("pricing"));
    JSONArray items = pricing.getJSONArray("items");
%>

<table border="1">
    <tr>
        <th>Product ID</th>
        <th>Unit Price</th>
        <th>Quantity</th>
        <th>Subtotal</th>
        <th>Discount</th>
    </tr>

<%
    for (int i = 0; i < items.length(); i++) {
        JSONObject item = items.getJSONObject(i);
%>
    <tr>
        <td><%= item.getInt("product_id") %></td>
        <td><%= item.getDouble("unit_price") %></td>
        <td><%= item.getInt("quantity") %></td>
        <td><%= item.getDouble("subtotal") %></td>
        <td><%= item.getDouble("discount") %></td>
    </tr>
<%
    }
%>
</table>

<p>Tax: <%= pricing.getDouble("tax") %></p>
<p><strong>Total: <%= pricing.getDouble("final_total") %></strong></p>

<form action="submitOrder" method="post">
    <input type="hidden" name="order_payload"
           value='{
             "customer_id": <%= request.getAttribute("customer_id") %>,
             "products": <%= request.getAttribute("products") %>
           }'>
    <button type="submit">Confirm Order</button>
</form>

</body>
</html>
