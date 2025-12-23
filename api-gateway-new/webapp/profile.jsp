<%@ page contentType="text/html;charset=UTF-8" %>

<html>
<head>
    <title>Customer Profile</title>
</head>
<body>

<h2>Customer Profile</h2>

<pre>
<%= request.getAttribute("customer") %>
</pre>

<a href="home">Back to Home</a>

</body>
</html>
