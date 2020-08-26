<html>

<head>
    <title>Test PHP</title>
    <meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no" />
	<link rel="icon" href="favicon.ico" />
</head>

<body>
    <p>Test:
        <?php
        $test = $_GET["test"];
        print($test);
        ?>
    </p>
</body>

</html>