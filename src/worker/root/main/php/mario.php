<html>

<head>
	<title>Mario</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no" />
	<link rel="icon" href="favicon.ico" />
	<?php
	if (isset($_GET['x'])) {
		echo "<meta http-equiv=\"refresh\" content=\"1\">\n";
	}
	?>
</head>

<body>
	<p>X:</p>
	<?php
	$fp = fopen('yoko.txt', "r+") or die("error: cannot open file.");
	$count = intval(fgets($fp, 1024));

	if (isset($_GET['x'])) $count += intval($_GET['x']);

	fseek($fp, 0);

	fputs($fp, $count);
	fclose($fp);
	echo "<img src=\"./mario.png\" hspace=\"{$count}\" vspace=\"20\">\n";
	echo "<p>{$count}</p>\n";
	?>
	<form method="GET" action="mario.php">
		<input type="text" name="x" value="-20">
		<input type="submit" value="<--">
	</form>
	<form method="GET" action="mario.php">
		<input type="text" name="x" value="20">
		<input type="submit" value="-->">
	</form>
</body>

</html>