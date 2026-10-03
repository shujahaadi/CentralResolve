from fastapi import APIRouter, UploadFile, File, HTTPException

from app.parsers.whatsapp import parse_whatsapp_chat
from app.parsers.discord import parse_discord_chat


router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze")
async def analyze_chats(
    whatsapp_file: UploadFile = File(...),
    discord_file: UploadFile = File(...),
):
    if not whatsapp_file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="WhatsApp file must be a .txt file",
        )

    if not discord_file.filename.endswith(".json"):
        raise HTTPException(
            status_code=400,
            detail="Discord file must be a .json file",
        )

    whatsapp_content = await whatsapp_file.read()
    discord_content = await discord_file.read()

    whatsapp_text = whatsapp_content.decode("utf-8")
    discord_text = discord_content.decode("utf-8")

    whatsapp_messages = parse_whatsapp_chat(whatsapp_text)
    discord_messages = parse_discord_chat(discord_text)

    all_messages = whatsapp_messages + discord_messages

    return {
        "whatsapp_messages": len(whatsapp_messages),
        "discord_messages": len(discord_messages),
        "total_messages": len(all_messages),
    }