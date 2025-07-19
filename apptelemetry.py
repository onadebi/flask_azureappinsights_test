import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Reduce telemetry batching frequency to minimize background logging
os.environ["OTEL_BSP_SCHEDULE_DELAY"] = "30000"  # 30 seconds instead of default 5 seconds
os.environ["OTEL_BSP_MAX_QUEUE_SIZE"] = "512"    # Smaller queue size
os.environ["OTEL_BSP_EXPORT_BATCH_SIZE"] = "128"  # Smaller batch size

# os.environ["OTEL_SERVICE_NAME"] = "onaxtelemetry"
# os.environ["OTEL_TRACES_SAMPLER_ARG"] = "0.1"  # Set a low sampling rate for testing

# Configure basic logging format for fallback
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Suppress verbose Azure SDK logging
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("azure.monitor").setLevel(logging.WARNING)
logging.getLogger("azure.core").setLevel(logging.WARNING)
logging.getLogger("opentelemetry").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.ERROR)  # Suppress Flask's request logs

try:
    from azure.monitor.opentelemetry import configure_azure_monitor
    
    # Check if the connection string is available
    connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not connection_string or connection_string.strip() == "":
        raise ValueError("APPLICATIONINSIGHTS_CONNECTION_STRING not found in environment variables or is empty. Check your .env file.")
    
    # Configure Azure Monitor with environment variable
    configure_azure_monitor(connection_string=connection_string)
    print("✅ Azure Monitor configured successfully")
    print(f"📡 Using connection string from .env file")
    
except ValueError as ve:
    print(f"❌ Configuration Error: {ve}")
    print("📝 Continuing with basic logging...")
except Exception as e:
    print(f"⚠️  Failed to configure Azure Monitor: {e}")
    print("📝 Continuing with basic logging...")


def get_logger(name=None):
    """
    Get a logger that's configured with Azure Monitor telemetry
    
    Args:
        name (str, optional): Logger name. If None, uses current module name.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if name is None:
        name = __name__
    return logging.getLogger(name)