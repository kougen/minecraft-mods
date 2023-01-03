. .\libs\functions.ps1

$downloads = Get-Content .\config\mods.conf

$mode = PowershellMenu -MenuTitle "Select the source: " -MenuOptions "from-cdn", "from-local" -Columns 1 -MaximumColumnWidth 15 -ShowCurrentSelection $True
$destination = PowershellMenu -MenuTitle "Select the target: " -MenuOptions "server", "client" -Columns 1 -MaximumColumnWidth 15 -ShowCurrentSelection $True
$new = PowershellMenu -MenuTitle "Do you want a new setup?" -MenuOptions "Yes", "No" -Columns 1 -MaximumColumnWidth 15 -ShowCurrentSelection $True

if(!($destination -eq 0)){
    $path = "$env:APPDATA\.minecraft\mods"
}else{
    Add-Type -AssemblyName 'System.Windows.Forms'
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $path = $dialog.SelectedPath
        Write-Host "Directory selected is $Path"
    }
}

if($mode -eq 0){
    if($new -eq 0){
        Remove-Item "$path\*.jar"
    }

    foreach ($download in $downloads){
        if(!($download[0] -eq "#") -and !($download -eq "")){
            $options = $download.Split(" ")
            
            $link = "https://$($options[1]).forgecdn.net/files/$($options[2])"
            $filename = $options[2].Split('/')[2]
    
            if(!(Test-Path -Path "$path\$filename")){
                try { 
                    Write-Host "Downloading: $link to $path\$filename"
                    Invoke-WebRequest -Uri $link -OutFile "$path\$filename"
                }
                catch{
                    Write-Host "Download failed for: $link"
                }
            }  


            
        }
    }
}

Exit

foreach ($download in $downloads){
    if(!($download[0] -eq "#") -and !($download -eq "")){
        $options = $download.Split(" ")
        
        $link = "https://$($options[1]).forgecdn.net/files/$($options[2])"
        $filename = $options[2].Split('/')[2]
        $dir = "mods\$($options[0])"

        if (!(Test-Path -Path $dir)) {
            "Directory $dir not exists... creating it"
            New-Item -Path ".\" -Name $dir -ItemType "directory" 
        }

        if(!(Test-Path -Path "$dir\$filename")){
            try { 
                Write-Host "Downloading: $link to $dir\$filename"
                Invoke-WebRequest -Uri $link -OutFile "$dir\$filename"
            }
            catch{
                Write-Host "Download failed for: $link"
            }
        }        
    }
}
