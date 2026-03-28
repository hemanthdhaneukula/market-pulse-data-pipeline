A robust data engineering project that fetches live Bitcoin price data, performs moving average calculations, and persists time-series data to a cloud-hosted Supabase (PostgreSQL) instance.

Key Features:

Automated Ingestion: Fetches real-time price data using the CoinGecko REST API.

Streamlit Dashboard: Visualizes market trends and moving average crossovers.

Cloud Persistence: Securely stores historical data in Supabase with optimized schema indexing.

Security: Implements environment variable isolation via .env to protect API credentials.
