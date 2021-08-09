# Code Coverage
#### *official documentation: https://coverage.readthedocs.io* 
---

**Code coverage** is a way to determine the number of lines of code that is
successfully validated under a test procedure.
In different words, it is used to find dead code (unused) and it's a good idea
to find code that can no longer be executed and remove it.
Removing the dead code increases the source code's readability.

## Quick start

1. To run the coverage test use:
`pipenv run coverage run -m pytest`
This will execute the test suit and analyze the code coverage.

2. In Order to see the results enter:
`pipenv run coverage report`

preview of result:

![coverage_report](https://user-images.githubusercontent.com/40122521/128600397-d2be1f4f-b10a-460d-9ca6-7f80859a0e34.png)

3. A more visual and interactive report enter:
`pipenv run coverage html`
in order to see this visual report you can open it in VScode
and open htmlcov/index.html with  something called Live Server.

preview:
![coverate_htm_report](https://user-images.githubusercontent.com/40122521/128600460-a111d5f9-f6a2-4377-8281-29bea0e7b41f.png)