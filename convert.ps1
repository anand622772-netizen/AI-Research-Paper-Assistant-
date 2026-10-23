$docxPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
$pdfPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf"

Write-Host "Starting Word Application COM object..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "Exporting to PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "Conversion completed successfully!"
}
catch {
    Write-Error $_
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
