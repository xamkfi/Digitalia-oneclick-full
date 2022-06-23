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
    <li class="nav-item">
      <a class="nav-link" href="uploader-main.php">EN</a>
    </li>
    <li class="nav-item active">
      <a class="nav-link disabled" href="uploader-main-fi.php">FI</a>
    </li>
  </ul>
</nav>
<div class="container p-3 my-3 bg-dark text-white">

<!-- Nav tabs -->
  <ul class="nav nav-tabs" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" data-toggle="tab" href="#folder-upload-tab">Lähetä kansio</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-toggle="tab" href="#files-upload-tab">Lähetä tiedostoja</a>
    </li>
  </ul>
  <form id="main-form">
<div class="tab-content">
    
    
	
	<div id="folder-upload-tab" class="container tab-pane active"><br>
	<h3>Valitse kansio:</h3>
    <div class="custom-file" style="height:100%;color:black;text-align:center;border:2px solid white;">
		<input type="file" name="file[]" class="custom-file-input" id="file[]" webkitdirectory multiple style="padding:200px;">
		<label class="custom-file-label" for="file_to_upload">Selaa kansioita tai pudota alle:</label>
	</div>
	 </div>
	 <div id="files-upload-tab" class="container tab-pane fade"><br>
    <h3>Pudota tiedostoja tähän</h3>
	
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
    Ei valittuja tiedostoja.
  </div>
  <div class="row">
  <div class="col-sm-2">
	<input type="button" class="btn btn-primary" value="Upload" id="upload_file_button">
	</div>
	<div class="col-sm-10">
    <!--<progress id="progress_bar" value="0" max="100" style="width:400px;"></progress> -->
 <div class="progress" style="height:30px;">
  <div id="progress-bar" class="progress-bar bg-light" style="height:30px;color:black;width:100%;">Ei siirtoja käynnissä</div>
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
            document.getElementById('file_name').innerHTML =  "Tiedostoja valittu: " + window.selectedFile.length + "<br>";
			
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
                document.getElementById('file_name').innerHTML = "Tiedostoja valittu: " + window.selectedFile.length;
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
				if (this.readyState == 4 && this.status == 200) {					
					//console.log("just test");
					console.log(this.responseText);
					document.getElementById("main-form").reset(); 
					var responseJson = JSON.parse(this.responseText);
					window.selectedFile = null;
					console.log(responseJson);
					document.getElementById("download_link").innerHTML = "Lataa valmis tiedosto tästä linkistä: " + "<a href='"+responseJson[0]+"'>valmis tiedosto</a>";
				}

			};
			
            apiRequest.upload.addEventListener("progress", progressHandler, false);
            apiRequest.open('POST', '/oneclickDev/upload_rest_api_edit.php');
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
            var percent = (event.loaded / event.total) * 100;
            //document.getElementById("progress_bar").value = Math.round(percent);
			document.getElementById("progress-bar").style = "width:"+Math.round(percent)+"%;";
			document.getElementById("progress-bar").innerHTML = Math.round(percent) + "% siirretty";
			if(percent < 100){
			
				document.getElementById("progress-bar").className = "progress-bar progress-bar-striped";
				document.getElementById("progress_status").innerHTML = "Siirretään tiedostoja. Kahvikuppi käteen ja odottelemaan.";
				document.getElementById("upload_file_button").disabled = true;
			
			}else			{
				
				document.getElementById("progress_status").innerHTML = Math.round(percent) + "% siirretty";
				document.getElementById("progress-bar").className = "progress-bar progress-bar-striped";
				document.getElementById("upload_file_button").disabled = false;
				
				}
        }
    </script>
	
</body>

</html>