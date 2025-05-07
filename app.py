from flask import Flask, render_template, send_file, request
from io import BytesIO
from PyPDF2 import PdfMerger

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def merge_pdfs():
    if request.method == 'POST':

        # get the selected pdf files
        pdf_files = request.files.getlist("pdf_files")
        
        # get the merger class from the library
        merger = PdfMerger()

        # merge all pdf together
        for pdf in pdf_files:
            merger.append(pdf)

        # create a temporary container for those merged files
        buffer = BytesIO()

        # put them into the buffer (container)
        merger.write(buffer)

        # after writing, the pointer is at the end of the buffer. 
        # if we want to send the contents of the buffer, we need to resent the pointer back to the start
        buffer.seek(0)

        ## allow the file to be downloaded

        return send_file(buffer, as_attachment=True, download_name="mergered_files.pdf")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)