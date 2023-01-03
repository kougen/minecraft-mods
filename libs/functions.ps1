Function PowershellMenu (){
    #Start-Transcript "C:\_RRC\MenuLog.txt"
    Param(
        [Parameter(Mandatory=$True)][String]$MenuTitle,
        [Parameter(Mandatory=$True)][array]$MenuOptions,
        [Parameter(Mandatory=$True)][String]$Columns = "Auto",
        [Parameter(Mandatory=$False)][int]$MaximumColumnWidth=20,
        [Parameter(Mandatory=$False)][bool]$ShowCurrentSelection=$False
    )

    $MaxValue = $MenuOptions.count-1
    $Selection = 0
    $EnterPressed = $False

    If ($Columns -eq "Auto"){
        $WindowWidth = (Get-Host).UI.RawUI.MaxWindowSize.Width
        $Columns = [Math]::Floor($WindowWidth/($MaximumColumnWidth+2))
    }

    If ([int]$Columns -gt $MenuOptions.count){
        $Columns = $MenuOptions.count
    }

    $RowQty = ([Math]::Ceiling(($MaxValue+1)/$Columns))
        
    $MenuListing = @()

    For($i=0; $i -lt $Columns; $i++){
            
        $ScratchArray = @()

        For($j=($RowQty*$i); $j -lt ($RowQty*($i+1)); $j++){

            $ScratchArray += $MenuOptions[$j]
        }

        $ColWidth = ($ScratchArray |Measure-Object -Maximum -Property length).Maximum

        If ($ColWidth -gt $MaximumColumnWidth){
            $ColWidth = $MaximumColumnWidth-1
        }

        For($j=0; $j -lt $ScratchArray.count; $j++){
            
            If(($ScratchArray[$j]).length -gt $($MaximumColumnWidth -2)){
                $ScratchArray[$j] = $($ScratchArray[$j]).Substring(0,$($MaximumColumnWidth-4))
                $ScratchArray[$j] = "$($ScratchArray[$j])..."
            } Else {
            
                For ($k=$ScratchArray[$j].length; $k -lt $ColWidth; $k++){
                    $ScratchArray[$j] = "$($ScratchArray[$j]) "
                }

            }
            
            $ScratchArray[$j] = " $($ScratchArray[$j]) "
        }
        $MenuListing += $ScratchArray
    }
    
    Clear-Host

    While($EnterPressed -eq $False){
        
        Write-Host "$MenuTitle"
        
        If ($ShowCurrentSelection -eq $True){
            $Host.UI.RawUI.WindowTitle = "CURRENT SELECTION: $($MenuOptions[$Selection])"
        }

        For ($i=0; $i -lt $RowQty; $i++){

            For($j=0; $j -le (($Columns-1)*$RowQty);$j+=$RowQty){

                If($j -eq (($Columns-1)*$RowQty)){
                    If(($i+$j) -eq $Selection){
                        Write-Host -BackgroundColor cyan -ForegroundColor Black "$($MenuListing[$i+$j])"
                    } Else {
                        Write-Host "$($MenuListing[$i+$j])"
                    }
                } Else {

                    If(($i+$j) -eq $Selection){
                        Write-Host -BackgroundColor Cyan -ForegroundColor Black "$($MenuListing[$i+$j])" -NoNewline
                    } Else {
                        Write-Host "$($MenuListing[$i+$j])" -NoNewline
                    }
                }
                
            }

        }

        #Uncomment the below line if you need to do live debugging of the current index selection. It will put it in green below the selection listing.
        #Write-Host -ForegroundColor Green "$Selection"

        $KeyInput = $host.ui.rawui.readkey("NoEcho,IncludeKeyDown").virtualkeycode

        Switch($KeyInput){
            13{
                $EnterPressed = $True
                Return $Selection
                Clear-Host
                break
            }

            37{ #Left
                If ($Selection -ge $RowQty){
                    $Selection -= $RowQty
                } Else {
                    $Selection += ($Columns-1)*$RowQty
                }
                Clear-Host
                break
            }

            38{ #Up
                If ((($Selection+$RowQty)%$RowQty) -eq 0){
                    $Selection += $RowQty - 1
                } Else {
                    $Selection -= 1
                }
                Clear-Host
                break
            }

            39{ #Right
                If ([Math]::Ceiling($Selection/$RowQty) -eq $Columns -or ($Selection/$RowQty)+1 -eq $Columns){
                    $Selection -= ($Columns-1)*$RowQty
                } Else {
                    $Selection += $RowQty
                }
                Clear-Host
                break
            }

            40{ #Down
                If ((($Selection+1)%$RowQty) -eq 0 -or $Selection -eq $MaxValue){
                    $Selection = ([Math]::Floor(($Selection)/$RowQty))*$RowQty
                    
                } Else {
                    $Selection += 1
                }
                Clear-Host
                break
            }
            Default{
                Clear-Host
            }
        }
    }
}
