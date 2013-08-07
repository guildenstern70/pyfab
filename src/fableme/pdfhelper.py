""" 
 
 FABLE-O-MATIC 
 A LittleLite Web Application
 
 pdfhelper.py
 
"""

from fpdf.fpdf import FPDF

class PDF(FPDF):
    """ PDF Helper class """
    
    def header(self):
        self.set_font('Times', 'B', 15)
        # Calculate width of title and position
        wdth = self.get_string_width(self.title) + 6
        self.set_x((210 - wdth) / 2)
        # Colors of frame, background and text
        self.set_draw_color(200, 220, 255)
        self.set_fill_color(230, 230, 230)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(wdth, 9, self.title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Times', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'http://www.fableme.com/ - Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Times', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, "Chapter %d : %s" % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, txt):
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)
