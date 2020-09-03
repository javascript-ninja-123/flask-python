from marshmallow import Schema, fields, INCLUDE, EXCLUDE

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str()
    description = fields.Str()
    
    
class Book:
    def __init__(self, title: str, author: str, description: str):
        self.title = title
        self.author = author
        self.description = description
        
        
book = Book("clean code", "Bob Martin", "A book about writing cleaning code")

book_schema = BookSchema()
book_dict = book_schema.dump(book)

print(book_dict)

# incoming book data

incomebook = {
    "title":"Clean code",
    "author":"Bob Martin",
    "description":"A book about writing cleaner code"
}


#  book_schema = BookSchema(unknown=INCLUDE/EXCLUDE)
book_schema = BookSchema()
book = book_schema.load(incomebook)

print(book)
