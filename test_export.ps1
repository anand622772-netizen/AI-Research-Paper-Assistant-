
 = New-Object -ComObject Word.Application
.Visible = False
 = .Documents.Open('C:\Users\anand\.gemini\antigravity\brain\4b96934e-3d55-4176-8be2-931a8f265f99\.user_uploaded\media_1792755620267_d5803262.docx')
 = 'C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\header_footer_sample.pdf'
.ExportAsFixedFormat(, 17)
.Close([ref]False)
.Quit()
Write-Output 'Exported header_footer_sample.pdf'
