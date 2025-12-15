<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title>Checkout</title>
</head>
<body>

<h1>Checkout</h1>

<%
    String productId = request.getParameter("product_id");
    if (productId == null) productId = "";
%>

<form method="post" action="submitOrder">
    <label>
        Customer ID:
        <input type="text" name="customer_id" required />
    </label><br/><br/>

    <label>
        Product ID:
        <input type="text" name="product_id"
               value="<%= productId %>" readonly />
    </label><br/><br/>

    <label>
        Quantity:
        <input type="number" name="quantity"
               value="1" min="1" required />
    </label><br/><br/>

    <button type="submit">Place Order</button>
</form>

</body>
</html>
