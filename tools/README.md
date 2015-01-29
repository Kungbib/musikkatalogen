
# OCR AND PREVIEW IMG PROCESS

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


## Example output of cleaned scanner image

| Scanned        | Clean           |
| ------------- |:-------------:|
| ![Scanned catalog card](example_output/0035_alfa_20140709_0045.jpg?raw=true) | ![Cleaned catalog card](example_output/0035_alfa_20140709_0045_clean.jpg?raw=true) |


## Raw OCR output

```
- H a n s s o n , Axel Stig

Det bor tusende ömma små löften. Fbxtrot. Musik: Jules
Sylvain. Text: Sven-Olof Sandberg. Arr.: Niff Görling.
Sthlm. Edition Sylvain (E.S.25u7):tr.Br.Lagerström
19k; [Papual h,

Ur folmoperetten "Hans Majestäts rival"
```
