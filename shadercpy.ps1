if(!(Test-Path -Path "$env:APPDATA\.minecraft\shaderpacks\s-medium.zip" -PathType Leaf)){
    if(Test-Path -Path "$env:APPDATA\.minecraft\shaderpacks"){
        Copy-Item -Path "Shaders/s-medium.zip" -Destination "$env:APPDATA\.minecraft\shaderpacks"
        "Done"
    }
    else{
        "Shaderpack folder does not exist"
    }
}
else{
    "Shader file already exists"
}