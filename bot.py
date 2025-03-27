from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb, WebAppInfo
import pymongo
from pyrogram.enums import ChatMemberStatus

from datetime import datetime
import asyncio

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

# Stickers for bot responses
STICKERS = {
    'welcome': 'CAACAgQAAxkBAAEWpZpn5Ga_FS36Uc8kSiuAc_6LmQGDugACqgsAAsDqEFDQ3jt1DpvhoDYE',
    'processing': 'CAACAgUAAxkBAAEV_8RnkPiFEzAKWVUgzWeNcLTOWjsBkAACpwgAAtu6GFQ4oUoIL-_BgzYE'
}

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

# Validate configuration before starting
if not validate_config():
    import sys
    sys.exit(1)

# Initialize the bot
bot = Client(
    "terabox_bottt",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Configuration
admin_id = ADMIN_IDS
default_channel_id = DEFAULT_CHANNEL_ID
logs_channel_id = LOGS_CHANNEL_ID

# Global variables
under_maintainance = False
broadcast_on = False
current_channel_id = default_channel_id

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)
db = client['terabox_aditya_singh']
users_collection = db['users']
channels_collection = db['channels']  # New collection for channel management

# Initialize channel in MongoDB
async def init_channel():
    """Initialize or get current channel from MongoDB"""
    try:
        global current_channel_id
        channel_doc = channels_collection.find_one({"type": "force_sub"})
        
        if not channel_doc:
            # Initialize with default channel
            channels_collection.insert_one({
                "type": "force_sub",
                "channel_id": default_channel_id,
                "is_default": True,
                "last_updated": datetime.now()
            })
            current_channel_id = default_channel_id
        else:
            current_channel_id = channel_doc["channel_id"]
            
        # Verify channel is accessible
        try:
            await bot.get_chat(current_channel_id)
        except Exception:
            # If channel is not accessible, revert to default
            current_channel_id = default_channel_id
            channels_collection.update_one(
                {"type": "force_sub"},
                {
                    "$set": {
                        "channel_id": default_channel_id,
                        "is_default": True,
                        "last_updated": datetime.now()
                    }
                },
                upsert=True
            )
    except Exception as e:
        print(f"Error in init_channel: {e}")
        current_channel_id = default_channel_id

# Check if user has joined the required channel
def check_joined():
    async def func(flt, bot, message):
        try:
            user_id = message.from_user.id
            
            # Skip check for admin
            if user_id in admin_id:
                return True
            
            # Get current channel from MongoDB
            channel_doc = channels_collection.find_one({"type": "force_sub"})
            if channel_doc:
                global current_channel_id
                current_channel_id = channel_doc["channel_id"]
            
            # Check membership
            try:
                member = await bot.get_chat_member(current_channel_id, user_id)
                if member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                    return True
            except Exception as e:
                print(f"Error checking membership: {e}")
                # If there's an error checking membership, send force sub message
                try:
                    # Get channel info and invite link
                    channel = await bot.get_chat(current_channel_id)
                    invite_link = f"https://t.me/{channel.username}" if channel.username else channel.invite_link
                    
                    # Create buttons for force sub message
                    force_sub_buttons = ikm([
                        [ikb("🔔 Join Channel 🔔", url=invite_link)],
                        [ikb("✅ Check Subscription", callback_data="check_sub")]
                    ])
                    
                    # Send force sub message
                    await message.reply_text(
                        "**❗️ Access Restricted ❗️**\n\n"
                        f"**Join {channel.title} To Use This Bot**\n\n"
                        "**👉 Ye Channel Join Kar Lo ✅**",
                        reply_markup=force_sub_buttons
                    )
                except Exception as e:
                    print(f"Error sending force sub message: {e}")
                return False

            # If user is not a member, send force sub message
            channel = await bot.get_chat(current_channel_id)
            invite_link = f"https://t.me/{channel.username}" if channel.username else channel.invite_link
            
            force_sub_buttons = ikm([
                [ikb("🔔 Join Channel 🔔", url=invite_link)],
                [ikb("✅ Check Subscription", callback_data="check_sub")]
            ])
            
            await message.reply_text(
                "**❗️ Access Restricted ❗️**\n\n"
                f"**Join {channel.title} To Use This Bot**\n\n"
                "**👉 Ye Channel Join Kar Lo ✅**",
                reply_markup=force_sub_buttons
            )
            return False
            
        except Exception as e:
            print(f"Error in check_joined: {e}")
            # In case of any error, revert to default channel
            current_channel_id = default_channel_id
            channels_collection.update_one(
                {"type": "force_sub"},
                {
                    "$set": {
                        "channel_id": default_channel_id,
                        "is_default": True,
                        "last_updated": datetime.now()
                    }
                },
                upsert=True
            )
            return True

    return filters.create(func)

# URL Processing Functions
def process_terabox_url(url):
    """Process TeraBox URL and extract ID"""
    try:
        if '/s/' in url:
            # For URLs with /s/ pattern
            surl = url.split('/s/')[1].split('?')[0].split('#')[0]
        elif 'surl=' in url:
            # For URLs with surl parameter
            surl = url.split('surl=')[1].split('&')[0].split('?')[0].split('#')[0]
        elif 'id=' in url:
            # For URLs with id parameter
            surl = url.split('id=')[1].split('&')[0].split('?')[0].split('#')[0]
        else:
            # Get the last part of the URL
            surl = url.split('/')[-1].split('?')[0].split('#')[0]
        
        return surl
    except Exception as e:
        print(f"Error processing URL: {e}")
        return None

def create_streaming_url(surl):
    """Create streaming URL from TeraBox ID"""
    return f"https://muddy-flower-20ec.arjunavai273.workers.dev/?id={surl}"

# Database Functions
def store_user_info(user_id, username, first_name):
    """Store user information in the database"""
    if not users_collection.find_one({"user_id": user_id}):
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name
        }
        users_collection.insert_one(user_data)

async def fetch_all_users():
    """Fetch all user IDs from the database"""
    users = users_collection.find()
    return [user['user_id'] for user in users]

def update_force_sub_channel(channel_id, channel_title, channel_username=None, invite_link=None):
    """Update force subscription channel in database"""
    channels_collection.update_one(
        {"type": "force_sub"},
        {
            "$set": {
                "channel_id": channel_id,
                "is_default": False,
                "last_updated": datetime.now(),
                "channel_title": channel_title,
                "channel_username": channel_username,
                "is_private": not bool(channel_username),
                "invite_link": invite_link
            }
        },
        upsert=True
    )

def get_force_sub_channel():
    """Get current force subscription channel"""
    return channels_collection.find_one({"type": "force_sub"})

# Users command handler (admin only)
@bot.on_message(filters.command("users"))
async def users(client, message):
    """Show total user count (admin only)"""
    if message.from_user.id in admin_id:
        users = await fetch_all_users()
        await message.reply_text(f"<b><i>Total users: {len(users)}</i></b>")
    else:
        await message.reply_text("You are not authorized to use this command.")

# Broadcast command handler (admin only)
@bot.on_message(filters.command("broadcast"))
async def broadcast(client, message):
    """Broadcast a message to all users (admin only)"""
    global broadcast_on
    if message.from_user.id in admin_id:
        if message.reply_to_message:
            br = await message.reply_text("**🔄 Broadcasting...**")
            broadcast_on = True
            users = await fetch_all_users()
            broadcast_count = 0
            errors_count = 0
            
            # Get the replied message
            reply_msg = message.reply_to_message
            
            for user_id in users:
                try:
                    # Forward the exact message with all media and formatting
                    await reply_msg.copy(
                        chat_id=user_id,
                        caption=reply_msg.caption if reply_msg.caption else None,
                        caption_entities=reply_msg.caption_entities if reply_msg.caption_entities else None
                    )
                    broadcast_count += 1
                    # Add a small delay to prevent flooding
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"Error broadcasting to user {user_id}: {e}")
                    errors_count += 1
            
            # Calculate success rate
            total = broadcast_count + errors_count
            success_rate = (broadcast_count / total) * 100 if total > 0 else 0
            
            await br.edit_text(
                f"**📊 Broadcast Summary**\n\n"
                f"✅ Successfully sent: `{broadcast_count}`\n"
                f"❌ Failed: `{errors_count}`\n"
                f"📈 Success rate: `{success_rate:.1f}%`\n\n"
                f"Total users: `{total}`"
            )
            broadcast_on = False
        else:
            await message.reply_text(
                "**ℹ️ How to Broadcast:**\n\n"
                "1. Send or forward the content you want to broadcast\n"
                "2. Reply to that message with `/broadcast`\n\n"
                "**📝 Supported content:**\n"
                "• Text messages (with formatting)\n"
                "• Images (with captions)\n"
                "• Videos\n"
                "• Audio files\n"
                "• Voice messages\n"
                "• Stickers\n"
                "• Documents\n"
                "• And more!"
            )
    else:
        await message.reply_text("**⚠️ Only Admins can use this command!**")

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    """Handle the /start command"""
    try:
        # Initialize channel data
        await init_channel()
        
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        
        # Store user info
        store_user_info(user_id, username, first_name)
        
        # Send welcome sticker
        await message.reply_sticker(STICKERS['welcome'])
        
        # Get channel info
        channel = await client.get_chat(current_channel_id)
        
        # Create channel button
        channel_button = ikm([
            [ikb("📢 Join Our Channel", url="https://t.me/+kkUnhFtiQpA5ZGFl")]
        ])
        
        # Welcome message
        welcome_text = (
            f"**👋 Welcome {first_name}!**\n\n"
            f"🔗 Send any TeraBox link to get instant streaming access.\n\n"
            f"📢 Join our channel for updates."
        )
        
        await message.reply_text(
            welcome_text,
            reply_markup=channel_button
        )
        
        # Log new user to admin channel
        try:
            log_text = (
                f"**📱 New User Started Bot!\n\n"
                f"• Name: {first_name}\n"
                f"• ID: `{user_id}`\n"
                f"• Username: @{username if username else 'None'}\n"
                f"• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"• Status: ✅ Active**"
            )
            
            await client.send_message(
                logs_channel_id,
                log_text
            )
        except Exception as e:
            print(f"Error logging new user: {e}")
            
    except Exception as e:
        print(f"Error in start command: {e}")
        error_text = (
            "**⚠️ An error occurred while starting the bot.\n\n"
            "Please try:\n"
            "1. Restart the bot with /start\n"
            "2. Check if bot is working\n"
            "3. Contact support if issue persists**"
        )
        await message.reply_text(error_text)

# Stop/activate command handler (admin only)
@bot.on_message(filters.command('stop') | filters.command('activate'))
async def maintenance_toggle(client, message):
    """Toggle maintenance mode (admin only)"""
    if message.from_user.id in admin_id:
        global under_maintainance
        if message.text == '/stop':
            under_maintainance = True
            await message.reply_text('Bot Set to Maintenance Mode...')
        elif message.text == '/activate':
            under_maintainance = False
            await message.reply_text('Bot Set to Active Mode...')
    else:
        await message.reply_text('Only Admins can use this command...')

@bot.on_message(filters.command("add") & filters.user(admin_id))
async def add_channel(client, message):
    """Add force subscription channel"""
    try:
        # Check command format
        args = message.text.split()
        if len(args) != 2:
            await message.reply_text(
                "**Usage:**\n"
                "• For public channels: `/add @username` or `/add https://t.me/username`\n"
                "• For private channels: `/add -100xxxxxxxxxxxx` (channel ID)"
            )
            return

        channel_input = args[1].strip()  # Remove any whitespace
        
        try:
            # Try to get chat info based on input type
            if channel_input.startswith('-'):  # Private channel ID
                try:
                    # Remove any spaces and convert to integer
                    channel_id = int(channel_input.replace(" ", ""))
                    chat = await client.get_chat(channel_id)
                except (ValueError, Exception) as e:
                    print(f"Channel ID error: {e}")
                    await message.reply_text(
                        "**❌ Invalid channel ID!\n\n"
                        "Make sure:\n"
                        "1. Channel ID starts with -100\n"
                        "2. Channel ID is a valid number\n"
                        "3. Bot has access to the channel**"
                    )
                    return
            elif channel_input.startswith('https://t.me/'):  # Public channel link
                username = channel_input.replace('https://t.me/', '@')
                chat = await client.get_chat(username)
            else:  # Username (add @ if missing)
                if not channel_input.startswith('@'):
                    channel_input = '@' + channel_input
                chat = await client.get_chat(channel_input)
            
            # Check if bot is admin
            try:
                bot_member = await client.get_chat_member(chat.id, (await client.get_me()).id)
                if not bot_member.status == ChatMemberStatus.ADMINISTRATOR:
                    await message.reply_text(
                        "**❌ Bot is not admin in channel!\n\n"
                        "1. Add bot as admin in channel\n"
                        "2. Give these permissions:\n"
                        "   • Ban Users\n"
                        "   • Invite Users via Link\n"
                        "3. Try again after making bot admin**"
                    )
                    return
                
                # For private channels, try to create an invite link to verify permissions
                if not chat.username:
                    try:
                        test_invite = await client.export_chat_invite_link(chat.id)
                        if not test_invite:
                            await message.reply_text(
                                "**❌ Bot needs 'Invite Users via Link' permission!\n\n"
                                "This is required for private channels.**"
                            )
                            return
                    except Exception as e:
                        print(f"Invite link test error: {e}")
                        await message.reply_text(
                            "**❌ Bot needs 'Invite Users via Link' permission!\n\n"
                            "This is required for private channels.**"
                        )
                        return
                    
            except Exception as e:
                print(f"Admin check error: {e}")
                await message.reply_text(
                    "**❌ Bot is not admin in channel!\n\n"
                    "1. Add bot as admin first\n"
                    "2. Make sure bot has access to the channel\n"
                    "3. Try again after making bot admin**"
                )
                return

            # Update channel ID in both global variable and MongoDB
            global current_channel_id
            current_channel_id = chat.id
            
            # Get invite link for private channels
            invite_link = None
            if not chat.username:  # Private channel
                try:
                    invite_link = await client.export_chat_invite_link(chat.id)
                except Exception as e:
                    print(f"Error creating invite link: {e}")
                    await message.reply_text(
                        "**❌ Failed to create invite link!\n\n"
                        "Make sure bot has 'Invite Users via Link' permission.**"
                    )
                    return
            
            # Update MongoDB with new channel
            update_force_sub_channel(chat.id, chat.title, chat.username, invite_link)
            
            # Success message
            success_text = f"**✅ Force subscription updated successfully!\n\n📢 Channel: {chat.title}\n"
            if chat.username:
                success_text += f"👤 Username: @{chat.username}"
            else:
                success_text += f"🔒 Type: Private Channel\n💡 Channel ID: `{chat.id}`"
            
            await message.reply_text(success_text)
            
            # Log channel change to admin log channel
            try:
                log_text = (
                    f"**📢 Force Sub Channel Changed!\n\n"
                    f"• Title: {chat.title}\n"
                    f"• ID: `{chat.id}`\n"
                    f"• Type: {'Private' if not chat.username else 'Public'}\n"
                    f"• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"• Changed By: {message.from_user.first_name}**"
                )
                await client.send_message(logs_channel_id, log_text)
            except Exception as e:
                print(f"Error logging channel change: {e}")
            
        except Exception as e:
            print(f"Error adding channel: {e}")
            await message.reply_text(
                "**❌ Failed to add channel!\n\n"
                "Make sure:\n"
                "1. Channel ID/username/link is correct\n"
                "2. Bot is admin in the channel\n"
                "3. For private channels:\n"
                "   • Channel ID must start with -100\n"
                "   • Bot must have admin access\n"
                "   • Bot must have 'Invite Users via Link' permission**"
            )
            
    except Exception as e:
        print(f"Error in add command: {e}")
        await message.reply_text("**❌ Failed to process command**")

# Revert command handler (admin only)
@bot.on_message(filters.command("revert") & filters.user(admin_id))
async def revert_channel(client, message):
    """Revert to default force subscription channel"""
    try:
        global current_channel_id
        current_channel_id = default_channel_id
        
        # Update MongoDB to revert to default channel
        update_force_sub_channel(default_channel_id, "Default Channel", None, None)
        
        # Get channel info
        chat = await client.get_chat(default_channel_id)
        await message.reply_text(f"**✅ Reverted to default channel:\n📢 {chat.title}**")
        
    except Exception as e:
        await message.reply_text("**❌ Error reverting channel**")

@bot.on_message(filters.command("help") & filters.user(admin_id))
async def help_command(client, message):
    """Display admin help menu with all commands and examples"""
    help_text = """
**🔰 Admin Commands Help**

Here's a detailed guide of all admin commands:

**📊 User Management**
• `/users` - Get total user count
  Example: `/users`
  
**📢 Channel Management**
• `/add` - Add force subscription channel
  Examples: 
  ├ Public: `/add @channel_name`
  ├ Public URL: `/add https://t.me/channel_name`
  └ Private: `/add -100xxxxxxxxxxxx`

• `/revert` - Revert to default channel
  Example: `/revert`

**📡 Broadcast**
• `/broadcast` - Send message to all users
  Usage: Reply to any content with `/broadcast`
  Supports:
  ├ Text (formatted)
  ├ Images (with caption)
  ├ Videos
  ├ Audio files
  ├ Voice messages
  ├ Stickers
  └ Documents

**🛠️ Maintenance**
• `/stop` - Set bot to maintenance mode
  Example: `/stop`

• `/activate` - Resume bot service
  Example: `/activate`

**ℹ️ Help**
• `/help` - Show this help message
  Example: `/help`

**📝 Notes:**
• All commands are admin-only
• For private channels, bot needs:
  ├ Admin access
  └ "Invite Users via Link" permission
• Broadcast supports all media types
• Force subscription is automatic

**🔗 Quick Tips:**
• Test new channels before adding
• Monitor broadcast progress
• Keep invite permissions enabled

**⚠️ Troubleshooting:**
• If broadcast fails, check user blocks
• For private channels, verify bot permissions
• Keep bot as admin in all channels
"""
    
    # Send help message with a professional layout
    await message.reply_text(
        help_text,
        disable_web_page_preview=True
    )

# Main message handler
@bot.on_message(filters.text & filters.private & check_joined())
async def process_link(bot, message):
    """Process user messages containing links"""
    # Check if bot is in maintenance mode
    if under_maintainance:
        await message.reply_text("<b><i>Bot is under maintenance. Please try again later.</i></b>")
        return
    
    # Get user information
    user_id = message.from_user.id
    sticker = STICKERS['processing']
    w1 = await message.reply_sticker(sticker)
    username = message.from_user.username
    first_name = message.from_user.first_name
    store_user_info(user_id, username, first_name)
    
    # Get the message text and remove @ if present
    msg = message.text.replace("@", "")
    print(f"Received message from {user_id}: {msg}")
    
    # Process the link if it's a URL
    if msg.startswith('https://'):
        try:
            # Extract ID from URL - try different patterns
            surl = process_terabox_url(msg)
            
            if surl:
                # Create the streaming URL
                streaming_url = create_streaming_url(surl)
                
                print(f"Processing URL: {msg}")
                print(f"Extracted ID: {surl}")
                print(f"Streaming URL: {streaming_url}")
                
                # Create Mini App button
                keyboard = ikm([
                    [ikb(
                        text="🎬 Open Streaming Player",
                        web_app=WebAppInfo(url=streaming_url)
                    )]
                ])
                
                await w1.delete()
                await message.reply_text(
                    "**🎯 Link Processed Successfully!\n"
                    "🎬 Click Below to Start Streaming ⬇️**",
                    reply_markup=keyboard,
                    reply_to_message_id=message.id
                )
                
                # Log to admin channel
                try:
                    await bot.send_message(logs_channel_id, 
                        f"**👤 User: {message.from_user.first_name}\n"
                        f"🔗 Accessed: `{surl}`**"
                    )
                except Exception:
                    pass
            else:
                await w1.delete()
                await message.reply_text('**❌ Invalid Link!\n📝 Please send a valid TeraBox link**')
        except Exception as e:
            print(f"Error processing link: {e}")
            await w1.delete()
            await message.reply_text('**❌ Invalid Link!\n📝 Please send a valid TeraBox link**')
    else:
        await w1.delete()
        await message.reply_text('**❌ Invalid Format!\n📎 Link must start with https://**')

# Callback query handler for check subscription
@bot.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    try:
        user_id = callback_query.from_user.id
        
        # Check if user has joined the channel
        try:
            member = await client.get_chat_member(current_channel_id, user_id)
            if member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                # Delete the force sub message
                await callback_query.message.delete()
                # Send welcome message
                await start(client, callback_query.message)
                await callback_query.answer("✅ Welcome to the bot!", show_alert=True)
                return
        except Exception as e:
            print(f"Error checking subscription: {e}")
        
        # If user hasn't joined, show alert
        await callback_query.answer("❌ Please join the channel first!", show_alert=True)
        
    except Exception as e:
        print(f"Error in check_subscription: {e}")
        await callback_query.answer("❌ An error occurred. Please try again.", show_alert=True)

# Run the bot
if __name__ == "__main__":
    print("Starting TeraBox Link Processor Bot...")
    bot.run()

