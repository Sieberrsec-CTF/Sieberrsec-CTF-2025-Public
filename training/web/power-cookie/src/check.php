<?php
if (isset($_COOKIE['isAdmin'])) {
    $isAdmin = $_COOKIE['isAdmin'];

    if ($isAdmin == '1') {
        echo "sctf{gr4d3_A_c00k13}";
    }
    else {
        echo "We apologize, but we have no guest services at the moment.";
    }
} else {
    echo "We apologize, but we have no guest services at the moment.";
}
?>
