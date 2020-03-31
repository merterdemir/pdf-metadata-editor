# pdf-metadata-editor
Command Line PDF Metadata Editor (Python)

## Requirements
- pdfrw
- Argparser

## Usage
From command line:
```bash
python3 PDFMetadataEditor.py FILENAME [options]
```

In order to only print the metadata:
```bash
python3 PDFMetadataEditor.py FILENAME -p
```

Specify an output file name:
```bash
python3 PDFMetadataEditor.py FILENAME -e output_filename.pdf
```

Overwrite the current file:
```bash
python3 PDFMetadataEditor.py FILENAME -ow
```

You can combine `-p` option with other two options `[-ow, -e]`.