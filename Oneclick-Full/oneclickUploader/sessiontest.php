<?php

session_start();
$_SESSION["testi"] = "ekaaa";
echo session_id();
print_r($_SESSION);
echo $_SESSION["testi"];

session_unset();
session_destroy();

echo session_id();
print_r($_SESSION);
?>