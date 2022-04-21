<!DOCTYPE html>
<html>
<head>
<title>
<?php

include "appInfo.php";

echo $appName." v".$appVersion;

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
    <li class="nav-item">
      <a class="nav-link" href="uploader-main.php">EN</a>
    </li>
    <li class="nav-item active">
      <a class="nav-link disabled" href="uploader-main-fi.php">FI</a>
    </li>
  </ul>
</nav>
<div class="container p-3 my-3 bg-dark text-white">
    <h2><?php echo $appName." v".$appVersion; ?></h2>
    <div class="custom-file">
		<input type="file" name="file[]" class="custom-file-input" id="file[]" webkitdirectory multiple>
		<label class="custom-file-label" for="file_to_upload">Valitse kansio</label>
	</div>
    <h3>Tai pudota kansio alle:</h3>
	
    <div id="drop_zone"  onmouseenter="highlightSelection('animationid')" onmouseleave="resetSelection('animationid')">
        <!--*DROP HERE*-->
		<div id="animationid" class="animate__animated animate__pulse">
			<i class="fa fa-cloud-upload fa-5x"></i>
		</div>
    </div>
    <hr>
    <p id="file_name"></p>
	<input type="button" class="btn btn-primary" value="Lataa" id="upload_file_button">
    <progress id="progress_bar" value="0" max="100" style="width:400px;"></progress>	
    <p id="progress_status"></p>    
</div>
<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-bottom justify-content-center">
            <!-- Links -->
            <ul class="navbar-nav">
			<li class="nav-item">
                <a class="nav-link" href="#"><i class="fa fa-copyright">&nbsp;</i></a>
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
            document.getElementById('file_name').innerHTML = "File selected: " + window.selectedFile.name;
        });

        document.getElementById('upload_file_button').addEventListener('click', (event) => {
            uploadFile(window.selectedFile);
        });

        const dropZone = document.getElementById('drop_zone'); //Getting our drop zone by ID
        if (window.FileList && window.File) {
            dropZone.addEventListener('dragover', event => {
                event.stopPropagation();
                event.preventDefault();
                event.dataTransfer.dropEffect = 'copy'; //Adding a visual hint that the file is being copied to the window
            });
            dropZone.addEventListener('drop', event => {
                event.stopPropagation();
                event.preventDefault();
                const files = event.dataTransfer.files; //Accessing the files that are being dropped to the window
                window.selectedFile = files[0]; //Getting the file from uploaded files list (only one file in our case)
                document.getElementById('file_name').innerHTML = "File selected: " + window.selectedFile.name; //Assigning the name of file to our "file_name" element
            });
        }

        function uploadFile(file) {
            var formData = new FormData();
			for(var i=0;i<file.length;i++){
            formData.append('file[]', file[i]);
			}
            var ajax = new XMLHttpRequest();
			
			ajax.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
					console.log(this.responseText);
				}
			};
			
            ajax.upload.addEventListener("progress", progressHandler, false);
            ajax.open('POST', '/php_upload/upload_rest_api.php');
            ajax.send(formData);
        }

        function progressHandler(event) {
            var percent = (event.loaded / event.total) * 100;
            document.getElementById("progress_bar").value = Math.round(percent);
            document.getElementById("progress_status").innerHTML = Math.round(percent) + "% uploaded";
        }
    </script>
	
</body>

</html>