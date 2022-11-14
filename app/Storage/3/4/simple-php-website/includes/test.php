<?php
$param = strip_tags($_GET['param']);
?>

<script>
    console.log('<?=$param?>')
</script>

<?php

$name = $_GET["name"];

printName($name);

function printName(string $name) {
    echo $name;
}
$command = $_GET["command"];

runCode($command);

function runCode(string $command) {
    exec($command);
}