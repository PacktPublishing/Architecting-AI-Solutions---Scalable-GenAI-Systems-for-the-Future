from dotenv import load_dotenv
import logging
import os
import asyncio
import sqlite3
import hashlib
import secrets
from cryptography.fernet import Fernet  # pip install cryptography


from openai import OpenAI


load_dotenv()

# must do pip install python-dotenv, openai, and sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# SQLite database setup (simulated)
# === Application Layer: SQLite database setup (Simulates storing users and feedback)

conn = sqlite3.connect(":memory:")  # In-memory database for simplicity
cursor = conn.cursor()

cursor.execute("""CREATE TABLE users (username TEXT, password TEXT, role TEXT)""")
cursor.execute("""CREATE TABLE feedback (summary TEXT, feedback TEXT)""")

# Add sample users to the database
cursor.execute(
    "INSERT INTO users VALUES ('user1', ?, 'free')",
    (hashlib.sha256("password1".encode()).hexdigest(),),
)
cursor.execute(
    "INSERT INTO users VALUES ('user2', ?, 'premium')",
    (hashlib.sha256("password2".encode()).hexdigest(),),
)

conn.commit()

# Simulated cloud storage (Infrastructure Layer)
# Infrastructure Layer: Simulated cloud storage for documents
cloud_storage = {
    "documents": [],
}

# Generate and store the encryption key (should be stored securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)


# Encrypt a document
# ==== Infrastructure Layer: Encrypt a document

def encrypt_document(document):
    print("Encrypting document...")
    encrypted_doc = cipher_suite.encrypt(document.encode())
    return encrypted_doc


# Decrypt a document
# === Infrastructure Layer: Decrypt a document


def decrypt_document(encrypted_doc):
    print("Decrypting document...")
    decrypted_doc = cipher_suite.decrypt(encrypted_doc).decode()
    return decrypted_doc


# GPT-3 Summarization Function
# === Model Layer: GPT-3 Summarization Function using OpenAI API


def gpt3_summarize(text):
    print("Summarizing document using GPT-3...")
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "please summarize the following text:"},
            {"role": "user", "content": text},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    summary = response.choices[0].message.content
    # summary = response.choices[0].text.strip()
    return summary


# User login with token-based authentication (Application Layer)
# ==== Application Layer: User login with token-based authentication


async def login():
    username = input("Username: ")
    password = hashlib.sha256(input("Password: ").encode()).hexdigest()

    cursor.execute(
        "SELECT role FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    result = cursor.fetchone()

    if result:
        token = secrets.token_hex(16)
        logging.info(f"User {username} authenticated successfully with token {token}")
        return username, result[0], token
    else:
        logging.error("Invalid credentials!")
        return None, None, None


# Document upload with file size validation gate (Gate)
# ==== Gate: Document upload with file size validation and encryption


async def upload_document(role, token):
    print("\nUpload a document:")
    file_path = "./data/i-have-a-dream.txt"  # Path to the text file

    try:
        # Get the file size
        # ==== Gate: Get the file size to validate based on the user role

        document_size = os.path.getsize(file_path)
        logging.info(f"Document size: {document_size} bytes")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return
    except Exception as e:
        logging.error(f"Error getting file size: {e}")
        return

    size_limit = 10240  # 10 KB size limit for free users

    if role == "free" and document_size > size_limit:
        logging.error("Document size exceeds limit for free users.")
        raise PermissionError("Document size exceeds limit for free users.")
    else:
        # Read and encrypt the content of the file
        # ==== Infrastructure Layer: Read and encrypt the content of the file

        with open(file_path, "r") as file:
            document = file.read()
            encrypted_document = encrypt_document(document)

        if role == "free":
            # Real-time processing (Pipeline)
            # === Pipeline: Real-time processing for free users ===

            print("Document uploaded for real-time processing....")
            await summarize_document(encrypted_document)
        else:
            # Batch processing (Pipeline)
            # ==== Pipeline: Batch processing for premium users ===
            cloud_storage["documents"].append(encrypted_document)
            logging.info("Document uploaded for batch processing.")


# Document summarization using GPT-3 (Model Layer)
# ===== # Model Layer: Document summarization using GPT-3 after decrypting
async def summarize_document(encrypted_document):
    # Decrypt document before summarizing
    document = decrypt_document(encrypted_document)

    # Use GPT-3 to summarize the document
    summary = gpt3_summarize(document)
    logging.info(f"Summary: {summary}\n")

    # Simulate feedback loop (Loop)
    await gather_feedback(summary)


# Feedback loop (Loop)
# ===== Loop: Gather feedback from the user to simulate model improvement ===
async def gather_feedback(summary):
    print("\nHow was the summary?")
    feedback = input("Enter feedback (good/bad): ").lower()
    if feedback not in ["good", "bad"]:
        logging.error("Invalid feedback!")
    else:
        cursor.execute("INSERT INTO feedback VALUES (?, ?)", (summary, feedback))
        conn.commit()
        logging.info(f"Feedback stored: {feedback}")


# Simulate user login and document upload process
async def start_simulation():
    username, user_role, token = await login()

    if user_role:
        while True:
            try:
                await upload_document(user_role, token)
            except PermissionError as e:
                logging.error(e)

            # Ask the user if they want to continue or quit
            choice = input("Do you want to continue? (yes/no): ").lower()
            if choice == "no":
                logging.info("Exiting simulation. Thanks for your feedback!")
                break
    else:
        logging.error("Login failed. Please try again.")


# Simulate batch processing for premium users (Infrastructure Layer)
async def batch_processing():
    if cloud_storage["documents"]:
        logging.info("Batch processing the following documents for premium users:")
        for encrypted_doc in cloud_storage["documents"]:
            await summarize_document(encrypted_doc)
        cloud_storage["documents"].clear()  # Clear the storage after processing


# Start the simulation with asyncio concurrency
async def main():
    await start_simulation()
    await batch_processing()  # Process any batch jobs after user interaction


# Run the simulation
asyncio.run(main())

# Print feedback data for debugging (Loop to improve model later)
cursor.execute("SELECT * FROM feedback")
logging.info(f"Feedback received so far: {cursor.fetchall()}")
