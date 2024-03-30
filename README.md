# Static Magic

Static Magic is a simple static site generator that allows you to quickly convert Markdown files into HTML pages. It is designed to be easy to use and customizable.

## Usage

Follow these steps to use Static Magic:

1. **Clone the Repository**: Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/re-nanashi/static-magic.git
   ```
2. **Create Markdown Files**: Create your Markdown files and put them inside the `content` folder within the cloned repository. These Markdown files will be converted into HTML pages.

3. **Set Permissions**: Make the `main.sh` script executable by running the following command:

   ```bash
   chmod +x main.sh
   ```

4. **Run the Server**: Execute the `main.sh` script to generate the HTML pages from the Markdown files and run the server:
   ```bash
   ./main.sh
   ```

That's it! Your HTML pages will be generated and stored in the `public` folder within the repository.

## Dependencies

- Python 3.x
- Markdown library (install using `pip install markdown`)

## Customization

Static Magic can be easily customized to fit your needs. You can modify the templates, styles, and settings according to your preferences. Feel free to explore the code and make changes as necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
