<html>

<head>
	<title>CountIf</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no" />
	<link rel="icon" href="favicon.ico" />
</head>

<body>
	<p>X:</p>
	<?php
	$fp = fopen('./counter.txt', "r+") or die("error: cannot open file.");
	$count = intval(fgets($fp, 1024));
	if (isset($_GEFT['x'])) $count++;
	fseek($fp, 0);
	fputs($fp, $count);
	fclose($fp);
	echo $count;
	?>
</body>

</html>