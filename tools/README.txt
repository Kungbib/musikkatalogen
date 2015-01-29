
OCR AND PREVIEW IMG PROCESS
---------------------------

The toolchain consists of the following steps:


1. Scan cards to generate one folder of card images per box (manual process) /folder/boxfolder/<file>.jpg

2. makecleanimg.py
Prepare images for OCR (despeckle, contrast enhance etc) by generating /folder/boxfolder/<file>_clean.jpg

3. makeviewfile.py
Generate smaller preview jpegs (500 px wide) to /folder/boxfolder/<file>_view500.jpg

4. /ocr/ocrfolder.py
Run Tesseract OCR on cleaned image files and output raw ocr and clean ocr to
/folder/boxfolder/<file>_rawocr.txt and /folder/boxfolder/<file>_cleanocr.txt

Settings for tesseract is in the tessdata folder.
