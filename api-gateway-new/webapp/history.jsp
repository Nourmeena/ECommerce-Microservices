<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="org.json.JSONArray, org.json.JSONObject" %>

<html>
<head>
    <title>Order History</title>
</head>
<body>

<h2>Order History</h2>

<%
    JSONArray orders = new JSONArray((String) request.getAttribute("orders"));
    for (int i = 0; i < orders.length(); i++) {
        JSONObject o = orders.getJSONObject(i);
%>

    Order ID: <%= o.getString("order_id") %><br>
    Total: <%= o.getDouble("total_amount") %><br>
    Status: <%= o.getString("status") %><br>

    <a href="orderDetails?order_id=<%= o.getString("order_id") %>">
        View Details
    </a>

    <hr>

<%
    }
%>

</body>
</html>
