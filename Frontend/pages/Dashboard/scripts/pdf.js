function generatePDF() {
    // Create a new jsPDF instance
    var doc = new jsPDF(data);

    // Assuming 'data' is your dataset, you need to add it to the PDF using jsPDF methods
    doc.text("Hello, this is your dataset!", 10, 10);

    // Save the PDF with a specific name
    doc.save("generated.pdf");
}