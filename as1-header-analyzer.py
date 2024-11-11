# Path to the email text file
file_path = 'sampleheader.txt'

# Reading the email content from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Store words of each line in a different list
words_list = [line.split() for line in lines if line.strip()]

# Extract the second word from each line if it exists
second_words = [words[1] if len(words) > 1 else None for words in words_list]

# Initialize variables for storing relevant email data
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

# Determine the authentication status
pass_criteria = ["PASS", "'PASS'"]
statuses = [spf_status, dkim_status, dmarc_status]

if all(any(crit in status for crit in pass_criteria) for status in statuses):
    authentication_status = "Authenticated"
elif all("FAIL" in status for status in statuses):
    authentication_status = "Not Authenticated"
else:
    authentication_status = "Partially Authenticated"

# Print the extracted data
print("Sender:", sender_email)
print("Receiver:", receiver_email)
print("SPF:", spf_status)
print("DKIM:", dkim_status)
print("DMARC:", dmarc_status)
print("Authentication Status:", authentication_status)
