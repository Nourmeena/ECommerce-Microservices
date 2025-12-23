<%@ page contentType="text/html;charset=UTF-8" %>

<html>
<head>
    <title>Order Confirmation</title>
</head>
<body>

<h2>Order Confirmation</h2>

<pre>
<%= request.getAttribute("orderResponse") %>
</pre>

<a href="home">Back to Home</a>

</body>
</html>
