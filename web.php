<?php
if($_SERVER["REQUEST_METHOD"] == "GET"){
  $action = $_GET["action"];
  if($action=="read"){
    echo readfile("database.txt");
    exit();
  }elseif($action == "write"){
    $data = $_GET["data"];
    $file = fopen("database.txt","w");
    fwrite($file,$data);
    fclose($file);
    exit();
  }elseif($action == "append"){
    $data = $_GET["data"];
    $file = fopen("database.txt","a");
    fwrite($file,$data);
    fclose($file);
    exit();
  }else{
    echo "Wrong action";
  }
}


?>
cont = r.get("http://rajma.000webhostapp.com/manager1.php?action=read")