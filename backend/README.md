## Job Extraction and Cold Email Automation

## Overview

This project automates the extraction of job postings from a website's careers page and generates cold emails to potential clients. It leverages the power of a language model to perform these tasks efficiently, making it easier to handle large volumes of data and generate personalized emails.

## Features

- **Job Extraction**: Extracts job postings from scraped text, focusing on fields like role, experience, skills, and job description.
- **Cold Email Generation**: Automatically writes personalized cold emails to potential clients based on the extracted job information and company portfolio links.

## Technologies Used

- **Python**: The core language used for scripting and automation.
- **LangChain**: Utilized for creating prompt templates and processing the language model's responses.
- **ChatGroq**: A language model service used to interpret and generate natural language text.
- **dotenv**: For managing environment variables, particularly API keys.
- **OS Module**: To interact with the operating system and retrieve environment variables.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/SURESHBEEKHANI/Job-Extraction-and-Cold-Email-Automation.git
    cd Job-Extraction-and-Cold-Email-Automation
    ```

2. **Install Dependencies**:
    Ensure you have Python installed. Then, install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add your `GROQ_API_KEY`:
    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

## Usage

1. **Job Extraction**:
    - The `extract_jobs` method takes in cleaned text from a website's careers page and extracts the job postings in JSON format.
    - Example:
      ```python
      from your_module import Chain

      chain = Chain()
      jobs = chain.extract_jobs(cleaned_text="Your cleaned text here")
      print(jobs)
      ```

2. **Cold Email Generation**:
    - The `write_mail` method generates a cold email based on a job description and a list of portfolio links.
    - Example:
      ```python
      from your_module import Chain

      chain = Chain()
      email_content = chain.write_mail(job=jobs[0], links=["link1", "link2"])
      print(email_content)
      ```

3. **Running the Script**:
    - To test if your environment is set up correctly, run the script:
      ```bash
      python your_script.py
      ```
    - This will print the `GROQ_API_KEY` value to ensure it's correctly loaded.

## Customization

- **Prompt Templates**: Modify the `PromptTemplate` definitions in the `extract_jobs` and `write_mail` methods to adjust the language model's behavior according to your needs.
- **Model Configuration**: Change the `model_name` and `temperature` settings when initializing `ChatGroq` to customize the model's output style and behavior.

## Error Handling

- The `extract_jobs` method includes error handling to catch parsing errors due to large context sizes. An `OutputParserException` is raised if the model's response cannot be parsed into valid JSON.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides an overview of the project's purpose, setup instructions, and usage examples. For further information or support, please contact the project maintainer.
