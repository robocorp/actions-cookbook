from robocorp import browser
from robocorp.actions import action

from typing import Annotated
from pydantic import BaseModel, Field

class Prospect(BaseModel):
    first_name: Annotated[str, Field(description="User's first name")]
    last_name: Annotated[str, Field(description="User's last name")]
    company_name: Annotated[str, Field(description="Company name")]
    email: Annotated[str, Field(description="User's email address")]
    phone: Annotated[str, Field(description="User's phone number, use international format.")]
    

@action(is_consequential="False")
def fill_form_with_user_data(data: Prospect) -> str:
    """
    Fill in Robocorp Contact form with user details using a browser.
    
    Args:
        data: A person object that will be entered to the Robocorp Contact form.

    Returns:
        str: True if operation was success, and False if it failed, including an error message.

    """

    browser.configure(
        browser_engine="chromium",
        screenshot="only-on-failure",
        headless=False,
    )

    page = browser.goto("https://robocorp.com/contact-us-internal-test")
    page.locator("[name=firstname]").fill(data.first_name)
    page.locator("[name=lastname]").fill(data.last_name)
    page.locator("[name=email]").fill(data.email)
    page.locator("[name=company]").fill(data.company_name)
    page.locator("[name=phone]").fill(data.phone)
    page.locator("[name=how_can_our_team_help_you_]").select_option("Get a product demo")
    page.locator("xpath=//input[@value='Get in Touch']").click()

    try: 
        page.wait_for_selector('text="Thank you for contacting us. Our team will get back to you shortly."')
    except Exception as e:
        return f"False: {e}"
    finally:
        return "True"