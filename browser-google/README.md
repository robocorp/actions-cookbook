# Use Playwright for automating browser - Google Search

Yes we know there are easier ways to search Google than Playwright browser automation. 💁‍♂️ But this one is for the demonstration purposes!

The example shows how to open a browser (headless or not) and perform actions against a website. Make your AI app go to pages that it has never had access to before.

The example navigates to Google search, and then performs a search to find books on a given term, reads the results and returns them as text. Here's some of the fancy parts:

```py
from robocorp import browser
```

The browser automation is done with Robocorp Playwright library, making life easier for the developers than just the plain Playwright.

```py
browser.configure(browser_engine="chromium", headless=False)
```

Edit the boolean value for `headless` to either see, or unsee, the browser.

```py
return json.dumps(items[:count])
```

Your `@action` can only return text or boolean values for now (more type support coming soon), so remember to dump your dict to text when returning.

📹 Video coming soon!