# Control Tower

## Summary

### ct_provision_account
This script is used to provision a new account in the Control Tower. It automates the setup process, ensuring that all necessary configurations and resources are in place for the new account to operate within the Control Tower environment.

### enroll_existing_account
This script is designed to enroll an existing account into the Control Tower. It handles the integration of the account, applying the required policies and settings to bring it under the management of the Control Tower.


> **Warning**: These scripts are not production-ready and are not idempotent. Use them with caution and ensure you have proper backups and testing in place before running them in a live environment.

> **Note**: When enrolling an existing account:
>
> 1) The account should have the following role created: [AWSControlTowerExecution](https://docs.aws.amazon.com/controltower/latest/userguide/enroll-manually.html)
> 2) Invite the account to the organization.
> 3) User to accept the invitation.
> 4) Enroll in Control Tower.