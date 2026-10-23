$docxSrc = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
$docxDest = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
Copy-Item $docxSrc $docxDest -Force
Copy-Item $docxSrc "C:\Users\anand\Desktop\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx" -Force
Copy-Item $docxSrc "C:\Users\anand\Downloads\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx" -Force

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docxDest)
$doc.Fields.Update()
$pages = $doc.ComputeStatistics(2)
Write-Output "Total Page Count in Word: $pages"

$pdfDest = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf"
$doc.ExportAsFixedFormat($pdfDest, 17)
$doc.Close($false)
$word.Quit()

Copy-Item $pdfDest "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf" -Force
Copy-Item $pdfDest "C:\Users\anand\Desktop\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf" -Force
Copy-Item $pdfDest "C:\Users\anand\Downloads\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf" -Force
Write-Output "PDF Generation and Distribution Completed Successfully."
