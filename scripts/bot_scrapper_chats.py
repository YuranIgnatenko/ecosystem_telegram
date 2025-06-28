from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import Channel, Chat
import asyncio
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Telegram API credentials
API_ID = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']
PHONE = config['Telegram']['phone']

async def get_chat_info(client, chat):
	"""Get detailed information about a chat/channel"""
	try:
		if isinstance(chat, Channel):
			full_chat = await client(GetFullChannelRequest(chat))
			chat_info = full_chat.chats[0]
			full_info = full_chat.full_chat
		else:
			full_chat = await client(GetFullChatRequest(chat.id))
			chat_info = full_chat.chats[0]
			full_info = full_chat.full_chat

		# Get creator/admin information
		creator = None
		admins = []
		
		if hasattr(full_info, 'participants'):
			for participant in full_info.participants.participants:
				if participant.is_creator:
					creator = participant
				elif participant.is_admin:
					admins.append(participant)

		return {
			'id': chat_info.id,
			'title': chat_info.title,
			'username': getattr(chat_info, 'username', None),
			'type': 'Channel' if isinstance(chat, Channel) else 'Group',
			'creator': creator,
			'admins': admins,
			'members_count': getattr(full_info, 'participants_count', 0),
			'description': getattr(full_info, 'about', None)
		}
	except Exception as e:
		print(f"Error getting info for chat {chat.title}: {str(e)}")
		return None

async def main():
	# Create the client
	print("Creating client")

	if not os.path.exists("outputs_parsing_chats.txt"):
		open("outputs_parsing_chats.txt", "w", encoding="utf-8").close()

	client = TelegramClient('scrapper_session.session', API_ID, API_HASH)
	
	try:
		# Connect to Telegram
		await client.connect()
		
		if not await client.is_user_authorized():
			await client.send_code_request(PHONE)
			try:
				await client.sign_in(PHONE, input('Enter the code: '))
			except Exception as e:
				if "password" in str(e).lower():
					# If 2FA is enabled, ask for the password
					await client.sign_in(password=input('Please enter your 2FA password: '))
				else:
					raise e

		# Get all dialogs (chats, channels, groups)
		dialogs_count = 0
		async for dialog in client.iter_dialogs():
			dialogs_count += 1
			print(f"Processing dialog number: #{dialogs_count}")

			output_string = ""
			chat = dialog.entity
			
			# Skip private chats
			if isinstance(chat, (Channel, Chat)):
				output_string += f"\nProcessing: {chat.title}"
				chat_info = await get_chat_info(client, chat)
				
				if chat_info:
					output_string += f"\nTitle: {chat_info['title']}"
					output_string += f"\nType: {chat_info['type']}"
					output_string += f"\nUsername: @{chat_info['username']}" if chat_info['username'] else "No username"
					output_string += f"\nMembers: {chat_info['members_count']}"
					output_string += f"\nDescription: {chat_info['description']}"
					
					if chat_info['creator']:
						creator_user = await client.get_entity(chat_info['creator'].user_id)
						output_string += f"\nCreator: {creator_user.first_name} (@{creator_user.username})"
					
					output_string += "\nAdmins:"
					for admin in chat_info['admins']:
						admin_user = await client.get_entity(admin.user_id)
						output_string += f"\n- {admin_user.first_name} (@{admin_user.username})"
					output_string += "\n" + "-" * 50

					with open("outputs_parsing_chats.txt", "a", encoding="utf-8") as file:
						file.write(output_string)

	except Exception as e:
		print(f"An error occurred: {str(e)}")
	finally:
		await client.disconnect()
		print("Disconnected from Telegram")

if __name__ == '__main__':
	asyncio.run(main())
