# Simulated user data (Data Layer)
user_data = {
    "user1": {"password": "password1", "role": "free"},
    "user2": {"password": "password2", "role": "premium"},
}

# Simulated feedback storage (Loop for model improvement)
feedback_data = {}


# Simulate a simple AI model that adjusts its "quality" based on feedback
def adjust_model_based_on_feedback():
    good_feedback_count = sum(1 for f in feedback_data.values() if f == "good")
    return 100 - (
        5 * good_feedback_count
    )  # Reduce summary length by 5 chars for each good feedback


# User login simulation (Application Layer)
def login():
    username = input("Username: ")
    password = input("Password: ")

    if username in user_data and user_data[username]["password"] == password:
        return username, user_data[username]["role"]
    else:
        print("Invalid credentials!")
        return None, None


# Data validation gate and access control (Gate)
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
        # Document processing pipeline (Pipeline)
        document = (
            "This is a sample document for GenAI summarization. " * 5
        )  # A made-up text
        summarize_document(document)


# Document summarization (Model Layer)
def summarize_document(document):
    # Adjust summary based on feedback (Model Layer)
    summary_length = adjust_model_based_on_feedback()
    summary = document[
        :summary_length
    ]  # Truncate document based on "model adjustments"
    print(f"Summary: {summary}...\n")

    # Simulate a feedback loop (Loop)
    gather_feedback(summary)


# Simulate feedback loop (Loop)
def gather_feedback(summary):
    print("\nHow was the summary?")
    feedback = input("Enter feedback (good/bad): ").lower()
    if feedback not in ["good", "bad"]:
        print("Invalid feedback!")
    else:
        # Simulate storing feedback for future model improvement
        feedback_data[summary] = feedback
        print(f"Feedback stored: {feedback}")


# Pipeline: Simulate user login and document upload process
def start_simulation():
    username, user_role = login()

    if user_role:
        while True:
            try:
                # Pipeline: Simulate document upload and processing
                upload_document(user_role)
            except PermissionError as e:
                print(e)

            # Ask the user if they want to continue or quit
            choice = input("Do you want to continue? (yes/no): ").lower()
            if choice == "no":
                print("Exiting simulation. Thanks for your feedback!")
                break
    else:
        print("Login failed. Please try again.")


# Start the simulation
start_simulation()

# Print feedback data (Loop to improve model later)
print("\nFeedback received so far:", feedback_data)
