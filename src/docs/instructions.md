# Steps
1. Install "python 3X";
2. Add path to "\ python3X \", "\ python3X \ Scripts \" into the environment variable: "Path";
3. Using "pip" in the command console, install packages and libraries from the file: "packages.txt":
    ```
    cd "path to packages.txt"
    python -m pip install -r packages.txt
    ```
4. Download the test project from the git-repository;
5. Open the project in "PyCharm";
6. Create "Run \ Debug Configuration":
    - Add "Python tests" -> "pytest";
	- Determine the "Script path" to the test case file: "test_twitter.py";
	- Add "--alluredir ./results" to "Additional Arguments";
	- Project supports additional arguments: 
        ```
        --bearer_token valid_token
        ```
7. Start the test;
8. An JSON files will be created in the "results" folder;

## Optional
9. Setup the allure server: https://docs.qameta.io/allure/#_windows
10. Build a report by command: 
    ```
    allure serve "path_to\results"
    ```
