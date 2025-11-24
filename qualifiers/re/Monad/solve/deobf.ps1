$flag = @()
$len = 0

(Get-Content "flag.txt")[0..100] | %{ $flag += [char]($_ - 7); $len += 1 }

$copy = $flag[0..$len]

0..([int]($len / 2) - 1) | %{ $copy[$_ * 2] = $flag[$_ * 2 + 1]; $copy[$_ * 2 + 1] = $flag[$_ * 2]}

[String]::Concat($copy[-1..-10000])