from utils import *
import sys


def main():
    """
    This is program runner function from where the execution will start
    It will perform following steps:
    1. Fetching the data from dummyjson site
    2. Asking user how to sort data (by title or price)
    3. Sorting the data after user enter his choice
    4. Saving the sorted data in local
    5. Asking user whether to share data via email
        a. If Yes - Share file via email
        b. If No - Print the path of file in local
    """
    # Part 1: Fetching the data from dummyjson site
    data = []
    try:
        data = fetch_data()
    except requests.ConnectionError:
        print('Connection Timeout')
        sys.exit(1)
    except (ClientSideException, ServerSideException,
            RequestsErrorException, InvalidInputException,
            DataNotPresent) as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("Something went wrong !!")
        print(e)
        sys.exit(1)

    # Part 2: Asking user how to sort data
    i = 2
    sort_by = ''
    while i >= 0:
        sort_by = input("How do you want to sort the data? 'TITLE' Or 'PRICE'? ").lower()
        if sort_by == 'title' or sort_by == 'price':
            break
        print(f"Please enter values from following options (TITLE, PRICE) !! [{i} chances left]")
        i -= 1
    else:
        print("Program exited due to incorrect input")
        sys.exit(1)

    # Part 3: Sorting the data after user enter his choice
    sorted_data = sort_data(data, sort_by)

    # Part 4: Saving the sorted data
    save_data(sorted_data)

    # Part 5: Asking user whether to share data via email
    # If yes then share via email else just print the file location
    try:
        send_via_email = input("Do you want to share file via email? (YES/NO): ").lower()
        if send_via_email == 'yes':
            send_email(sort_by)
            print("File is shared via email")
        else:
            print("Result file is stored on below path:")
            print(get_result_location())
    except smtplib.SMTPAuthenticationError as e:
        print("Bad Credentials! Please pass the correct email credentials !!")
        print(e)
    except smtplib.SMTPResponseException as e:
        print("Please pass the email credentials !!")
        print("Make sure they are exported as ENV variables (EMAIL_ID, EMAIL_APP_PASSWORD)")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

