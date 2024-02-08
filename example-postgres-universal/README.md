# PostgreSQL Universal Actions

## Overview
This example simplifies interactions with PostgreSQL databases by allowing users to perform queries through 
conversational inputs translated by Large Language Models (LLMs), like OpenAI's GPT.
It focuses on read-only operations to ensure security and prevent unintended data modifications.

## Key Features
- **Simplified Database Queries**: Execute SQL queries using conversational language without deep SQL knowledge.
- **Secure Read-Only Operations**: Ensures database integrity by restricting actions to read-only transactions.
- **Integration with LLMs**: Designed for seamless integration with LLMs, enabling a conversational interface for database management.

## Example Use Case: Querying Sales Data

### Scenario
Imagine you're a sales manager looking to quickly find out this month's top-performing products without writing complex SQL queries.

### How This Package Helps
Our actions allow you to simply ask, "What are the top-selling products this month?" and handle the rest, fetching and presenting the data in an understandable format.

### Process
1. **Initiate a Query**: Start by expressing your query through a conversational interface powered by OpenAI's GPT.
2. **Behind-the-Scenes Action**: The system translates your input into a SQL query and fetches the relevant data from your PostgreSQL database.
3. **Data Presentation**: You receive a concise response with the query results, allowing for quick insights without needing to interpret complex data or SQL results.

## Getting Started

### Prerequisites
- Access to a PostgreSQL database
- Access to OpenAI's GPT for conversational interfaces

### Installation
1. Clone this example from this repository to your local machine.

### Running the Server
Expose the action server to enable integration with external services:
```bash
action-server start --expose
```

## Usage

### Initialize Connection

To securely establish a connection to your PostgreSQL database, replace `username`, `password`, 
`host`, `port`, and `database` with your actual database details:

**dsn:** `postgresql://username:password@host:port/database`

To do this securely, go to your Action Server UI http://localhost:8080 and execute the `init_postgres_connection` there. Copy the output from the execution to copy later for LLM use.

**NOTE:** You can optionally also do this through LLM, but that will reveal the exact connection info to the LLM.

This action configures the connection and provides a schema overview for LLM to use.

### Execute Query
Use OpenAI's GPT to formulate and send your queries. The `execute_query` action will interpret these inputs and perform the necessary SQL queries in a read-only manner.

## Security and Read-Only Operations
This project prioritizes data integrity, exclusively allowing read-only access to prevent accidental modifications. Our secure approach ensures that your database remains intact while facilitating meaningful data analysis and interaction.

## Integrating with OpenAI's GPT
To use this project with OpenAI's GPT:

1. **Configure your Action Server**: Ensure your action server is running and exposed.
2. **Connect to OpenAI's GPT**: Use the public URL and API Authorization Bearer key from your action server to set up the connection in OpenAI's platform.
3. **Create Custom Conversations**: In the GPT editor, set up custom prompts that trigger the actions provided by this server, enabling a seamless conversational interface for database queries.

### Benefits
- **Accessibility**: Makes database interactions intuitive and accessible for everyone, regardless of their SQL proficiency.
- **Security**: Maintains data safety with strict read-only access.
- **Integration**: Offers straightforward integration with LLMs like OpenAI's GPT, enhancing the user experience through natural language processing.

By enabling direct, conversational access to PostgreSQL databases, this example democratizes data analysis, 
making it accessible and secure for a wide range of users.
