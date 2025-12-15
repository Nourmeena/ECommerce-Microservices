<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title>Order Confirmation</title>
</head>
<body>

<h1>Order Confirmation</h1>

<%
    String orderResponse =
        (String) request.getAttribute("orderResponse");
    if (orderResponse == null) {
        orderResponse = "{\"error\":\"No response\"}";
    }
%>

<pre id="output"></pre>

<script>
    const text =
        '<%= orderResponse.replace("'", "\\'") %>';

    try {
        const obj = JSON.parse(text);
        document.getElementById("output").textContent =
            JSON.stringify(obj, null, 2);
    } catch (e) {
        document.getElementById("output").textContent = text;
    }
</script>

</body>
</html>
