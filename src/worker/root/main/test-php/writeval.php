<html>

<head>
	<title>WriteVal</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no" />
	<link rel="icon" href="favicon.ico" />
</head>

<body>
	<?php
	$fp = fopen('yoko.txt', "c+") or die("error: cannnot open file.");
	$count = fgets($fp, 64);
	if (isset($_GET['x'])) {
		$count += $_GET['x'];
	}
	fseek($fp, 0);
	fputs($fp, $count);
	fclose($fp);
	echo $count;
	?>
</body>

</html>