<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
	
// Read a file into an array
$lines = file('config.ini');

// Loop through the array
foreach ($lines as $line) {
	
	if(str_starts_with($line, "uploaddir"))	{
    $polku = substr($line, 13);

	}
}
    
$uploadedFiles = array();
$uploadersession = $_POST["uploadid"]."/";
    $countfiles = count($_FILES['file']['name']);
    for($i=0;$i<$countfiles;$i++){
        $filename = basename($_FILES['file']['name'][$i]);
		$path = trim($polku)."/".$uploadersession.pathinfo($_FILES['file']['full_path'][$i], PATHINFO_DIRNAME);
		if (!file_exists($path)) {
			mkdir($path, 0777, true);
		}
        move_uploaded_file($_FILES['file']['tmp_name'][$i],$path."/".$filename);
		array_push($uploadedFiles, $_FILES['file']['name'][$i]);
    }
	echo json_encode($uploadedFiles);
	} else {
		
		echo "Nothing to do.";
		
}


?>