import sys
import ast
import os
import fitz  # PyMuPDF
import spacy
from typing import List, Dict
import logging
import re
import numpy as np
import faiss  # Local vector database

class AdvancedDocumentQA:
    def __init__(self, index_name):
        """
        Advanced Document QA system with enhanced information extraction
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Load spaCy model for embeddings and keyword extraction
        self.nlp = spacy.load("en_core_web_md")
        
        # FAISS initialization
        self.dimension = self.nlp("test").vector.shape[0]  # Embedding dimension from spaCy
        self.index = faiss.IndexFlatL2(self.dimension)  # Using L2 distance metric
        self.metadata = {}  # Store metadata with vector IDs

        self.index_name = index_name
        self.logger.info(f"FAISS index {index_name} initialized with dimension {self.dimension}")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from PDF or text files with enhanced preprocessing
        """
        try:
            if file_path.lower().endswith('.pdf'):
                with fitz.open(file_path) as pdf:
                    text = " ".join([page.get_text() for page in pdf])
                    text = re.sub(r'\s+', ' ', text).strip()
                return text
            elif file_path.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    text = re.sub(r'\s+', ' ', text).strip()
                return text
            else:
                self.logger.warning(f"Unsupported file type: {file_path}")
                return ""
        except Exception as e:
            self.logger.error(f"Text extraction error for {file_path}: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        """
        Advanced text chunking with smart segmentation
        """
        def is_good_chunk(chunk: str) -> bool:
            """Ensure chunk has meaningful content"""
            return (len(chunk.split()) > 10 and 
                    len(chunk) < 500)
        
        chunks = []
        start = 0
        while start < len(text):
            chunk = text[start:start+chunk_size]
            if is_good_chunk(chunk):
                chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks
    
    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """
        Extract most important keywords from text
        """
        doc = self.nlp(text)
        # Using named entities and noun chunks for keywords
        keywords = [ent.text for ent in doc.ents] + [chunk.text for chunk in doc.noun_chunks]
        keyword_freq = {keyword: text.count(keyword) for keyword in keywords}
        sorted_keywords = sorted(keyword_freq, key=keyword_freq.get, reverse=True)
        return sorted_keywords[:top_k]
    
    def process_document(self, file_path: str):
        """
        Advanced document processing with multi-stage indexing
        """
        text = self.extract_text_from_file(file_path)
        global_keywords = self.extract_keywords(text)
        chunks = self.chunk_text(text)
        
        # Generate embeddings using spaCy
        embeddings = [self.nlp(chunk).vector for chunk in chunks]
        
        vector_ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{file_path}_{i}"
            self.metadata[vector_id] = {
                "text": chunk,
                "source": file_path,
                "keywords": global_keywords
            }
            vector_ids.append(vector_id)
        
        try:
            # Add vectors to FAISS index
            self.index.add(np.array(embeddings, dtype='float32'))
            self.logger.info(f"Processed {file_path}: {len(chunks)} chunks, {len(global_keywords)} keywords")
        except Exception as e:
            self.logger.error(f"Indexing error: {e}")
    
    def query_and_extract_info(self, question: str, top_k: int = 5) -> Dict:
        """
        Advanced query with multi-stage information extraction
        """
        try:
            query_embedding = self.nlp(question).vector.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_embedding, top_k)
            
            extracted_info = {
                'query': question,
                'results': [],
                'key_insights': []
            }
            
            for idx, distance in zip(indices[0], distances[0]):
                if idx < 0:
                    continue
                vector_id = list(self.metadata.keys())[idx]
                metadata = self.metadata[vector_id]
                extracted_info['results'].append({
                    'text': metadata['text'],
                    'source': metadata['source'],
                    'relevance_score': 1 - distance / 2  # Normalize cosine similarity
                })
            
            return extracted_info
        except Exception as e:
            self.logger.error(f"Query extraction error: {e}")
            return {}

def main():
    INDEX_NAME = 'advanced-document-qa'

    input_data = sys.stdin.read()
    try:
        data = ast.literal_eval(input_data)
    except Exception as e:
        print(f"Input parsing error: {e}")
        return
    
    uploaded_files = data.get("uploaded_files", [])
    questions = data.get("questions", "").split('\n')
    
    try:
        qa_system = AdvancedDocumentQA(INDEX_NAME)
        
        for file_path in uploaded_files:
            qa_system.process_document(file_path)
        
        for question in questions:
            if question.strip():
                extracted_info = qa_system.query_and_extract_info(question)
                print(f"\nQuestion: {question}")
                for result in extracted_info.get('results', []):
                    print(f"\nRelevant Snippet (Score: {result['relevance_score']:.2f}):")
                    print(f"Source: {result['source']}")
                    print(f"Text: {result['text']}")
    
    except Exception as e:
        print(f"Document QA System Error: {e}")

if __name__ == "__main__":
    main()
