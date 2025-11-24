# sieberr pop quiz

This is essentially a scripting challenge.

The google form uses client side validation. This includes:
- Needing to contain a certain text
- Needing to match a certain regex expression
- Needing to be equal to / greater than / less than a certain number, or be between 2 numbers
- Needing a min length of text

Provided is a tampermonkey script to autofill the google form. Press the escape key to trigger the script to run on the google form page.

> [!NOTE]
> You may obtain "400 Bad Request". This seemingly occurs when your answer to a question is too long. Usually, re-running the script until the RNG for the regex provides a shorter response works.
