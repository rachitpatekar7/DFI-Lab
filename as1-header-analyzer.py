#Code to implement email header analyzer and check if email is fully authenticated or not.
def ex_data(fp): #reading email content
    with open(fp, 'r') as f:
        lines = f.readlines()

    #storing words of each line in a different list
    words_list = [line.split() for line in lines if line.strip()]

    #extract the second word from each line 
    second_words = [words[1] if len(words) > 1 else None for words in words_list]

   #declaring variables
    sndr_email = None
    rcvr_email = None
    spf_status = None
    dkim_status = None
    dmarc_status = None

  #extracting data according to the header format
    for i, line in enumerate(lines):
        if line.startswith("From:"):
            sndr_email = second_words[i]
        elif line.startswith("To:"):
            rcvr_email = second_words[i]
        elif line.startswith("SPF:"):
            spf_status = ' '.join(words_list[i][1:]).strip()
        elif line.startswith("DKIM:"):
            dkim_status = ' '.join(words_list[i][1:]).strip()
        elif line.startswith("DMARC:"):
            dmarc_status = ' '.join(words_list[i][1:]).strip()

    #authentication
    pass_criteria = ["PASS", "'PASS'"]
    statuses = [spf_status, dkim_status, dmarc_status]

    if all(any(crit in status for crit in pass_criteria) for status in statuses):
        auth_status = "Authenticated"
    elif any("FAIL" in status for status in statuses):
        auth_status = "Partially Authenticated"
    else:
        auth_status = "Not Authenticated"

    return {
        "Sender": sndr_email,
        "Receiver": rcvr_email,
        "SPF": spf_status,
        "DKIM": dkim_status,
        "DMARC": dmarc_status,
        "Authentication Status": auth_status
    }

#header text file path
fp = 'sampleheader.txt'

#extracting data
email_data = ex_data(fp)
for key, value in email_data.items():
    print(f"{key}: {value}")
