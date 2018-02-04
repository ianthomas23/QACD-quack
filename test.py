from document import Document




doc = Document()


doc.load_csv_files('test_data', ['Ca K series.csv', 'O K series.csv'])
print(doc.elements)
