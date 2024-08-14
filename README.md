# Static Site Generator

## Description
This project is a static site generator that converts Markdown files into HTML. It is a command-line tool that takes a directory of Markdown files and converts them into HTML files. The tool also supports custom templates, allowing users to customize the look and feel of their generated website.

## Features
- Converts Markdown files to HTML
- Supports custom templates
- Recursively processes files in .md format and generates the html files

## Usage
- Modify the template.html to fit you needs, {{ Title }} and {{ Content }} are the placeholders for the title and content of the markdown file
- Place all the .md files in the Content directory, the tool will recursively process all the files in the directory
- All new files will be placed in the Public directory
- All files in the static folder will be copied into the Public directory in case you need support files
- Run ./main.sh to generate the HTML files

## Installation
Not much installation needed. Just clone the repository and run the project.

## Run the project
./main.sh

## Run the tests
./test.sh

## Limitations
- The tool only supports Markdown files with the .md extension
- The tool does not support nested tags in Markdown files