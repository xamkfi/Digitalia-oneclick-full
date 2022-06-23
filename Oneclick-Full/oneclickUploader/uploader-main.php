<?php
session_start();
$upload_id = session_id();
$_SESSION["upload_id"] = hash("md5",$upload_id);
?>
<!DOCTYPE html>
<html>
<head>
<title>
<?php

include "appInfo.php";

echo $appName." ".$appVersion;

?>
</title>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="styles2.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" />
<script src="animations.js"></script>

<!-- jQuery library -->
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>

<!-- Popper JS -->
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>

<!-- Latest compiled JavaScript -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>

</head>
<body>
<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
  <ul class="navbar-nav">
    <li class="nav-item active">
      <a class="nav-link disabled" href="uploader-main.php">EN</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" href="uploader-main-fi.php">FI</a>
    </li>
  </ul>
</nav>
<div class="container p-3 my-3 bg-dark text-white">

<!-- Nav tabs -->
  <ul class="nav nav-tabs" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" data-toggle="tab" href="#folder-upload-tab">Upload folder</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-toggle="tab" href="#files-upload-tab">Upload files</a>
    </li>
  </ul>
  <form id="main-form">
    	<div class="tab-content">
    	<div id="folder-upload-tab" class="container tab-pane active"><br>
    	<h3>Choose folder to upload:</h3>
        <div class="custom-file" style="height:100%;color:black;text-align:center;border:2px solid white;">
    		<input type="file" name="file[]" class="custom-file-input" id="file[]" webkitdirectory multiple style="padding:200px;">
    		<label class="custom-file-label" for="file_to_upload">Choose folder or drop below</label>
    	</div>
    	 </div>
    	 <div id="files-upload-tab" class="container tab-pane fade"><br>
        <h3>Drag & drop files:</h3>
    	
        <div id="drop_zone"  onmouseenter="highlightSelection('animationid')" onmouseleave="resetSelection('animationid')">
            <!--*DROP HERE*-->
    		<div id="animationid" class="animate__animated animate__pulse">
    			<i class="fa fa-cloud-upload fa-5x"></i>
    		</div>
        </div>
    	</div>
        <hr>
        <p id="file_name"></p>
    	<div class="alert alert-warning" id="nofolder" style="display:none;">
        No folder selected.
      </div>
      <div class="row">
      <div class="col-sm-2">
    	<input type="button" class="btn btn-primary" value="Upload" id="upload_file_button">
    	</div>
    	<div class="col-sm-10">
        <!--<progress id="progress_bar" value="0" max="100" style="width:400px;"></progress> -->
     <div class="progress" style="height:30px">
      <div id="progress-bar" class="progress-bar bg-light" style="height:30px;color:black;width:100%;">No uploads in progress</div>
    </div>
    </div>
    </div> 	
        <p id="progress_status"></p>
    	<p id="download_link"></p>
       
    </div>
</form> 
</div>
<div class="container p-4 my-4" style="padding-bottom: 200px;">
</div>
<nav class="navbar navbar-expand-sm bg-dark navbar-dark justify-content-center fixed-bottom">
            <!-- Links -->
            <ul class="navbar-nav">
			<li class="nav-item">
                <a class="nav-link disabled" href="#"><i class="fa fa-copyright">&nbsp;</i></a>
              </li>
			<?php $partnersLength = count($partners); 
					for($partnersLkm=0;$partnersLkm<$partnersLength;$partnersLkm++)
					{						 
					
			
			?>
              <li class="nav-item">
                <a class="nav-link" href="#">&nbsp;<?php echo $partners[$partnersLkm]; ?></a>
              </li>
			  <?php 
				}; //for ends
			  ?>
            </ul>
        </nav> 
    <script>
        document.getElementById('file[]').addEventListener('change', (event) => {
			window.selectedFile = event.target.files;
			document.getElementById('file_name').innerHTML = "Files selected: " + window.selectedFile.length+ "<br>";
			
        });

        document.getElementById('upload_file_button').addEventListener('click', (event) => {
            uploadFile(window.selectedFile);
        });

        const dropZone = document.getElementById('drop_zone');
        if (window.FileList && window.File) {
            dropZone.addEventListener('dragover', event => {
                event.stopPropagation();
                event.preventDefault();
                event.dataTransfer.dropEffect = 'copy';
            });
            dropZone.addEventListener('drop', event => {
                event.stopPropagation();
                event.preventDefault();
                const files = event.dataTransfer.files;
                window.selectedFile = files;
                document.getElementById('file_name').innerHTML = "Files selected: " + window.selectedFile.length;
            });
        }

        function uploadFile(file) {
			if(file && file.length != 0){
			document.getElementById("nofolder").style = "display:none;";
            var formData = new FormData();
			for(var i=0;i<file.length;i++){
            formData.append('file[]', file[i]);
			}
			formData.append('uploadid', '<?php echo $_SESSION["upload_id"]; ?>');
            var apiRequest = new XMLHttpRequest();
			
			apiRequest.onreadystatechange = function() {
				console.log("ReadyState & Status =");
				console.log(this.readyState, this.status);
				if (this.readyState == 4 && this.status == 200) {
					document.getElementById("main-form").reset(); 
					console.log("AAA");
					console.log(this.responseText);
					console.log("BBB");
					var responseJson = JSON.parse(this.responseText);
					window.selectedFile = null;
					console.log("CCC");
					console.log(responseJson);
					document.getElementById("download_link").innerHTML = "<h2>Download the created SIP file(s)</h2><br>"; 
					for (const key in responseJson){
						document.getElementById("download_link").innerHTML += "<br><a href='"+responseJson[key]+"'>Link</a>";
						}				
					
				}else{
					console.log("Something else for testing");
				}

			};
			
            apiRequest.upload.addEventListener("progress", progressHandler, false);
            console.log("Before reading config file");
			apiRequest.open('POST', 'upload_rest_api_edit.php');
            console.log("After config reading");
			apiRequest.send(formData);
			for (var pair of formData.entries()) {
				console.log(pair[0]+ ' - ' + pair[1].name); 
			}
			}//if file
			else	{
				document.getElementById("nofolder").style = "display:block;";
			}
        }

        function progressHandler(event) {
            var percentUploaded = (event.loaded / event.total) * 100;
            //document.getElementById("progress_bar").value = Math.round(percentUploaded);
			document.getElementById("progress-bar").style = "width:"+Math.round(percentUploaded)+"%;";
			document.getElementById("progress-bar").innerHTML = Math.round(percentUploaded) + "% uploaded";
			if(percentUploaded < 100){
			
				document.getElementById("progress-bar").className = "progress-bar progress-bar-striped";
				document.getElementById("progress_status").innerHTML = "Uploading files. Time to get a cup of coffee and relax.";
				document.getElementById("upload_file_button").disabled = true;
			
			}else			{
				
				document.getElementById("progress_status").innerHTML = Math.round(percentUploaded) + "% uploaded";
				document.getElementById("progress-bar").className = "progress-bar progress-bar-striped";
				document.getElementById("upload_file_button").disabled = false;
				
				}
        }
    </script>
	
</body>

</html>