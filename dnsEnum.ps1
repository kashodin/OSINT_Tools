#Powershell script to match IPv4 address to hostnames for all hostnames in the inputfile
#input file name passed as command line argument, format should be one hostname per line
#no spaces after hostname, just newline


if($args[0] -eq $null)
{
    Write-Host('Please Specify the file containing the list of hostnames, one hostname per line, with no space after the hostname');
    Write-Host('EX:');
    Write-Host('host1');
    Write-Host('host2');
}
else
{
    $InputFile = $PWD;
    $InputFile = Join-Path -Path "$InputFile" -ChildPath "$args";
    $info = get-content $InputFile;

    $responses = New-Object System.Collections.ArrayList;
    $output = New-Object System.Collections.ArrayList;
    $hostnames = New-Object System.Collections.ArrayList;

    foreach($name in $info)
    {
        $hostnames.Add("$name") > $null;
        $response = Ping -n 1 -4 -a "$name";
        $responses.Add("$response") > $null;
    }
    
    $count = 0;

    foreach($res in $responses)
    {

        if ($res -like "*pinging*")
        {
            $place = $hostnames[$count]+" : "+$res.split(" ")[3];
            $output.Add($place) > $null;
            $count++
        }
        else
        {
            $place = $hostnames[$count]+" : ---";
            $output.Add($place) > $null;
            $count++
        }
    }
    $output
    
    
}

    