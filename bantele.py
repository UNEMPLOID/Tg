
import asyncio
import logging
import json
from dataclasses import dataclass
from typing import List
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PeerIdInvalidError, FloodWaitError
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import PeerChannel


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class ReportConfig:
    channel_id: str
    report_count: int
    api_id: int
    api_hash: str
    session_name: str
    reason: int

async def send_report_via_telegram(client: TelegramClient, peer: PeerChannel, reason: int) -> None:
    try:
        await client(ReportRequest(
            peer=peer,
            id=peer.channel_id,
            reason=reason,
            message='Relatório enviado automaticamente.'
        ))
        logging.info(f"Relatório enviado para {peer.channel_id}.")
    except FloodWaitError as e:
        logging.error(f"Excesso de solicitações. Aguarde {e.seconds} segundos.")
        await asyncio.sleep(e.seconds)
    except PeerIdInvalidError:
        logging.error("ID do canal inválido.")
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")

async def report_channel_or_account(client: TelegramClient, channel_id: str, report_count: int, reason: int) -> None:
    try:

        entity = await client.get_entity(channel_id)
        peer = PeerChannel(entity.id)
        
        for _ in range(report_count):
            logging.info(f"Enviando relatório para {channel_id}")
            await send_report_via_telegram(client, peer, reason)
            await asyncio.sleep(5)  
    except Exception as e:
        logging.error(f"Erro ao processar o canal {channel_id}: {e}")

async def load_configuration_from_file() -> ReportConfig:
    with open('config.json', 'r') as file:
        config_data = json.load(file)
    
    print("Digite as informações de configuração:")
    
    channel_id = input("Digite o ID do canal (ou o link): ").strip()
    report_count = int(input("Digite a quantidade de relatórios: ").strip())
    
    print("Escolha o motivo do relatório:")
    print("1. Violência")
    print("2. Pornografia")
    print("3. Drogas")
    print("4. Spam")
    print("5. Assédio")
    print("6. Violação de direitos autorais")
    print("7. Informação falsa")
    print("8. Bullying")
    print("9. Criminoso")
    print("10. Discursos de ódio")
    
    reason_map = {
        1: 0,  # Ajuste conforme necessário
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 7,
        9: 8,
        10: 9
    }
    
    reason_input = int(input("Digite o número do motivo: ").strip())
    reason = reason_map.get(reason_input, 0)
    
    return ReportConfig(
        channel_id=channel_id,
        report_count=report_count,
        api_id=config_data['api_id'],
        api_hash=config_data['api_hash'],
        session_name=config_data['session_name'],
        reason=reason
    )

async def run_reports(config: ReportConfig) -> None:
    client = TelegramClient(config.session_name, config.api_id, config.api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        phone_number = input("Digite seu número de telefone (incluindo o código do país): ").strip()
        try:
            await client.send_code_request(phone_number)
            code = input("Digite o código de confirmação enviado no seu app do telegram: ").strip()
            await client.sign_in(phone_number, code)
        except Exception as e:
            logging.error(f"Erro de autenticação: {e}")
            await client.disconnect()
            return

    await report_channel_or_account(client, config.channel_id, config.report_count, config.reason)

    logging.info("Todos os relatórios foram enviados com sucesso.")
    await client.disconnect()

async def main() -> None:
    config = await load_configuration_from_file()
    
    logging.info(f"Processando configuração: {config}")
    await run_reports(config)

if __name__ == "__main__":
    asyncio.run(main())
    
    # script feita por nex @inovertt caso for postar dê creditos.