def get_dest_emails(dest_email_address, additional_email_addresses):
    ret_list = []
    ret_list.append(dest_email_address)
    if additional_email_addresses:
        for entry in additional_email_addresses.split(','):
            ret_list.append(
                entry.strip()
            )
    return ret_list