# app/pdf_generator.py
from fpdf import FPDF
import os
from datetime import date
from typing import Optional
import qrcode
from io import BytesIO
import textwrap
from flask import current_app

class TripPDF(FPDF):
    def header(self):
        """Add header to each page."""
        # Use Helvetica (built-in) instead of Arial
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'TripAI - Your Travel Itinerary', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        """Add a chapter title."""
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, text):
        """Add chapter text with proper wrapping."""
        self.set_font('Helvetica', '', 12)
        # Split text into lines that fit within page width
        effective_page_width = self.w - 2 * self.l_margin
        # Calculate maximum characters per line (approximate)
        max_chars_per_line = int(effective_page_width / (self.font_size * 0.5))
        
        lines = text.split('\n')
        for line in lines:
            # Skip empty lines
            if not line.strip():
                self.ln()
                continue
                
            # Wrap long lines
            wrapped_lines = textwrap.wrap(line, width=max_chars_per_line)
            for wrapped_line in wrapped_lines:
                self.multi_cell(effective_page_width, 6, wrapped_line)
            self.ln(2)

def generate_trip_pdf(itinerary: str, start_location: str, destination: str, 
                     start_date: date, end_date: date) -> str:
    """Generate a PDF file containing the trip itinerary."""
    # Initialize PDF
    pdf = TripPDF()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Add cover page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(0, 20, f'Trip to {destination}', 0, 1, 'C')
    
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, f'From: {start_location}', 0, 1, 'C')
    pdf.cell(0, 10, f'Date: {start_date.strftime("%B %d, %Y")} - {end_date.strftime("%B %d, %Y")}', 0, 1, 'C')
    
    # Generate QR code
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"https://tripai.app/trip/{id}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        pdf.image(qr_buffer, x=85, y=100, w=40)
        pdf.ln(80)
        pdf.cell(0, 10, 'Scan to view digital version', 0, 1, 'C')
    except Exception as e:
        print(f"Error generating QR code: {e}")
    
    # Add itinerary content
    pdf.add_page()
    pdf.chapter_title('Detailed Itinerary')
    
    # Process and format itinerary content
    current_text = ""
    for line in itinerary.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('# '):
            if current_text:
                pdf.chapter_body(current_text)
                current_text = ""
            pdf.chapter_title(line[2:])
        elif line.startswith('## '):
            if current_text:
                pdf.chapter_body(current_text)
                current_text = ""
            pdf.set_font('Helvetica', 'B', 14)
            pdf.cell(0, 10, line[3:], 0, 1, 'L')
            pdf.set_font('Helvetica', '', 12)
        else:
            current_text += line + "\n"
    
    # Process final section
    if current_text:
        pdf.chapter_body(current_text)
    
    # Generate filename and proper path
    filename = f"trip_{destination.lower().replace(' ', '_')}_{start_date.strftime('%Y%m%d')}.pdf"
    
    # Use Flask's instance path for file storage
    pdf_dir = os.path.join(current_app.instance_path, 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    filepath = os.path.join(pdf_dir, filename)
    
    # Save PDF
    pdf.output(filepath)
    return filepath