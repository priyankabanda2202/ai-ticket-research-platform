# AI Ticker Research Platform

Multi-Agent AI stock research platform built using LangGraph.

## Features

- Market Data Agent
- Sentiment Analysis Agent
- Decision Agent
- PDF Report Generator
- Telegram Bot Integration
- FastAPI Backend

## Tech Stack

- Python
- LangGraph
- FastAPI
- Telegram Bot API
- Yahoo Finance
- ReportLab

## Architecture
![Uploading image.png…]()


User → Telegram/Web UI → FastAPI → LangGraph Agents → Research Report

## Setup

pip install -r requirements.txt

python run_bot.py

## Demo

Send a stock ticker:

AAPL

and receive:

Recommendation
Confidence Score
AI-generated rationale
PDF Report
