from pyrogram import Client
import asyncio

# Apni details yahan bharo
API_ID = 123456          # my.telegram.org se lo
API_HASH = "your_api_hash_here"   # my.telegram.org se lo
SESSION_NAME = "my_account"

# Group ka username ya ID
GROUP = "PBX_CHAT"  # e.g. "mygroupchat" ya -100xxxxxxxxxx

async def delete_my_messages():
    async with Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH) as app:
        me = await app.get_me()
        my_id = me.id
        
        deleted_count = 0
        msg_ids = []

        print(f"[*] Scanning messages in group: {GROUP}")
        
        async for message in app.get_chat_history(GROUP, limit=None):
            if message.from_user and message.from_user.id == my_id:
                msg_ids.append(message.id)
                
                # Batch mein delete karo (100 ek baar)
                if len(msg_ids) == 100:
                    await app.delete_messages(GROUP, msg_ids)
                    deleted_count += len(msg_ids)
                    print(f"[+] Deleted {deleted_count} messages so far...")
                    msg_ids = []
                    await asyncio.sleep(1)  # Rate limit se bachne ke liye
        
        # Baaki bache hue messages
        if msg_ids:
            await app.delete_messages(GROUP, msg_ids)
            deleted_count += len(msg_ids)
        
        print(f"\n✅ Done! Total deleted: {deleted_count} messages")

asyncio.run(delete_my_messages())
