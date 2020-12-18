<!doctype html>
<HTML lang="en">
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
		<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
		<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
		<link rel="stylesheet" type="text/css" href="../../../rayaburong.css">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>arun.</title>
	</head>
	<body class="row u-no-margin u-dark-text">
		<div class="u-flex-grow"></div>
		<div class="u-flex-grow" style="max-width: 1000px;">
			<div class="u-orange-back u-white-text u-thicc" align="center" width="100%" id="arun">
                <h1><a href="../../index.html" class="u-inherit-color">arun</a> > Gallery > <a href="../2020.html" class="u-inherit-color">2020</a>.</h1>
                <p>CNX+LPT</p>
			</div>
			<div id="images">
				<div class="row u-no-margin">
					<?php
						$dir = __DIR__;
						$images = glob($dir . "*.jpg", GLOB_BRACE);
						foreach ($images as $i) {
							printf("<div class='col-6 mb-1'><img style='object-fit:contain' width='100%' src='%s'></div>", basename($i));
						}
					?>
				</div>
			</div>
		</div>
		<div class="u-flex-grow"></div>
	</body>
</HTML>
