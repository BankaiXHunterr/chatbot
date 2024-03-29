from fastapi import HTTPException
from io import BytesIO
from PyPDF2 import PdfReader
import pandas as pd
from docx import Document

class FileProcessor:
    async def read_pdf(self, file_content: bytes) -> str:
        """Reads the text content from a PDF file provided as bytes.

        Args:
            file_content (bytes): The content of the PDF file in bytes format.

        Returns:
            str: The extracted text content from all pages of the PDF.

        Raises:
            HTTPException: If an error occurs during PDF reading.
        """

        try:
            # Use BytesIO to create a file-like object from the bytes content
            file_stream = BytesIO(file_content)

            # Create a PdfReader object using the BytesIO stream
            pdf_reader = PdfReader(file_stream)

            # Extract text from all pages and concatenate
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            return text

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    async def read_txt(self, file_content: bytes) -> str:
        """Decodes file content using different encoding schemes.

        Args:
            file_content (bytes): The content of the file in bytes format.

        Returns:
            str: The decoded content.

        Raises:
            UnicodeDecodeError: If the content cannot be decoded using any of the specified encodings.
        """
        # List of encoding schemes to try
        encodings = ["utf-8", "latin-1"]  # Add more if necessary
        
        # Try decoding with each encoding scheme
        for encoding in encodings:
            try:
                decoded_content = file_content.decode(encoding)
                # If decoding succeeds, return the decoded content
                return decoded_content
            except UnicodeDecodeError:
                # If decoding fails, try the next encoding scheme
                continue
        
        # If none of the encodings succeed, raise an error
        raise UnicodeDecodeError("Unable to decode the file content with any of the specified encodings")

    async def read_docx(self, file_content: bytes) -> str:
        """Reads the text content from a DOCX file provided as bytes.

        Args:
            file_content (bytes): The content of the DOCX file in bytes format.

        Returns:
            str: The extracted text content from all paragraphs of the DOCX.

        Raises:
            HTTPException: If an error occurs during DOCX reading.
        """
        try:
            # Load the DOCX document from the file content
            doc = Document(BytesIO(file_content))
            
            # Extract text from all paragraphs in the document
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"  # Add newline for each paragraph
            
            return text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading DOCX: {str(e)}")

    async def get_csv(self, file_content: bytes) -> str:
        """Reads the content of a CSV file provided as bytes and converts it to a string.

        Args:
            file_content (bytes): The content of the CSV file in bytes format.

        Returns:
            str: The content of the CSV file converted to a string.

        Raises:
            HTTPException: If an error occurs during CSV reading.
        """
        try:
            # Load the CSV file from the file content
            df = pd.read_csv(BytesIO(file_content))
            file_content = df.to_string(index=False)
            return file_content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")

    async def process_file_by_extension(self, file_extension: str, file_content: bytes) -> str:
        """Processes file content based on file extension.

        Args:
            file_extension (str): The file extension (e.g., 'pdf', 'docx', 'csv').
            file_content (bytes): The content of the file in bytes format.

        Returns:
            str: The text content extracted from the file.

        Raises:
            HTTPException: If an error occurs during processing based on file extension.
        """
        file_extension = file_extension.lower()
        if file_extension == 'pdf':
            return await self.read_pdf(file_content)
        elif file_extension == 'docx':
            return await self.read_docx(file_content)
        elif file_extension == 'csv':
            return await self.get_csv(file_content)
        elif file_extension == 'txt':
            return await self.read_txt(file_content)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file extension: {file_extension}")
