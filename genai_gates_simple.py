# Simulated user data
user_data = {
    "user1": {"password": "password1", "role": "free"},
    "user2": {"password": "password2", "role": "premium"},
}


# User login simulation
def login():
    username = input("Username: ")
    password = input("Password: ")

    if username in user_data and user_data[username]["password"] == password:
        return user_data[username]["role"]
    else:
        print("Invalid credentials!")
        return None


# Document upload gate with user-input document size
def upload_document(role):
    try:
        document_size = int(input("Enter the size of the document in bytes: "))
    except ValueError:
        print("Invalid input for document size. Please enter an integer value.")
        return

    size_limit = 10240  # 10 KB size limit for free users
    print(f"Document size: {document_size} bytes")

    if role == "free" and document_size > size_limit:
        raise PermissionError("Document size exceeds limit for free users.")
    else:
        summarize_document()


# Simulated document processing
def summarize_document():
    print("Document is being processed and summarized...")


# Simulate user login and document upload
user_role = login()

if user_role:
    try:
        # Simulate document upload with size check
        upload_document(user_role)
    except PermissionError as e:
        print(e)
else:
    print("Login failed. Please try again.")
