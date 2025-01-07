import boto3
from icecream import ic
import time
import re

sc_client = boto3.client("servicecatalog")


def slugify(value):
    """
    Converts a string to a slug format, suitable for use in URLs and filenames.
    Args:
        value (str): The string to be converted to a slug.
    Returns:
        str: The slugified string.
    """
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-")
    return value


def get_provisioned_params(account_id):
    """
    Retrieve provisioning parameters for a given AWS account.

    This function uses the AWS Organizations client to describe an account
    and extract relevant information to create a list of provisioning parameters.

    Args:
        account_id (str): The AWS account ID for which to retrieve provisioning parameters.

    Returns:
        list: A list of dictionaries containing provisioning parameters with keys:
            - 'AccountEmail': The email associated with the AWS account.
            - 'AccountName': The name of the AWS account.
            - 'ManagedOrganizationalUnit': The organizational unit (hardcoded as 'Sandbox (ou-jefs-1f8d3s88)').
            - 'SSOUserEmail': The email associated with the AWS account.
            - 'SSOUserFirstName': The first name of the SSO user (hardcoded as 'Robert').
            - 'SSOUserLastName': The last name of the SSO user (hardcoded as 'Abed').
    """

    client = boto3.client("organizations")
    response = client.describe_account(AccountId=account_id)
    account_email = response["Account"]["Email"]
    account_name = response["Account"]["Name"]
    provisioning_parameters = [
        {"Key": "AccountEmail", "Value": account_email},
        {"Key": "AccountName", "Value": f"{account_name}"},
        {
            "Key": "ManagedOrganizationalUnit",
            "Value": "Sandbox (ou-jefs-1f8d3s88)",
        },  # should be function argument
        {"Key": "SSOUserEmail", "Value": account_email},
        {"Key": "SSOUserFirstName", "Value": "Robert"},
        {"Key": "SSOUserLastName", "Value": "Abed"},
    ]
    ic(provisioning_parameters)
    return provisioning_parameters


def get_product_id():
    """
    Retrieves the product ID for the 'AWS Control Tower Account Factory' product.
    This function searches for products using the AWS Service Catalog client and filters the results
    to find the 'AWS Control Tower Account Factory' product. It then extracts and returns the product ID
    from the search results.
    Returns:
        str: The product ID of the 'AWS Control Tower Account Factory' product.
    """

    response = sc_client.search_products(
        Filters={"FullTextSearch": ["AWS Control Tower Account Factory"]}
    )
    product_id = response["ProductViewSummaries"][0]["ProductId"]
    ic(product_id)
    return product_id


def get_product_version(product_id):
    """
    Retrieve the provisioning artifact ID for a given product.
    Args:
        product_id (str): The ID of the product for which to retrieve the provisioning artifact ID.
    Returns:
        str: The ID of the first provisioning artifact associated with the specified product.
    Raises:
        botocore.exceptions.ClientError: If there is an error in the AWS Service Catalog client request.
    """

    response = sc_client.list_provisioning_artifacts(ProductId=product_id)
    product_artifact_id = response["ProvisioningArtifactDetails"][0]["Id"]
    ic(product_artifact_id)
    return product_artifact_id


def provision_account(product_id, product_artifact_id, provisioning_parameters):
    """
    Provisions a new account using the specified product and provisioning parameters.
    Args:
        product_id (str): The unique identifier of the product to provision.
        product_artifact_id (str): The unique identifier of the product artifact.
        provisioning_parameters (list): A list of dictionaries containing the provisioning parameters.
    Returns:
        str: The unique identifier of the provisioned product.
    """

    response = sc_client.provision_product(
        ProductId=product_id,
        ProvisioningArtifactId=product_artifact_id,  # You need to get this ID from the product
        ProvisionedProductName=slugify(provisioning_parameters[1].get("Value")),
        ProvisioningParameters=provisioning_parameters,
    )

    provisioned_product_id = response["RecordDetail"]["ProvisionedProductId"]
    return provisioned_product_id


if __name__ == "__main__":
    product_id = get_product_id()
    product_artifact_id = get_product_version(product_id)
    provisioning_parameters = get_provisioned_params("940482448078")
    provisioned_product_id = provision_account(
        product_id, product_artifact_id, provisioning_parameters
    )
    while True:
        status = sc_client.describe_provisioned_product(Id=provisioned_product_id)
        current_status = status["ProvisionedProductDetail"]["Status"]
        ic(current_status)
        if current_status in ["AVAILABLE", "ERROR", "TAINTED"]:
            break
        time.sleep(30)
