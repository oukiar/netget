<?
//script que almacena y resuelve la lista de servidores netget disponibles

if( isset( $_GET['set_server_ip'] ) )
{
  $f = fopen('sitesol_server.txt', 'w');
  fwrite($f, $_SERVER['REMOTE_ADDR']);
  fclose($f);
}
else if( isset( $_GET['get_server_ip']) )
{
  $f = fopen('sitesol_server.txt', 'r');
  $ip = fread($f, filesize('sitesol_server.txt'));
  echo $ip;
}


?>
