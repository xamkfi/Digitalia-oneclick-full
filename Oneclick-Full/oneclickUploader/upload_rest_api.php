<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
$uploadedFiles = array();

    $countfiles = count($_FILES['file']['name']);
    for($i=0;$i<$countfiles;$i++){
        $filename = basename($_FILES['file']['name'][$i]);
		//console.log($filename);
        $path = "uploads/".pathinfo($_FILES['file']['full_path'][$i], PATHINFO_DIRNAME);
        //console.log($path);
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