<?php


if ($_SERVER["REQUEST_METHOD"] == "POST") {		
	//echo ("Just test");
    if (file_exists("config.ini")){
        $lines = file('config.ini');
    }
	$basePath = "";
	//Loop through the array
	
	foreach ($lines as $line) {
		#echo($line);
		if(str_starts_with($line, "uploaddir"))	{			
			$pieces = explode("=", $line);
			$processPath = trim($pieces[1]);				
			$basePath = dirname($processPath); //Gets the parent path of the defined path
			$tempPath = $basePath."/temp";
			//echo ($tempPath."\r\n");
			//echo file_exists($tempPath);
			if (!is_dir($tempPath)){
				//echo ("Create dir ".$tempPath."\r\n");
				mkdir($tempPath, 0777, true);
			}			
			
		}
		if(str_starts_with($line, "completeddir"))	{
			$pieces = explode("=", $line);
			$sip_path = trim($pieces[1]);
			
		}
		if(str_starts_with($line, "ip"))	{
		    $pieces = explode("=", $line);
		    $ip = trim($pieces[1]);
		    //echo ($ip);
		}
		if(str_starts_with($line, "port"))	{
		    $pieces = explode("=", $line);
		    $port = trim($pieces[1]);
		    
		}
	}
	
	$dir_separator = DIRECTORY_SEPARATOR; 
	//$uploadedFiles = array(); //This is used for what..?
	$sipfileArray = array();
	$uploadersession = $_POST["uploadid"].$dir_separator;
	/*
	 * Just prints the content of the post message	 * 
	 */
	foreach ($_POST as $key => $value){
	    echo "<tr>";
	    echo "<td>";
	    echo $key;
	    echo "</td>";
	    echo "<td>";
	    echo $value;
	    echo "</td>";
	    echo "</tr>";
	}
	
	
	/*
	 * Creates the final zip dir if not exist already
	 */
	$finalSIPPath = trim($sip_path.$dir_separator.$uploadersession);
	if (!is_dir($finalSIPPath)) {
	    //echo ("\r\nCreate dir ".$finalSIPPath."\r\n");
	    mkdir($finalSIPPath, 0755, true);
	}      
	
    //echo("Session id = ".$uploadersession."\r\n");
	$countfiles = count($_FILES['file']['name']);
	echo("Testiä\r\n");
    for($i=0;$i<$countfiles;$i++){
        echo("Round ".$i);
        $filename = basename($_FILES['file']['name'][$i]);		
		echo($_FILES['file']['lastModifiedDate'][$i]);
		$path = trim($tempPath).$dir_separator.$uploadersession.pathinfo($_FILES['file']['full_path'][$i], PATHINFO_DIRNAME);
		//echo("\r\nPolku ".$path."\r\n");
		if (!is_dir($path)) {
			mkdir($path, 0777, true);
		}        
		//echo("Testiä\r\n");
		//echo ($_FILES['file']['tmp_name'][$i]);
		//echo("\r\nempty--\r\n");
		move_uploaded_file($_FILES['file']['tmp_name'][$i],$path.$dir_separator.$filename);
		//array_push($uploadedFiles, $_FILES['file']['name'][$i]); //Kun ainoa viite on tämä lisäys
    }
	/*All files should now be in the temporary location
		Now lets move those into the watched folder defined in config.ini file
	*/
	
	$tmpPath = trim($tempPath).$dir_separator.$uploadersession;
	$processPath = $processPath.$dir_separator.$uploadersession;
	//echo("\r\ntemp path = ".$tmpPath." and new path is ".$processPath."\r\n");
	moveToProcess($tmpPath, $processPath);
	
	
	/*
	 * This part should start a folder watcher that adds all found .zip 
	 * files to the list of downloadable files
	 * Use e.g. inotify https://www.php.net/manual/en/intro.inotify.php
	 */
	
	/*
	$sipfile_name = "sipfile".$_POST["uploadid"];
	$timestamp = time();
	$sipfile = fopen($sip_file_path.$sipfile_name."_".$timestamp.".txt", "w") or die("Unable to open file!");
	$txt = "Testing... write something into a .txt file";
	fwrite($sipfile, $txt);
	fclose($sipfile);
	*/
	sleep(10);
	$files = array_diff(scandir($finalSIPPath), array('.', '..'));
	while (count($files)==0){
	    //echo("Sleeping 10 seconds");
	    sleep(10);
	    $files = array_diff(scandir($finalSIPPath), array('.', '..'));
	}	
	
	//echo("Files in completed dir = ".count($files));
	//echo($_SERVER['DOCUMENT_ROOT']); 
	
	
	if (count($files)>0){
	    foreach ($files as $onefile){
	        $relative = "http://".$ip.":".$port."/oneclickUploader/zipit/".$uploadersession."/".$onefile;
	        
	        //$relative = "http://10.25.36.72:8080/oneclickUploader/zipit/".$uploadersession."/".$onefile;
	        $absolute = $finalSIPPath."/".$onefile;
	        //echo("Relative path = ".$relative);
	        $filetime = date("Y-m-d H:i:s", filectime($absolute));
	        
	        //Will be replaced with arrayname[indexname] = value
	        //array_push($sipfileArray,$relative);
	        $sipfileArray[$filetime] = $relative;
	    }
	    /*
	    for($z=0;$z<count($files);$z++){
	        if($files[$z]==$sipfile_name."_".$timestamp.".txt"){
	            array_push($sipfileArray,$sip_file_path.$dir_separator.$allFiles[$z]);
	        }
	    }*/
	    #Need to remove /var/www/html/ part from the final array --> try $_SERVER['DOCUMENT_ROOT']
	    //echo $_SERVER['DOCUMENT_ROOT'];
	    echo json_encode($sipfileArray);	    
	}
	

	}
	
	else {		
		echo "Nothing to do.";		
	}
	
function moveToProcess($originalPath, $processPath){
	//echo("\r\nMoving from ".$originalPath." to ".$processPath);
	$result = rename($originalPath, $processPath);
	return $result; 
}


?>