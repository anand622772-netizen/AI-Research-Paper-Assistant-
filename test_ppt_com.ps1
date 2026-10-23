try {
    $ppt = New-Object -ComObject PowerPoint.Application
    Write-Host "PowerPoint COM Available"
    $ppt.Quit()
} catch {
    Write-Host "PowerPoint COM Not Available: $_"
}
