def extract_email_data_from_file(file_path):
    # Reading the email content from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Store words of each line in a different list
    words_list = [line.split() for line in lines if line.strip()]

    # Extract the second word from each line if it exists
    second_words = [words[1] if len(words) > 1 else None for words in words_list]

    # Extracting relevant email data
    sender_email = None
    receiver_email = None
    spf_status = None
    dkim_status = None
    dmarc_status = None

    for i, line in enumerate(lines):
        if line.startswith("From:"):
            sender_email = second_words[i]
        elif line.startswith("To:"):
            receiver_email = second_words[i]
        elif line.startswith("SPF:"):
            spf_status = ' '.join(words_list[i][1:]).strip()
        elif line.startswith("DKIM:"):
            dkim_status = ' '.join(words_list[i][1:]).strip()
        elif line.startswith("DMARC:"):
            dmarc_status = ' '.join(words_list[i][1:]).strip()

    # Determining the authentication status
    pass_criteria = ["PASS", "'PASS'"]
    statuses = [spf_status, dkim_status, dmarc_status]

    if all(any(crit in status for crit in pass_criteria) for status in statuses): #all pass
        authentication_status = "Authenticated"
    elif all("FAIL" in status for status in statuses): #all fail
        authentication_status = "Not Authenticated"
    else:
        authentication_status = "Partially Authenticated" #one of them fail

    return {
        "Sender": sender_email,
        "Receiver": receiver_email,
        "SPF": spf_status,
        "DKIM": dkim_status,
        "DMARC": dmarc_status,
        "Authentication Status": authentication_status
    }

# Path to the email text file
file_path = 'sampleheader.txt'

# Extracting data
email_data = extract_email_data_from_file(file_path)
for key, value in email_data.items():
    print(f"{key}: {value}")
