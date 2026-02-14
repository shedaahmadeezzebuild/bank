#!/usr/bin/env python3
"""Test script to verify the banking bot works correctly."""

from banking_bot import BankingBot

# Initialize the bot
api_key = "hKjvYtwfSKR7Ysd7WKvmItCtPL6YfjdR"
csv_path = "hbdb_banking_faqs (2) (1).csv"

print("Initializing Banking Bot...")
bot = BankingBot(api_key=api_key, csv_path=csv_path)

print("\nTesting bot with sample question...")
print("=" * 50)
print("Question: How do I open a savings account?")
print("=" * 50)

print("\nAnswer:")
for chunk in bot.get_response("How do I open a savings account?"):
    print(chunk, end="", flush=True)

print("\n" + "=" * 50)
print("Bot test completed successfully!")
