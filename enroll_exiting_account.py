import boto3
from icecream import ic
import time


def invite_account_to_org(account_id):
    client = boto3.client("organizations")

    try:
        response = client.invite_account_to_organization(
            Target={
                "Id": account_id,  # Replace with the AWS account ID you want to invite
                "Type": "ACCOUNT",
            },
            Notes="Invitation to join the organization",
        )
        ic(response)
    except client.exceptions.AccountOwnerNotVerifiedException as e:
        ic(f"Account owner not verified: {e}")
    except client.exceptions.AWSOrganizationsNotInUseException as e:
        ic(f"AWS Organizations not in use: {e}")
    except client.exceptions.ConcurrentModificationException as e:
        ic(f"Concurrent modification: {e}")
    except client.exceptions.ConstraintViolationException as e:
        ic(f"Constraint violation: {e}")
    except client.exceptions.DuplicateAccountException as e:
        ic(f"Duplicate account: {e}")
    except client.exceptions.FinalizingOrganizationException as e:
        ic(f"Finalizing organization: {e}")
    except client.exceptions.HandshakeConstraintViolationException as e:
        ic(f"Handshake constraint violation: {e}")
    except client.exceptions.InvalidInputException as e:
        ic(f"Invalid input: {e}")
    except client.exceptions.ServiceException as e:
        ic(f"Service exception: {e}")
    except client.exceptions.TooManyRequestsException as e:
        ic(f"Too many requests: {e}")
    except Exception as e:
        ic(f"Unexpected error: {e}")

    while True:
        try:
            response = client.describe_account(AccountId=account_id)
            if response["Account"]["JoinedMethod"] == "INVITED":
                ic(f"Account {account_id} has successfully joined the organization.")
                break
        except client.exceptions.AccountNotFoundException as e:
            ic(f"Account not found: {e}")
        except Exception as e:
            ic(f"Error checking if account has joined the organization: {e}")
        time.sleep(20)


def check_prerequisites(): ...


def enroll_existing_account():
    """
    Enrolls an existing account into AWS Control Tower.
    """


if __name__ == "__main__":
    invite_account_to_org("940482448078")
