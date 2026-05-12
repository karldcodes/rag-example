from src.models.text_file import TextFile
from pathlib import Path

class TextFileReader:

    def get_files(self):
        docs_dir = Path("./src/docs")
        return docs_dir.glob("*.txt")
    
    def read(self, file) -> TextFile:
        text = file.read_text(encoding="utf-8")
        return TextFile(name=file.name, text=text)