<html lang="en">

<head>
	<title>Counter</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no" />
	<link rel="icon" href="favicon.ico" />
</head>

<body>
	<?php
	$fp = fopen("./counter.txt", "c+") or die("error: cannot open file.");
	$counter = fgets($fp, 64);
	if (!is_string($counter)) {
		$counter = 0;
	}
	$counter++;
	rewind($fp);
	fputs($fp, $counter);
	fclose($fp);
	echo "<p>" . $counter . "</p>";
	echo "<p>OK</p>";
	?>
</body>

</html>