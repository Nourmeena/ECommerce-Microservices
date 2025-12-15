<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title>Product Catalog</title>
</head>
<body>

<h1>Product Catalog</h1>

<%
    String productsJson = (String) request.getAttribute("productsJson");
    if (productsJson == null) {
        productsJson = "{\"success\":false,\"products\":[]}";
    }
%>

<script>
    const response =
        JSON.parse('<%= productsJson.replace("'", "\\'") %>');
    const products = response.products || [];

    function render() {
        const div = document.getElementById("catalog");

        if (products.length === 0) {
            div.innerHTML = "<p>No products available.</p>";
            return;
        }

        let html = "<ul>";
        for (let p of products) {
            html += `
                <li>
                    <strong>${p.product_name}</strong><br/>
                    Price: ${p.unit_price}<br/>
                    Available: ${p.quantity_available}<br/>
                    <form method="get" action="checkout.jsp">
                        <input type="hidden" name="product_id" value="${p.product_id}" />
                        <button type="submit">Buy</button>
                    </form>
                </li><hr/>
            `;
        }
        html += "</ul>";
        div.innerHTML = html;
    }

    window.onload = render;
</script>

<div id="catalog"></div>

</body>
</html>
