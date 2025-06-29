import os
import random
from reportlab.lib.pagesizes import letter as LETTER, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# List of simple French words (colors, numbers, seasons, shapes)
words = [
    "rouge", "bleu", "vert", "jaune",
    "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
    "été", "hiver",
    "rond", "carré",
]

# Page and layout settings
SQUARE_SIZE = 4 * cm
FONT_SIZE = 48
PAGE_WIDTH, PAGE_HEIGHT = landscape(LETTER)
os.makedirs("fiches_collage", exist_ok=True)

def create_worksheet(word):
    filename = f"fiches_collage/{word}.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(LETTER))

    # Define y_cut
    y_cut = 3 * cm

    # French instruction
    c.setFont("Helvetica", 16)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 2 * cm, "Découpe les lettres en bas, puis colle-les au bon endroit au centre.")

    # Title with the example word
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 6 * cm, f"Mot à reconstituer : {word.upper()}")

    # Shuffle letters
    letters = list(word.upper())
    shuffled_letters = letters[:]
    while shuffled_letters == letters:
        random.shuffle(shuffled_letters)

    # Draw paste squares in the center
    y_paste = y_cut + SQUARE_SIZE + 2 * cm
    x_paste_start = (PAGE_WIDTH - len(letters) * (SQUARE_SIZE + 0.5 * cm)) / 2
    for _ in letters:
        c.rect(x_paste_start, y_paste, SQUARE_SIZE, SQUARE_SIZE)
        x_paste_start += SQUARE_SIZE + 0.5 * cm

    # Dashed line separator between cut and paste area
    c.setDash(3, 3)
    c.line(1 * cm, y_cut + SQUARE_SIZE + 1 * cm, PAGE_WIDTH - 1 * cm, y_cut + SQUARE_SIZE + 1 * cm)
    c.setDash()

    # Draw cut-out letters at the bottom
    x_cut_start = (PAGE_WIDTH - len(shuffled_letters) * (SQUARE_SIZE + 0.5 * cm)) / 2
    c.setFont("Helvetica-Bold", FONT_SIZE)
    for char in shuffled_letters: 
        c.rect(x_cut_start, y_cut, SQUARE_SIZE, SQUARE_SIZE)
        c.drawCentredString(x_cut_start + SQUARE_SIZE / 2, y_cut + SQUARE_SIZE / 3, char)
        x_cut_start += SQUARE_SIZE + 0.5 * cm

    c.showPage()
    c.save()

# Generate worksheets
for word in words:
    create_worksheet(word)

print("Done")