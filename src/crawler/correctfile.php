<?php
function add_id_to_json($json, $id)
{
	$out = ["id" =>$id];
	$data = json_decode($json);
	$out+=(array)$data;
	return json_encode($out);
}

foreach (array_slice($argv, 1) as $filename)
{
	$json=file_get_contents($filename);
	$id=basename($filename);
	$id=substr($id, 0, -4);
	$t= add_id_to_json($json, $id);
	file_put_contents($filename.".json", $t);
}
