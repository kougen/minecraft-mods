. .\functions.ps1

$date = Get-Date -Format "yyyy-MM-dd_HH-mm"
$dateExists = $false

function DoBackup {
    "Test to see if folder [$Path\back\]  exists"
    if (!(Test-Path -Path "$Path\back\")) {
        "Directory not exists... creating it"
        New-Item -Path "$Path" -Name "back" -ItemType "directory" 
    }

    $Back = "$Path\back"
    if(!(Test-Path -Path "$Back\$date")){
        New-Item -Path "$Back" -Name "$date" -ItemType "directory"
        $Back = "$Back\$date"
    }
    else{
        $dateExists = $true
    }

    if($dateExists -eq $false){
        "Moving [$Path\*.jar] -> $Back"
        Move-Item -Path "$Path\*.jar" -Destination $Back
    }
    else{
        
        "Backup skipped [date already exists: $dateExists]!"
    }    
}

$ver = PowershellMenu -MenuTitle "Select the target" -MenuOptions "Server", "Client" -Columns 1 -MaximumColumnWidth 15 -ShowCurrentSelection $True
$modpacks = Get-Content "modpacks.txt"
$modpacks += "Custom"
$modpackId = PowershellMenu -MenuTitle "Select a modpack" -MenuOptions $modpacks -Columns 1 -MaximumColumnWidth 30 -ShowCurrentSelection $True
$modpack = $modpacks[$modpackId]

$mods = Get-Content "mods.txt"

"Selected modpack: $modpack"

if(!($ver -eq 0)){
    $Path = "$env:APPDATA\.minecraft\mods"
}else{
    Add-Type -AssemblyName 'System.Windows.Forms'
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $Path = $dialog.SelectedPath
        Write-Host "Directory selected is $Path"
    }
}

Get-ChildItem $Path -Include *.* -Recurse | ForEach-Object  { $_.Delete()}
if($modpackId -eq ($modpacks.count - 1)){
    $Folders = Get-ChildItem -Path "mods\" -Directory
    $list = ""
    foreach ($folder in $Folders)
    {
        if($folder[0] -ne '-'){
            $list += "$folder "
        }
        
    }
    $opt = Read-Host -Prompt "Enter the options ($list)"
}
else{
    $mods = Get-Content "modpack-content.txt"
    $opt = $mods[$modpackId]    
}

$options = $opt.Split(" ")

foreach ($option in $options)
{
    "Copy [$option\*.jar] -> [$Path]"
    Copy-Item -Path "mods\$option\*" -Destination $Path -Recurse
}