# Load environment variables from .env file

# Bot configuration
BOT_TOKEN = "7829127559:AAHcTGVvYRgMRXca3Uo6k3Ox-uMMDpdmgw0"
API_ID = 1712043
API_HASH = "965c994b615e2644670ea106fd31daaf"

# MongoDB configuration
MONGODB_URI = "mongodb+srv://smit:smit@cluster0.pjccvjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Admin configuration
ADMIN_IDS = [6121699672,5675220252,5545790759]
DEFAULT_CHANNEL_ID = -1002478587806  # Your permanent channel ID
LOGS_CHANNEL_ID = -1002532688002  # Channel for logging

# Validate required configuration
def validate_config():
    """Validate that all required configuration variables are set."""
    missing = []
    
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not MONGODB_URI:
        missing.append("MONGODB_URI")
    if not ADMIN_IDS:
        missing.append("ADMIN_IDS")
    if not DEFAULT_CHANNEL_ID:
        missing.append("DEFAULT_CHANNEL_ID")
    if not LOGS_CHANNEL_ID:
        missing.append("LOGS_CHANNEL_ID")
    
    if missing:
        print(f"Error: Missing required configuration: {', '.join(missing)}")
        print("Please check your configuration")
        return False
    
    return True 
