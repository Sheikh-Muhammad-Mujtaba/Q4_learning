# Crypto Data Assistant
A Streamlit application powered by a Gemini Flash agent to provide real-time cryptocurrency prices and trending coin information.

## Overview
This application serves as a simple yet effective cryptocurrency assistant. Users can inquire about the current price of specific cryptocurrencies or ask for a list of top trending coins. The backend utilizes the Gemini 2.0 Flash model via OpenRouter, with custom tools implemented to fetch data from the CoinLore API.

## Features
**Get Crypto Price:** Retrieve the current price, 24-hour change, and market cap for a specified cryptocurrency.
**Get Trending Coins:** Fetch a list of top 30 trending cryptocurrencies based on their 24-hour percentage change.
**AI-Powered Responses:** Leverages the Gemini 2.0 Flash model to understand user queries and utilize the appropriate tools.
**Streamlit UI:** Interactive and user-friendly web interface.

## How it Works
The application uses an AI agent built with the agents library. This agent is configured with:

**gemini-2.0-flash model:** For its conversational abilities and function calling.
**get_crypto_price tool**: Queries the CoinLore API for a specific coin's data.
**get_crypto_info tool:** Queries the CoinLore API for a list of all coins and then sorts them to identify trending ones.
When a user enters a query, the agent determines which tool (if any) is needed, executes it, and then uses the tool's output to formulate a concise and accurate response.

